# Dataset metadata — MERRA-2 (NASA atmospheric/aerosol reanalysis)

Companion documentation to the Stage 1 input-data table.
This file describes **MERRA-2** — NASA's Modern-Era Retrospective analysis
for Research and Applications, Version 2 — the **second long-term
atmospheric composition reanalysis** in the project's L2 layer
alongside CAMS EAC4 (different agency, different model, different
assimilation system) and the meteorological backbone alongside ERA5.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**MERRA-2's distinctive feature: it was the first long-term global
reanalysis to assimilate space-based aerosol observations.** This makes
it directly comparable to CAMS EAC4 for aerosol-focused work, and
useful as an **independent cross-check** on the project's CAMS-derived
aerosol fields. The two reanalyses use different models (NASA GEOS-5
vs ECMWF IFS), different aerosol modules (GOCART vs CAMS Aerosol),
and different assimilation systems (NASA 3DVar/4DEnVar vs ECMWF 4DVar),
so their agreement provides genuine consensus information rather than
single-source confirmation.

---

## 19. MERRA-2 — NASA Modern-Era Retrospective Analysis v2

### Summary

| Field | Value |
|---|---|
| Dataset | **MERRA-2** = Modern-Era Retrospective analysis for Research and Applications, Version 2. NASA's global atmospheric reanalysis covering **January 1980 to present**, produced by the **NASA Global Modeling and Assimilation Office (GMAO)** at Goddard Space Flight Center. Underlying model: **GEOS-5** (Goddard Earth Observing System Model version 5.12.4) coupled to the **GOCART** aerosol module. **First long-term reanalysis to assimilate space-based aerosol observations** — making it especially valuable for aerosol-focused work. |
| Producer / Agency | **NASA GMAO** (production) → **NASA Goddard Earth Sciences Data and Information Services Center (GES DISC)** (distribution). Open data, free for any use, attribution required. |
| Sub-products in the family | Multiple "collections" identified by short names: **M2T1NXAER** (hourly time-averaged 2D aerosol diagnostics — **the primary project-relevant collection**), **M2T1NXADG** (extended aerosol diagnostics: deposition, emissions, sedimentation), **M2I3NPASM** (3-hourly instantaneous 3D pressure-level state), **M2T1NXSLV** (hourly time-averaged single-level surface met diagnostics), **M2T1NXFLX** (hourly time-averaged surface flux diagnostics), **M2I6NVANA** (6-hourly instantaneous 3D model-level analysis), and many others. Naming convention: `M2<T/I><1/3/6/U><N><X/V>< collection abbreviation>` where T=time-averaged, I=instantaneous, U=climatological-diurnal, N=natural surface, X=2D single-level, V=3D model-level. **Note:** the user-facing "long names" used by GES DISC use the alternative convention (e.g. `tavg1_2d_aer_Nx` = M2T1NXAER) — both refer to the same data. |
| Spatial resolution | **0.5° latitude × 0.625° longitude** — corresponds to **~55 km N-S × ~48 km E-W at Cluj's latitude (46.77°N)**. Coarser than ERA5 (0.25°), comparable to CAMS Global (~40 km), much coarser than CAMS European ENSEMBLE (10 km). |
| Vertical resolution | **72 hybrid sigma-pressure levels** from surface to ~0.01 hPa (model top ~80 km). Hybrid sigma-pressure follows terrain near the surface and transitions to pressure levels aloft, the same general approach as ERA5's 137 levels but with fewer total levels. **Adequate for synoptic to mesoscale work, less resolved in the boundary layer than ERA5.** |
| Temporal resolution | **Hourly** (1-hour) for 2D fields like M2T1NXAER aerosols and M2T1NXSLV surface met. **3-hourly** for most 3D fields. **6-hourly** for analysis-only 3D state on model levels. **Monthly** climatological means also available. |
| Temporal coverage and latency | **1980 to present** (45+ years of continuous record), updated continuously. **Latency for the operational stream: approximately 2–3 weeks** behind real time, longer than ERA5T (~5 days) and CAMS EAC4 (~1 year). **Not suitable as an NRT operational driver**; suitable for retrospective analysis, climatology, and cross-validation. |
| Assimilated aerosol observations | **MODIS** (Terra + Aqua) AOD, **MISR** AOD (where available), **AVHRR** AOD over ocean, **AERONET** AOD (selected sites). **TROPOMI is NOT currently assimilated** in MERRA-2 (the system is in a frozen mid-2010s configuration relative to current satellite observations). For events post ~2018 where TROPOMI brings new information, expect MERRA-2 to be slightly behind state-of-the-art compared to CAMS which assimilates TROPOMI directly. |
| File format | **NetCDF4 (CF-compliant)**, HDF5-backed. Each granule is one daily file per collection (e.g. one M2T1NXAER file = 24 hours of all aerosol variables globally on the 0.5°×0.625° grid). |
| Filename pattern | `MERRA2_<stream>.<collection_long_name>.<YYYYMMDD>.nc4` — e.g. `MERRA2_400.tavg1_2d_aer_Nx.20260318.nc4`. The **stream number** (300, 400, 401 etc.) reflects a major GEOS system version change within the MERRA-2 record — important to understand when cross-stream consistency matters (see Notes/caveats). |
| Authentication | **NASA Earthdata Login** (free, separate from EUMETSAT / ESA / ECMWF credentials). One Earthdata Login account also covers **ATLID's L2 products on the NASA CMR catalogue**, NASA's PACE mission, GES DISC-hosted MODIS reprocessed products, and many other NASA Earth-science archives — so this credential, once set up, opens a large data ecosystem. |
| Programmatic access | YES — multiple paths: (1) **HTTPS direct download** via `wget`/`curl` with Earthdata Login token; (2) **OPeNDAP** for subset-on-the-fly (request a spatial/temporal/variable subset and download only that); (3) **NASA `earthaccess` Python library** (recommended modern path); (4) **direct S3 access** via NASA Earthdata Cloud (newest path, free for cloud-resident workflows); (5) **Google Earth Engine** mirror (free for non-commercial use); (6) **CMR / Earthdata Search web UI** for interactive discovery. |
| Layer destination | **L2:** FLEXPART (MERRA-2 hourly 3D wind/T/Q on model levels can serve as an alternative meteorological driver to ERA5 — but with significant pipeline rewrite cost, since FLEXPART expects GRIB and MERRA-2 is NetCDF; **not recommended unless ERA5 is unavailable**); HYSPLIT (similar — ARL converters exist for MERRA-2 but unofficial); **primary L2 use: cross-validation reference for CAMS EAC4 aerosol fields** at Cluj. **L3:** Knowledge Graph (MERRA-2 surface PM2.5/PM10 and AOD-by-species as a historical climatology layer + cross-source agreement indicator alongside CAMS). |

