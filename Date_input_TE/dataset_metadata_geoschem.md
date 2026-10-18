# Dataset metadata — GEOS-Chem and HEMCO

Companion documentation to the Stage 1 input-data table.
This file describes the **GEOS-Chem chemistry-transport model** and its
emissions component **HEMCO** — the research-grade independent
counterpart to the operational CAMS and MERRA-2 reanalyses in the
project's L2 chemistry layer.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**Critical architectural distinction:** Unlike every other entry in the
input-data table — which describes a **pre-computed dataset** that the
project downloads — GEOS-Chem is a **model the project would run
itself.** This entry therefore documents three distinct project-relevant
artefacts:

1. **GEOS-Chem itself** — the model, what it computes, what runs cost
2. **HEMCO standalone** — the emissions aggregator can be used independently of GEOS-Chem as a powerful tool for combining EDGAR, CEDS, GFED5, GFAS, and other inventories into a unified gridded emission product
3. **The GEOS-Chem Input Data archive on AWS** (`s3://geos-chem/`) — open-data S3 bucket containing curated MERRA-2, GEOS-FP meteorology + preprocessed emission inventories that can be directly useful for the project even without running GEOS-Chem

---

## 21. GEOS-Chem and HEMCO — research-grade chemistry-transport model + emissions component

### Summary

| Field | Value |
|---|---|
| Software | **GEOS-Chem** = global 3D chemistry-transport model originally developed at Harvard by Daniel Jacob's group; now **community-maintained** by an international consortium with a Steering Committee, Working Groups, and a Support Team at WashU (Randall Martin's group) / Harvard. Open-source under MIT License. **HEMCO** = Harmonized Emissions Component — the emissions preprocessor used inside GEOS-Chem; also runs **standalone** as a generic emissions-data tool usable by other models or pipelines. |
| Current versions (May 2026) | **GEOS-Chem v14.7.0** (released February 2026) — major recent additions in v14.6.0–14.7.0: **12 km nested-grid capability** (Wang et al. 2026), **CEDS v_2021_04_21 anthropogenic emissions at 0.1°×0.1°**, nonspherical mineral dust optics, updated dust module. **HEMCO v3.12.0** (released February 2026) — the modular emissions handler. |
| Two flavours of GEOS-Chem | **(a) GEOS-Chem Classic** — Fortran code, runs offline on driving meteorology (GEOS-FP or MERRA-2 pre-processed for GEOS-Chem). Standard for most research applications. **(b) GCHP (GEOS-Chem High Performance)** — same chemistry on a cubed-sphere grid, MPI-parallel, scales to many cores. For high-resolution or large-ensemble work. |
| Source code repositories | **GEOS-Chem Classic:** <https://github.com/geoschem/GCClassic>. **GEOS-Chem core science modules** (shared with GCHP): <https://github.com/geoschem/geos-chem>. **HEMCO:** <https://github.com/geoschem/HEMCO>. **Documentation:** <https://geos-chem.readthedocs.io/>. |
| Underlying meteorology | **NASA GEOS-FP** (NRT operational) or **MERRA-2** (reanalysis, also covered in `dataset_metadata_merra2.md`). GEOS-Chem is *driven* by these — it does not assimilate observations itself. Both meteorologies are pre-processed by the GMAO into a GEOS-Chem-ready format and distributed via the GEOS-Chem Input Data archive. |
| Chemistry capabilities | **Detailed gas-phase tropospheric and stratospheric chemistry** via the KPP solver (Kinetic PreProcessor) — hundreds of species, thousands of reactions. **Aerosol modules:** sulfate, nitrate, ammonium, **secondary organic aerosol (SOA)**, black carbon, primary organic carbon, dust (multiple bins), sea salt (multiple bins). **Key project-relevant strength: GEOS-Chem includes a full nitrate aerosol scheme** with proper thermodynamic equilibrium (ISORROPIA-II) — this is the most important chemical capability missing from MERRA-2 GOCART and limited in CAMS. **For Cluj winter PM2.5 (where nitrate dominates under stagnant anticyclones), GEOS-Chem is the most physically realistic model in the project's L2 layer.** |
| Resolution options for the project | **Global Classic:** 4°×5° (~500 km, fast, dev/testing), 2°×2.5° (~280 km, modest), 0.5°×0.625° MERRA-2 native (~50 km global, expensive). **Nested Classic:** 0.5°×0.625° MERRA-2-driven OR 0.25°×0.3125° GEOS-FP-driven (~28 km at Cluj, recommended for European studies) OR **0.125°×0.15625° (~12 km, NEW in v14.6.0)** for 2021+. **GCHP:** any cubed-sphere resolution, typically c180 (~50 km) to c720 (~12 km) or finer. **For Cluj: 0.25°×0.3125° GEOS-FP nested over Europe is the recommended baseline; the new 12 km capability is the higher-end option.** |
| Output | NetCDF4 files containing 3D + 2D fields of all simulated species at user-specified output frequency (typically hourly or 3-hourly). Standard diagnostics include species concentration, AOD, deposition fluxes, source-attribution diagnostics, etc. |
| Authentication | **NONE** — GEOS-Chem source code is open MIT; input data on AWS S3 is part of the **AWS Open Data Sponsorship Program** (no egress fees, anonymous access works). **Like the HYSPLIT meteorological data, this is a fully open-access resource with no credential requirements.** |
| Layer destination | **L2:** Primary use is as **research-grade comparator** for CAMS and MERRA-2 in specific case studies, especially events where chemistry detail matters (nitrate-dominated winter PM, biogenic SOA episodes, mixed-source events). HEMCO standalone can produce harmonised gridded emission inputs to FLEXPART runs. **L3:** Knowledge Graph (case-study GEOS-Chem outputs as overlay layers for retrospective publications; not for NRT operations). |

