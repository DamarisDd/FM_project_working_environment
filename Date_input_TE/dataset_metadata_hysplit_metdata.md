# Dataset metadata — HYSPLIT input meteorological data (NOAA GFS / GDAS in ARL format)

Companion documentation to the Stage 1 input-data table.
This file describes the **meteorological data inputs to the HYSPLIT
trajectory + dispersion model** — specifically the **pre-converted
ARL-format archives** of NOAA's GFS and GDAS systems that the project's
HYSPLIT engine ingests natively.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**This is the HYSPLIT analogue of ERA5 for FLEXPART.** Both engines need
3D meteorological fields (winds, temperature, humidity, surface
properties); each has a preferred input path. **For HYSPLIT, the path of
least resistance is NOAA's GFS/GDAS in pre-converted ARL format** —
delivered by NOAA's Air Resources Laboratory (ARL) ready for direct
ingestion. ERA5 → HYSPLIT is technically possible but requires manual
ARL conversion with community-maintained tools that have no official
NOAA or ECMWF support.

---

## 18. HYSPLIT meteorological input data — NOAA ARL archives

### Summary

| Field | Value |
|---|---|
| Datasets | **NOAA's GFS and GDAS analysis/forecast products, pre-converted to ARL format by NOAA's Air Resources Laboratory (ARL).** Multiple temporal/spatial resolutions cover the full historical and forecast period needed for Cluj operations. |
| Consumer / engine | **HYSPLIT** (HYbrid Single-Particle Lagrangian Integrated Trajectory) — NOAA's air mass trajectory and dispersion model. **HYSPLIT is the only consumer of these data files in the project.** Other dispersion engines (FLEXPART, CMAQ, etc.) require different input formats. |
| Producing agency | **NOAA** — specifically the **National Centers for Environmental Prediction (NCEP)** runs the underlying weather models (GFS, GDAS), and the **Air Resources Laboratory (ARL)** converts the operational output into HYSPLIT-compatible ARL format and serves it via FTP, AWS S3 (NODD), and the READY web interface. |
| File format | **ARL packed binary format** — a NOAA-proprietary, HYSPLIT-specific binary structure. **Not GRIB, not NetCDF.** A rough format spec is at <https://www.ready.noaa.gov/gdas1.php>. Read directly by HYSPLIT; for Python inspection without HYSPLIT, see community tool `ARLreader` by Martin Radenz (<https://github.com/martin-rdz/ARLreader>). **The ARL format is not interchangeable with FLEXPART's GRIB inputs** — completely separate ingest pipelines. |
| Status | **OPERATIONAL — open public access.** All current archives continuously updated; frozen archives remain accessible. |
| Authentication | **NONE.** Anonymous access via FTP, HTTP, or unauthenticated AWS S3 (the `--no-sign-request` flag for the AWS CLI). **This is the only data source in the input table requiring no credentials** — no ECMWF account, no ESA account, no EUMETSAT account, no CDSE account, nothing. Just `wget` / `aws s3 cp` / FTP and you have the data. |
| Layer destination | **L2:** **HYSPLIT** (sole consumer — trajectory + dispersion calculations). **L3:** HYSPLIT outputs (back-trajectories, source-region attribution maps, dispersion concentration fields) → Knowledge Graph as trajectory overlay layer + dispersion contour layer. **This row is purely an input dependency for the HYSPLIT row in the table.** |

### The HYSPLIT-relevant archives (for Cluj operations)

**The complete current operational list** of HYSPLIT-compatible global archives, ordered by project relevance for Cluj:

#### 18.1 GFS 0.25° (current operational — the primary one)

