#!/usr/bin/env python3
"""Download public Cluj CHM15k files. Standard library only; no key needed.

python fetch_ceilometer.py                       # yesterday UTC, processed L1b
python fetch_ceilometer.py --date 2026-05-01
python fetch_ceilometer.py --start 2026-05-01 --end 2026-05-07
python fetch_ceilometer.py --nrt-only             # only returned rrt/nrt records
python fetch_ceilometer.py --raw                 # original instrument files
"""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

BASE='https://cloudnet.fmi.fi/api'


def open_url(url):
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname!='cloudnet.fmi.fi' or parsed.username or parsed.password:
        raise ValueError('Unexpected download destination; inspect the API response.')
    for attempt in range(4):
        try:
            response=urlopen(Request(url,headers={'User-Agent':'cluj-ceilometer-fetch/1.0'}),timeout=90)
            if urlparse(response.geturl()).scheme!='https':
                response.close()
                raise ValueError('Refusing an unencrypted redirect.')
            return response
        except HTTPError as err:
            if err.code not in (429,500,502,503,504) or attempt==3:
                raise
            wait=err.headers.get('Retry-After','')
            err.close()
            time.sleep(min(int(wait),30) if wait.isdigit() else 2**attempt)
        except (URLError,TimeoutError):
            if attempt==3:raise
            time.sleep(2**attempt)


def get_json(url):
    with open_url(url) as response:
        return json.load(response)


def digest(path,expected):
    algorithm='sha256' if len(expected)==64 else 'md5' if len(expected)==32 else None
    if algorithm is None:
        raise ValueError('Unknown API checksum format; refusing unverified download.')
    h=hashlib.new(algorithm,usedforsecurity=False)
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def valid_file(path,record):
    if not path.exists():return False
    return path.stat().st_size==int(record['size']) and digest(path,record['checksum'])==record['checksum'].lower()


def download(record,output):
    name=record['filename']
    if Path(name).name!=name or '/' in name or '\\' in name or name in ('.','..'):
        raise ValueError('Invalid server filename.')
    target=output/name
    if valid_file(target,record):
        print('Already current (checksum verified):',name,flush=True)
        return target
    if target.exists():
        # Preserve previous local data when a volatile server product is revised.
        target=output/(Path(name).stem+'_'+record['checksum']+Path(name).suffix)
        if valid_file(target,record):
            print('Already current (versioned file):',target.name,flush=True)
            return target
        if target.exists():raise RuntimeError('Existing versioned file failed verification; inspect it before retrying.')
    part=target.with_suffix(target.suffix+'.part')
    if part.exists():raise RuntimeError(f'Partial file exists: {part}. Inspect/remove it before rerunning.')
    total=int(record['size']);received=0;started=time.monotonic();last=started-1
    print(f'Downloading {name} ({total/1024**2:.1f} MiB)...',flush=True)
    try:
        with open_url(record['downloadUrl']) as response,part.open('xb') as f:
            while True:
                block=response.read(256*1024)
                if not block:break
                f.write(block);received+=len(block)
                now=time.monotonic()
                if now-last>=1:
                    print(f'\r  {received/1024**2:.1f}/{total/1024**2:.1f} MiB  {100*received/max(total,1):.1f}%',end='',flush=True)
                    last=now
        print(flush=True)
        if not valid_file(part,record):raise RuntimeError('Downloaded size/checksum differs from API metadata; no completed file saved.')
        with part.open('rb') as f:
            magic=f.read(8)
        if not (magic.startswith(b'CDF') or magic==b'\x89HDF\r\n\x1a\n'):
            raise RuntimeError('Response is not recognized as NetCDF/HDF5.')
        part.rename(target)
    except BaseException:
        part.unlink(missing_ok=True)
        raise
    print('Saved and checksum verified:',target,flush=True)
    return target


def main():
    yesterday=(datetime.now(timezone.utc).date()-timedelta(days=1)).isoformat()
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--date',help='Single UTC measurement date YYYY-MM-DD.')
    p.add_argument('--start',help='First UTC date, inclusive.')
    p.add_argument('--end',help='Last UTC date, inclusive; defaults to start.')
    p.add_argument('--nrt-only',action='store_true',help='Keep metadata timeliness rrt/nrt; this is not an age filter.')
    p.add_argument('--raw',action='store_true',help='Download original files instead of Cloudnet processed lidar.')
    p.add_argument('--list-only',action='store_true',help='Inspect metadata without downloading scientific files.')
    p.add_argument('--output',type=Path,default=Path('cloudnet_cluj'))
    args=p.parse_args()
    if args.date and (args.start or args.end):p.error('Use --date OR --start/--end.')
    if args.end and not args.start:p.error('--end requires --start.')
    if args.raw and args.nrt_only:p.error('Raw records do not expose timeliness; use --nrt-only on processed products.')
    start=date.fromisoformat(args.date or args.start or yesterday)
    end=date.fromisoformat(args.date or args.end or args.start or yesterday)
    if start>end:p.error('Start must not follow end.')
    args.output.mkdir(parents=True,exist_ok=True)
    site=get_json(BASE+'/sites/cluj')
    print(f"Site: {site['humanReadableName']} | {site['latitude']} N, {site['longitude']} E | {site['altitude']} m",flush=True)
    (args.output/'site.json').write_text(json.dumps(site,indent=2))
    records=[];day=start
    while day<=end:
        params={'site':'cluj','date':day.isoformat()}
        params['instrument' if args.raw else 'product']='chm15k' if args.raw else 'lidar'
        endpoint='/raw-files' if args.raw else '/files'
        data=get_json(BASE+endpoint+'?'+urlencode(params))
        if not isinstance(data,list):raise RuntimeError('API response layout changed; expected a list.')
        for r in data:
            if r.get('site',{}).get('id')!='cluj':raise RuntimeError('Unexpected site in response.')
            if r.get('instrument',{}).get('instrumentId')!='chm15k':continue
            if r.get('tombstoneReason'):continue
            if args.nrt_only and r.get('timeliness') not in ('rrt','nrt'):continue
            records.append(r)
        day+=timedelta(days=1)
    records=list({r['uuid']:r for r in records}.values())
    manifest=args.output/f"manifest_{'raw' if args.raw else 'lidar'}_{start}_{end}.json"
    manifest.write_text(json.dumps(records,indent=2))
    print(f'{len(records)} matching files ({start} through {end} UTC).',flush=True)
    for r in records:
        inst=r['instrument']
        print(r['filename'],'| timeliness:',r.get('timeliness','not supplied'),
              '| instrument:',inst['uuid'],'| PID:',inst.get('pid',''),flush=True)
    if not records:
        print('No matching records. This does not indicate missing credentials; try an earlier date or omit --nrt-only.',flush=True)
        return
    if args.list_only:return
    failures=0
    for i,r in enumerate(records,1):
        print(f'\nFile {i}/{len(records)}',flush=True)
        try:download(r,args.output)
        except Exception as err:
            failures+=1;print(f'Failed: {type(err).__name__}: {err}',file=sys.stderr,flush=True)
    if failures:raise RuntimeError(f'{failures} downloads failed; successful files retained.')
    print('All matching files downloaded.',flush=True)


if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:
        print('\nCancelled.',file=sys.stderr);sys.exit(130)
    except Exception as err:
        print(f'Error: {type(err).__name__}: {err}',file=sys.stderr);sys.exit(1)
