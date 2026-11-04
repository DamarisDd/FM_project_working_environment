#!/usr/bin/env python3
"""Download Cluj optical lidar products from the official ACTRIS ARES API.

No API key or pip installation required for the public route verified here.

Defaults reproduce the user's historical query; availability is not continuous.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

BASE='https://api.actris-ares.eu/api/services/restapi'


def open_api(path):
    if not path.startswith('/') or path.startswith('//'):
        raise ValueError('Expected relative API path.')
    for attempt in range(4):
        try:
            r=urlopen(Request(BASE+path,headers={'User-Agent':'cluj-earlinet-fetch/1.0'}),timeout=90)
            if not r.geturl().startswith('https://'):
                r.close();raise RuntimeError('Refusing insecure redirect.')
            return r
        except HTTPError as err:
            if err.code not in (429,500,502,503,504) or attempt==3:raise
            wait=err.headers.get('Retry-After','');err.close()
            time.sleep(min(int(wait),30) if wait.isdigit() else 2**attempt)
        except (URLError,TimeoutError):
            if attempt==3:raise
            time.sleep(2**attempt)


def get_json(path):
    with open_api(path) as r:return json.load(r)


def verify(path,record):
    if not path.exists() or path.stat().st_size!=int(record['File Size']):return False
    expected=str(record.get('Checksum','')).strip().lower()
    if len(expected)==64:algorithm='sha256'
    elif len(expected)==32:algorithm='md5'
    else:raise RuntimeError('Unsupported or missing metadata checksum; cannot verify product.')
    h=hashlib.new(algorithm,usedforsecurity=False)
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()==expected


def download(record,out):
    filename=record['Filename']
    if Path(filename).name!=filename or '/' in filename or '\\' in filename or filename in ('.','..'):
        raise ValueError('Invalid returned filename.')
    # Distinct IDs avoid overwriting earlier versions sharing a filename.
    folder=out/str(int(record['ID']));folder.mkdir(parents=True,exist_ok=True)
    target=folder/filename
    if verify(target,record):
        print('Already present (checksum verified):',target,flush=True);return target
    if target.exists():raise RuntimeError('Existing output failed verification; inspect/remove it before rerunning.')
    part=target.with_suffix(target.suffix+'.part')
    if part.exists():raise RuntimeError(f'Partial file exists: {part}; inspect/remove it before retrying.')
    total=int(record['File Size']);received=0;start=time.monotonic();last=start-1
    print(f'Downloading {filename} ({total/1024:.1f} KiB)...',flush=True)
    try:
        with open_api(f"/opticalproducts/id/{int(record['ID'])}/downloads") as r,part.open('xb') as f:
            while True:
                block=r.read(256*1024)
                if not block:break
                f.write(block);received+=len(block)
                now=time.monotonic()
                if now-last>=1:
                    print(f'\r  {received/1024:.1f}/{total/1024:.1f} KiB ({100*received/max(total,1):.1f}%)',end='',flush=True);last=now
        print(flush=True)
        if not verify(part,record):raise RuntimeError('Downloaded size/checksum does not match API metadata.')
        with part.open('rb') as f:magic=f.read(8)
        if not (magic.startswith(b'CDF') or magic==b'\x89HDF\r\n\x1a\n'):
            raise RuntimeError('Response is not recognized as NetCDF/HDF5.')
        part.rename(target)
    except BaseException:
        part.unlink(missing_ok=True);raise
    print('Saved and checksum verified:',target,flush=True)
    return target


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--start',default='2026-01-01')
    p.add_argument('--end',default='2026-05-18')
    p.add_argument('--product',choices=['backscatter','extinction','both'],default='backscatter')
    p.add_argument('--level',choices=['1','2'],help='Optional quality level; default all returned levels.')
    p.add_argument('--wavelength',type=int,help='Exact metadata wavelength in nm; filtered locally.')
    p.add_argument('--max-files',type=int,default=0,help='0=all matches; use 1 for a small validation download.')
    p.add_argument('--list-only',action='store_true')
    p.add_argument('--output',type=Path,default=Path('earlinet_cluj'))
    args=p.parse_args()
    if date.fromisoformat(args.start)>date.fromisoformat(args.end):p.error('Start must not follow end.')
    if args.max_files<0:p.error('max-files must be nonnegative.')
    stations=get_json('/stations')
    matches=[s for s in stations if s.get('ID')=='CLJ' and 'cluj' in s.get('Location','').lower()]
    if len(matches)!=1:raise RuntimeError('Could not unambiguously resolve CLJ/Cluj in the station dictionary.')
    station=matches[0]
    print(f"Station {station['ID']}: {station['Location']} | {station['Latitude']} N, {station['Longitude']} E, {station['Altitude']} m",flush=True)
    params={'stations':station['ID'],'fromDate':args.start,'toDate':args.end}
    if args.product!='both':params['fileTypes']='b' if args.product=='backscatter' else 'e'
    if args.level:params['levels']=args.level
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'station.json').write_text(json.dumps(station,indent=2))
    try:
        rows=get_json('/opticalproducts?'+urlencode(params))
    except HTTPError as err:
        if err.code==404:
            print('Search returned HTTP 404. The verified service also returns this for empty selections; try a broader date range or omit level/product filters.',flush=True)
            (args.output/f'query_{args.start}_{args.end}.json').write_text(json.dumps({'parameters':params,'status':404,'note':'No product list returned; this is not a credential diagnosis.'},indent=2))
            return
        raise
    if not isinstance(rows,list):raise RuntimeError('Unexpected product-response layout.')
    for r in rows:
        if r.get('Station',{}).get('ID')!='CLJ':raise RuntimeError('Unexpected station; refusing to mislabel another site as Cluj.')
        if args.level and float(r['Level']['Level'])!=float(args.level):raise RuntimeError('Level filter was not respected by service.')
        if args.product!='both' and r.get('File Type',{}).get('Code')!=params['fileTypes']:raise RuntimeError('Product filter was not respected by service.')
    if args.wavelength is not None:
        rows=[r for r in rows if r.get('Emission Wavelength',{}).get('Value')==args.wavelength]
    rows=sorted({r['ID']:r for r in rows}.values(),key=lambda r:(r['Start Time'],r['ID']))
    (args.output/f'manifest_{args.start}_{args.end}_{args.product}_level{args.level or "all"}_wavelength{args.wavelength or "all"}.json').write_text(json.dumps({'query':params,'wavelength':args.wavelength,'products':rows},indent=2))
    print(f'{len(rows)} matching files. Levels below are actual metadata, not assumed Level 2.',flush=True)
    for r in rows:
        print(r['ID'],r['Filename'],'| level',r['Level']['Level'],'| nm',r.get('Emission Wavelength',{}).get('Value'),flush=True)
    if not rows or args.list_only:return
    selected=rows if args.max_files==0 else rows[:args.max_files]
    failed=[]
    for i,r in enumerate(selected,1):
        print(f'\nFile {i}/{len(selected)}',flush=True)
        try:download(r,args.output)
        except Exception as err:
            failed.append(r['ID']);print(f'Failed ID {r["ID"]}: {type(err).__name__}: {err}',file=sys.stderr,flush=True)
    if failed:raise RuntimeError(f'Failed product IDs: {failed}. Successful files retained.')
    print('All selected files downloaded.',flush=True)


if __name__=='__main__':
    try:main()
    except KeyboardInterrupt:print('\nCancelled.',file=sys.stderr);sys.exit(130)
    except Exception as err:print(f'Error: {type(err).__name__}: {err}',file=sys.stderr);sys.exit(1)
