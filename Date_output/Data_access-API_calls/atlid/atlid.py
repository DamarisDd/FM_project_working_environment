#!/usr/bin/env python3
"""Fetch ATLID data from ESA MAAP with a single Python command.

No pip installs or environment-variable setup required. Prompts securely for
your personal replacement offline token; never saves it. Default: Cluj,
last 30 days, all matching candidate files. Use --search-only for metadata only.

Based on https://catalog.maap.eo.esa.int/doc/examples/ESAMAAP_ecdataaccess.html
Search is public. Downloads use ESA EO Sign In authorization.
Output files are full products intersecting a bounding box, not radius subsets.
"""
import argparse
import getpass
import sys
import time
from datetime import datetime, timedelta, timezone
import json
import math
import os
from pathlib import Path
from urllib.parse import urlparse, urlencode, urljoin
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError


CATALOG = 'https://catalog.maap.eo.esa.int/catalogue'
TOKEN_URL = 'https://iam.maap.eo.esa.int/realms/esa-maap/protocol/openid-connect/token'
# These are the COMMON PUBLIC client credentials published in ESA's example.
# They are not your personal token. The personal offline token is read separately.
CLIENT_ID = 'offline-token'
CLIENT_SECRET = 'p1eL7uonXs6MDxtGbgKdPVRAmnGxHpVE'
COLLECTION = 'EarthCAREL2Validated_MAAP'


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HttpResponse:
    def __init__(self, raw, url):
        self.raw = raw
        self.status_code = raw.status
        self.url = raw.geturl() or url

    def close(self):
        self.raw.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def raise_for_status(self):
        if not 200 <= self.status_code < 300:
            status = self.status_code
            self.close()
            raise RuntimeError(f'ESA HTTP request failed ({status}). Check service availability and account access.')

    def json(self):
        try:
            return json.load(self.raw)
        finally:
            self.close()

    def iter_content(self, size):
        while True:
            chunk = self.raw.read(size)
            if not chunk:
                break
            yield chunk


class HttpSession:
    """Standard library HTTP; preserves proxy/CA configuration; no redirects."""
    def __init__(self):
        self.opener = build_opener(NoRedirect())

    def request(self, method, url, *, params=None, data=None, headers=None, **unused):
        if params:
            url += ('&' if '?' in url else '?') + urlencode(params)
        hdr = {'User-Agent': 'earthcare-one-script/1.0', **(headers or {})}
        body = None
        if data is not None:
            body = urlencode(data).encode()
            hdr['Content-Type'] = 'application/x-www-form-urlencoded'
        req = Request(url, data=body, headers=hdr, method=method)
        attempts = 4 if method == 'GET' else 1
        for attempt in range(attempts):
            try:
                return HttpResponse(self.opener.open(req, timeout=180), url)
            except HTTPError as err:
                if method == 'GET' and err.code in (429, 500, 502, 503, 504) and attempt < attempts-1:
                    delay = err.headers.get('Retry-After', '')
                    delay = min(float(delay), 30) if delay.isdigit() else 2**attempt
                    err.close()
                    time.sleep(delay)
                    continue
                return HttpResponse(err, url)
            except (URLError, TimeoutError):
                if attempt < attempts-1:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError('Network connection failed. Check connectivity, proxy settings and TLS trust.') from None

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)


def make_session():
    return HttpSession()


def trusted_url(url, *, data=False):
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname != 'catalog.maap.eo.esa.int' or p.username or p.password:
        raise ValueError('Unexpected catalogue/download host; inspect metadata before sending credentials.')
    if data and not p.path.startswith('/data/'):
        raise ValueError('Expected an ESA MAAP /data/ asset.')
    return url


def search_items(session, params):
    url = CATALOG + '/collections/' + COLLECTION + '/items'
    seen_pages = set()
    items = {}
    while url:
        trusted_url(url)
        response = session.get(url, params=params, timeout=(15, 90))
        response.raise_for_status()
        if response.url in seen_pages:
            raise RuntimeError('Repeated pagination URL; stopping rather than looping.')
        seen_pages.add(response.url)
        page = response.json()
        for item in page.get('features', []):
            if item['properties'].get('product:type') != 'ATL_EBD_2A':
                raise RuntimeError('Catalogue returned a different product; inspect the filter.')
            items[item['id']] = item
        nxt = next((x for x in page.get('links', []) if x.get('rel') == 'next'), None)
        if nxt and nxt.get('method', 'GET').upper() != 'GET':
            raise RuntimeError('Unexpected POST pagination; this script uses the documented GET route.')
        url = urljoin(response.url, nxt['href']) if nxt else None
        params = None
    # As in the Cloudnet downloader: keep newest baseline/processing per frame.
    newest = {}
    for item in items.values():
        p = item['properties']
        key = p['product:type'], p.get('start_datetime', p['datetime'])
        rank = str(p.get('version', '')), str(p.get('processing:datetime', ''))
        old = newest.get(key)
        if old is None or rank > old[0]:
            newest[key] = rank, item
    return sorted((v[1] for v in newest.values()), key=lambda x: x['properties']['datetime'])


class TokenManager:
    def __init__(self, session, offline):
        self.session, self.offline, self.access = session, offline, None

    def refresh(self):
        r = self.session.post(TOKEN_URL, data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token', 'refresh_token': self.offline,
            'scope': 'offline_access openid',
        }, timeout=(15, 60), allow_redirects=False)
        # Do not include response bodies or token values in errors/logs.
        if r.status_code != 200:
            raise RuntimeError(f'MAAP token exchange failed (HTTP {r.status_code}). Check token expiry/account authorization.')
        result = r.json()
        self.access = result['access_token']
        # Preserve a rotated refresh token within this process if one is issued.
        self.offline = result.get('refresh_token', self.offline)


