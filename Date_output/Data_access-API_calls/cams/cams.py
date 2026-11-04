#!/usr/bin/env python3
"""Download the four CAMS product families described in the repository.

python fetch_cams.py --dry-run
python fetch_cams.py --products europe
python fetch_cams.py

Uses ADS, NOT the ERA5/CDS service. Terms must be accepted manually.
Public form fields checked 2026-11-04. Protected retrieval not tested here.
"""
import argparse
from datetime import date, datetime, timedelta, timezone
import getpass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import venv
import zipfile

ADS = 'https://ads.atmosphere.copernicus.eu/api'
DATASETS = {
    'europe': 'cams-europe-air-quality-forecasts',
    'global': 'cams-global-atmospheric-composition-forecasts',
    'eac4': 'cams-global-reanalysis-eac4',
    'gfas': 'cams-global-fire-emissions-gfas',
}
# Format and selector values checked against the LIVE ADS forms, 4 Nov 2026.
FIRE_PM25 = 'wildfire_flux_of_particulate_matter_d_2_5_\u00b5m'


def days(start, end):
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    if a > b:
        raise ValueError('Start date must not be later than end date.')
    while a <= b:
        yield a.isoformat()
        a += timedelta(days=1)


def build_jobs(args):
    jobs=[]
    def add(family, label, day, request):
        jobs.append({'family':family,'label':label,'day':day,'dataset':DATASETS[family], 'request':request})
    fmt='grib' if args.format=='grib' else 'netcdf_zip'
    if 'europe' in args.products:
        for d in days(args.forecast_start,args.forecast_end):
            add('europe','ensemble_pm25_surface',d,{
                'variable':['particulate_matter_2.5um'],'model':['ensemble'],'level':['0'],
                'date':d,'type':['forecast'],'time':['00:00'],
                'leadtime_hour':[str(h) for h in range(97)],'area':args.europe_area,'data_format':fmt,
            })
    if 'global' in args.products:
        for d in days(args.forecast_start,args.forecast_end):
            if d < '2019-07-07':
                raise ValueError('This global forecast recipe uses 137 levels; select dates on/after 2019-07-07.')
            base={'date':d,'time':['00:00','12:00'],'leadtime_hour':[str(h) for h in range(0,121,3)],
                  'type':['forecast'],'area':args.global_area,'data_format':fmt}
            add('global','single_level_pm_aod',d,{**base,'variable':[
                'particulate_matter_2.5um','particulate_matter_10um','total_aerosol_optical_depth_550nm',
            ]})
            add('global','lowest_model_level_137',d,{**base,'variable':[
                'dust_aerosol_0.55-0.9um_mixing_ratio','carbon_monoxide','nitrogen_dioxide','ozone','sulphur_dioxide',
            ],'model_level':['137']})
    if 'eac4' in args.products:
        for d in days(args.history_start,args.history_end):
            base={'date':d,'time':[f'{h:02}:00' for h in range(0,24,3)],'area':args.global_area,'data_format':fmt}
            add('eac4','single_level_pm_aod',d,{**base,'variable':[
                'total_aerosol_optical_depth_550nm','particulate_matter_2.5um','dust_aerosol_optical_depth_550nm',
            ]})
            add('eac4','co_lowest_model_level_60',d,{**base,'variable':['carbon_monoxide'],'model_level':['60']})
    if 'gfas' in args.products:
        for d in days(args.fire_start,args.fire_end):
            add('gfas','daily_fire_emissions',d,{
                'variable':['wildfire_radiative_power','wildfire_flux_of_carbon_monoxide',FIRE_PM25,
                            'wildfire_flux_of_organic_carbon','wildfire_flux_of_black_carbon'],
                'date':d,'time':['00:00'],'temporal_aggregation':['daily'],
                'data_format':'grib' if args.format=='grib' else 'netcdf',
            })
    return jobs