| Field | Value |
|---|---|
| Archive period | **June 13, 2019 — present** (continuously updated daily) |
| Resolution | **0.25° × 0.25°** (~28 × 19 km at Cluj's latitude) |
| Vertical | **Native GFS hybrid sigma coordinate system** — terrain-following near the surface, transitioning to pressure surfaces aloft. **This is the right vertical coordinate for accurate boundary-layer dispersion**, and matches what HYSPLIT was designed to consume. |
| Temporal | **3-hourly** time steps (00, 03, 06, 09, 12, 15, 18, 21 UTC analyses + forecasts) |
| File organisation | **Daily files**, each ~2.5 GB compressed |
| Source NCEP system | NCEP GFS.v15 / GFS.v16 (FV3 dynamical core) — the current operational US global forecasting system |
| Naming pattern | `gfs0p25.YYYYMMDD` (daily file) or per-cycle (e.g. `hysplit.YYYYMMDD.00z.gfs0p25f`) |
| Cluj relevance | **The current default operational HYSPLIT driver for Cluj.** Hybrid sigma vertical coordinate + 0.25° resolution + 3-hourly cadence are well-matched to back-trajectory work over Europe. Use this for any case study from June 2019 onwards. |

#### 18.2 GDAS 0.5° (frozen archive — historical use only)

| Field | Value |
|---|---|
| Archive period | **September 1, 2007 — June 11, 2019** (frozen; no longer updated) |
| Resolution | 0.5° × 0.5° (~56 × 38 km at Cluj) |
| Vertical | Native GFS hybrid sigma coordinate system |
| Temporal | 3-hourly |
| File organisation | Daily files, ~500 MB |
| Source NCEP system | Pre-FV3 GFS (older spectral dynamical core) |
| Cluj relevance | **For event studies in the 2007–June 2019 window.** Coarser than the current GFS 0.25°, but methodologically homogeneous within its period. **Frozen — do not expect updates.** |

#### 18.3 GDAS 1° (ongoing weekly archive — long historical record)

| Field | Value |
|---|---|
| Archive period | **2005 — present** (continuously updated; weekly files) |
| Resolution | 1° × 1° (~111 × 76 km at Cluj) |
| Vertical | **Pressure levels** (NOT hybrid sigma — coarser vertical representation) |
| Temporal | 3-hourly |
| File organisation | **Weekly files** (W1 = days 1–7; W2 = 8–14; W3 = 15–21; W4 = 22–28; W5 = 29-end), ~600 MB each |
| Cluj relevance | **Coarser fallback / long historical record.** When the higher-resolution archives are not appropriate (e.g. very long climatologies, computation cost concerns, or the data is mid-2005 to mid-2007 before GDAS 0.5° existed), GDAS 1° provides continuity. **Less accurate near complex terrain like Cluj's** because of the coarser grid + pressure-level vertical interpolation. |

#### 18.4 NCEP/NCAR Reanalysis (very long historical context — 1948 onwards)

| Field | Value |
|---|---|
| Archive period | **1948 — present** (continuous; updated regularly) |
| Resolution | 2.5° × 2.5° (~278 × 191 km at Cluj — very coarse) |
| Vertical | 17 pressure levels |
| Temporal | 6-hourly |
| File organisation | Monthly or annual files |
| Cluj relevance | **Long-period climatology + very old events only.** At 2.5° resolution, Cluj is sub-grid; back-trajectories will be qualitatively useful for synoptic-scale attribution (e.g. "this air came from the Atlantic vs the Sahara") but quantitatively poor. Use only when finer-resolution data does not exist for the period of interest. |

#### 18.5 GFS forecast (forward-trajectory operational use)

| Field | Value |
|---|---|
| Archive period | NRT — the current forecast cycle (00, 06, 12, 18 UTC, each with up to 384-hour forecast) |
| Resolution | 0.25° |
| Vertical | Hybrid sigma |
| Temporal | 3-hourly forecast cadence (within the file) |
| File organisation | Per-cycle forecast files; AWS S3 paths vary by cycle |
| Cluj relevance | **For forward dispersion forecasts.** When the warning chain needs to predict where a current Cluj pollution event will travel in the next 1–7 days, HYSPLIT runs forward with GFS forecast inputs. |

#### 18.6 GEFS (Global Ensemble Forecast System — for uncertainty quantification)

| Field | Value |
|---|---|
| Archive period | NRT (operational); rolling archive |
| Resolution | 0.5° (currently) |
| Members | 30+ ensemble members |
| Cluj relevance | **For trajectory-uncertainty quantification.** Running HYSPLIT with all GEFS members produces a spread of trajectories — the divergence between members at 5-day back-trajectory horizon is a direct uncertainty estimate. Optional / advanced use case; not required for the basic warning chain. |

#### 18.7 Regional archives — NOT relevant for Cluj

The following HYSPLIT archives **cover only North America and are not usable for Cluj operations**:
- **EDAS** (40 km, Eta Data Assimilation System, 2004–present, North America only)
- **NAM12** (12 km, 2007–present, North America only)
- **NARR** (32 km, North American Regional Reanalysis, 1979–present)
- **HRRR** (3 km, June 2015–present, contiguous US only)

These are flagged here so future readers don't waste time evaluating them. **For a European city, always use the global archives** (GFS / GDAS / NCEP-NCAR Reanalysis).

### References

**Primary HYSPLIT model reference:**
- Stein, A. F., Draxler, R. R., Rolph, G. D., Stunder, B. J. B., Cohen, M. D., & Ngan, F. (2015). NOAA's HYSPLIT atmospheric transport and dispersion modeling system. *Bulletin of the American Meteorological Society*, 96(12), 2059–2077. DOI: [10.1175/BAMS-D-14-00110.1](https://doi.org/10.1175/BAMS-D-14-00110.1)

**Original HYSPLIT papers (historical context):**
- Draxler, R. R., & Hess, G. D. (1998). An overview of the HYSPLIT_4 modeling system for trajectories, dispersion, and deposition. *Australian Meteorological Magazine*, 47, 295–308.
- Draxler, R. R. (1999). HYSPLIT4 user's guide. NOAA Tech. Memo. ERL ARL-230 — current version of the user's guide is at <https://www.arl.noaa.gov/documents/reports/hysplit_user_guide.pdf>.

**Meteorological model references (the underlying NOAA systems):**
- **GFS** (Global Forecast System): the operational global model, documented at <https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php>. Major upgrade GFSv15→v16 in 2021; GFSv17 in development with potential ~2026 deployment (check NCEP for current status).
- **GDAS** (Global Data Assimilation System): the analysis system that initialises GFS via 4D hybrid EnVar data assimilation.
- **NCEP/NCAR Reanalysis:** Kalnay, E., Kanamitsu, M., Kistler, R., Collins, W., Deaven, D., Gandin, L., Iredell, M., Saha, S., White, G., Woollen, J., Zhu, Y., Chelliah, M., Ebisuzaki, W., Higgins, W., Janowiak, J., Mo, K. C., Ropelewski, C., Wang, J., Leetmaa, A., Reynolds, R., Jenne, R., & Joseph, D. (1996). The NCEP/NCAR 40-year reanalysis project. *Bulletin of the American Meteorological Society*, 77, 437–471. DOI: [10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2](https://doi.org/10.1175/1520-0477(1996)077%3C0437:TNYRP%3E2.0.CO;2)

**Citation phrasing (NOAA recommended):**
*"This work used NOAA Air Resources Laboratory (ARL) HYSPLIT-compatible meteorological data archives. The data are part of the NOAA Open Data Dissemination (NODD) Program."* Plus the Stein et al. 2015 BAMS paper when HYSPLIT itself is used.

### Host / Server

**Modern recommended access (AWS S3, NODD program):**
- **S3 bucket:** `s3://noaa-oar-arl-hysplit-pds/` (region: us-east-1, no authentication needed)
- **HTTPS-equivalent browse:** <https://noaa-oar-arl-hysplit-pds.s3.amazonaws.com/index.html>
- **AWS CLI access** (no AWS account required): `aws s3 ls --no-sign-request s3://noaa-oar-arl-hysplit-pds/`

**Legacy access (still operational):**
- **ARL FTP server:** `ftp://arlftp.arlhq.noaa.gov/` (anonymous login; email address as password)
- **ARL Data Archive web interface:** <https://www.ready.noaa.gov/archives.php>
- **READY web portal:** <https://www.ready.noaa.gov/> (interactive trajectory runs without local HYSPLIT install)

**HYSPLIT software + documentation:**
- **HYSPLIT homepage:** <https://www.arl.noaa.gov/hysplit/>
- **HYSPLIT user guide:** <https://www.ready.noaa.gov/hysplitusersguide/>
- **HYSPLIT downloads (binary distributions for Windows/macOS/Linux):** <https://www.arl.noaa.gov/hysplit/hysplit/>
- **HYSPLIT forum (technical questions):** <https://hysplitbbs.arl.noaa.gov/>
- **HYSPLIT Docker container** (community-maintained): see HYSPLIT homepage for current links.

**Community ARL-format readers (Python, for inspection / custom analysis):**
- **ARLreader by Martin Radenz:** <https://github.com/martin-rdz/ARLreader>

### Programmatic download

**Step 1 — AWS CLI install (one-time, if not already on system):**

```bash
# Most Linux distributions:
sudo apt install awscli            # Debian/Ubuntu
# or via pip:
pip install awscli
```

**Step 2 — Browse the bucket structure (no auth):**

```bash
# Top-level directories visible
aws s3 ls --no-sign-request s3://noaa-oar-arl-hysplit-pds/

# Drill down into a specific dataset, e.g. GFS 0.25°
aws s3 ls --no-sign-request s3://noaa-oar-arl-hysplit-pds/gfs0p25/

# Listing for a specific date
aws s3 ls --no-sign-request s3://noaa-oar-arl-hysplit-pds/gfs0p25/2026/
```

**Step 3 — Download GFS 0.25° for a specific date:**

```bash
# Single day for HYSPLIT back-trajectory or dispersion run
aws s3 cp --no-sign-request \
    s3://noaa-oar-arl-hysplit-pds/gfs0p25/2026/hysplit.20260318.00z.gfs0p25f \
    ./

# Or a date range for a multi-day back-trajectory:
for d in 20260312 20260313 20260314 20260315 20260316 20260317 20260318; do
    aws s3 cp --no-sign-request \
        s3://noaa-oar-arl-hysplit-pds/gfs0p25/${d:0:4}/hysplit.${d}.00z.gfs0p25f \
        ./
done
```

**Step 4 — Python equivalent using `boto3`:**

```python
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from datetime import datetime, timedelta

# Unauthenticated S3 client
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
bucket = "noaa-oar-arl-hysplit-pds"

# Download 7 days of GFS 0.25° ending today
end = datetime.utcnow().date()
for n in range(7):
    d = end - timedelta(days=n)
    key = f"gfs0p25/{d.year}/hysplit.{d:%Y%m%d}.00z.gfs0p25f"
    s3.download_file(bucket, key, f"hysplit.{d:%Y%m%d}.00z.gfs0p25f")
    print(f"Downloaded {key}")
```

**Step 5 — Run HYSPLIT back-trajectory (after data download):**

```bash
# Assuming HYSPLIT is installed at /opt/hysplit
# Set up CONTROL file pointing to downloaded met data, then:
/opt/hysplit/exec/hyts_std

# Or via the HYSPLIT GUI which auto-detects available ARL files in the working dir
```

**Step 6 — Inspecting ARL file content with the Python ARLreader (no HYSPLIT install required):**

```python
# pip install git+https://github.com/martin-rdz/ARLreader.git
import ARLreader as arl

reader = arl.Reader("hysplit.20260318.00z.gfs0p25f")
print(reader.indexinfo)         # metadata: date, levels, parameters, grid
# Pull a 2D field at one time/level:
u_wind = reader.load_var(parameter="UWND", level=8, valid_time="2026-03-18 12:00")
```

### Manual download (interactive web UI)

- **NOAA READY archives browser:** <https://www.ready.noaa.gov/archives.php> — drill down by dataset, year, month, file. Each file links to the ARL FTP location.
- **READY web trajectory tool** (run HYSPLIT in the cloud without local install): <https://www.ready.noaa.gov/HYSPLIT.php> — useful for one-off back-trajectory plots and sanity-checking the local HYSPLIT setup.
- **AWS S3 browser** (HTTPS): <https://noaa-oar-arl-hysplit-pds.s3.amazonaws.com/index.html> — navigable web view of the bucket, files individually downloadable.

### Notes / caveats

- **No authentication is required.** This is the only data source in the entire project that needs zero credentials, no signup, no terms-of-use acceptance — pure NOAA Open Data Dissemination policy. **Build the HYSPLIT ingest as the absolute simplest pipeline path.**
- **AWS S3 is the modern recommended access path.** The legacy FTP server (`arlftp.arlhq.noaa.gov`) still operates but is slower and less reliable than S3. **New code should target S3**; only fall back to FTP if S3 is unavailable. The S3 bucket is in `us-east-1`, served via standard AWS S3 throughput (multi-GB/s if needed).
- **The GFS 0.25° dataset transitioned from GFSv14 → GFSv15 (FV3 dynamical core) on June 13, 2019**, which is the boundary between two distinct sub-archives: `GFS.v1` (May 2016 – June 2019, GFSv14 spectral core) and `GFS` (≥ June 13, 2019, GFSv15+ FV3 core). For Cluj operations starting now, only the post-June-2019 GFS archive is relevant. The earlier sub-archive is preserved for retrospective consistency studies but is **not** the default — be careful when scripting paths that span the boundary.
- **ARL packed binary format is NOAA-specific and not interchangeable with anything else.** It is read directly by HYSPLIT (and by `ARLreader` in Python). It is NOT GRIB; converters from GRIB to ARL exist (the `arw2arl` and `era52arl` community tools) but require manual configuration and are not officially supported by NOAA. **For the project, accept that HYSPLIT inputs live in the ARL world and don't try to unify them with FLEXPART's GRIB inputs at the file-format level** — unify at the result level (trajectory output, dispersion fields) instead.
- **Each ARL file is large (~2.5 GB for daily GFS 0.25°).** A 7-day back-trajectory back-cast = ~18 GB of ARL meteorology. Cache locally per run; S3 download is fast (typically 60-90 MB/s from us-east-1 to Europe) but not free of cost in run time. **For repeated analyses on the same period, cache aggressively.**
- **Vertical coordinate matters for boundary-layer accuracy.** The native hybrid sigma coordinate (in GFS 0.25° and the frozen GDAS 0.5° archive) is terrain-following near the surface — exactly the right structure for boundary-layer dispersion at Cluj's ~405 m elevation. The pressure-level GDAS 1° interpolates onto pressure surfaces, losing terrain following — **use GDAS 1° only when the higher-resolution archives are unavailable** for the period of interest.
- **For Cluj-specific back-trajectory runs, recommended domain configuration:** GFS 0.25° on the global grid is fine; HYSPLIT will use the global file but only do calculations within the trajectory path. **No domain subsetting needed at the input-file level** (HYSPLIT handles this internally).
- **Update cadence is daily.** New daily ARL files appear on S3 typically within a few hours of the GFS analysis cycle running. For the operational warning chain, NRT HYSPLIT runs using GFS 0.25° can be initialised with at most ~6–12 hour data lag from analysis time.
- **GFS is a forecast model with embedded analyses.** The same archive serves both: analysis fields at 00/06/12/18 UTC + short-range forecasts (3-hourly out to several days) initialised from each analysis. For back-trajectories: use the analyses. For forward trajectories: use the forecasts from the most recent analysis cycle. The HYSPLIT CONTROL file specifies which to read.
- **HYSPLIT versions and Docker.** HYSPLIT 5.x is the current major version. NOAA distributes Linux/macOS/Windows binaries free of charge; a community Docker image also exists which simplifies deployment in containerised pipelines. **For the project pipeline, the Docker approach is probably cleanest** — pin the HYSPLIT version explicitly so re-runs are reproducible.
- **ERA5 vs GFS/GDAS — choice of driver.** **Recommendation already established in the ERA5 file:** drive FLEXPART with ERA5 (its native preferred path), drive HYSPLIT with GFS/GDAS (its native preferred path). The two engines are then independent and can be cross-validated. Trying to use ERA5 for HYSPLIT requires manual `era52arl` conversion which is community-maintained, unsupported, and adds significant pipeline complexity for no real gain — GFS/GDAS at 0.25° is comparable quality to ERA5 at 0.25° for back-trajectory purposes. **Pragmatic operational choice: use both as the native preferred inputs of their respective engines.**
- **NOAA licensing is fully open.** Data are public domain. Attribution requested but not legally required; the project should still cite NOAA properly per the citation phrasing above.
- **Long-term continuity is essentially guaranteed.** NOAA's GFS/GDAS are core operational NWP products of the US National Weather Service. They will be running and freely distributed for the foreseeable future. **Lower programmatic-continuity risk than almost any other data source in the project.**

---