def download_item(session, tokens, item, out):
    asset = item['assets']['enclosure_h5']
    url = trusted_url(asset['href'], data=True)
    filename = Path(urlparse(url).path).name
    if not filename.lower().endswith('.h5'):
        raise RuntimeError('Expected HDF5 asset filename.')
    path = out / filename
    expected = asset.get('file:size')
    if path.exists():
        if expected is not None and path.stat().st_size == int(expected):
            print('Already present (catalogue size matches):', filename)
            return
        raise RuntimeError(f'Existing file has unknown/wrong size: {path}. Inspect it before replacing.')
    if tokens.access is None:
        tokens.refresh()
    for attempt in range(2):
        r = session.get(url, headers={'Authorization': 'Bearer ' + tokens.access},
                        stream=True, timeout=(15, 180), allow_redirects=False)
        if r.status_code == 401 and attempt == 0:
            r.close()
            tokens.refresh()
            continue
        if r.status_code != 200:
            status = r.status_code
            r.close()
            raise RuntimeError(f'Data download failed (HTTP {status}); redirects are not followed with credentials.')
        break
    part = path.with_suffix('.h5.part')
    if part.exists():
        r.close()
        raise RuntimeError(f'Partial file exists: {part}. Inspect/remove it before retrying.')
    try:
        with r, part.open('xb') as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)
        if expected is not None and part.stat().st_size != int(expected):
            raise RuntimeError('Downloaded byte count does not match catalogue metadata.')
        with part.open('rb') as f:
            if f.read(8) != b'\x89HDF\r\n\x1a\n':
                raise RuntimeError('Downloaded response is not HDF5.')
        part.rename(path)
    except BaseException:
        part.unlink(missing_ok=True)
        raise
    print('Downloaded:', path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--days', type=int, default=30)
    p.add_argument('--lat', type=float, default=46.77)
    p.add_argument('--lon', type=float, default=23.55)
    p.add_argument('--radius-km', type=float, default=200)
    p.add_argument('--output', type=Path, default=Path('earthcare_cluj'))
    p.add_argument('--search-only', action='store_true', help='Search without token or data downloads.')
    p.add_argument('--non-interactive', action='store_true', help='Read token from MAAP_OFFLINE_TOKEN; fail if absent.')
    p.add_argument('--max-files', type=int, default=0, help='Download at most this many files; default 0 means all matches.')
    args = p.parse_args()
    if not (args.days > 0 and -85 <= args.lat <= 85 and -180 <= args.lon <= 180
            and 0 < args.radius_km <= 1000 and args.max_files >= 0):
        p.error('Use positive days/radius, nonnegative max-files, lat in [-85,85], lon in [-180,180].')
    now = datetime.now(timezone.utc)
    # Conservative spherical bounding box enclosing the radius at this latitude.
    ang = args.radius_km / 6371.0088
    dlat = math.degrees(ang)
    dlon = math.degrees(math.asin(min(1, math.sin(ang)/math.cos(math.radians(args.lat)))))
    bbox = [args.lon-dlon, args.lat-dlat, args.lon+dlon, args.lat+dlat]
    if bbox[0] < -180 or bbox[2] > 180 or bbox[1] < -90 or bbox[3] > 90:
        p.error('This simple bbox helper does not handle date-line/pole crossings.')
    fmt = lambda t: t.strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        'bbox': ','.join(map(str, bbox)),
        'datetime': fmt(now-timedelta(days=args.days)) + '/' + fmt(now),
        'filter': '"product:type"=\'ATL_EBD_2A\'',
        'filter-lang': 'cql2-text', 'limit': 200,
    }
    s = make_session()
    items = search_items(s, params)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {'catalogue': CATALOG, 'collection': COLLECTION, 'query': params, 'features': items}
    (args.output/'manifest.json').write_text(json.dumps(manifest, indent=2))
    print(f'{len(items)} latest-per-frame candidates intersect the search BOX; exact 200 km profile filtering is a separate step.')
    for item in items:
        asset = item.get('assets', {}).get('enclosure_h5', {})
        print(item['id'], 'bytes=', asset.get('file:size', 'unknown'))
    if args.search_only or not items:
        return
    token = os.environ.get('MAAP_OFFLINE_TOKEN', '').strip()
    if not token:
        if args.non_interactive:
            raise SystemExit('Non-interactive mode requires MAAP_OFFLINE_TOKEN in the job environment.')
        if not sys.stdin.isatty():
            raise SystemExit('Run in a terminal to enter the token securely, or set MAAP_OFFLINE_TOKEN.')
        print('Get a personal token at https://portal.maap.eo.esa.int/ini/services/auth/token/90dToken.php')
        token = getpass.getpass('Paste your replacement MAAP offline token (hidden): ').strip()
        if not token:
            raise SystemExit('No token entered; no download attempted.')
    selected = items if args.max_files == 0 else items[:args.max_files]
    print(f'Downloading {len(selected)} of {len(items)} candidates.')
    tokens = TokenManager(s, token)
    for item in selected:
        download_item(s, tokens, item, args.output)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled.', file=sys.stderr)
        sys.exit(130)
    except Exception as err:
        # Keep request bodies, auth headers and token values out of logs.
        print(f'Could not complete: {type(err).__name__}: {err}', file=sys.stderr)
        sys.exit(1)