def ensure_cdsapi():
    if importlib.util.find_spec('cdsapi') is not None:
        from importlib.metadata import version
        nums=tuple(int(n) for n in version('cdsapi').split('.')[:3])
        if nums >= (0,7,7):
            return
    # Isolated dependency installation, without altering global/site packages.
    root=Path(__file__).resolve().parent/'.cams_api_venv'
    python=root/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    if Path(sys.prefix).resolve()==root.resolve():
        raise RuntimeError('cdsapi>=0.7.7 is not usable in the script environment; check installation.')
    if not python.exists():
        print('Preparing an isolated CDS API client environment...',flush=True)
        venv.EnvBuilder(with_pip=True).create(root)
    subprocess.run([str(python),'-m','pip','install','--disable-pip-version-check','cdsapi>=0.7.7'],check=True)
    # A new process re-reads credentials securely; none go into its command line.
    os.execv(str(python),[str(python),str(Path(__file__).resolve()),*sys.argv[1:]])


def get_ads_key():
    key=os.environ.get('ADS_API_KEY','').strip()
    if key:
        return key
    # Read locally but NEVER print configuration contents or credential values.
    cfg=Path.home()/'.cdsapirc'
    if cfg.exists():
        import yaml
        settings=yaml.safe_load(cfg.read_text()) or {}
        if isinstance(settings,dict) and str(settings.get('url','')).rstrip('/')==ADS:
            key=str(settings.get('key','')).strip()
            if key and 'YOUR_' not in key:
                return key
        print('No usable ADS entry in .cdsapirc; a CDS/ERA5 key will not be reused.',flush=True)
    if not sys.stdin.isatty():
        raise RuntimeError('Provide ADS_API_KEY or an ADS .cdsapirc for non-interactive use.')
    key=getpass.getpass('Paste your replacement ADS personal access token (hidden): ').strip()
    if not key:
        raise RuntimeError('No ADS token supplied.')
    return key


def inspect_output(path):
    with path.open('rb') as f:
        magic=f.read(8)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            bad=z.testzip()
            if bad:
                raise RuntimeError('Downloaded ZIP failed its CRC check.')
            if not z.namelist():
                raise RuntimeError('Downloaded ZIP is empty.')
        return '.zip'
    if magic.startswith(b'GRIB'):
        return '.grib'
    if magic.startswith(b'CDF') or magic==b'\x89HDF\r\n\x1a\n':
        return '.nc'
    raise RuntimeError('Result is not recognized as ZIP, GRIB or NetCDF/HDF5; inspect the .part file.')


def retrieve_job(client, job, folder):
    encoded=json.dumps({'dataset':job['dataset'],'request':job['request']},sort_keys=True).encode()
    digest=hashlib.sha256(encoded).hexdigest()
    name=f"{job['family']}_{job['label']}_{job['day']}_{digest[:10]}"
    request_file=folder/(name+'.request.json')
    request_file.write_bytes(encoded)  # no credentials in request manifest
    marker=folder/(name+'.complete.json')
    if marker.exists():
        m=json.loads(marker.read_text());target=folder/m['filename']
        if target.parent.resolve()!=folder.resolve():
            raise RuntimeError('Invalid completion-manifest path.')
        if (m.get('request_sha256')==digest and target.exists()
                and target.stat().st_size==m.get('bytes') and inspect_output(target)==target.suffix):
            print('Already completed:',target.name,flush=True)
            return
        raise RuntimeError('Existing completion manifest does not match its output; inspect it before retrying.')
    part=folder/(name+'.part')
    if part.exists():
        raise RuntimeError(f'Partial file remains: {part}. Inspect/remove it before retrying this job.')
    print('Submitting request. ADS may queue it; client status messages follow.',flush=True)
    client.retrieve(job['dataset'],job['request'],str(part))
    suffix=inspect_output(part)
    target=folder/(name+suffix)
    if target.exists():
        raise RuntimeError(f'Output already exists without completion marker: {target}. Inspect before retrying.')
    part.rename(target)
    marker.write_text(json.dumps({'filename':target.name,'bytes':target.stat().st_size,
                                 'request_sha256':digest,'completed_utc':datetime.now(timezone.utc).isoformat()},indent=2))
    print('Saved:',target,flush=True)


