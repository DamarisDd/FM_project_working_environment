#!/usr/bin/env python3
"""Convert EARLINET NetCDF profiles to CSV, retaining flags/errors/metadata.

Install once: python -m pip install netCDF4
One file:     python nc_to_csv.py "measurement.nc"
Folder:       python nc_to_csv.py "earlinet_cluj" --recursive

Primary axes are time, wavelength, and altitude (or height/range). Scalar
metadata repeat on each row. Extra dimensions such as nv are expanded into
columns, NOT a Cartesian-product set of extra rows. CF missing values become
empty cells, scale/offset are decoded, and metadata are saved in JSON.
"""
import argparse
import csv
import itertools
import json
import math
from pathlib import Path
import sys
import warnings
import os
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

try:
    import netCDF4 as nc
    import numpy as np
except ImportError:
    nc = None
    np = None

PRIMARY = ('time', 'wavelength', 'altitude', 'height', 'range')


def json_value(v):
    if isinstance(v,bytes):return v.decode('utf-8',errors='replace')
    if isinstance(v,np.ndarray):return json_value(v.tolist())
    if isinstance(v,(list,tuple)):return [json_value(x) for x in v]
    if isinstance(v,dict):return {str(k):json_value(x) for k,x in v.items()}
    if isinstance(v,np.generic):return json_value(v.item())
    if isinstance(v,float) and not math.isfinite(v):return None
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    return str(v)


def cell_value(v):
    if np.ma.is_masked(v):return ''
    if isinstance(v,np.generic):v=v.item()
    if isinstance(v,bytes):return v.decode('utf-8',errors='replace')
    if isinstance(v,float) and not math.isfinite(v):return ''
    if isinstance(v,np.ndarray):return json.dumps(json_value(v))
    return v


