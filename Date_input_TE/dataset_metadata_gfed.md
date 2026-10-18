# Dataset metadata — GFED (Global Fire Emissions Database)

Companion documentation to the Stage 1 input-data table.
This file describes **GFED** — the **Global Fire Emissions Database** —
the research-grade fire emissions inventory that complements the
operational **GFAS** product covered in the CAMS metadata file
(`dataset_metadata_cams.md`). The two products serve distinct roles in
the project's fire-source attribution chain.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**Critical update vs older documentation: GFED5 was released
November 2025** (van der Werf et al. 2025, *Scientific Data*). This
**supersedes GFED4s** which had been the standard since 2017. The
project should ingest GFED5 directly; any references to GFED4 or GFED4s
in the source docx should be updated.

---

## 20. GFED5 — Global Fire Emissions Database, Version 5

### Summary

| Field | Value |
|---|---|
| Dataset | **GFED5** = Global Fire Emissions Database, fifth version. Released in **November 2025** via peer-reviewed publication in *Scientific Data* (van der Werf et al. 2025). The standard research-grade gridded fire emissions inventory used worldwide for atmospheric chemistry, biogeochemistry, and carbon-budget studies. |
| Producer / Agencies | **Wageningen University & Research** (lead: Guido van der Werf), with co-authors from **University of California Irvine** (James Randerson), **NASA Goddard Space Flight Center** (Douglas Morton), **University of Maryland** (Louis Giglio, Joanne Hall), and others. Originally a Vrije Universiteit Amsterdam (VU) + UCI partnership; the lead institution moved to Wageningen with van der Werf. Funded through NASA Carbon Monitoring System and Dutch national funding. |
| Underlying method | Multiplies **burned area × fuel consumption × emission factors** for each 0.25° grid cell and time step, using a biogeochemical modelling framework (heritage CASA-GFED, now substantially revised for GFED5). **Major GFED5 improvements over GFED4s:** updated burned area from MODIS Collection 6 + Landsat 8 / Sentinel-2 small-fire detections; revised fuel-load estimates from NASA CMS biomass datasets; updated emission factors from NEIVA + new field studies; better representation of small fires. |
| Status (May 2026) | **OPERATIONAL — peer-reviewed v5.1 published November 2025**, plus rolling beta extensions for recent and NRT data (see "GFED5 product tiers" below). |
| Sub-products / tiers within GFED5 | The GFED5 distribution on `globalfiredata.org` has four sub-directories: **(1) GFED5.1** — fully validated, peer-reviewed, **1997 to 2022**. **(2) GFED5.1ext_Beta** — beta extension, **2023 to last year (2025)**, subject to revision. **(3) GFED5.1ext_NRT_Beta** — current-year, updated **daily**, beta status. **(4) Ancillary** — input datasets, code, summary tables. |
| Spatial resolution | **0.25° × 0.25°** for the MODIS era (**2001 onwards**) — ~28 × 19 km at Cluj's latitude. **1.0° × 1.0°** for the pre-MODIS era (**1997–2000**) reflecting larger uncertainties before global burned-area satellite observations were available. |
| Temporal resolution | **Monthly** (canonical primary product). **Daily** (with NRT updates). **3-hourly diurnal scalars** for disaggregating monthly totals to sub-daily timesteps. **Diurnal cycles** provided separately for boreal, temperate, and tropical ecosystems. |
| Temporal coverage | **1997 to present** (continuously updated daily on the NRT-beta stream). The longest-record published fire emissions inventory available. |
| Post-2022 methodology change | **Important caveat.** GFED5.1 (1997–2022) uses MODIS active-fire and burned-area observations as the primary observational base. **For 2023 onwards, the system uses VIIRS active-fire data** (because MODIS Terra/Aqua are well past design life and observational continuity required a switch). The bridge is via relationships between VIIRS active fire and burned area + emissions calibrated during the MODIS-VIIRS overlapping period. **Practical consequence:** small step-change in derived emissions can appear at the 2022/2023 boundary; treat pre-2023 vs post-2023 fire trends with caution unless using the official methodology corrections. |
| Variables | **Burned area** (km²) per fire type. **Carbon (C)** emissions. **Dry matter (DM)**. **Trace gases:** CO₂, CO, CH₄, NMOC (gaseous), H₂, NOx (as NO), N₂O. **Aerosols:** PM2.5, TPC (total particulate carbon), OC, BC. **Other gases:** SO₂, NH₃. **Specific VOCs:** C₂H₆ (ethane), CH₃OH (methanol), C₂H₅OH, C₃H₈, C₂H₂, C₂H₄, C₃H₆, C₅H₈ (isoprene), C₁₀H₁₆ (monoterpenes), C₇H₈ (toluene), C₆H₆ (benzene), C₈H₁₀ (xylene), higher alkanes/alkenes, CH₂O (formaldehyde), C₂H₆S (DMS), HCN (hydrogen cyanide), HCOOH, CH₃COOH. **~40 species total** — the broadest chemical breakdown of any fire-emissions inventory. |
| Fire-type partitioning (the distinctive GFED feature) | **5 categories in GFED5:** (1) **Normal** (`Norm`) — partitioned by 17 major land cover types underneath. (2) **Cropland burning** (`Crop`) — agricultural residue burning, common in Ukraine/Russia spring + autumn. (3) **Deforestation burning** (`Defo`) — primarily tropical, mostly Amazon + SE Asia + Africa. (4) **Peatland burning** (`Peat`) — Indonesia + boreal peat. (5) **Total** (`Total`) — sum of all categories. **This partitioning is GFED's unique value-add over GFAS** — GFAS reports total fire emissions only; GFED tells you *what type* of fire is burning, which has implications for the chemical composition + smoke optical properties + likely transport pathway. (Note: GFED4s used 6 categories: SAVA, BORF, TEMF, DEFO, PEAT, AGRI — GFED5 consolidated these into the simpler scheme above.) |
| File format | **NetCDF4 (CF-compliant)**. One file per category per time period (monthly or daily). |
| Authentication | **SFTP credentials** required for the live `globalfiredata.org` distribution (registration is free, instant); **static published versions on Zenodo** are completely open. Lightweight registration step. |
| Programmatic access | YES — via **SFTP** (`paramiko` or `pysftp` Python libraries; or any standard SFTP client). For static versions, direct HTTPS download from Zenodo. |
| Layer destination | **L2:** FLEXPART (alternative biomass-burning emission input to GFAS — useful for source-attribution work where fire-type partitioning matters); HYSPLIT (similar role). **Primary L2 use: source-type attribution alongside GFAS.** **L3:** Knowledge Graph (historical fire activity climatology over Cluj's source regions; ecosystem-type breakdown of fire contributions to Cluj events). |

### GFAS vs GFED — when to use which (the operational question)

Both products quantify fire emissions; they have distinct strengths and the project should use both. The decision matrix:

| Property | **GFAS** (CAMS, separate metadata file) | **GFED5** (this file) |
|---|---|---|
| Source data | MODIS Fire Radiative Power (FRP) | MODIS burned area + CASA-GFED biogeochemistry model (1997–2022); VIIRS active fire (2023+) |
| Spatial resolution | **0.1°** (finer) | 0.25° |
| Temporal resolution | **Daily** | Monthly + daily (with 3-hourly diurnal scalars) |
| NRT latency | **~1 day** (operational) | **~daily but beta** for NRT; ~6 months for validated |
| Record start | 2003 | **1997 (oldest)** |
| Fire-type partitioning | **No** (total emissions only) | **YES** (Crop, Defo, Peat, Normal × 17 land covers) |
| Number of chemical species | ~40 | **~40 (similar)** |
| Validation level | Operational | **Research-grade, peer-reviewed** |
| Methodology stability | Updated continuously | **Frozen v5.1 (with future v5.2, v6 etc.)** |
| Distribution | ADS (Copernicus Atmosphere Data Store) | globalfiredata.org SFTP + Zenodo |
| **Best use for the project** | **Operational FLEXPART NRT runs (fire-driven)** | **Source-type attribution; historical climatology; published case studies** |

**Recommendation for the project pipeline:** use **GFAS as the operational NRT input** (drives daily FLEXPART runs during fire events), and use **GFED5 as the retrospective/attribution layer** (when an event has occurred, post-hoc analysis with GFED5 gives the fire-type breakdown that GFAS cannot provide, and contributes to publications + technical reports).

### Cluj source regions for biomass burning

GFED's fire-type partitioning is most valuable when interpreted against known regional fire patterns affecting Cluj. The primary upstream fire sources for Cluj are:

- **Ukrainian + southern Russian agricultural burning** (spring March-April + autumn October) — picked up as `Crop` category in GFED5. Common transport path: easterly winds, 1-3 day transit. Major contributor to early-spring PM2.5 elevations across central/eastern Europe.
- **Mediterranean wildfires** (summer June-September) — picked up as `Norm` category (savanna/forest land covers). Transport via southerly/southwesterly flow when active.
- **Balkan + Carpathian regional fires** (summer August-September) — `Norm` category, near-field source for Cluj.
- **Boreal forest fires (Siberia, Scandinavia)** (summer June-August) — `Norm` (boreal forest land cover). Long-range transport contributes to elevated free-tropospheric PM2.5, often seen as elevated layers in EARLINET profiles at Cluj.
- **Saharan/Sahelian dry-season burning** (December-February) — `Norm` (savanna land cover). Less commonly reaches Cluj but possible during specific atmospheric patterns.

GFED5's `Norm × 17 land cover` partitioning allows finer breakdown of these source types — the project's L2 source-attribution layer should preserve the land cover information when sampling GFED5 along FLEXPART back-trajectory paths.

### References

**Primary GFED5 reference (always cite when using GFED5 data):**
- van der Werf, G. R., Randerson, J. T., van Wees, D., Chen, Y., Giglio, L., Hall, J., Vernooij, R., Mu, M., Binte Shahid, S., Barsanti, K. C., Yokelson, R., & Morton, D. C. (2025). Landscape fire emissions from the 5th version of the Global Fire Emissions Database (GFED5). *Scientific Data*, 12, 1870. DOI: [10.1038/s41597-025-06127-w](https://doi.org/10.1038/s41597-025-06127-w)
  - Publisher Correction (January 2026): *Scientific Data*, 13, 44. DOI: [10.1038/s41597-026-06613-9](https://doi.org/10.1038/s41597-026-06613-9)

**Previous-version references (still useful for historical context):**
- van der Werf, G. R., Randerson, J. T., Giglio, L., van Leeuwen, T. T., Chen, Y., Rogers, B. M., Mu, M., van Marle, M. J. E., Morton, D. C., Collatz, G. J., Yokelson, R. J., & Kasibhatla, P. S. (2017). Global fire emissions estimates during 1997–2016. *Earth System Science Data*, 9, 697–720. DOI: [10.5194/essd-9-697-2017](https://doi.org/10.5194/essd-9-697-2017) — **canonical GFED4s reference; for any pre-2025 publications using GFED, this is the citation.**
- Giglio, L., Randerson, J. T., & van der Werf, G. R. (2013). Analysis of daily, monthly, and annual burned area using the fourth-generation global fire emissions database (GFED4). *Journal of Geophysical Research: Biogeosciences*, 118, 317–328. DOI: [10.1002/jgrg.20042](https://doi.org/10.1002/jgrg.20042)

**Companion burned-area paper:**
- Chen, Y., Hall, J., van Wees, D., Andela, N., Hantson, S., Giglio, L., van der Werf, G. R., Morton, D. C., & Randerson, J. T. (2023/2024). Multi-decadal trends and variability in burned area from the 5th version of the Global Fire Emissions Database (GFED5). *Earth System Science Data Discussions* — see globalfiredata.org for the current canonical citation as the paper progresses through peer review.

**Data archive citation (Zenodo persistent identifier for the static GFED5.1 release):**
- van der Werf, G. R., Randerson, J. T., van Wees, D., et al. (2025). Global Fire Emissions Database version 5 (GFED5). *Zenodo*. DOI: [10.5281/zenodo.16794692](https://doi.org/10.5281/zenodo.16794692)

**Citation phrasing (van der Werf et al. recommend):** *"This work used fire emissions data from the Global Fire Emissions Database (GFED5, van der Werf et al. 2025)."* Plus the Zenodo or paper DOI as appropriate.

### Host / Server

- **Main GFED website:** <https://www.globalfiredata.org/>
- **GFED5 data download page:** <https://www.globalfiredata.org/data.html>
- **SFTP server** (registration + credentials at the data page above)
- **Zenodo persistent archive for GFED5.1:** <https://zenodo.org/records/16794692>
- **GFED5 burned-area only (Chen et al.) on Zenodo:** <https://zenodo.org/records/7668424>
- **GFED Analysis Tool (online interactive visualisation):** <https://www.globalfiredata.org/analysis.html>
- **NASA CMS GFED project page:** <https://cce.nasa.gov/cgi-bin/cce/cce_profile.pl?project_group_id=3750>

### Programmatic download

**Step 1 — Register for SFTP access (one-time):**

1. Visit <https://www.globalfiredata.org/data.html>
2. Follow the "login details" link to register for SFTP credentials
3. Wait for credentials email (typically same-day)

**Step 2 — Pull the static published GFED5.1 release from Zenodo (no auth needed):**

```bash
# Monthly emissions (1997-2022, ~50-100 MB compressed)
wget https://zenodo.org/records/16794692/files/GFED5.1_monthly.zip
unzip GFED5.1_monthly.zip -d gfed5_monthly/

# Daily emissions (1997-2022, ~500 MB compressed)
wget https://zenodo.org/records/16794692/files/GFED5.1_daily.zip
unzip GFED5.1_daily.zip -d gfed5_daily/

# Ecosystem-partitioned monthly burned area + carbon (2002-2022)
wget https://zenodo.org/records/16794692/files/GFED5.1_ecosystem.zip
unzip GFED5.1_ecosystem.zip -d gfed5_ecosystem/
```

**Step 3 — Pull rolling NRT data via SFTP:**

```python
import pysftp

# Credentials from your registration email
sftp_host = "globalfiredata.org"   # verify exact hostname in registration email
sftp_user = "your_username"
sftp_pass = "your_password"

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None   # accept any host key; in production, validate properly

with pysftp.Connection(host=sftp_host, username=sftp_user,
                       password=sftp_pass, cnopts=cnopts) as sftp:
    # Pull the NRT beta for the current year
    sftp.chdir("/GFED5/GFED5.1ext_NRT_Beta/")
    files = sftp.listdir()
    for f in files:
        if f.endswith(".nc"):
            sftp.get(f, f"./gfed5_nrt/{f}")
            print(f"Downloaded {f}")
```

**Step 4 — Reading a GFED5 NetCDF file in Python (xarray):**

```python
import xarray as xr

# Example: monthly trace-gas emissions for a specific year
ds = xr.open_dataset("./gfed5_monthly/GFED5.1_monthly_2020.nc")
print(ds)
# Typical variable names: BurnedArea, C, DM, CO2, CO, CH4, PM2p5, OC, BC, ...
# Dimensions: time (months), lat (0.25° from -90 to 90), lon (0.25° from -180 to 180)

# Spatial subset to source-region domain for Cluj (broad: Europe + Mediterranean + West Asia)
cluj_sources = ds.sel(
    lat=slice(30, 70),
    lon=slice(-10, 60),
)

# Time series of monthly fire CO emissions from cropland burning in the Ukraine region
ukraine_box = cluj_sources.sel(lat=slice(45, 52), lon=slice(22, 40))
ukraine_co_monthly = ukraine_box["CO"].sum(dim=["lat", "lon"])  # total emissions in box
ukraine_co_monthly.plot()
```

**Step 5 — Source-type attribution for a Cluj event (along FLEXPART back-trajectory):**

```python
# Pseudocode — assumes FLEXPART back-trajectory already computed
import xarray as xr
import numpy as np

# Load GFED5 ecosystem-partitioned data for the event month
gfed5 = xr.open_dataset("./gfed5_ecosystem/GFED5.1_ecosystem_2024.nc")

# FLEXPART back-trajectory positions (lat, lon, time) for an air mass arriving Cluj
trajectory = load_flexpart_trajectory(...)   # implementation specific

# Sample GFED5 fire emissions along trajectory positions during the relevant month
fire_contributions = {}
for fire_type in ["Norm", "Crop", "Defo", "Peat"]:
    emissions_at_traj = gfed5[fire_type].sel(
        lat=xr.DataArray(trajectory["lat"], dims="traj"),
        lon=xr.DataArray(trajectory["lon"], dims="traj"),
        time=event_month,
        method="nearest",
    )
    fire_contributions[fire_type] = emissions_at_traj.sum().item()

# Result: relative contribution of each fire type to the Cluj event
total = sum(fire_contributions.values())
for fire_type, val in fire_contributions.items():
    print(f"{fire_type}: {100*val/total:.1f}% of biomass-burning emission encountered")
```

### Manual download (interactive web UI)

- **Main data page:** <https://www.globalfiredata.org/data.html> — drills into each sub-directory with file listings
- **GFED Analysis Tool** (online interactive plotter): <https://www.globalfiredata.org/analysis.html> — useful for quick visual checks of "what fires are active in this month over Eurasia?" before committing to API downloads
- **Zenodo published GFED5.1 archive:** <https://zenodo.org/records/16794692>

### Notes / caveats

- **GFED5 supersedes GFED4s; the docx should be updated.** If the source docx references GFED4 or GFED4s, those are the older versions (2017 paper, last update mid-2010s). **GFED5 is the current canonical version** as of November 2025. The two are not numerically identical — GFED5 estimates ~70% higher global carbon emissions (3.4 Pg C/yr vs ~2.0 Pg C/yr) due to better representation of small fires and updated fuel-load estimates. **For any new analysis use GFED5; preserve GFED4s only for backward-compatibility comparisons.**
- **The 2022/2023 methodology boundary is real but bridgeable.** GFED5.1 (1997–2022) uses MODIS as the primary observational base. GFED5.1ext (2023+) uses VIIRS, calibrated against MODIS during the overlap period. **For any analysis spanning the 2022/2023 boundary**, the project pipeline should flag the boundary in the metadata and acknowledge the methodology transition in any deliverables. For Cluj NRT operations (always working with recent dates) the boundary is now in the past — relevant for retrospective climatology studies, not operational use.
- **MODIS Terra/Aqua end-of-life affects GFED's observational continuity.** Same caveat as flagged in the CAMS file for GFAS: both rely (or relied) on MODIS Terra+Aqua. **GFED5 has already partially transitioned to VIIRS for the 2023+ period** — GFAS will follow on a different timeline (the GFAS team's transition strategy is documented separately). **Mid-term continuity of fire emission products is contingent on the VIIRS transitions on both products.**
- **Beta-status for NRT data.** GFED5.1ext_NRT_Beta is **explicitly beta** — the dataset documentation states it is subject to change. For operational warning chain runs in real-time, this is the only NRT GFED option, but the project should record the data version at download time and re-pull when promoted to validated status (typically annual update cycles).
- **Fire-type partitioning is GFED's distinguishing capability.** **GFAS does not partition by fire type** (it reports total emissions per pixel). **For source attribution — answering "is this Cluj PM event from Ukrainian agricultural burning or from Mediterranean wildfires?" — GFED5 is the necessary tool.** The fire-type information is the project's primary reason to ingest GFED5 alongside the GFAS NRT operational stream.
- **Monthly vs daily resolution choice.** For operational forward dispersion modelling, daily GFED5 emissions are preferred (closer to actual fire activity timing). For attribution + climatology + retrospective publications, monthly GFED5 is the conventional reference. **3-hourly diurnal scalars** are provided to disaggregate monthly emissions to sub-daily timesteps, but the underlying daily data is already at the finest meaningful resolution given the satellite observation cadence.
- **Spatial resolution at Cluj source regions is ~28 × 19 km** — coarser than GFAS (~10 km at Cluj) but adequate for synoptic-scale fire source attribution. **Cluj itself is rarely a fire source** (urban area, low fire activity); GFED5 is most useful for characterising the source regions upwind. For local fires in the Carpathian region (occasional summer events), the coarser GFED5 resolution may underestimate intensity vs GFAS.
- **No vertical injection profile.** GFED5 provides **surface emission flux only** — it does not specify the injection height of the smoke plume (which can be 1–5 km AGL for large convective fires). FLEXPART needs an injection height assumption; standard practice is to inject across a 0–500 m AGL layer for small fires, 500–3000 m for medium fires, and use plume-rise parametrisations (e.g. Sofiev) for major events. **The injection-height assumption is a significant uncertainty source** for any fire-driven dispersion modelling, regardless of whether GFAS or GFED5 is used as the emission input.
- **SFTP access is the live distribution path.** The Zenodo archive captures static published versions only. **For ongoing NRT pipeline work, plan around SFTP credentials** — pretty standard, but worth flagging as a different access mode from the HTTPS/S3 pattern dominant elsewhere in the project.
- **Free license; attribution required.** GFED data are public, no commercial restrictions. Cite van der Werf et al. 2025 + the Zenodo DOI of the specific GFED5 sub-version used.
- **Cross-validation against GFAS.** For any Cluj event with significant biomass-burning contribution, pull both GFAS and GFED5 emissions over the suspected source region for the relevant period. **Strong agreement = high confidence**; disagreement may indicate either methodology-driven differences (FRP vs burned-area approaches respond differently to fire intensity vs fire area) or genuine event-specific issues. **GFED5 typically reports somewhat higher emissions than GFAS** for the same event because GFED5 incorporates small-fire detections beyond MODIS sensitivity that GFAS misses. Plan for ~20-50% systematic difference in absolute emission magnitude between the two products even when both are correctly characterising the same event.
- **NEIVA emission factors are the new standard.** GFED5 emission factors come from the NEIVA (Network for Emission Inventory and Validation in the Atmosphere) compilation plus several recent landscape-scale field campaigns. These are different from the Akagi 2011 emission factors used in GFED4s, so per-species emissions in GFED5 are not directly comparable to GFED4s on a species-by-species basis without unit-conversion using the published cross-walk tables in the GFED5 paper.

---