def main():
    yesterday=(datetime.now(timezone.utc).date()-timedelta(days=1)).isoformat()
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--products',nargs='+',choices=list(DATASETS),default=list(DATASETS))
    p.add_argument('--forecast-start',default=yesterday,help='Forecast INITIALIZATION date, default yesterday UTC.')
    p.add_argument('--forecast-end',help='Last initialization date, default same as start.')
    p.add_argument('--history-start',default='2024-03-15')
    p.add_argument('--history-end',default='2024-03-22')
    p.add_argument('--fire-start',help='First GFAS day, default forecast-start.')
    p.add_argument('--fire-end',help='Last GFAS day, default fire-start.')
    p.add_argument('--europe-area',nargs=4,type=float,default=[48,22,45,26],metavar=('N','W','S','E'))
    p.add_argument('--global-area',nargs=4,type=float,default=[50,20,42,28],metavar=('N','W','S','E'))
    p.add_argument('--format',choices=['netcdf','grib'],default='netcdf')
    p.add_argument('--output',type=Path,default=Path('cams_data'))
    p.add_argument('--dry-run',action='store_true',help='Print/save planned requests; no installation/key/API submission.')
    args=p.parse_args()
    args.forecast_end=args.forecast_end or args.forecast_start
    args.fire_start=args.fire_start or args.forecast_start
    args.fire_end=args.fire_end or args.fire_start
    for area in [args.europe_area,args.global_area]:
        n,w,s,e=area
        if not (-90<=s<=n<=90 and -180<=w<=e<=180):
            p.error('Area must be N,W,S,E with valid non-crossing bounds.')
    jobs=build_jobs(args)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'planned_requests.json').write_text(json.dumps(jobs,indent=2))
    print(f'{len(jobs)} daily requests planned. Dates for forecasts are initialization dates, not valid-time windows.',flush=True)
    print('European/global/EAC4 spatial subset uses N,W,S,E. GFAS recipe downloads global fields.',flush=True)
    print('Lowest-level composition alone is NOT complete FLEXPART boundary-condition input.',flush=True)
    for i,job in enumerate(jobs,1):
        print(f"{i}/{len(jobs)} {job['dataset']} | {job['label']} | {job['day']}",flush=True)
    if args.dry_run:
        print('Dry run only: no authenticated requests submitted.',flush=True)
        return
    ensure_cdsapi()
    import cdsapi
    client=cdsapi.Client(url=ADS,key=get_ads_key(),debug=False,quiet=False)
    failures=[]
    for i,job in enumerate(jobs,1):
        print(f"\n[{i}/{len(jobs)}] {job['family']} {job['day']} {job['label']}",flush=True)
        try:
            retrieve_job(client,job,args.output)
        except Exception:
            # Avoid dumping exception/HTTP bodies that could contain auth details.
            failures.append(job)
            print('Job failed. Check the preceding ADS status, dataset terms, allowed dates/choices, quota and connectivity. Continuing other jobs.',flush=True)
    if failures:
        (args.output/'failed_requests.json').write_text(json.dumps(failures,indent=2))
        print(f'{len(failures)} jobs failed; see failed_requests.json. Successful jobs are retained.',flush=True)
        return 1
    print('All requested jobs completed.',flush=True)
    return 0


if __name__=='__main__':
    try:
        sys.exit(main() or 0)
    except KeyboardInterrupt:
        print('\nCancelled; partial files may remain.',file=sys.stderr)
        sys.exit(130)
    except Exception as err:
        print(f'Unable to run ({type(err).__name__}). Check dates, local configuration, dependencies and output directory.',file=sys.stderr)
        sys.exit(1)