### Project-priority collections: which MERRA-2 files matter for Cluj

The MERRA-2 catalogue lists ~100 collections; only a handful are directly project-relevant. Prioritised:

#### 19.1 M2T1NXAER (the primary aerosol product)

| Field | Value |
|---|---|
| Long name | `tavg1_2d_aer_Nx` — 2D, 1-hourly, time-averaged, single-level, assimilation, aerosol diagnostics |
| Dataset DOI | [10.5067/KLICLTZ8EM9D](https://doi.org/10.5067/KLICLTZ8EM9D) |
| Variables | Per-species **column mass density** (kg m⁻²): BCCMASS (black carbon), DUCMASS (dust), DUCMASS25 (dust PM2.5), OCCMASS (organic carbon), SO4CMASS (sulfate), SSCMASS (sea salt). Per-species **surface mass concentration** (kg m⁻³): BCSMASS, DUSMASS, DUSMASS25, OCSMASS, SO4SMASS, SSSMASS. **Total AOT at 550 nm**: TOTEXTTAU (total extinction AOT), TOTSCATAU (total scattering AOT), TOTANGSTR (Ångström exponent 470–870 nm). **Per-species AOT at 550 nm**: BCEXTTAU, DUEXTTAU, OCEXTTAU, SO4EXTTAU, SSEXTTAU. Plus dust-specific PM bin diagnostics. |
| PM derivation | **PM2.5 and PM10 are NOT direct variables** in MERRA-2; they must be **derived** from the surface mass concentrations using documented formulas. The GES DISC FAQ at <https://disc.gsfc.nasa.gov/information/faqs?title=MERRA-2%20FAQs> provides the exact derivation. Typical formula: `PM2.5 ≈ 1.375 × SO4SMASS + OCSMASS + BCSMASS + DUSMASS25 + 0.029 × SSSMASS` (with version-specific scaling). |
| Spatial | 0.5° × 0.625° global; ~55 × 48 km at Cluj |
| Temporal | Hourly time-averaged, time-stamped at the **central time of the hour** (00:30, 01:30, …, 23:30 UTC) |
| Cluj relevance | **THE most directly project-useful MERRA-2 product.** Provides hourly per-species aerosol surface concentrations and column AOD at Cluj from 1980 onwards — a 45+-year aerosol climatology baseline plus cross-validation against CAMS EAC4 (2003 onwards) and against the project's ground EARLINET/AERONET data. |

#### 19.2 M2T1NXADG (extended aerosol diagnostics)

| Field | Value |
|---|---|
| Long name | `tavg1_2d_adg_Nx` — extended aerosol diagnostics |
| Variables | **Deposition** (dry + wet) per species; **dust emissions** by size bin; **sea-salt emissions**; **organic-carbon convective scavenging**; sulfur cycle diagnostics; ammonia processes. Hourly time-averaged. |
| Project relevance | Useful for source attribution studies — answering "what fraction of the Cluj PM2.5 budget is from dust emission vs sulfate formation vs biomass-burning OC?" |

#### 19.3 M2I3NPASM (3D state on pressure levels — meteorological driver candidate)

| Field | Value |
|---|---|
| Long name | `inst3_3d_asm_Np` — 3D instantaneous assimilated state on pressure levels |
| Variables | U, V (winds), T, Q (specific humidity), OMEGA (vertical velocity), H (geopotential height), CLOUD, etc. on 42 pressure levels (1000 to 0.1 hPa). |
| Project relevance | Alternative meteorological driver to ERA5 for retrospective FLEXPART work; same role MERRA-2 plays for many published aerosol transport studies. **Not the project's default** (ERA5 is preferred for FLEXPART per the ERA5 file's recommendation), but useful as a cross-validation if a particular event's transport pattern is uncertain. |

