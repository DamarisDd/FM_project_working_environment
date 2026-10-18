# Dataset metadata — ERA5 (ECMWF reanalysis)

Companion documentation to the Stage 1 input-data table.
This file describes the **ERA5 atmospheric reanalysis** from ECMWF
(European Centre for Medium-Range Weather Forecasts) — the primary
meteorological driver for the project's **FLEXPART** and **HYSPLIT**
dispersion/trajectory engines, and the meteorological backbone for
context fields in the warning chain's Knowledge Graph.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

ERA5 is the project's **largest single data dependency by volume.** Each
FLEXPART or HYSPLIT run that produces a dispersion/back-trajectory result
in the warning chain consumes hours of model-level ERA5 fields over a
domain large enough to cover all possible source regions for Cluj.
**Designing the ERA5 ingest cache is the single biggest architectural
decision in the project's L2 layer.**

---

## 16. ERA5 — ECMWF fifth-generation atmospheric reanalysis

### Summary

| Field | Value |
|---|---|
| Dataset family | **ERA5** = fifth-generation ECMWF atmospheric reanalysis of the global climate. **Covers January 1940 to ~5 days before present** (continuously extended via the ERA5T preliminary stream). Produced by the **Copernicus Climate Change Service (C3S)** at **ECMWF** under contract from the European Commission. Reanalysis combines a frozen-version forecast model (ECMWF IFS Cy41r2) with all available historical observations via 4D-Var data assimilation, producing a physically consistent, gap-free record of the atmospheric state. |
| Producer / Agency | **ECMWF** (Reading, UK — implementation + production) on behalf of **C3S** / European Commission. Open data, free for any use, attribution required. |
| Sub-products in the family | **ERA5 single-level** (surface and 2D fields), **ERA5 pressure-levels** (37 standard pressure levels), **ERA5 model-levels / "complete"** (137 native hybrid-sigma model levels, full vertical resolution — **the FLEXPART/HYSPLIT-relevant product**), **ERA5 ensemble** (ten-member ensemble at half resolution, for uncertainty quantification), **ERA5-Land** (land-surface only, at 0.1° / ~9 km, higher-resolution subset). **ERA5.1** (corrected version 2000–2006 only — fixes a stratospheric temperature discontinuity in original ERA5 for that period). |
| Spatial resolution (atmosphere) | **31 km global (0.25° × 0.25° regular lat/lon grid for distributed products)** — native model is reduced Gaussian grid TL639, distributed grid is interpolated. **For Cluj** at 46.77°N, 23.55°E, this is a grid cell of approximately **0.25° × 0.25° = ~28 km × ~19 km** (cosine of latitude shrinks the E-W extent at higher latitudes). |
| Spatial resolution (ERA5-Land) | **0.1° × 0.1° (~9 km × ~7 km at Cluj's latitude)** — significantly higher resolution than atmospheric ERA5, but **land-surface fields only** (skin temperature, soil moisture, snow, runoff, etc.). Not useful as meteorological driver for FLEXPART/HYSPLIT (which need wind + temperature + humidity profiles), but useful for surface-context layers in the Knowledge Graph (e.g. surface temperature anomalies, soil moisture status for dust emission potential). |
| Vertical resolution | **137 hybrid-sigma model levels** from surface (model level 137) up to ~0.01 hPa (~80 km, model level 1). Model levels are denser near the surface (~10–30 m spacing in the boundary layer, ~150–300 m in the free troposphere, coarsening at altitude). **For FLEXPART/HYSPLIT this is essential** — the model levels follow terrain and give the actual vertical structure the dispersion solvers need. **The 37 standard pressure levels are only adequate for column work; FLEXPART/HYSPLIT prefer model levels.** |
| Temporal resolution | **Hourly** (1-hour timestep) for all atmospheric variables — a major improvement vs the predecessor ERA-Interim's 6-hourly resolution. This hourly cadence is what makes ERA5 suitable for sub-daily dispersion modelling against rapidly evolving events. |
| Temporal coverage and latency | **1940 to present**, updated continuously. **Final ERA5: ~3 months latency** (data goes through quality control + reprocessing). **ERA5T: ~5 days latency** ("preliminary" stream — same model, same variables, same access path, just earlier in the QA cycle). **ERA5T data is replaced by final ERA5 ~3 months later**; downstream pipelines should be aware that ERA5T data for any given date may be revised when promoted to final. For the warning chain, **ERA5T is the operational stream** — 5 days back is recent enough to drive next-7-day FLEXPART/HYSPLIT forecasts. |
| File format | **GRIB1 / GRIB2** (native ECMWF format, smaller files, requires ECMWF eccodes library to parse) or **NetCDF4** (CF-style, easier ingest with xarray, larger files). The `data_format` parameter in CDS API requests controls which is delivered. **For FLEXPART, GRIB is the native and preferred format** (FLEXPART's `flex_extract` tool produces GRIB directly). **For HYSPLIT, NOAA ARL-format files are needed** (separate conversion step required). **For Python data analysis layers (the Knowledge Graph context fields), NetCDF is more convenient.** |
| Filename pattern | Filenames are user-specified at download time (CDS API target parameter). Conventional pipeline naming: `era5_<level_type>_<variable>_<YYYYMMDD>_<HH>.grib` or similar. |
| Status (May 2026) | **OPERATIONAL — open public access.** The entire ERA5 family is continuously produced and distributed. **CRITICAL: the access infrastructure migrated mid-2024** (see "Authentication" below) — any pipeline code written before September 2024 against the legacy CDS endpoint will fail. |
| Cluj subset size | A ±5° box around Cluj (~22°E to ~29°E, ~42°N to ~52°N covering source regions for trajectories) at 0.25° = ~29 × 41 = ~1190 grid points per level. For 137 model levels + 24 hours/day + ~6 essential variables (u, v, w, T, Q, surface fields) = **~120 MB/day GRIB / ~400 MB/day NetCDF (rough estimate)** per analysis pipeline run. A 7-day back-trajectory FLEXPART run needs ~7 days of input = ~1 GB. The ingest cache architecture should be sized accordingly. |
| Authentication | **NEW (post-Sept 2024) credential path:** ECMWF account → CDS personal access token. **Old CDS UID:KEY format is dead.** Setup steps documented under "Programmatic download" below. |
| Programmatic access | YES — `cdsapi` Python library (must be the post-2024 version, ≥ 0.7.0). STAC catalogue browsing available at <https://cds.climate.copernicus.eu/stac-browser/>. **For FLEXPART specifically**, the canonical tool is `flex_extract` (developed at Univ. Vienna / BOKU) which wraps CDS API calls and produces FLEXPART-ready GRIB files. **For HYSPLIT**, no equivalent tool — manual ARL conversion is needed if ERA5 is preferred over NOAA's native GFS/GDAS data. |
| Layer destination | **L1:** Direct ingestion of GRIB/NetCDF subset over the relevant domain (Cluj ±10° typical for FLEXPART, ±20° for long-range HYSPLIT back-trajectories). **L2:** **FLEXPART** (full model-level u, v, w, T, Q, surface pressure, surface fluxes — primary use); **HYSPLIT** (alternative meteorological driver to NOAA GFS/GDAS, requires ARL conversion). **L3:** Knowledge Graph (selected derived fields as context layers: 10 m wind, 2 m temperature, boundary layer height, total precipitable water, CAPE — gives the GUI a meteorological context overlay alongside the aerosol fields). |

### Why ERA5 is central to the warning chain

ERA5 is not a measurement source; it is a **meteorological driver**. The warning chain uses ERA5 in three distinct ways:

1. **Driving the dispersion/trajectory engines.** FLEXPART (forward dispersion: "where will this pollution plume be in 24 / 48 / 72 hours?") and HYSPLIT (back-trajectories: "where did the air mass currently over Cluj originate?") both need full 3D wind + temperature + humidity fields at high temporal cadence. ERA5 provides the standard meteorology that both engines support natively or with minor conversion. **Without ERA5 (or its equivalent), L2 dispersion modelling is impossible.**

2. **Surface-context layers in the GUI.** 10 m wind direction, 2 m temperature, mixed-layer/boundary-layer height, total precipitable water, CAPE — these aren't strictly required for the warning logic, but they massively help operational interpretation of the aerosol field. *"Why is the AOD at Cluj this high?"* often has a meteorological answer (low boundary layer trapping local emissions; specific wind direction transporting a regional source; precipitation washing the layer out) that the operator can immediately recognise if the meteorological context is overlaid.

3. **Cross-validation for forecast products downstream.** CAMS forecasts and the project's own FLEXPART/HYSPLIT runs are all driven by either ERA5 (reanalysis) or ECMWF IFS (forecast). Comparing CAMS forecast surface PM against ERA5-driven FLEXPART surface concentration estimates provides one form of internal model intercomparison.

### References

**Primary reference (always cite when using ERA5 data):**
- Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz-Sabater, J., Nicolas, J., Peubey, C., Radu, R., Schepers, D., Simmons, A., Soci, C., Abdalla, S., Abellan, X., Balsamo, G., Bechtold, P., Biavati, G., Bidlot, J., Bonavita, M., De Chiara, G., Dahlgren, P., Dee, D., Diamantakis, M., Dragani, R., Flemming, J., Forbes, R., Fuentes, M., Geer, A., Haimberger, L., Healy, S., Hogan, R. J., Hólm, E., Janisková, M., Keeley, S., Laloyaux, P., Lopez, P., Lupu, C., Radnoti, G., de Rosnay, P., Rozum, I., Vamborg, F., Villaume, S., & Thépaut, J.-N. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999–2049. DOI: [10.1002/qj.3803](https://doi.org/10.1002/qj.3803)

**ERA5-Land reference:**
- Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C., & Thépaut, J.-N. (2021). ERA5-Land: a state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data*, 13, 4349–4383. DOI: [10.5194/essd-13-4349-2021](https://doi.org/10.5194/essd-13-4349-2021)

**Data citation DOIs (per CDS-issued dataset DOIs — cite the specific dataset you used, not the mission paper):**
- ERA5 hourly data on single levels from 1940 to present: [10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.adbb2d47)
- ERA5 hourly data on pressure levels from 1940 to present: [10.24381/cds.bd0915c6](https://doi.org/10.24381/cds.bd0915c6)
- ERA5-Land hourly data from 1950 to present: [10.24381/cds.e2161bac](https://doi.org/10.24381/cds.e2161bac)
- Complete ERA5 (model levels, via MARS): cite the Hersbach 2020 paper plus the dataset web page <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-complete>.

**Citation example** (CDS-recommended phrasing): *"Generated using Copernicus Climate Change Service information [YEAR]. Contains modified Copernicus Climate Change Service information [YEAR]. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains."*

### Host / Server

- **Copernicus Climate Data Store (CDS):** <https://cds.climate.copernicus.eu/> (the post-Sept-2024 platform — the only operational one)
- **CDS API endpoint:** `https://cds.climate.copernicus.eu/api`
- **ECMWF account creation:** <https://www.ecmwf.int/user/login> (required for CDS access — old CDS account is no longer valid)
- **CDS personal access token page:** <https://cds.climate.copernicus.eu/how-to-api>
- **ERA5 documentation:** <https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation>
- **CDS STAC catalogue:** <https://cds.climate.copernicus.eu/stac-browser/>
- **CDS user forum** (for API troubleshooting): <https://forum.ecmwf.int/>
- **`flex_extract` tool** (FLEXPART preprocessor for CDS data): <https://www.flexpart.eu/flex_extract/>
- **HYSPLIT ARL format converters** (community-maintained, e.g. via ARL's NOAA pages): <https://www.ready.noaa.gov/READYcmet.php>

### Programmatic download

**Step 1 — Account and credentials setup (one-time, mandatory after Sept 2024):**

1. Create or sign in to an **ECMWF account** at <https://www.ecmwf.int/user/login>. (Note: the legacy CDS-only credentials were deprecated in 2024 — accounts must be ECMWF-unified now.)
2. Visit <https://cds.climate.copernicus.eu/how-to-api> and copy your **personal access token** (a long opaque string).
3. Create or update `~/.cdsapirc` with exactly two lines:
   ```
   url: https://cds.climate.copernicus.eu/api
   key: <PERSONAL-ACCESS-TOKEN>
   ```
   The **URL `https://cds.climate.copernicus.eu/api` is the post-2024 endpoint.** Any old URLs ending in `/api/v2` or pointing to `cds-beta.climate.copernicus.eu` are deprecated.
4. Install the post-2024 `cdsapi` package: `pip install --upgrade cdsapi` (verify version ≥ 0.7.0).
5. **Accept the terms of use** for every dataset you intend to download. This must be done **once per dataset, manually, via the web UI** (visit the dataset page, scroll to the bottom of the download form, click "Accept terms"). API calls fail with a 403 error if the terms have not been accepted for the requested dataset.

**Step 2 — Basic CDS API retrieval for ERA5 over the Cluj domain:**

```python
import cdsapi
import os
from datetime import datetime, timedelta

client = cdsapi.Client()

# Cluj region domain: ~22-29°E, ~42-52°N (covers typical 3-7 day back-trajectory source regions)
cluj_area = [52.0, 22.0, 42.0, 29.0]   # [N, W, S, E] in CDS convention

# Pressure-level fields for general atmospheric analysis (FLEXPART prefers model levels, see below)
target_pressure = "era5_pl_cluj_20260318.nc"
client.retrieve(
    "reanalysis-era5-pressure-levels",
    {
        "product_type": ["reanalysis"],
        "variable": [
            "u_component_of_wind", "v_component_of_wind", "vertical_velocity",
            "temperature", "specific_humidity", "geopotential",
        ],
        "pressure_level": [
            "50", "100", "150", "200", "250", "300", "400", "500", "600",
            "700", "750", "800", "850", "900", "925", "950", "975", "1000",
        ],
        "year": ["2026"], "month": ["03"], "day": ["18"],
        "time": [f"{h:02d}:00" for h in range(24)],
        "area": cluj_area,
        "grid": [0.25, 0.25],
        "data_format": "netcdf",
    },
    target_pressure,
)

# Surface fields (10 m winds, 2 m T, MSLP, boundary layer height, total precipitable water,
# surface fluxes — relevant for KG context layers and FLEXPART boundary conditions)
target_sfc = "era5_sfc_cluj_20260318.nc"
client.retrieve(
    "reanalysis-era5-single-levels",
    {
        "product_type": ["reanalysis"],
        "variable": [
            "10m_u_component_of_wind", "10m_v_component_of_wind",
            "2m_temperature", "2m_dewpoint_temperature",
            "mean_sea_level_pressure", "boundary_layer_height",
            "total_column_water_vapour", "convective_available_potential_energy",
            "surface_sensible_heat_flux", "surface_latent_heat_flux",
            "surface_solar_radiation_downwards", "total_precipitation",
        ],
        "year": ["2026"], "month": ["03"], "day": ["18"],
        "time": [f"{h:02d}:00" for h in range(24)],
        "area": cluj_area,
        "grid": [0.25, 0.25],
        "data_format": "netcdf",
    },
    target_sfc,
)
```

**Step 3 — Model-level data for FLEXPART (the preferred path):**

```python
# Model-level ERA5 ("reanalysis-era5-complete") is on the native 137-level grid
# and is accessed via MARS through the CDS API. NOTE: this is on tape archive,
# so retrieval is slower (queued; expect minutes to hours, sometimes a few days
# for old data — see "Notes/caveats" below). MARS syntax is used in the request.

client.retrieve(
    "reanalysis-era5-complete",
    {
        # MARS syntax — keywords 'expver' and 'class' are imposed by the dataset and omitted
        "date": "2026-03-18",
        "stream": "oper",
        "type": "an",            # analysis (vs forecast 'fc')
        "levtype": "ml",         # model levels (vs 'pl' pressure, 'sfc' surface)
        "levelist": "1/to/137",  # all 137 model levels — use a subset to save data volume
        "param": "130/131/132/133/152",  # T, U, V, Q, lnsp (log surface pressure)
        # 130=T, 131=U, 132=V, 133=Q, 152=lnsp, 135=W (omega), 138=vorticity, etc.
        # Full param list at https://apps.ecmwf.int/codes/grib/param-db/
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "grid": "0.25/0.25",
        "area": "52/22/42/29",   # N/W/S/E
        "format": "grib",
    },
    "era5_ml_cluj_20260318.grib",
)
```

**Step 4 — FLEXPART-specific extraction via `flex_extract`:**

```bash
# flex_extract handles all the MARS-specific details + GRIB post-processing required
# for FLEXPART input format. Install from https://www.flexpart.eu/flex_extract/

git clone --branch master https://www.flexpart.eu/repos/flex_extract.git
cd flex_extract
# Edit Run/Control/CONTROL_<your_setup>.GLOBAL with your domain, dates, levels
# Then:
./Run/run_local.sh
# Output: GRIB files ready for FLEXPART consumption
```

**Step 5 — Reading ERA5 NetCDF in Python for KG context layers:**

```python
import xarray as xr
ds_sfc = xr.open_dataset("era5_sfc_cluj_20260318.nc")
# Variables in the dataset:
# - u10, v10 (10m wind components)
# - t2m (2m temperature)
# - msl (mean sea level pressure)
# - blh (boundary layer height — directly useful as a context layer for "is the BL trapping pollution?")
# - tcwv (total column water vapour)
# - cape (instability proxy for convective mixing)

# Extract a Cluj timeseries at the nearest grid point:
cluj_ts = ds_sfc.sel(latitude=46.77, longitude=23.55, method="nearest")
cluj_ts['blh'].plot()  # Diurnal boundary layer height cycle over Cluj
```

### Manual download (interactive web UI)

- **CDS website search:** <https://cds.climate.copernicus.eu/> → search "ERA5"
- **Main ERA5 datasets:**
  - ERA5 hourly data on single levels: <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels>
  - ERA5 hourly data on pressure levels: <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels>
  - ERA5 monthly means: <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means>
  - ERA5-Land hourly data: <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land>
  - Complete ERA5 (model levels via MARS — API only): <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-complete>

Each dataset page has an interactive "Download data" form that builds the request and shows the corresponding API code snippet via the "Show API request code" button — useful for verifying API syntax against current dataset conventions.

### Notes / caveats

- **The CDS migration of mid-2024 is the single most important pipeline-affecting change.** The old `https://cds.climate.copernicus.eu/api/v2` endpoint was decommissioned on **26 September 2024**, alongside the old UID:KEY auth format and the CDS-specific account system. Any project code written before that date against the legacy CDS will silently fail or return cryptic errors. **All ingest scripts must use the new endpoint + ECMWF-unified account + personal access token.** This is the single most likely thing to be outdated in the docx.
- **`cdsapi` package version matters.** Use ≥ 0.7.0 for the new CDS. Older versions hard-code legacy URLs and will not work even with the new credentials. Pin in the pipeline's `requirements.txt`: `cdsapi >= 0.7.0`.
- **ERA5 vs ERA5T — the operational distinction.** Final ERA5 has ~3 month latency (data goes through full QC reprocessing). **ERA5T is the preliminary stream at ~5 days latency** — same model, same variables, same access path. **For the operational warning chain ERA5T is the relevant stream.** Be aware that ERA5T data for any given date will be **silently replaced by final ERA5 ~3 months later**, with potentially small numerical changes. **If you cache ERA5T data, re-pull as final-ERA5 once the 3-month cutoff passes,** especially for any retrospective analysis.
- **Model levels are on tape (MARS archive) and slower to retrieve.** The `reanalysis-era5-complete` dataset is not on spinning disk — it's on ECMWF's MARS tape archive. CDS API requests for model-level data are queued and can take **minutes to hours** (sometimes longer during high-load periods). The latest ~2 months of ERA5T model levels are kept on disk and respond faster. **Plan the FLEXPART input pipeline to be asynchronous** — submit requests, poll for completion, then trigger downstream runs.
- **CDS request queueing and limits.** Each user has concurrent-request limits (typically 1–2 simultaneous queued requests, ~20 GB/request soft cap). For high-volume bulk historical extraction, contact ECMWF directly or use the **WekEO** service which is a Copernicus-funded operational data-access platform with higher throughput. For the project's operational scale (one daily run pulling ~7 days of model-level data over Cluj ±5°), the standard CDS quota is sufficient.
- **ERA5-Land is land-only — not a meteorological driver.** ERA5-Land's higher 0.1° resolution applies only to land-surface variables (skin T, soil moisture, snow, runoff). It does NOT contain wind, temperature profile, or any atmospheric column data above the surface. **Cannot substitute for ERA5 atmospheric** as a FLEXPART/HYSPLIT driver. Use ERA5-Land for surface-context layers in the GUI only (e.g. "is the surface dry, supporting dust suspension?").
- **GRIB vs NetCDF choice — significant operational difference.** GRIB is ECMWF's native format, smaller files (~3-5× smaller than NetCDF for the same data), but requires `cfgrib` / `eccodes` to read in Python. NetCDF is larger but xarray reads it natively. **For FLEXPART: GRIB (flex_extract produces GRIB).** **For analysis/visualization layers: NetCDF.** Some teams maintain both versions of the cache; trade-off is disk space vs ingest speed.
- **For HYSPLIT — alternative driver paths.** HYSPLIT is a NOAA tool and is designed around NOAA's native GFS / GDAS / NAM / HRRR datasets, which are pre-converted to NOAA's ARL format and freely available from NOAA's READY/ARL servers at <https://www.ready.noaa.gov/>. **For the warning chain, using GFS/GDAS for HYSPLIT (skipping ERA5 entirely for that engine) is the path of least resistance** — NOAA tools download and ingest the data directly without any conversion. ERA5 → HYSPLIT requires an ARL-format conversion step (community tools exist but are not officially supported by either ECMWF or NOAA). **Recommendation: drive FLEXPART with ERA5 (its native preferred path) and drive HYSPLIT with GFS/GDAS (its native preferred path); cross-validate.**
- **Vertical coordinate is hybrid sigma-pressure, not pure pressure.** Model levels follow terrain near the surface and transition to pressure levels aloft. **For Cluj at ~405 m elevation in mountainous terrain, the lowest few model levels follow the actual orography**, which is exactly what's needed for accurate boundary-layer dispersion. Pressure-level interpolation loses this terrain following and is acceptable for free-troposphere transport but degrades surface emission attribution. **Always use model levels (`levtype=ml`) when driving FLEXPART for Cluj-scale work.**
- **Hourly cadence is real but uncertainty grows for sub-grid features.** ERA5 is hourly *output*, but the underlying assimilation is 12-hourly 4D-Var. Between assimilation windows, ERA5 hourly fields are a free-running short forecast. For synoptic-scale meteorology this is fine; for fine-scale convection or boundary-layer features, ERA5 is smoother and less skilful than NWP forecasts driven by local observations. **For Cluj's complex topography, expect ERA5's resolved wind field to be a regional-scale signal**, not a local-canyon-flow signal — operators should be aware that local thermal/topographic flows in Cluj are sub-grid.
- **Hersbach 2020 paper is the canonical citation** — always cite it in addition to the dataset-specific DOI when ERA5 data is used in any publication, technical report, or deliverable.
- **License is open, attribution required.** ERA5 is free for any use including commercial. Attribution wording per CDS recommendation included above.
- **Domain sizing for back-trajectories.** Cluj 5-day back-trajectories typically reach the Atlantic, North Africa, or Central Asia depending on synoptic conditions. **Recommended minimum domain for HYSPLIT back-trajectory work: 20°W to 60°E, 25°N to 65°N.** For shorter 24–48 hour forward FLEXPART dispersion, ±5–10° around Cluj is sufficient. Size the ERA5 cache accordingly — bigger domains = much bigger volume.

---