def convert(source,target,*,delimiter=',',overwrite=False,max_rows=5000000,max_columns=10000):
    meta_target=target.with_suffix('.metadata.json')
    if not overwrite and (target.exists() or meta_target.exists()):
        raise FileExistsError(f'Output already exists: {target}. Use --overwrite only if intended.')
    csv_part=target.with_suffix('.csv.part')
    meta_part=meta_target.with_suffix('.json.part')
    if csv_part.exists() or meta_part.exists():raise FileExistsError('Partial output exists; inspect/remove before retrying.')
    target.parent.mkdir(parents=True,exist_ok=True)
    try:
        with nc.Dataset(source) as ds:
            if ds.groups:
                raise ValueError('This EARLINET converter expects root-level variables. Grouped files need a group-aware conversion.')
            core=[d for d in PRIMARY if d in ds.dimensions]
            if not any(d in core for d in ('altitude','height','range')):
                raise ValueError('No altitude/height/range dimension found; this does not match the supported profile layout.')
            sizes={d:len(ds.dimensions[d]) for d in core}
            row_count=math.prod(sizes.values())
            if row_count>max_rows:
                raise ValueError(f'{row_count} rows exceeds --max-rows={max_rows}; choose a subset or increase the limit deliberately.')
            entries=[]
            metadata={
                'source_file':str(source.resolve()),
                'source_format':ds.data_model,
                'row_dimensions':sizes,
                'all_dimensions':{k:{'size':len(v),'unlimited':v.isunlimited()} for k,v in ds.dimensions.items()},
                'global_attributes':{a:json_value(ds.getncattr(a)) for a in ds.ncattrs()},
                'variables':{},'csv_columns':{},
                'conversion':{'missing_values':'empty CSV cells; NaN/infinity also empty',
                              'scale_offset':'decoded by netCDF4; source packing attributes retained only as documentation',
                              'extra_dimensions':'expanded into columns, not additional rows',
                              'quality_filter':'none; all profiles/bins retained with quality/error fields',
                              'strings':'UTF-8; no Excel formula escaping, to preserve literal source text',
                              'time':'CF time converted to ISO text in an added column; numeric time retained'},
            }
            for name,var in ds.variables.items():
                attrs={a:json_value(var.getncattr(a)) for a in var.ncattrs()}
                metadata['variables'][name]={'dimensions':list(var.dimensions),'shape':list(var.shape),'dtype':str(var.dtype),'attributes':attrs}
                if len(set(var.dimensions))!=len(var.dimensions):
                    raise ValueError(f'{name} repeats a dimension name; ambiguous indexing.')
                var.set_auto_maskandscale(True)
                # Keep character dimensions explicit rather than silently joining them.
                var.set_auto_chartostring(False)
                data=var[...]
                extra=[d for d in var.dimensions if d not in core]
                count=math.prod(len(ds.dimensions[d]) for d in extra)
                if len(entries)+count>max_columns:
                    raise ValueError(f'Expanded columns exceed --max-columns={max_columns}.')
                for extra_indices in itertools.product(*(range(len(ds.dimensions[d])) for d in extra)):
                    fixed=dict(zip(extra,extra_indices))
                    col=name+''.join(f'__{d}_{i}' for d,i in fixed.items())
                    entries.append((col,var.dimensions,data,fixed))
                    metadata['csv_columns'][col]={'variable':name,'extra_dimension_indices':fixed,'units':attrs.get('units','')}
            index_headers=[d+'_index' for d in core]
            time_var=ds.variables.get('time')
            time_header=None;iso_times=None
            if time_var is not None and time_var.dimensions==('time',) and 'time' in core and ' since ' in str(getattr(time_var,'units','')):
                cal=str(getattr(time_var,'calendar','standard'))
                standard=cal in ('standard','gregorian','proleptic_gregorian')
                time_header='time_utc' if standard else 'time_calendar'
                iso_times=[]
                for value in time_var[:]:
                    if np.ma.is_masked(value) or not np.isfinite(value):iso_times.append('');continue
                    dt=nc.num2date(value,time_var.units,calendar=cal)
                    iso_times.append(dt.isoformat()+('Z' if standard else ''))
                metadata['csv_columns'][time_header]={'derived_from':'time','calendar':cal,'units':'ISO 8601 UTC' if standard else 'ISO-like date in source calendar'}
            headers=index_headers+([time_header] if time_header else [])+[e[0] for e in entries]
            if len(headers)!=len(set(headers)):
                raise ValueError('Generated CSV column names collide with source names.')
            with csv_part.open('x',encoding='utf-8-sig',newline='') as f:
                writer=csv.writer(f,delimiter=delimiter);writer.writerow(headers)
                for position in itertools.product(*(range(sizes[d]) for d in core)):
                    indices=dict(zip(core,position));row=list(position)
                    if time_header:row.append(iso_times[indices['time']])
                    for col,dims,data,fixed in entries:
                        selection=tuple(indices[d] if d in indices else fixed[d] for d in dims)
                        row.append(cell_value(data[selection] if dims else data[()]))
                    writer.writerow(row)
            metadata['csv_row_count']=row_count
            metadata['csv_column_count']=len(headers)
            metadata['delimiter']=delimiter
            meta_part.write_text(json.dumps(metadata,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
        csv_part.replace(target);meta_part.replace(meta_target)
    except BaseException:
        csv_part.unlink(missing_ok=True);meta_part.unlink(missing_ok=True)
        raise
    print(f'{source.name} -> {target} ({row_count} rows, {len(headers)} columns)',flush=True)
    return row_count,len(headers)


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('input',nargs='?',type=Path,default=Path('.'),help='One .nc file or a directory; default current directory.')
    p.add_argument('--recursive',action='store_true',help='Find .nc files in nested downloader folders.')
    p.add_argument('--output',type=Path,default=Path('csv_output'))
    p.add_argument('--delimiter',default=',',help='One character; use ";" for some regional Excel settings.')
    p.add_argument('--overwrite',action='store_true')
    p.add_argument('--max-rows',type=int,default=5000000)
    p.add_argument('--max-columns',type=int,default=10000)
    args=p.parse_args()
    if len(args.delimiter)!=1 or args.delimiter in ('\n','\r','"'):
        p.error('Choose one separator character, e.g. comma or semicolon.')
    if args.max_rows<1 or args.max_columns<1:p.error('Row/column limits must be positive.')
    if args.input.is_file():
        files=[args.input];base=args.input.parent
    elif args.input.is_dir():
        base=args.input
        files=sorted(x for x in (base.rglob('*') if args.recursive else base.iterdir()) if x.is_file() and x.suffix.lower()=='.nc')
    else:p.error('Input file/directory does not exist.')
    if not files:raise SystemExit('No .nc files found. Use --recursive for nested EARLINET downloader directories.')
    failures=0
    for source in files:
        target=args.output/source.relative_to(base).with_suffix('.csv')
        try:convert(source,target,delimiter=args.delimiter,overwrite=args.overwrite,max_rows=args.max_rows,max_columns=args.max_columns)
        except Exception as err:
            failures+=1;print(f'FAILED {source}: {type(err).__name__}: {err}',file=sys.stderr)
    if failures:raise SystemExit(f'{failures} conversion(s) failed; successful outputs retained.')
    print('Done. Units, quality definitions and original attributes are in the companion .metadata.json files.')



def gui_main():
    """File/folder picker; all conversion and installation work runs off the UI thread."""
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ImportError:
        raise SystemExit('This Python installation has no Tkinter. Use a Python installation with Tk support, or the command-line converter.')
    import os
    import queue
    import subprocess
    import threading
    import venv

    root=tk.Tk()
    root.title('EARLINET NetCDF to CSV')
    root.geometry('620x280')
    root.minsize(580,260)
    ttk.Label(root,text='Convert EARLINET .nc files to CSV',font=('',15,'bold')).pack(pady=(18,8))
    ttk.Label(root,text='Choose files, then choose an output folder. No typed paths needed.').pack()
    status=tk.StringVar(value='Ready. Original NetCDF files will remain unchanged.')
    ttk.Label(root,textvariable=status,wraplength=580).pack(pady=12)
    progress=ttk.Progressbar(root,mode='indeterminate')
    progress.pack(fill='x',padx=25,pady=5)
    frame=ttk.Frame(root);frame.pack(pady=12)
    messages=queue.Queue()
    busy=False
    buttons=[]

    def set_busy(value):
        nonlocal busy
        busy=value
        for b in buttons:b.configure(state='disabled' if value else 'normal')
        if value:progress.start(12)
        else:progress.stop()

    def install_dependencies():
        if not messagebox.askyesno('First-time setup',
            'The NetCDF reader is missing. Install it into a private environment beside this script?\n\n'
            'This needs Internet access. Your global Python packages will not be changed.',parent=root):
            return
        set_busy(True);status.set('Installing the NetCDF reader; this may take a few minutes...')
        def work():
            try:
                env=Path(__file__).resolve().parent/'.nc_csv_venv'
                python=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
                if Path(sys.prefix).resolve()==env.resolve():
                    raise RuntimeError('Reader is unavailable inside the private environment. Remove or repair .nc_csv_venv and retry.')
                if not python.exists():venv.EnvBuilder(with_pip=True).create(env)
                proc=subprocess.run([str(python),'-m','pip','install','--disable-pip-version-check','netCDF4'],
                                    capture_output=True,text=True)
                if proc.returncode:
                    raise RuntimeError('Dependency installation failed. Check Internet access and Python pip/venv support.\n\n'+proc.stderr[-1800:])
                subprocess.Popen([str(python),str(Path(__file__).resolve())])
                messages.put(('reopened',None))
            except Exception as err:messages.put(('error',str(err)))
        threading.Thread(target=work,daemon=True).start()

    def choose(folder=False):
        if nc is None:
            install_dependencies();return
        if folder:
            name=filedialog.askdirectory(title='Choose folder containing EARLINET .nc files',parent=root)
            if not name:return
            base=Path(name)
            files=sorted(x for x in base.rglob('*') if x.is_file() and x.suffix.lower()=='.nc')
        else:
            selected=filedialog.askopenfilenames(title='Choose one or more EARLINET NetCDF files',parent=root,
                                                 filetypes=[('NetCDF files','*.nc'),('All files','*.*')])
            if not selected:return
            files=[Path(x) for x in selected]
            base=Path(os.path.commonpath([str(x.parent) for x in files]))
        if not files:
            messagebox.showinfo('No files','No .nc files were found in that folder.',parent=root);return
        name=filedialog.askdirectory(title='Choose where to save CSV files',parent=root)
        if not name:return
        output=Path(name)
        set_busy(True);status.set(f'Converting {len(files)} file(s)...')
        def work():
            successes=0;failures=[]
            for index,source in enumerate(files,1):
                messages.put(('status',f'Converting {index}/{len(files)}: {source.name}'))
                try:
                    target=output/source.relative_to(base).with_suffix('.csv')
                    convert(source,target)
                    successes+=1
                except Exception as err:failures.append(f'{source.name}: {type(err).__name__}: {err}')
            messages.put(('done',(successes,failures,output)))
        threading.Thread(target=work,daemon=True).start()

    files_button=ttk.Button(frame,text='Choose .nc files...',command=lambda:choose(False))
    files_button.pack(side='left',padx=8);buttons.append(files_button)
    folder_button=ttk.Button(frame,text='Choose a folder...',command=lambda:choose(True))
    folder_button.pack(side='left',padx=8);buttons.append(folder_button)
    ttk.Label(root,text='One row per time / wavelength / altitude; units and attributes saved in metadata JSON.',
              wraplength=580).pack(pady=5)

    def poll():
        while True:
            try:kind,payload=messages.get_nowait()
            except queue.Empty:break
            if kind=='status':status.set(payload)
            elif kind=='reopened':root.destroy();return
            elif kind=='error':
                set_busy(False);status.set('Setup failed. See the error message.')
                messagebox.showerror('Setup failed',payload,parent=root)
            elif kind=='done':
                successes,failures,output=payload
                set_busy(False)
                status.set(f'Finished: {successes} converted, {len(failures)} not converted.')
                summary=f'{successes} file(s) converted.\nOutput folder:\n{output}\n\nEach CSV has a companion metadata JSON file.'
                if failures:
                    summary+='\n\nErrors (existing outputs are not overwritten):\n'+'\n'.join(failures[:6])
                    messagebox.showwarning('Conversion results',summary,parent=root)
                else:messagebox.showinfo('Conversion complete',summary,parent=root)
        root.after(100,poll)

    def close():
        if busy:
            messagebox.showinfo('Work in progress','Please wait until the current operation finishes.',parent=root)
        else:root.destroy()
    root.protocol('WM_DELETE_WINDOW',close)
    root.after(100,poll)
    root.mainloop()


if __name__=='__main__':
    if len(sys.argv)==1:
        gui_main()
    elif nc is None:
        raise SystemExit('Install netCDF4, or open this script without arguments to use guided setup.')
    else:
        main()