### Three project-relevant uses of GEOS-Chem (in order of feasibility)

#### Use case 1: HEMCO standalone for emissions aggregation (most feasible)

**HEMCO** is the GEOS-Chem emissions preprocessor — but it also runs **completely standalone** without GEOS-Chem. In standalone mode, HEMCO is a powerful generic tool for:

- Reading any of the **hundreds of emission inventories** in its built-in library (EDGAR all versions, CEDS, GFED4s + GFED5, GFAS, EMEP, NEI, MEGAN biogenic, AEIC aviation, EDGAR-NH3, custom inventories, etc.)
- Regridding inventories to a **user-specified grid** at any resolution
- **Combining inventories** with masks, scaling factors, time-dependent extensions, vertical distribution
- Computing **meteorology-dependent natural emissions** (dust, sea salt, soil NOx, lightning NOx, biogenic VOCs from MEGAN, etc.) on-the-fly given input meteorology
- Outputting unified gridded emission fields in **NetCDF4** ready for ingestion into FLEXPART, HYSPLIT, or any other model

**For the project: HEMCO standalone is the most directly usable GEOS-Chem component.** It allows the project to:
- Aggregate **EDGAR (anthropogenic) + GFED5 (fire) + biogenic + dust + sea salt** into one consistent emission product over Cluj's source region
- Output emission fields directly usable as FLEXPART inputs (with appropriate format conversion)
- Provide a single emissions reference layer in the Knowledge Graph that can be queried per species, per source sector

#### Use case 2: Pre-built input data archive as a general-purpose data source

The **GEOS-Chem Input Data archive on AWS S3** (`s3://geos-chem/`) is a curated, open-access archive of:

- **MERRA-2 meteorology** pre-processed for GEOS-Chem (already on the GEOS-Chem grid, easier to consume than raw GES DISC MERRA-2 in some cases)
- **GEOS-FP meteorology** (NRT, ~5-day latency — closer to real-time than MERRA-2)
- **HEMCO emission inventories** in pre-regridded NetCDF form (EDGAR, CEDS, GFED, etc.)
- **Chemistry input data** (photolysis cross-sections, reaction-rate coefficients)
- **Initial condition restart files** for spinning up runs
- **Land-surface ancillary data** (UV albedo, land type, etc.)