#### 19.4 M2T1NXSLV (surface meteorology)

| Field | Value |
|---|---|
| Long name | `tavg1_2d_slv_Nx` — 2D, 1-hourly, time-averaged, single-level, assimilation, surface meteorology diagnostics |
| Variables | T2M, U10M, V10M, QV2M (2 m humidity), SLP, **PBLH (boundary layer height)**, TQV (total precipitable water), TS (skin temp), and others. |
| Project relevance | Same role as the ERA5 single-level surface fields for KG context layers (boundary layer height, surface winds, etc.) — provides an independent estimate from a different model framework. |

### References

**Primary mission reference (always cite when using MERRA-2 data):**
- Gelaro, R., McCarty, W., Suárez, M. J., Todling, R., Molod, A., Takacs, L., Randles, C. A., Darmenov, A., Bosilovich, M. G., Reichle, R., Wargan, K., Coy, L., Cullather, R., Draper, C., Akella, S., Buchard, V., Conaty, A., da Silva, A. M., Gu, W., Kim, G.-K., Koster, R., Lucchesi, R., Merkova, D., Nielsen, J. E., Partyka, G., Pawson, S., Putman, W., Rienecker, M., Schubert, S. D., Sienkiewicz, M., & Zhao, B. (2017). The Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2). *Journal of Climate*, 30(14), 5419–5454. DOI: [10.1175/JCLI-D-16-0758.1](https://doi.org/10.1175/JCLI-D-16-0758.1)

**Aerosol-specific MERRA-2 reference:**
- Randles, C. A., da Silva, A. M., Buchard, V., Colarco, P. R., Darmenov, A., Govindaraju, R., Smirnov, A., Holben, B., Ferrare, R., Hair, J., Shinozuka, Y., & Flynn, C. J. (2017). The MERRA-2 Aerosol Reanalysis, 1980 Onward. Part I: System Description and Data Assimilation Evaluation. *Journal of Climate*, 30(17), 6823–6850. DOI: [10.1175/JCLI-D-16-0609.1](https://doi.org/10.1175/JCLI-D-16-0609.1)
- Buchard, V., Randles, C. A., da Silva, A. M., Darmenov, A., Colarco, P. R., Govindaraju, R., Ferrare, R., Hair, J., Beyersdorf, A. J., Ziemba, L. D., & Yu, H. (2017). The MERRA-2 Aerosol Reanalysis, 1980 Onward. Part II: Evaluation and Case Studies. *Journal of Climate*, 30(17), 6851–6872. DOI: [10.1175/JCLI-D-16-0613.1](https://doi.org/10.1175/JCLI-D-16-0613.1)

**Per-collection dataset DOIs (cite the specific collection used):**
- M2T1NXAER (hourly aerosol): [10.5067/KLICLTZ8EM9D](https://doi.org/10.5067/KLICLTZ8EM9D)
- M2T1NXADG (extended aerosol): [10.5067/HM00OHQBHKTP](https://doi.org/10.5067/HM00OHQBHKTP) — verify against current GES DISC page
- M2I3NPASM (3D pressure-level state): [10.5067/QBZ6MG944HW0](https://doi.org/10.5067/QBZ6MG944HW0) — verify
- M2T1NXSLV (surface meteorology): [10.5067/VJAFPLI1CSIV](https://doi.org/10.5067/VJAFPLI1CSIV) — verify
- Always check the dataset landing page on <https://earthdata.nasa.gov/> for the current canonical DOI.

**Citation phrasing (NASA recommended):** *"The data used in this study/product were provided by the Global Modeling and Assimilation Office (GMAO) at NASA Goddard Space Flight Center. MERRA-2 data are openly available without restriction in accordance with the EOSDIS Data Use and Citation Guidance."*

### Host / Server

- **NASA Earthdata main portal:** <https://www.earthdata.nasa.gov/>
- **GES DISC (data archive home for MERRA-2):** <https://disc.gsfc.nasa.gov/>
- **MERRA-2 mission landing page (catalogue):** <https://disc.gsfc.nasa.gov/datasets?project=MERRA-2>
- **NASA Earthdata Search (web UI for discovery + manual download):** <https://search.earthdata.nasa.gov/>
- **NASA Common Metadata Repository (CMR) API:** <https://cmr.earthdata.nasa.gov/>
- **NASA Earthdata Login (account registration):** <https://urs.earthdata.nasa.gov/>
- **NASA `earthaccess` Python library** (recommended modern client): <https://github.com/nsidc/earthaccess>
- **MERRA-2 file specification** (variable lists per collection): <https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf>
- **GES DISC OPeNDAP server:** `https://opendap.disc.gsfc.nasa.gov/opendap/`

### Programmatic download

**Step 1 — Account setup (one-time):**

1. Register at NASA Earthdata Login: <https://urs.earthdata.nasa.gov/users/new>
2. Link the account to GES DISC: after first login, visit the GES DISC service authorization page (one-time approval prompt; documented at <https://disc.gsfc.nasa.gov/earthdata-login>)
3. (Optional but recommended) Generate an Earthdata Login Token for use in scripts: <https://urs.earthdata.nasa.gov/profile> → "Generate Token"

**Step 2 — Install the NASA `earthaccess` Python library:**

```bash
pip install earthaccess
```

**Step 3 — Authenticate + search + download M2T1NXAER for a Cluj week:**

```python
import earthaccess

# Authentication: uses ~/.netrc or interactive login, or env var EARTHDATA_TOKEN
auth = earthaccess.login(strategy="netrc")   # or "interactive", or "environment"

# Search for the hourly aerosol diagnostics around a week of interest
results = earthaccess.search_data(
    short_name="M2T1NXAER",
    version="5.12.4",
    temporal=("2026-03-12", "2026-03-18"),
    # Global dataset — subset spatially during read, not during search
)
print(f"Found {len(results)} granules")

# Download (default location: ./local-data/<collection>/<filename>.nc4)
files = earthaccess.download(results, "./merra2_cache")

# Each file is one full daily granule (~200-400 MB depending on the collection)
```

**Step 4 — Spatial subset to Cluj region with xarray + OPeNDAP (alternative — avoids full-file download):**

```python
import xarray as xr

# OPeNDAP URL pattern for MERRA-2 (with earthdata authentication via netrc)
url = (
    "https://opendap.disc.gsfc.nasa.gov/opendap/MERRA2/M2T1NXAER.5.12.4/"
    "2026/03/MERRA2_400.tavg1_2d_aer_Nx.20260318.nc4"
)

# Open via OPeNDAP — only the bytes for the subset are transferred
ds = xr.open_dataset(url, engine="netcdf4")

# Subset to ±5° around Cluj (the OPeNDAP server only sends those bytes back)
cluj_subset = ds.sel(
    lat=slice(42.0, 52.0),
    lon=slice(18.0, 30.0),
)
print(cluj_subset)

# Derive PM2.5 (GES DISC FAQ formula)
pm25 = (
    1.375 * cluj_subset["SO4SMASS"]
    + cluj_subset["OCSMASS"]
    + cluj_subset["BCSMASS"]
    + cluj_subset["DUSMASS25"]
    + 0.029 * cluj_subset["SSSMASS"]
) * 1e9   # convert kg/m³ to µg/m³
pm25.attrs["units"] = "µg m^-3"
pm25.to_netcdf("merra2_cluj_pm25_20260318.nc")
```

**Step 5 — Direct S3 access from a cloud environment (newest, fastest path for AWS workflows):**

```python
# Only available from AWS us-west-2 region (Earthdata Cloud data centre)
# For workflows running outside AWS, use the HTTPS/OPeNDAP paths above
import earthaccess

auth = earthaccess.login()
results = earthaccess.search_data(short_name="M2T1NXAER", temporal=("2026-03-18", "2026-03-18"))

# Get cloud-direct S3 URLs (faster than HTTPS if running in us-west-2):
s3_credentials = earthaccess.get_s3_credentials(daac="GES_DISC")
fs = earthaccess.get_s3fs_session(daac="GES_DISC")

for granule in results:
    s3_url = granule.data_links(access="direct")[0]   # s3://gesdisc-cumulus-prod-protected/...
    with fs.open(s3_url) as f:
        ds = xr.open_dataset(f)
        # process...
```

### Manual download (interactive web UI)

- **NASA Earthdata Search:** <https://search.earthdata.nasa.gov/> → search for "MERRA-2", filter by collection, draw bounding box around Cluj, select date range, download granule list
- **GES DISC MERRA-2 dataset browser:** <https://disc.gsfc.nasa.gov/datasets?project=MERRA-2> → drill into M2T1NXAER → use the "Subset / Get Data" tool which generates wget scripts or OPeNDAP URLs for custom subsets
- **Giovanni** (NASA's online visual/analytical tool for MERRA-2 and other GES DISC data): <https://giovanni.gsfc.nasa.gov/giovanni/> — useful for quick visual sanity checks on a Cluj subset before committing to API downloads
- **Worldview** (NASA's interactive satellite imagery + reanalysis viewer): <https://worldview.earthdata.nasa.gov/> — includes MERRA-2 aerosol layers as overlays

### Notes / caveats

- **NASA Earthdata Login is a separate credential family from EUMETSAT, ECMWF, ESA.** The project pipeline now manages: (1) ECMWF account + CDS token (ERA5), (2) ECMWF account + ADS token (CAMS), (3) EUMETSAT EO Portal account (SEVIRI/FCI/SLSTR/Sentinel-5/Sentinel-4), (4) ESA EO Sign In (ATLID), (5) CDSE (Sentinel-2 MSI, Sentinel-3 mirror), (6) NOAA NODD (no credentials — HYSPLIT met data), and (7) **NASA Earthdata Login (MERRA-2, plus MODIS reprocessed products and others)**. **Same NASA Earthdata Login also covers the MODIS LAADS L1/L2 products** the project already ingests for MODIS aerosol — so this may already exist in the pipeline rather than being a new credential.
- **The NASA Web Unification Project is ongoing through end of 2026.** Many MERRA-2 dataset pages are migrating from the GES DISC subdomain (`disc.gsfc.nasa.gov/datasets/...`) to the unified Earthdata domain (`www.earthdata.nasa.gov/data/catalog/...`). Bookmarks and pipeline URLs may need updating during the transition. **Use the persistent DOI links** in citations rather than the catalogue URL.
- **MERRA-2 stream numbers reflect GEOS system version changes.** The MERRA-2 record is divided into "streams" indicated by the first 3 digits of the filename (`MERRA2_100`, `MERRA2_200`, `MERRA2_300`, `MERRA2_400`, `MERRA2_401`). Stream boundaries occur where the underlying GEOS system was upgraded mid-record (with care taken to maintain assimilation continuity). **For most analyses this is transparent**, but for high-precision trend studies, be aware of the stream boundaries (current operational stream is MERRA2_400, switching to MERRA2_401 occurred in mid-2021 for some collections). Documented at <https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/data_access/MERRA2_Stream_dates.pdf>.
- **MERRA-2 latency (~2–3 weeks) is not NRT.** Unlike ERA5T (5 days) or CAMS Global Forecasts (real-time), MERRA-2 is a retrospective product. **Cannot drive the operational warning chain alone** — useful for retrospective analysis, climatology, and validation against other reanalyses. For NRT applications use CAMS Global Forecasts or the operational forecast component of ERA5T.
- **Aerosol assimilation in MERRA-2 is "frozen" at the mid-2010s observation system.** MERRA-2 assimilates AOD from MODIS Terra+Aqua, MISR (limited), AVHRR, and AERONET. **It does NOT assimilate TROPOMI, VIIRS Deep Blue, or other newer-mission aerosol products** — its observation operator was set in the mid-2010s and the system is held fixed for cross-temporal consistency. For events post ~2018 where the newer observation systems would matter, **CAMS EAC4 (which has periodic system upgrades) is more state-of-the-art than MERRA-2.** For pre-2018 events, MERRA-2 and CAMS EAC4 are roughly comparable.
- **GOCART aerosol module simplifications.** MERRA-2 uses the GOCART aerosol scheme: **5 dust size bins, 5 sea-salt size bins, plus BC, OC, SO₄**. **Nitrate aerosol is NOT modelled** in standard MERRA-2 (it is in CAMS), which means **MERRA-2 will systematically underestimate winter PM₂.₅ in nitrate-dominated regions like central Europe**. Cluj is squarely in this affected region. Expect MERRA-2 winter PM₂.₅ at Cluj to read low compared to RNMCA observations and CAMS, especially under stagnant winter anticyclonic conditions.
- **PM derivation must use the official formula.** The variables shipped in M2T1NXAER are per-species surface mass concentrations and column densities. The PM2.5 (and PM10) values are NOT direct outputs — they must be computed from species concentrations using the formula in the GES DISC FAQ. **Different formulas give different PM2.5 estimates** — there's a "MERRA-2-recommended" formula and several variant formulas in the literature; use the GMAO-recommended one for project consistency, and cite the formula explicitly when reporting PM values.
- **Direct S3 access is only fast inside AWS us-west-2.** NASA Earthdata Cloud hosts MERRA-2 in AWS us-west-2. Workflows running in that region get free, fast S3 access. Workflows running elsewhere (including Europe) should use HTTPS or OPeNDAP — the S3 endpoint is still accessible but transit cost + latency outweigh the throughput benefit for European-hosted pipelines.
- **OPeNDAP subsetting is the recommended path for Cluj-focused analysis.** Full daily granules for MERRA-2 aerosol diagnostics are ~200–400 MB each; downloading the full global field every day quickly fills storage. Using OPeNDAP to request only the Cluj-region subset reduces per-file download to ~1–5 MB. Highly recommended for the operational pipeline.
- **Spatial resolution at Cluj (~55 × 48 km) is similar to ERA5 at 0.25° (~28 × 19 km) but coarser.** For city-scale work this is too coarse — Cluj appears as one grid cell. **Use MERRA-2 for synoptic-scale aerosol context + climatology, not for urban-scale Cluj prediction.** The CAMS European ENSEMBLE at 10 km is the right tool for urban-scale forecasting; MERRA-2 is the right tool for 45+-year climatology and cross-reanalysis comparison.
- **Long historical record is the genuine value-add.** ERA5 covers 1940 onward; CAMS EAC4 covers 2003 onward; MERRA-2 covers 1980 onward. For decadal-trend analyses or climatology baselines spanning the 1980s and 1990s, MERRA-2 is the project's most natural aerosol-reanalysis option (CAMS doesn't go back that far). For event analyses, MERRA-2 and CAMS EAC4 should agree within their respective uncertainties — disagreement between them is a useful flag indicating either an unusual event or a model-system limitation.
- **Cross-validation strategy with CAMS EAC4.** For any Cluj event during the period both reanalyses cover (2003 onwards): pull both MERRA-2 M2T1NXAER and CAMS EAC4 aerosol fields, compare surface PM, AOD per species, and total AOD. **Strong agreement = high confidence in the reanalysed event**; significant disagreement = flag for closer investigation (which is itself useful information for the warning chain). The project should design the L2 layer to compute MERRA-2 vs CAMS difference fields as a diagnostic output.
- **Long-term continuity is good but not multi-decade-guaranteed.** MERRA-2 is the second-generation NASA reanalysis (after MERRA, which is now retired). A third-generation reanalysis from NASA (working name "GEOS-IT" or similar — based on the newer GEOS-CF chemistry-transport configuration) is in development but not yet operational as a long-record reanalysis. **MERRA-2 is expected to continue operational production for several more years.** When a successor product appears, plan a parallel-run / cross-validation period before switching.

---
