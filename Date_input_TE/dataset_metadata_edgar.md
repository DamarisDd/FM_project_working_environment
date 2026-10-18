# Dataset metadata — EDGAR (Emissions Database for Global Atmospheric Research)

Companion documentation to the Stage 1 input-data table.
This file describes **EDGAR** — the **Emissions Database for Global
Atmospheric Research** — the JRC's global anthropogenic emissions
inventory and the backbone of non-fire emissions for the project's
FLEXPART and chemistry-transport modelling.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**EDGAR is the anthropogenic counterpart to GFED5/GFAS** (fire emissions
covered in `dataset_metadata_cams.md` and `dataset_metadata_gfed.md`).
Together, the three answer the question "what is emitted into the
atmosphere over Cluj's source region, and from what?" — EDGAR covers
the anthropogenic sectors (energy, industry, transport, residential
heating, agriculture, waste, solvents), GFED5 covers biomass burning,
and GFAS provides the NRT fire-emission operational stream. **Without
EDGAR, FLEXPART non-fire runs have no emission input.**

---

## 22. EDGAR v8.1 Air Pollutants — JRC global anthropogenic emissions

### Summary

| Field | Value |
|---|---|
| Dataset | **EDGAR** = Emissions Database for Global Atmospheric Research, maintained by the **European Commission Joint Research Centre (JRC)** in Ispra, Italy, in collaboration with the **PBL Netherlands Environmental Assessment Agency**. Two parallel product lines: **EDGAR GHG** (greenhouse gases, updated yearly — latest `EDGAR 2025 GHG` covers 1970–2024) and **EDGAR Air Pollutants** (the project-relevant product — latest `EDGAR v8.1 Air Pollutants` covers 1970–2022, released 2024). |
| Producer / Agency | **JRC** (Ispra, Italy) — Crippa, Guizzardi, Pagani, Muntean, Vignati and team. **Increasingly co-developed with the International Energy Agency (IEA)** for fossil CO₂ (the joint product is IEA-EDGAR CO₂ v4), making EDGAR the de facto operational EU/IEA reference for anthropogenic emissions reporting. |
| Status (May 2026) | **OPERATIONAL — open public access, no authentication required.** Updated approximately annually. |
| Current version (project-relevant) | **EDGAR v8.1 Air Pollutants** (released 2024) covering **1970–2022 annual** and **2000–2022 monthly**, plus an updated **EDGAR v8.1 Global Speciated NMVOC** dataset (released February 2026) for VOC speciation. |
| Pollutant species in v8.1 Air Pollutants | **Ozone precursors:** CO (carbon monoxide), NOx (nitrogen oxides), NMVOC (non-methane volatile organic compounds), CH₄ (methane). **Acidifying gases:** NH₃ (ammonia), NOx (also relevant), SO₂ (sulfur dioxide). **Primary particulates:** PM₁₀, PM₂.₅, BC (black carbon), OC (organic carbon). **Excluded from EDGAR:** large-scale biomass burning (use GFED5/GFAS instead) and LULUCF (land use, land use change, and forestry). |
| Sectoral resolution | **Detailed by IPCC 1996 and 2006 codes** — Energy (power generation, industry combustion, transport, residential heating, fuel exploitation), Industrial Processes (cement, chemicals, metals), Agriculture (livestock, agricultural soils, manure management), Waste (landfills, wastewater), Solvents and Product Use. Specific sub-sectors are distinguished — for example, transport breaks down into road, rail, aviation (domestic + international), shipping. **This sectoral detail is the key value-add over a single bulk-emission number.** |
| Activity data sources | **Energy sectors:** IEA World Energy Balances (2022 data). **Agriculture:** FAO FAOSTAT (2022). Population and economic data from various authoritative international sources. **This means EDGAR inherits the temporal lag of the IEA + FAO data:** EDGAR v8.1 with 2022 endpoint reflects IEA 2022 data; full Romania-specific energy + activity data underpins the Cluj grid cell. |
| Spatial resolution | **0.1° × 0.1° regular lat/lon grid** — ~10 km at Cluj's latitude. **Identical resolution to the CAMS European ENSEMBLE** — convenient for like-with-like comparison between observed/forecast atmospheric composition (CAMS ENSEMBLE) and the upstream emissions (EDGAR). Many other emission inventories at 0.5° or 1° resolution are coarser. |
| Spatial coverage | **Global** — all countries, gridded everywhere on land. |
| Temporal coverage and resolution | **1970–2022** for annual emissions. **2000–2022 for monthly** emissions. **No daily or hourly EDGAR** (the temporal resolution is monthly at finest; for sub-monthly variation use HEMCO's diurnal scalers or alternative inventories). For 1970–1999 only annual emissions are available; monthly disaggregation starts in 2000. |
| Update cadence and latency | **Annual** updates, typically lagging the data endpoint by ~1.5–2 years (e.g. v8.1 released 2024 covers through 2022). **Not NRT.** EDGAR is fundamentally a retrospective inventory — current-year emissions are not available until the following IEA/FAO data cycles complete. For NRT operational use, the most recent EDGAR year's spatial distribution + sectoral shares are extrapolated forward (standard practice in CAMS, HEMCO, etc.). |
| File format | **NetCDF4 (CF-compliant)** for gridded emissions. **Excel (.xlsx)** for country-level + sectoral summary tables. NetCDF organisation: one file per pollutant per sector per year, with monthly time dimensions where available. |
| Filename pattern | `v8.1_<pollutant>_<year>_<sector>.0.1x0.1.nc` (e.g. `v8.1_NOx_2022_TRO.0.1x0.1.nc` for road transport NOx 2022). Sector codes use IPCC 2006 conventions. |
| Authentication | **NONE.** Free direct download from the JRC website and the European Data Portal. **Like the HYSPLIT met data and the GEOS-Chem AWS bucket, EDGAR requires no credentials.** |
| Programmatic access | YES — direct HTTPS download of individual NetCDF files from the JRC website. **No formal API** — file structure is well-organised so `wget`-loop scripts or programmatic file listing via web scraping is the standard pattern. EDGAR is also pre-regridded and packaged inside the HEMCO library (`s3://geos-chem/ExtData/HEMCO/EDGAR/`) which is the easiest path if HEMCO is already in the project pipeline (see `dataset_metadata_geoschem.md`). |
| Layer destination | **L2:** FLEXPART (anthropogenic emission input for non-fire dispersion runs); HYSPLIT (similar role); HEMCO (built-in inventory option for unified emission aggregation, the recommended path per the GEOS-Chem entry). **L3:** Knowledge Graph (sectoral breakdown of Cluj's local emission profile — **the GUI can display "what fraction of the local NOx comes from road transport vs power generation vs residential heating?"** answered directly from EDGAR's Cluj grid cells). |

### Why EDGAR matters specifically for Cluj

Cluj at 46.77°N, 23.55°E sits in a single 0.1°×0.1° EDGAR grid cell (approximately 23.5°–23.6°E, 46.7°–46.8°N). The surrounding source region for a typical 24-hour back-trajectory at Cluj extends across central and eastern Europe, encompassing tens to hundreds of EDGAR grid cells. EDGAR's value-add for the project:

1. **Sectoral attribution at urban scale.** For Cluj's local emission profile, EDGAR's sectoral split tells the operator whether elevated NO₂ at Cluj is driven by **road transport** (rush-hour) vs **residential heating** (winter morning/evening) vs **power generation** (steady baseline) vs **industrial sources**. This sectoral breakdown is the operational explanation behind the diurnal patterns the warning chain measures and predicts.

2. **Regional source attribution.** When a back-trajectory from Cluj traverses, say, eastern Hungary or Ukraine, EDGAR provides the gridded emissions along that path — feeding the source-attribution L2 layer. **Without EDGAR, regional sources outside Cluj's immediate grid cell cannot be quantitatively attributed.**

3. **Long-term context.** The 1970–2022 record provides the **regional emissions trend over five decades**. For climatological context layers in the Knowledge Graph (e.g. "is current Cluj NOx still elevated relative to the historical baseline?"), EDGAR provides the necessary anchor.

4. **IEA-EDGAR CO₂ as the operational EU benchmark.** For EU-level policy reporting and climate-action validation, the IEA-EDGAR CO₂ v4 joint product is the de facto operational reference. **The project's deliverables are positioned more credibly when local Cluj measurements + warning-chain outputs are placed against the IEA-EDGAR baseline** — this is the inventory that EU policymakers will cite.

### Sector codes (IPCC 2006) — which sectors matter for Cluj

The EDGAR sectoral codes most relevant for Cluj's emission profile:

| IPCC 2006 code | Sector | Cluj relevance |
|---|---|---|
| **1A1a** | Public electricity and heat production | Cluj's CHP/heating plants — significant NOx + SO₂ + CO₂ |
| **1A2** | Manufacturing industries | Local industrial sources (cement, food processing, etc.) |
| **1A3a** | Aviation (domestic + international) | Cluj Airport (CLJ) — small but locally identifiable NOx |
| **1A3b** | Road transport | **Primary local NOx + PM source** — dominates Cluj urban air quality |
| **1A3c** | Rail transport | Modest contribution |
| **1A3d** | Domestic navigation | Negligible at Cluj |
| **1A4a** | Commercial / institutional | Heating + small commercial emissions |
| **1A4b** | Residential | **Winter PM + CO + NOx** from residential heating — peak emissions in winter months, the dominant source of stagnant-anticyclone winter PM exceedances |
| **2A** | Industrial processes (mineral, chemical, metal) | Local production processes |
| **3A** | Livestock | Regional NH₃ source (agricultural areas surrounding Cluj) |
| **3D** | Agricultural soils | Regional NH₃ source — connects to nitrate aerosol formation |
| **5A** | Solid waste disposal | Landfill CH₄ emissions |

For warning-chain interpretation: **Cluj's nitrate-dominated winter PM (flagged in MERRA-2 and GEOS-Chem entries) is fundamentally driven by NH₃ from agricultural sectors 3A + 3D combining with NOx from sectors 1A1a + 1A3b + 1A4b.** EDGAR's sectoral split tells exactly which sector contributes how much.

### References

**Primary EDGAR v8.1 Air Pollutants reference (always cite when v8.1 air pollutant data is used):**
- Crippa, M., Guizzardi, D., Pagani, F., Banja, M., Muntean, M., Schaaf, E., Becker, W., Monforti-Ferrario, F., Quadrelli, R., Risquez Martin, A., Köykkä, J., Grassi, G., Rossi, S., Brandao De Melo, J., Jacome Felix Oom, D., Branco, A., San-Miguel, J., & Vignati, E. (2024). EDGAR v8.1 Global Air Pollutant Emissions. European Commission, Joint Research Centre (JRC) [Dataset]. PID: <http://data.europa.eu/89h/a3af16e4-21ac-420a-b98c-b78a9b7723be>

**EDGAR GHG 2025 release (for fossil CO₂ + non-CO₂ GHG):**
- Crippa, M., Guizzardi, D., Pagani, F., Banja, M., Muntean, M., Schaaf, E., Quadrelli, R., Risquez Martin, A., Taghavi-Moharamli, P., Köykkä, J., Grassi, G., Rossi, S., Brandao De Melo, J., Jacome Felix Oom, D., Branco, A., Suarez-Moreno, M., San-Miguel, J., Sedano, F., Manca, G., Pisoni, E., & Pekar, F. (2026). EDGAR 2025 Greenhouse Gas Emissions. European Commission, Joint Research Centre [Dataset]. DOI: [10.2905/JRC.1K6V990](https://doi.org/10.2905/JRC.1K6V990)

**Companion JRC technical report (annual, summarises the version's methodology + key findings):**
- Crippa, M., Guizzardi, D., Pagani, F., Banja, M., Muntean, M., et al. (2025). *GHG emissions of all world countries — 2025 Report*. Publications Office of the European Union, Luxembourg. (Each annual EDGAR release has a corresponding Publications Office report. The v8.1 air pollutant equivalent is the 2024 IEA-EDGAR CO₂ technical report at doi:[10.2760/953322](https://doi.org/10.2760/953322).)

**EDGAR methodology + historical context:**
- Crippa, M., Solazzo, E., Huang, G., Guizzardi, D., Koffi, E., Muntean, M., Schieberle, C., Friedrich, R., & Janssens-Maenhout, G. (2020). High resolution temporal profiles in the Emissions Database for Global Atmospheric Research. *Scientific Data*, 7, 121. DOI: [10.5038/s41597-020-0462-2](https://doi.org/10.1038/s41597-020-0462-2) — **the methodology paper for monthly temporal profiles, useful for any work distinguishing seasonal patterns in EDGAR data.**
- Crippa, M., Guizzardi, D., Muntean, M., Schaaf, E., Dentener, F., van Aardenne, J. A., Monni, S., Doering, U., Olivier, J. G. J., Pagliari, V., & Janssens-Maenhout, G. (2018). Gridded emissions of air pollutants for the period 1970–2012 within EDGAR v4.3.2. *Earth System Science Data*, 10, 1987–2013. DOI: [10.5194/essd-10-1987-2018](https://doi.org/10.5194/essd-10-1987-2018) — **the methodology paper for the air-pollutant gridded products specifically.**

**EDGAR v8.1 NMVOC speciation (released Feb 2026 — relevant for any SOA-chemistry work):**
- Crippa, M., Guizzardi, D., et al. (2026). EDGAR v8.1 Global speciated NMVOC Emissions. JRC Data Catalogue (DOI to be assigned at publication).

**Citation phrasing (JRC-recommended):** *"Users of the data are obliged to acknowledge the source of the data with a reference to the EDGARv8.1 air pollutant website (https://edgar.jrc.ec.europa.eu/dataset_ap81). Co-authorship and involvement of the EDGAR Team in the emission data analysis is highly appreciated."*

### Host / Server

- **Main EDGAR website:** <https://edgar.jrc.ec.europa.eu/>
- **EDGAR v8.1 Air Pollutants dataset page:** <https://edgar.jrc.ec.europa.eu/dataset_ap81>
- **EDGAR 2025 GHG dataset page:** <https://edgar.jrc.ec.europa.eu/dataset_ghg_2025>
- **JRC Data Catalogue (EDGAR collection):** <https://data.jrc.ec.europa.eu/collection/edgar>
- **European Data Portal (EDGAR records):** <https://data.europa.eu/data/datasets?query=EDGAR>
- **EDGAR-hosted summary spreadsheets:** linked from each dataset page (per-country, per-sector, per-pollutant Excel tables)
- **HEMCO-packaged EDGAR (recommended for FLEXPART-ready format):** `s3://geos-chem/ExtData/HEMCO/EDGAR/` (no authentication, see `dataset_metadata_geoschem.md` for AWS CLI access)
- **Contact:** JRC-EDGAR@ec.europa.eu

### Programmatic download

**Step 1 — Direct HTTPS download from JRC (no auth):**

```python
import requests
import os

# Pattern: download v8.1 NOx 2022, gridded, sector "TRO" (road transport)
# Filename pattern: v8.1_<species>_<year>_<sector_code>.0.1x0.1.nc
# Note: exact path structure has evolved across versions; always verify against
# the EDGAR website's "Download data" link for current paths.

base_url = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v81_AP/"
species = "NOx"
year = 2022
sector = "TRO"   # road transport — full sector code list on dataset page

filename = f"v8.1_{species}_{year}_{sector}.0.1x0.1.nc"
url = f"{base_url}{species}/{filename}"

response = requests.get(url, stream=True)
response.raise_for_status()
with open(filename, "wb") as f:
    for chunk in response.iter_content(chunk_size=65536):
        f.write(chunk)
print(f"Downloaded {filename}")
```

**Step 2 — Reading EDGAR NetCDF in Python (xarray):**

```python
import xarray as xr

ds = xr.open_dataset("v8.1_NOx_2022_TRO.0.1x0.1.nc")
# Typical structure:
# - dimensions: time (12 months), lat (1800, -90 to 90 at 0.1°), lon (3600, -180 to 180 at 0.1°)
# - variable: emi_nox (with units kg/m²/s, typically)

# Subset to ±2° around Cluj
cluj_emis = ds.sel(lat=slice(45, 49), lon=slice(21, 26))

# Annual sum (sum across time dimension, weighted by month length)
days_per_month = ds.time.dt.days_in_month
annual_emis_road = (cluj_emis["emi_nox"] * days_per_month * 86400).sum(dim="time")
# Unit: kg/m²/year — multiply by grid cell area for total emission per cell

import numpy as np
lat_rad = np.deg2rad(cluj_emis.lat)
cell_area_m2 = (0.1 * 111e3) * (0.1 * 111e3 * np.cos(lat_rad))   # rough at 0.1°
annual_emis_kg_per_cell = annual_emis_road * cell_area_m2
print(f"Total NOx from road transport over Cluj region in 2022: "
      f"{annual_emis_kg_per_cell.sum().item() / 1e6:.2f} kt")
```

**Step 3 — Loop over all sectors to build the full anthropogenic NOx field:**

```python
# Full sector list for v8.1 Air Pollutants (IPCC 2006 codes)
SECTORS = [
    "ENE", "REF_TRF", "IND", "TRO", "TNR_Aviation_CDS", "TNR_Aviation_CRS",
    "TNR_Aviation_LTO", "TNR_Other", "TNR_Ship", "RCO", "PRO", "PRO_COAL",
    "PRO_GAS", "PRO_OIL", "FFF", "CHE", "IRO", "NMM", "NEU", "AGS", "AWB",
    "AGR", "MNM", "ENF", "SWD_LDF", "SWD_INC", "WWT", "FOO_PAP", "SOL",
    "TRF", "TYR", "ASH",
]
# Note: not all sectors apply to all species; AGS+MNM dominate NH3, ENE+TRO dominate NOx, etc.

all_sectors_data = {}
for sector in SECTORS:
    filename = f"v8.1_NOx_2022_{sector}.0.1x0.1.nc"
    # ... download + open ...
    # ... extract Cluj region ...
    all_sectors_data[sector] = annual_emis_per_sector

# Now you have NOx emission contribution from each sector at Cluj
# This is what feeds the L3 KG layer for "sectoral attribution of local NOx"
```

**Step 4 — Alternative: use the HEMCO-packaged EDGAR (already on AWS S3, pre-regridded):**

```bash
# HEMCO library has EDGAR in pre-regridded NetCDF format with consistent naming
aws s3 ls --no-sign-request s3://geos-chem/ExtData/HEMCO/EDGAR/

# Download EDGAR v8 in HEMCO format (consistent with all other HEMCO inventories,
# easy to mix-and-match with GFED5, CEDS, biogenic, etc.)
aws s3 cp --no-sign-request s3://geos-chem/ExtData/HEMCO/EDGAR/v8/ ./edgar_hemco/ --recursive
```

### Manual download (interactive web UI)

- **EDGAR website:** <https://edgar.jrc.ec.europa.eu/> → "Datasets" tab → "Air Pollutants" → "EDGAR v8.1 Air Pollutants"
- **Per-pollutant download page** (e.g. for NOx): drill into the dataset page; each pollutant has its own download section with per-sector NetCDF files + a global Excel summary table
- **Country-level summaries:** the .xlsx files under each dataset page give per-country annual totals (1970–2022) — useful for quick Romania-specific context
- **JRC Data Catalogue interface:** <https://data.jrc.ec.europa.eu/collection/edgar>

### Notes / caveats

- **EDGAR v8.1 Air Pollutants is the current operational version** (released 2024, covering 1970–2022). **Earlier versions (v4.3.2, v5, v6, v7) are still accessible but should NOT be used for new analyses** unless backward-comparability requires it. If the source docx references EDGAR v4.x, v5, v6, v7 — that should be updated to v8.1.
- **Two parallel product lines, do not confuse:** **EDGAR Air Pollutants** (v8.1, last released 2024, covers CO, NOx, NMVOC, NH₃, SO₂, PM₁₀, PM₂.₅, BC, OC) vs **EDGAR GHG** (release 2025, last released 2026, covers CO₂, CH₄, N₂O, F-gases). The two have **different release cadences, different DOIs, different summary tables, and different web pages.** For an aerosol-focused warning chain, **the v8.1 Air Pollutants product is the primary** — the GHG product is secondary (CH₄ contributes to ozone chemistry but is not directly aerosol-relevant).
- **Resolution match with CAMS European ENSEMBLE is convenient.** Both EDGAR and CAMS European ENSEMBLE are on 0.1° × 0.1° grids. This means the project can do **like-with-like** comparison of "what EDGAR says is emitted here" vs "what CAMS says is in the air here" without resampling — directly informative for closure/source-receptor work.
- **Monthly resolution, not daily.** EDGAR provides monthly emissions starting 2000; before 2000 only annual. For sub-monthly variation (e.g. weekday/weekend cycles, diurnal patterns), use **HEMCO's diurnal scalers** (built into the HEMCO library) which break monthly totals into hourly by sector — or use a sub-monthly emission inventory like CAMS-REG, EMEP, or GAINS for European-domain work.
- **No biomass burning, no LULUCF.** EDGAR's exclusion of large-scale biomass burning means you must supplement with **GFED5 or GFAS** for the fire emission side of the warning chain. LULUCF (forestry, deforestation, soil organic carbon) is also not in EDGAR — relevant for full climate-balance work but not for the project's aerosol chain.
- **NRT limitation: ~1.5–2 year lag.** v8.1 released 2024 covers through 2022. For NRT operational warning chain runs in 2026, the standard practice is to **use the most recent EDGAR year's spatial + sectoral distribution, scaled forward** by recent activity-data estimates (or simply assumed constant for short-term operational windows). HEMCO and CAMS both apply this kind of forward extrapolation internally.
- **Activity data inheritance from IEA and FAO.** EDGAR is not an independent observational dataset — it is fundamentally an **accounting product** that uses IEA energy statistics + FAO agricultural statistics + emission factors to estimate emissions per country per sector. This means: **(a)** EDGAR is most accurate where IEA + FAO data are reliable (OECD countries including Romania), less accurate elsewhere. **(b)** Updates to IEA/FAO data trigger EDGAR re-releases. **(c)** Country-level EDGAR totals can be cross-checked against national emission inventories submitted to UNFCCC / CLRTAP — for Romania, the EMEP-reported emissions and EDGAR should broadly agree at the country level.
- **HEMCO library is the recommended ingest path** if the project is using HEMCO standalone for emission aggregation (per the GEOS-Chem entry). The HEMCO version of EDGAR is **pre-regridded, pre-named consistently, and pre-aligned with other HEMCO inventories** — significant overhead saved vs raw JRC NetCDF.
- **Speciated NMVOC product is separate** (EDGAR v8.1 Global Speciated NMVOC, released February 2026). Standard EDGAR provides total NMVOC; for chemistry-detailed modelling (where individual VOC species matter for ozone + SOA formation), the speciated product provides the breakdown into ~30 individual VOCs. **Relevant if the project does any SOA chemistry; not relevant if NMVOC is treated as a lumped tracer.**
- **No authentication needed for any path.** EDGAR is fully open Copernicus-style data licence (CC-BY 4.0 with attribution). The project pipeline does not add an EDGAR-specific credential to the credential management family — straightforward.
- **Update cycle is "summer" annually.** New EDGAR releases (both GHG and Air Pollutants product lines) typically appear in summer or autumn. **Plan annual update windows in the project pipeline** to refresh EDGAR data + verify reference DOIs.
- **Citation matters for EU credibility.** EDGAR is an EU JRC product. **For deliverables to Romanian or EU local-authority audiences, citing EDGAR explicitly anchors the project's emission inputs to the EU's own canonical emission reference**, which is valuable for credibility. Use the JRC-recommended citation phrasing in every project document where EDGAR data is presented or visualised.

---