**For the project:** the archive is a **free open-data alternative** to running emission preprocessing in-house. Even if the project never runs GEOS-Chem itself, the harmonised emission files from this archive may be directly useful in FLEXPART or HYSPLIT pipelines.

#### Use case 3: Running GEOS-Chem for case studies (most resource-intensive)

For specific Cluj events that warrant deep investigation, the project could run a nested-Europe GEOS-Chem simulation. Realistic resource estimates:

| Configuration | Compute cost (rough) | Output volume per simulated month | Project applicability |
|---|---|---|---|
| Global 4°×5° | ~10 CPU-hours/month-simulated | ~5 GB | Sensitivity studies only |
| Global 2°×2.5° | ~100 CPU-hours/month-simulated | ~30 GB | Boundary conditions for nested run |
| **Nested 0.25°×0.3125° Europe** | **~500–2000 CPU-hours/month-simulated** | **~100–300 GB** | **Recommended baseline for project case studies** |
| Nested 12 km Europe (v14.6.0+) | ~5000+ CPU-hours/month-simulated | ~1 TB | Best resolution, only for high-priority events |
| GCHP at c720 | Supercomputer-scale | Multi-TB | Beyond project scope |

**Practical recommendation:** unless the project has access to an HPC cluster (several hundred dedicated cores), the GEOS-Chem case-study use case is impractical. **The pragmatic strategy is to use HEMCO standalone (Use case 1) and the input data archive (Use case 2) without running full GEOS-Chem.** Specific event-driven simulations could be commissioned via collaboration with a GEOS-Chem-running group (NASA GMAO, Harvard Atmospheric Chemistry Modeling Group, WashU, KNMI, FMI, etc.) rather than maintained as an in-house operational capability.

### References

**Primary GEOS-Chem mission reference (always cite when GEOS-Chem outputs or HEMCO are used):**
- Bey, I., Jacob, D. J., Yantosca, R. M., Logan, J. A., Field, B. D., Fiore, A. M., Li, Q., Liu, H., Mickley, L. J., & Schultz, M. G. (2001). Global modeling of tropospheric chemistry with assimilated meteorology: Model description and evaluation. *Journal of Geophysical Research*, 106(D19), 23073–23095. DOI: [10.1029/2001JD000807](https://doi.org/10.1029/2001JD000807)

**Aerosol module reference:**
- Park, R. J., Jacob, D. J., Field, B. D., Yantosca, R. M., & Chin, M. (2004). Natural and transboundary pollution influences on sulfate-nitrate-ammonium aerosols in the United States: implications for policy. *Journal of Geophysical Research: Atmospheres*, 109, D15204. DOI: [10.1029/2003JD004473](https://doi.org/10.1029/2003JD004473)

**HEMCO references:**
- Keller, C. A., Long, M. S., Yantosca, R. M., Da Silva, A. M., Pawson, S., & Jacob, D. J. (2014). HEMCO v1.0: a versatile, ESMF-compliant component for calculating emissions in atmospheric models. *Geoscientific Model Development*, 7, 1409–1417. DOI: [10.5194/gmd-7-1409-2014](https://doi.org/10.5194/gmd-7-1409-2014)
- Lin, H., Jacob, D. J., Lundgren, E. W., Sulprizio, M. P., Keller, C. A., Fritz, T. M., Eastham, S. D., Emmons, L. K., Campbell, P. C., Baker, B., Saylor, R. D., & Montuoro, R. (2021). Harmonized Emissions Component (HEMCO) 3.0 as a versatile emissions component for atmospheric models: application in the GEOS-Chem, NASA GEOS, WRF-GC, CESM2, NOAA GEFS-Aerosol, and NOAA UFS models. *Geoscientific Model Development*, 14, 5487–5506. DOI: [10.5194/gmd-14-5487-2021](https://doi.org/10.5194/gmd-14-5487-2021)

**12 km capability (newest, the relevant cutting-edge for Europe):**
- Wang, X., Sulprizio, M. P., Zhuge, Y., Martin, R. V., & Jacob, D. J. (2026). Technical note: 12-km resolution capability for the global GEOS-Chem model of atmospheric composition. *EGUsphere*. DOI: [10.5194/egusphere-2025-5811](https://doi.org/10.5194/egusphere-2025-5811) (preprint at time of writing; final published version to follow in *Geoscientific Model Development*)

**Per-version GEOS-Chem releases on Zenodo (cite the specific version used):**
- Each minor version (14.5.0, 14.6.0, 14.7.0, etc.) has its own Zenodo DOI. Listed at <https://geoschem.github.io/citations.html>.

**HEMCO inventory-specific references** (cite the original inventory papers when using inventories via HEMCO):
- For EDGAR: Crippa et al. 2018, 2020 — cite the version-specific paper (covered in the planned EDGAR metadata file).
- For CEDS: Hoesly et al. 2018, McDuffie et al. 2020 — historical emissions of anthropogenic species.
- For GFED5: van der Werf et al. 2025 (covered in `dataset_metadata_gfed.md`).
- For MEGAN biogenic VOCs: Guenther et al. 2012.

**Citation phrasing (GEOS-Chem-recommended):** *"This work used the GEOS-Chem chemistry-transport model (DOI: 10.5281/zenodo.<version-specific>), driven by GEOS-FP/MERRA-2 meteorology from the NASA Global Modeling and Assimilation Office and emissions processed via the Harmonized Emissions Component (HEMCO, Lin et al. 2021)."*

### Host / Server

- **Main GEOS-Chem homepage:** <https://geoschem.github.io/>
- **Documentation (read-the-docs):** <https://geos-chem.readthedocs.io/>
- **Wiki (Harvard, legacy but still active):** <https://wiki.seas.harvard.edu/geos-chem/index.php/Main_Page>
- **Citations + version DOIs:** <https://geoschem.github.io/citations.html>
- **HEMCO documentation:** <https://hemco.readthedocs.io/>

**Source code:**
- **GEOS-Chem Classic:** <https://github.com/geoschem/GCClassic>
- **GEOS-Chem science modules:** <https://github.com/geoschem/geos-chem>
- **HEMCO:** <https://github.com/geoschem/HEMCO>
- **GCHP:** <https://github.com/geoschem/GCHP>

**Input data archive (AWS Open Data Sponsorship — no auth, no egress fees):**
- **S3 bucket:** `s3://geos-chem/` (region: us-east-1)
- **HTTPS browse:** <https://geos-chem.s3.amazonaws.com/index.html>
- **WashU mirror:** <http://geoschemdata.wustl.edu>
- **Input data catalogs (for bashdatacatalog tool):** <https://github.com/geoschem/input-data-catalogs>

**Community + support:**
- **GEOS-Chem Forum (discussions):** <https://github.com/geoschem/geos-chem/discussions>
- **YouTube channel** (tutorials, working group meetings): search "GEOS-Chem"
- **GEOS-Chem Steering Committee + Working Groups:** structure at <https://geoschem.github.io/people.html>

### Programmatic download (for HEMCO standalone or input data archive)

**Step 1 — AWS CLI (no auth, same as for HYSPLIT met data):**

```bash
# List the top-level structure of the open-data archive
aws s3 ls --no-sign-request s3://geos-chem/

# Drill into ExtData for the data directories
aws s3 ls --no-sign-request s3://geos-chem/ExtData/

# HEMCO inventories (where EDGAR, CEDS, GFED, etc. live in HEMCO format)
aws s3 ls --no-sign-request s3://geos-chem/ExtData/HEMCO/

# GEOS-FP nested over Europe is not in the public bucket because of licensing —
# only North America nested is widely distributed. Cluj-relevant: use the global
# MERRA-2 0.5°×0.625° or global GEOS-FP 0.25°×0.3125° and crop to Cluj region.
aws s3 ls --no-sign-request s3://geos-chem/ExtData/GEOS_0.25x0.3125/GEOS_FP/2026/03/
```

**Step 2 — Download a specific HEMCO emission inventory:**

```bash
# Example: EDGAR v8 anthropogenic emissions as preprocessed in HEMCO format
aws s3 cp --no-sign-request \
    s3://geos-chem/ExtData/HEMCO/EDGAR/v8/ \
    ./edgar_v8_hemco/ \
    --recursive

# Example: GFED4s monthly fire emissions in HEMCO format (note: GFED5 is at
# globalfiredata.org in its native format; HEMCO library was at GFED4s last check —
# verify current GFED version in HEMCO at the input data catalog)
aws s3 cp --no-sign-request \
    s3://geos-chem/ExtData/HEMCO/GFED4/v2020-02/ \
    ./gfed4s_hemco/ \
    --recursive
```

**Step 3 — Install HEMCO standalone:**

```bash
# Clone with submodules (HEMCO depends on shared GEOS-Chem build infrastructure)
git clone --recurse-submodules https://github.com/geoschem/HEMCO.git HEMCO-build
cd HEMCO-build
git checkout main   # or a specific version tag, e.g. v3.12.0

# Build (requires CMake, NetCDF, and a Fortran compiler — gfortran or ifort)
mkdir build && cd build
cmake .. -DRUNDIR=$HOME/hemco-rundir
make -j install
```

**Step 4 — Run HEMCO standalone over a Cluj-region grid:**

```bash
# Create a run directory (provided utility scripts walk through the prompts)
cd $HOME/hemco-rundir
# Edit HEMCO_Config.rc to:
# - turn on/off the inventories you want (EDGAR, GFED5, MEGAN, dust, sea salt)
# - set the grid: e.g. 0.25°×0.3125° nested Europe, or a custom Cluj-region grid
# - set the time period

# Then run:
./hemco_standalone
# Outputs: NetCDF4 files with hourly emission fluxes per species, per grid cell,
# combined across all enabled inventories
```

**Step 5 — Reading HEMCO output for downstream pipeline use:**

```python
import xarray as xr

ds = xr.open_dataset("HEMCO_diagnostics.20260318_0000z.nc4")
# Variables include EmisNOx, EmisCO, EmisSO2, EmisNH3, EmisOC, EmisBC, etc.
# Dimensions: time, lev (vertical layers), lat, lon

# Subset to Cluj region
cluj_emis = ds.sel(lat=slice(45, 48), lon=slice(22, 26))

# Sum across vertical levels to get total column emission
nox_total = cluj_emis["EmisNOx"].sum(dim="lev")
nox_total.plot()   # Spatial pattern of NOx emission over Cluj region
```

### Manual download (interactive web UI)

- **S3 bucket HTTPS browse:** <https://geos-chem.s3.amazonaws.com/index.html> (navigable web view, individual files downloadable)
- **WashU mirror:** <http://geoschemdata.wustl.edu> (alternative if S3 has performance issues)
- **GEOS-Chem benchmark output gallery** (look at published example simulations): <http://ftp.as.harvard.edu/gcgrid/geos-chem/1yr_benchmarks/> (legacy Harvard server)

### Notes / caveats

- **This is not a downloadable pre-computed product.** GEOS-Chem is a model the project would run; this metadata file therefore documents the model, its emissions component (HEMCO), and the open-data input archive (S3). **If the original docx treated GEOS-Chem as a "dataset to download" the framing should be corrected to "model to run + input archive."**
- **HEMCO standalone is the most practical project use.** Without running full GEOS-Chem chemistry, HEMCO can still be used as a sophisticated emission inventory aggregator. **This is likely the highest-value use of GEOS-Chem assets for the project.** It can produce unified gridded emission files combining EDGAR + CEDS + GFED5 + biogenic + dust + sea salt in one consistent product over Cluj's source region.
- **Running full GEOS-Chem requires HPC.** A single Cluj-region nested 0.25° simulation for one month costs ~500–2000 CPU-hours. **Realistic only with HPC access** (institutional cluster or commercial cloud like AWS EC2 c5.24xlarge instances). For event case studies once or twice a year, this is feasible; for routine NRT operations, it is not.
- **Open-source MIT licence, fully community-developed.** No paywalls, no institutional barriers. Code on GitHub; reproducible builds; well-documented; active forum + Working Groups. **The lowest-friction collaborative software in the project's L2 layer.**
- **Versions update fast.** v14.7.0 in February 2026, with v14.6.0 having introduced 12 km capability less than a year earlier. **Pin a specific version in the project pipeline** and only update with explicit re-validation. Each minor version has a Zenodo DOI — cite the actual version used in any deliverable.
- **GEOS-Chem nitrate aerosol is the chemistry advantage over MERRA-2.** As flagged in the MERRA-2 file, GOCART (MERRA-2's aerosol module) does NOT include nitrate. **GEOS-Chem includes a full ISORROPIA-II thermodynamic nitrate scheme** — for Cluj winter PM2.5 (nitrate-dominated under stagnant winter conditions), GEOS-Chem is significantly more physically realistic than MERRA-2. For any winter Cluj case study, a GEOS-Chem run provides the best-available chemistry simulation. Whether the project can afford to run it is a separate question.
- **GEOS-Chem secondary organic aerosol (SOA) is one of the more sophisticated schemes available.** Recent versions (v14.x) have multi-step SOA formation chemistry from biogenic + anthropogenic precursors with semi-volatile partitioning. For summertime Cluj events with potential biogenic + biomass-burning SOA contribution, this is the project's most realistic chemistry option.
- **The 12 km nested capability (v14.6.0+) is brand new and rapidly evolving.** Released 2025, only stable in v14.6.0+ (Feb 2026 onwards). For European simulations at finer than 25 km, this is the cutting edge. Expect rough edges and active development through 2026.
- **HEMCO library overlaps significantly with the rest of the project's emission inputs.** EDGAR, CEDS, GFED4/5, GFAS (via CAMS), MEGAN are all in HEMCO. **For consistency across the L2 layer, consider standardising on HEMCO's pre-regridded versions of these inventories** rather than ingesting each from its primary source separately. This reduces format-conversion overhead and ensures the project's FLEXPART, HYSPLIT, and (potential) GEOS-Chem runs all start from the same emission baseline.
- **Open data, no egress fees on AWS.** The `s3://geos-chem/` bucket is part of AWS Open Data Sponsorship Program. Anonymous access works; data egress to anywhere is free. **Operationally, this is the easiest cloud-data path in the entire project after the NOAA HYSPLIT met archive** — no credentials, no egress costs, no quota limits.
- **MERRA-2 vs GEOS-FP choice for the project.** MERRA-2 is reanalysis (~2-3 weeks lag, scientifically validated, suitable for retrospective case studies). GEOS-FP is the NASA operational analysis (NRT, ~24-hour latency, suitable for NRT runs). **GEOS-FP is the operational analog of ERA5T**, MERRA-2 is the operational analog of ERA5 final. For NRT operations: GEOS-FP. For published case studies: MERRA-2.
- **The combination CAMS + MERRA-2 + GEOS-Chem provides three independent chemistry reanalyses/models** with different model frameworks, different chemistry, different data assimilation (or none, for GEOS-Chem). **For any high-stakes Cluj event interpretation, agreement across all three is strong evidence for the diagnostic; disagreement is itself useful information indicating an unusual event or a chemistry-detail-limited scenario.**
- **Not suitable for NRT operational use as-is.** GEOS-Chem is fundamentally a research tool. It can be run in NRT mode (some operational groups do, e.g. NASA GMAO's GEOS-CF system), but maintaining a GEOS-Chem NRT pipeline is a substantial engineering commitment. **For the project's warning chain operational use, CAMS forecasts remain the right primary input; GEOS-Chem fits in the case-study / publication / cross-validation role.**

---
