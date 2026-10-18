# Dataset metadata — CAMS (Copernicus Atmosphere Monitoring Service)

Companion documentation to the Stage 1 input-data table.
This file describes the **CAMS** product family from ECMWF / C3S — the
operational atmospheric composition + air quality service that
**directly produces the kind of forecasts the warning chain itself
will generate**, making it both an input (boundary conditions,
benchmark forecasts) and a comparator for the project's own outputs.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**CAMS is to atmospheric composition what ERA5 is to meteorology.**
ERA5 (previous file) is the meteorological backbone; CAMS is the
atmospheric-composition backbone. The two share the same ECMWF
infrastructure but reside in separate Data Stores (CDS for ERA5,
ADS for CAMS) with separate credentials, separate quotas, but
identical API conventions.

---

## 17. CAMS — Copernicus Atmosphere Monitoring Service products

### Summary

| Field | Value |
|---|---|
| Service | **CAMS** = Copernicus Atmosphere Monitoring Service — the operational atmospheric composition arm of the EU Copernicus programme, complementary to C3S (climate, hosts ERA5). Implemented by **ECMWF** on behalf of the **European Commission**. Provides operational forecasts + reanalyses + emission inventories + supporting products for: air quality, climate forcing, ozone layer + UV, solar radiation, greenhouse gases, and emissions. |
| Status (May 2026) | **OPERATIONAL — all products in routine production.** Migration to the modern ADS infrastructure was completed alongside the CDS migration in mid-2024 (legacy ADS decommissioned September 2024). |
| Main products relevant to the project | (1) **CAMS global atmospheric composition forecasts** (NRT, twice daily 5-day forecasts, ~40 km resolution, ~70 species). (2) **CAMS European air quality forecasts (Regional ENSEMBLE)** (**0.1° / ~10 km, 11-model ensemble**, daily 4-day forecast for European domain — this is **the project's most directly comparable benchmark product**). (3) **CAMS global reanalysis EAC4** (2003–end 2024 currently, ~80 km, 3-hourly, full atmospheric composition). (4) **CAMS European air quality reanalyses** (annual reanalyses at 0.1° using validated EEA observations). (5) **GFAS** — Global Fire Assimilation System (daily fire emissions at 0.1°, derived from MODIS fire radiative power — **the primary biomass-burning emission input for FLEXPART**). |
| Secondary products | CAMS Solar Radiation, CAMS UV products, CAMS Greenhouse Gas reanalyses (EGG4), CAMS Greenhouse Gas inversion-optimised fluxes, CAMS Climate Forcings, CAMS Policy Products. Lower priority for the aerosol warning chain; mentioned only for completeness. |
| Operating institution(s) for European ENSEMBLE | **Ensemble assembly + dissemination:** Météo-France + INERIS (France) on behalf of CAMS. **11 contributing model systems:** CHIMERE (INERIS, France), EMEP (MET Norway), EURAD-IM (Jülich IEK, Germany), LOTOS-EUROS (KNMI + TNO, Netherlands), MATCH (SMHI, Sweden), MOCAGE (Météo-France), SILAM (FMI, Finland), DEHM (Aarhus University, Denmark), GEM-AQ (IEP-NRI, Poland), MONARCH (BSC, Spain), MINNI (ENEA, Italy). The two newest additions (MONARCH, MINNI) joined the operational ensemble after a 3-year benchmarking period — ENEA's MINNI joined officially in 2018; the move from 9 to 11 models marked the consolidation of southern-European model expertise in the ensemble. |
| File format | **NetCDF4 / CF-compliant** (default for most products), **GRIB1/GRIB2** also available for the global forecasts and ENSEMBLE forecast (GRIB Edition 2). The `data_format` parameter in the ADS API request controls which is delivered. |
| Filename pattern | User-specified at download time (ADS API `target` parameter). |
| Authentication | **NEW (post-Sept 2024) credential path:** ECMWF account → ADS personal access token. **Note:** ADS uses a **separate personal access token from CDS**, even though both share the same ECMWF account. Pipelines need both `~/.cdsapirc` (for CDS / ERA5) and an analogous configuration pointing to `https://ads.atmosphere.copernicus.eu/api` (for ADS / CAMS). See "Programmatic download" below. |
| Programmatic access | YES — same `cdsapi` Python library (≥ 0.7.0) used for CDS, just pointed at the ADS endpoint with the ADS token. STAC catalogue available at <https://ads.atmosphere.copernicus.eu/stac-browser/>. |
| Layer destination | **L2:** FLEXPART (CAMS Global as initial/boundary conditions for chemistry — much richer chemical setup than starting from zero; **GFAS** as the biomass-burning emission source for fire-driven FLEXPART runs); HYSPLIT (less natural fit, but CAMS Global concentrations can be sampled along back-trajectories as exposure context); GRASP (CAMS aerosol AOD is one validation reference). **L3:** Knowledge Graph (**CAMS Regional ENSEMBLE surface PM2.5/PM10/O3/NO2 forecasts** displayed directly in the GUI as the "external official forecast" benchmark layer for operational comparison with the warning chain's own dispersion-derived predictions). |

### The CAMS products in detail (for the project)

#### 17.1 CAMS Global Atmospheric Composition Forecasts (NRT)

| Field | Value |
|---|---|
| Dataset name (ADS) | `cams-global-atmospheric-composition-forecasts` |
| Description | The operational global chemical-weather forecasting system. Twice-daily initialisation (00 UTC and 12 UTC), each producing 5-day forecasts. Initial conditions come from 4D-Var assimilation of satellite observations of CO, O₃, NO₂, AOD (MODIS, VIIRS, TROPOMI, IASI) into the ECMWF IFS-COMPO chemistry model. |
| Spatial resolution | **~40 km at the equator** (currently TCo399 grid, post-June 2023 upgrade); higher latitudes have proportionally smaller grid cells. **At Cluj (~47°N): ~28 × 28 km²** effective resolution. |
| Vertical | **137 model levels** (same vertical grid as ERA5 / IFS), surface to ~80 km. |
| Temporal | **1-hour cadence** for surface fields; 3-hour cadence for 3D fields. **5-day forecast** from each initialisation. |
| Variables | **~70 species** including 7 aerosol types (sea-salt 3 bins, dust 3 bins, organic matter, black carbon, sulphate, nitrate, ammonium), full tropospheric chemistry (O₃, NO₂, CO, SO₂, HCHO, CH₄, etc.), AOD at multiple wavelengths (469, 550, 670, 865, 1240 nm), surface PM2.5 + PM10. |
| Cluj relevance | **Provides 5-day forecasts of every key chemical + aerosol variable at Cluj** at 40 km grid scale. Most useful as **boundary/initial conditions for FLEXPART chemistry runs** rather than direct warning-chain output (40 km is too coarse for urban-scale Cluj prediction — that's where the Regional ENSEMBLE comes in). |
| Archive depth | Rolling NRT archive on ADS; older archive history maintained for several years. |
| NRT latency | Forecast becomes available **within hours of initialisation**; typically operational by 06 UTC for the 00 UTC run, 18 UTC for the 12 UTC run. |

#### 17.2 CAMS European Air Quality Forecasts — Regional ENSEMBLE (the Cluj-relevant one)

| Field | Value |
|---|---|
| Dataset name (ADS) | `cams-europe-air-quality-forecasts` |
| Description | Daily ensemble forecasts of European air quality at **0.1° / ~10 km resolution** from 11 European air quality models (listed in the Summary table above). The ENSEMBLE = **median across 11 individual model outputs**; spread between models = forecast uncertainty estimate. Each contributing model is driven by **ECMWF's IFS high-resolution weather forecasts** (so the meteorological consistency across the ensemble is high). Daily analyses also produced by assimilating **EEA air quality observations** (which connects directly to Romania's RNMCA inputs). |
| Spatial resolution | **0.1° × 0.1° (~10 km at Cluj's latitude)** — the highest-resolution operational atmospheric composition forecast routinely available for Cluj. |
| Spatial coverage | European domain: **25°W to 45°E, 30°N to 72°N**. Cluj at (46.77°N, 23.55°E) is well within the domain — roughly centred E-W, in the northern half N-S. |
| Vertical | **7 height levels: surface + 6 above** (typically surface, 50, 100, 250, 500, 1000, 3000 m). Surface concentration is the primary deliverable. |
| Temporal | **1-hour cadence**; **4-day forecast** (D0 = 0–24h, D1 = 25–48h, D2 = 49–72h, D3 = 73–96h); daily analysis covers the previous day with EEA data assimilation. |
| Variables | **Primary pollutants**: O₃, NO₂, SO₂, CO, PM2.5, PM10. Additional: dust concentration at surface, sea-salt, NH₃, residual aerosols. Pollen forecasts (alder, birch, grass, olive, ragweed, mugwort) are a separate sub-product but accessed via the same dataset family. |
| Production schedule | Forecast D0 (0–24h) at **05:50 UTC**, D1 (25–48h) at **05:55 UTC**, D2 (49–72h) at **07:30 UTC**, D3 (73–96h) at **08:00 UTC**. Analysis (previous-day reanalysis with EEA observations) at **11:00 UTC**. |
| Cluj relevance | **THE MOST DIRECTLY COMPARABLE PRODUCT for the project's warning chain.** Same domain (Europe + N. Africa), same temporal cadence (hourly), comparable resolution (10 km vs the project's intended <10 km local-scale), same pollutants (PM2.5, PM10, O₃, NO₂, SO₂, CO + dust). **The project's GUI should ingest the CAMS ENSEMBLE forecast as a benchmark layer for Cluj** — the operational forecast from the European service that local authorities are likely already aware of and may consult independently. The project's outputs should be presented as "CAMS-European-ENSEMBLE-compatible" so users see consistent stories from both sources. |
| Archive depth | **3-year rolling NRT archive on ADS.** Older forecasts are not maintained at NRT quality (use the annual reanalyses for older periods). |
| Citation | Météo-France et al. (2020) "A regional air quality forecasting system over Europe: CAMS European Air Quality Forecasts" — dataset DOI is on the ADS catalogue page (changes with releases; always check the page). |

#### 17.3 CAMS Global Reanalysis EAC4

| Field | Value |
|---|---|
| Dataset name (ADS) | `cams-global-reanalysis-eac4` |
| Description | The 20+-year ECMWF Atmospheric Composition Reanalysis (4th generation), the global atmospheric-composition equivalent of ERA5. 4D-Var assimilation of satellite observations into a frozen-version IFS-COMPO model, producing a time-consistent 3D global atmospheric composition dataset. Builds on the earlier MACC reanalysis and CAMS interim reanalysis. |
| Spatial resolution | **~80 km** (coarser than the operational forecast at ~40 km, because reanalysis uses a frozen older model cycle for long-term consistency). |
| Vertical | **60 model levels (frozen at the EAC4 model cycle), 25 pressure levels distributed: 1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000 hPa.** |
| Temporal | **3-hourly** (00, 03, 06, 09, 12, 15, 18, 21 UTC). Monthly means also available. |
| Coverage | **2003 to end-2024** (current as of May 2026 — extends continuously as new reanalysis years are released). A successor reanalysis (EAC5) is in preparation but not yet operationally released. |
| Variables | 50+ species (same as the operational forecast but on the frozen reanalysis cycle): aerosols (7 types), full chemistry, AOD, PM. |
| Cluj relevance | **Historical context layer.** For any event in the warning chain, EAC4 provides "what did CAMS see at this exact time + location historically?" — useful for: (a) calibrating the warning thresholds against historical CAMS values, (b) climatology of atmospheric composition over Cluj for the seasonal-context layer in the GUI, (c) retrospective case studies of past events. |
| Citation DOI | [10.24381/cds.f375d2c8](https://doi.org/10.24381/cds.f375d2c8) (EAC4 hourly data on single levels) — verify against the current ADS catalogue page for any version updates. |

#### 17.4 CAMS European Air Quality Reanalyses

| Field | Value |
|---|---|
| Dataset name (ADS) | `cams-europe-air-quality-reanalyses` |
| Description | Annual reanalyses of European air quality, produced once per year, at the same 0.1° / ~10 km resolution as the operational ENSEMBLE forecast. Two flavours: **"unvalidated"** (uses NRT observations from EEA, available within ~6 months of year-end) and **"validated"** (uses fully QC'd EEA observations, available ~18 months after year-end). |
| Spatial resolution | **0.1° × 0.1° (~10 km)** — same as the operational forecast. |
| Coverage | Annual files, currently covering ~2013 to most recent complete year. |
| Cluj relevance | **Best high-resolution historical air quality dataset for Cluj.** For climatology + event-retrospective work, this is the highest-quality dataset available. RNMCA observations from Cluj's stations are part of the data assimilation inputs (via EEA reporting), so the reanalysis incorporates the project's own ground network indirectly. |

#### 17.5 GFAS — Global Fire Assimilation System

| Field | Value |
|---|---|
| Dataset name (ADS) | `cams-global-fire-emissions-gfas` |
| Description | **Daily global gridded fire emissions** derived from MODIS Fire Radiative Power (FRP) observations on Terra + Aqua. Provides emissions for ~40 species (CO, CO₂, NOx, SO₂, NH₃, NMVOCs, BC, OC, PM2.5, etc.) and the fire radiative power itself. The primary operational fire emission input for FLEXPART, GEOS-Chem, and most chemistry-transport models worldwide. |
| Spatial resolution | **0.1° × 0.1°** global. |
| Temporal | **Daily** emission flux estimates (kg m⁻² s⁻¹). |
| Coverage | **2003 to present** (continuously updated, ~1-day latency on the NRT stream). |
| Cluj relevance | **Critical for biomass-burning episodes.** When wildfire smoke is suspected as a source for a Cluj aerosol event (e.g. Mediterranean summer fires, Eastern European spring agricultural burning, occasional Saharan-trans-Atlantic transport), GFAS provides the gridded emission rate that FLEXPART needs to model the plume. Without GFAS (or equivalent), FLEXPART cannot quantify fire contributions to Cluj. |
| Reference | Kaiser, J. W., Heil, A., Andreae, M. O., Benedetti, A., Chubarova, N., Jones, L., Morcrette, J.-J., Razinger, M., Schultz, M. G., Suttie, M., & van der Werf, G. R. (2012). Biomass burning emissions estimated with a global fire assimilation system based on observed fire radiative power. *Biogeosciences*, 9, 527–554. DOI: [10.5194/bg-9-527-2012](https://doi.org/10.5194/bg-9-527-2012) |

### References

**Primary mission / system references:**
- Inness, A., Ades, M., Agustí-Panareda, A., Barré, J., Bechtold, P., Bocquet, M., Coopmann, O., Eskes, H., Flemming, J., Huijnen, V., Jones, L., Kipling, Z., Massart, S., Parrington, M., Peuch, V.-H., Razinger, M., Remy, S., Schulz, M., & Suttie, M. (2019). The CAMS reanalysis of atmospheric composition. *Atmospheric Chemistry and Physics*, 19, 3515–3556. DOI: [10.5194/acp-19-3515-2019](https://doi.org/10.5194/acp-19-3515-2019) — **the canonical EAC4 reanalysis reference; cite when EAC4 data is used.**
- Benedetti, A., Morcrette, J.-J., Boucher, O., Dethof, A., Engelen, R. J., Fisher, M., Flentje, H., Huneeus, N., Jones, L., Kaiser, J. W., Kinne, S., Mangold, A., Razinger, M., Simmons, A. J., & Suttie, M. (2009). Aerosol analysis and forecast in the European Centre for Medium-Range Weather Forecasts Integrated Forecast System: 2. Data assimilation. *Journal of Geophysical Research: Atmospheres*, 114, D13205. DOI: [10.1029/2008JD011115](https://doi.org/10.1029/2008JD011115) — **aerosol-specific reference for the CAMS forecast aerosol scheme.**
- Morcrette, J.-J., Boucher, O., Jones, L., Salmond, D., Bechtold, P., Beljaars, A., Benedetti, A., Bonet, A., Kaiser, J. W., Razinger, M., Schulz, M., Serrar, S., Simmons, A. J., Sofiev, M., Suttie, M., Tompkins, A. M., & Untch, A. (2009). Aerosol analysis and forecast in the European Centre for Medium-Range Weather Forecasts Integrated Forecast System: Forward modeling. *Journal of Geophysical Research: Atmospheres*, 114, D06206. DOI: [10.1029/2008JD011235](https://doi.org/10.1029/2008JD011235) — **forward-model companion paper.**

**CAMS European Regional ENSEMBLE:**
- Marécal, V., Peuch, V.-H., Andersson, C., Andersson, S., Arteta, J., Beekmann, M., Benedictow, A., Bergström, R., Bessagnet, B., Cansado, A., Chéroux, F., Colette, A., Coman, A., Curier, R. L., Denier van der Gon, H. A. C., Drouin, A., Elbern, H., Emili, E., Engelen, R. J., Eskes, H. J., Foret, G., Friese, E., Gauss, M., Giannaros, C., Guth, J., Joly, M., Jaumouillé, E., Josse, B., Kadygrov, N., Kaiser, J. W., Krajsek, K., Kuenen, J., Kumar, U., Liora, N., Lopez, E., Malherbe, L., Martinez, I., Melas, D., Meleux, F., Menut, L., Moinat, P., Morales, T., Parmentier, J., Piacentini, A., Plu, M., Poupkou, A., Queguiner, S., Robertson, L., Rouïl, L., Schaap, M., Segers, A., Sofiev, M., Tarasson, L., Thomas, M., Timmermans, R., Valdebenito, Á., van Velthoven, P., van Versendaal, R., Vira, J., & Ung, A. (2015). A regional air quality forecasting system over Europe: the MACC-II daily ensemble production. *Geoscientific Model Development*, 8, 2777–2813. DOI: [10.5194/gmd-8-2777-2015](https://doi.org/10.5194/gmd-8-2777-2015) — **foundational ENSEMBLE reference; cite when European ENSEMBLE data is used.**
- Per-product dataset DOIs are on each ADS catalogue page — always check before locking citations.

**GFAS:**
- Kaiser et al. 2012 (DOI above) — primary GFAS reference.
- Heymann, J., Reuter, M., Buchwitz, M., Schneising, O., Bovensmann, H., Burrows, J. P., Massart, S., Kaiser, J. W., & Crisp, D. (2017). CO₂ emission of Indonesian fires in 2015 estimated from satellite-derived atmospheric CO₂ concentrations. *Geophysical Research Letters*, 44, 1537–1544 — example of GFAS-driven inverse modelling.

**Citation phrasing (per Copernicus data licence):**
*"Generated using Copernicus Atmosphere Monitoring Service information [YEAR]. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains."*

### Host / Server

- **Atmosphere Data Store (ADS):** <https://ads.atmosphere.copernicus.eu/>
- **ADS API endpoint:** `https://ads.atmosphere.copernicus.eu/api`
- **ECMWF account creation:** <https://www.ecmwf.int/user/login> (same account as for CDS, but a SEPARATE personal access token must be generated specifically for ADS)
- **ADS personal access token page:** <https://ads.atmosphere.copernicus.eu/how-to-api>
- **CAMS overview / news:** <https://atmosphere.copernicus.eu/>
- **CAMS Regional production documentation:** <https://confluence.ecmwf.int/display/CKB/CAMS+Regional%3A+European+air+quality+analysis+and+forecast+data+documentation>
- **CAMS Quality Assurance / validation reports:** <https://atmosphere.copernicus.eu/quality-evaluation-information>
- **AeroVal validation dashboard:** <https://aeroval.met.no/>
- **CAMS Regional interactive viewer:** <https://regional.atmosphere.copernicus.eu/>
- **CAMS Global interactive viewer:** <https://atmosphere.copernicus.eu/charts/cams> 

### Programmatic download

**Step 1 — Credentials setup (one-time):**

1. Sign in to the same ECMWF account used for CDS at <https://www.ecmwf.int/user/login>.
2. Visit <https://ads.atmosphere.copernicus.eu/how-to-api> and copy the **ADS personal access token** (different from the CDS token, even though it's the same account).
3. Create or update `~/.adsapirc` (note: many users instead put a separate URL/key directly into a Python `cdsapi.Client(url=..., key=...)` call to avoid the ambiguity of two config files):
   ```
   url: https://ads.atmosphere.copernicus.eu/api
   key: <ADS-PERSONAL-ACCESS-TOKEN>
   ```
4. Accept the terms of use for each ADS dataset via the web UI before first API call.

**Step 2 — Pull CAMS European ENSEMBLE PM2.5 forecast for Cluj region:**

```python
import cdsapi
import os

# Construct ADS client explicitly (separate from CDS):
client = cdsapi.Client(
    url="https://ads.atmosphere.copernicus.eu/api",
    key=os.environ["ADS_API_KEY"],
)

# European ENSEMBLE forecast — today's 00 UTC run, all 96 forecast hours
target = "cams_europe_ens_pm25_cluj.nc"
client.retrieve(
    "cams-europe-air-quality-forecasts",
    {
        "variable": ["particulate_matter_2.5um"],
        "model": ["ensemble"],     # the 11-model median; also "chimere", "emep", etc., individually
        "level": ["0"],            # surface (other levels: 50, 100, 250, 500, 1000, 3000 m)
        "date": ["2026-03-18/2026-03-22"],
        "type": ["forecast"],      # also "analysis" for the EEA-assimilated previous-day analysis
        "time": ["00:00"],         # forecast initialisation hour
        "leadtime_hour": [f"{h}" for h in range(0, 97)],   # D0-D3 hourly
        "area": [48, 22, 45, 26],   # [N, W, S, E] — ±~1.5° box around Cluj
        "data_format": "netcdf",
    },
    target,
)
```

**Step 3 — Pull CAMS Global atmospheric composition forecast (boundary conditions for FLEXPART):**

```python
client.retrieve(
    "cams-global-atmospheric-composition-forecasts",
    {
        "variable": [
            "particulate_matter_2.5um", "particulate_matter_10um",
            "total_aerosol_optical_depth_550nm",
            "dust_aerosol_0.55-0.9um_mixing_ratio",
            "carbon_monoxide", "nitrogen_dioxide", "ozone", "sulphur_dioxide",
        ],
        "model_level": ["137"],   # surface model level (for surface concentrations)
        "date": "2026-03-18/2026-03-22",
        "time": ["00:00", "12:00"],  # both initialisations
        "leadtime_hour": [f"{h}" for h in range(0, 121, 3)],  # 5-day forecast every 3 hours
        "type": ["forecast"],
        "area": [50, 20, 42, 28],
        "data_format": "netcdf",
    },
    "cams_global_forecast_cluj.nc",
)
```

**Step 4 — Pull EAC4 reanalysis for a historical event analysis:**

```python
client.retrieve(
    "cams-global-reanalysis-eac4",
    {
        "variable": [
            "total_aerosol_optical_depth_550nm",
            "particulate_matter_2.5um",
            "dust_aerosol_optical_depth_550nm",
            "carbon_monoxide",
        ],
        "date": "2024-03-15/2024-03-22",   # e.g. a past dust event
        "time": ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"],
        "area": [50, 20, 42, 28],
        "data_format": "netcdf",
    },
    "cams_eac4_event_2024.nc",
)
```

**Step 5 — Pull GFAS fire emissions for a FLEXPART biomass-burning run:**

```python
client.retrieve(
    "cams-global-fire-emissions-gfas",
    {
        "variable": [
            "wildfire_radiative_power",
            "wildfire_flux_of_carbon_monoxide",
            "wildfire_flux_of_particulate_matter_d_2_5_um",
            "wildfire_flux_of_organic_carbon",
            "wildfire_flux_of_black_carbon",
        ],
        "date": "2026-03-15/2026-03-22",
        "data_format": "netcdf",
    },
    "gfas_emissions.nc",
)
```

### Manual download (interactive web UI)

- **CAMS European ENSEMBLE:** <https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-forecasts>
- **CAMS Global forecasts:** <https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts>
- **EAC4 reanalysis:** <https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4>
- **European reanalyses:** <https://ads.atmosphere.copernicus.eu/datasets/cams-europe-air-quality-reanalyses>
- **GFAS fire emissions:** <https://ads.atmosphere.copernicus.eu/datasets/cams-global-fire-emissions-gfas>
- **CAMS Regional interactive forecast viewer:** <https://regional.atmosphere.copernicus.eu/> — useful for quick "what is the ENSEMBLE saying about Cluj today?" visual checks before committing to an API download.

### Notes / caveats

- **CAMS and CDS use separate Data Stores with separate API tokens.** Same ECMWF account, but two separate personal access tokens, two separate endpoints (`https://cds.climate.copernicus.eu/api` vs `https://ads.atmosphere.copernicus.eu/api`), two separate terms-of-use-acceptance flows per dataset. Pipelines must manage both. Many users get tripped up by trying to use their CDS token for ADS — it fails silently or with cryptic auth errors. **Generate, store, and inject the tokens explicitly in code rather than relying on `~/.cdsapirc` to disambiguate.**
- **The ADS migration in mid-2024 paralleled the CDS migration.** Legacy ADS was decommissioned in September 2024. Any pipeline code written before September 2024 against the old ADS endpoints will fail. Same fix: upgrade `cdsapi ≥ 0.7.0`, regenerate tokens, accept terms again per dataset.
- **CAMS European ENSEMBLE is the most directly project-relevant product.** At 10 km resolution, hourly cadence, 4-day forecast, with EEA-data-assimilation analyses — it's the **operational reference benchmark** for the project's own warning chain. Operators looking at the GUI for Cluj should see (a) the project's own dispersion-derived predictions, (b) the CAMS ENSEMBLE forecast side-by-side, ideally with a difference / agreement-indicator panel. **When the two agree, confidence is high; when they diverge, the operator needs to know why** (different source assumptions, different boundary conditions, different model physics). The warning-chain documentation should explain this clearly to non-modeller end-users.
- **CAMS Global is too coarse for direct Cluj prediction (~40 km), but useful as boundary conditions.** The 40 km Cluj grid cell smears Cluj urban + surrounding rural area into a single value. Useful for boundary conditions feeding finer FLEXPART runs, or for very large-scale trans-continental events, but not as a Cluj-specific operational forecast. Always prefer the European ENSEMBLE at 10 km when both are available for the same time + variable.
- **CAMS European ENSEMBLE = median, not mean.** The 11-model median is the recommended product (more robust against single-model outliers than the mean). The ENSEMBLE spread (standard deviation across the 11 models) is provided separately as an uncertainty estimate. **The project should display the spread alongside the median** — when the 11 models agree (low spread), confidence is high; when they disagree (high spread), the operational warning should be flagged as "uncertain".
- **Daily analysis assimilates EEA observations — direct link to RNMCA.** The "analysis" (vs "forecast") product in `cams-europe-air-quality-forecasts` is the previous-day estimate after assimilating EEA air quality station observations. Romanian RNMCA data feeds into EEA, so **the CAMS European analysis indirectly incorporates Cluj station observations.** This creates a circular dependency the project should be aware of when comparing the project's own warning-chain output against the CAMS analysis: **the two are NOT independent** if the project's chain also uses RNMCA data directly. **Validation should be against held-out stations or against the unassimilated forecast (D0-D3), not the analysis.**
- **3-year rolling archive for European ENSEMBLE NRT.** Old forecasts > 3 years roll off the NRT archive. For longer historical work, use the annual reanalyses (which are produced at the same 10 km resolution but with full validation lag). Don't assume CAMS NRT data older than 3 years is accessible — it's intentionally not.
- **EAC4 stops at end-2024 (as of May 2026).** The CAMS global reanalysis is updated annually, typically with ~1-year lag (i.e. data through 2024 is available by late 2025; data through 2025 will appear in late 2026). A successor reanalysis (working name EAC5) is in preparation but not yet operational. **For event analyses in 2025 or 2026, EAC4 is not the right tool** — use the operational forecast archive instead.
- **GFAS depends on MODIS Terra + Aqua observations.** MODIS Terra was launched in 1999 and is past its design life; Aqua launched in 2002, also past design life. While both continue to operate, **GFAS data quality after Terra/Aqua end-of-life will rely on VIIRS-based replacement products** — the CAMS team is preparing for this transition. **For warning-chain architecture, treat GFAS as the current operational source but expect a methodology change in the 2027–2030 horizon as the underlying satellite stream migrates from MODIS to VIIRS.**
- **GFAS is the standard FLEXPART biomass-burning emission input.** No alternative widely-used in operational European air-quality modelling. Other emission products exist (FINN, QFED, FEER), but GFAS is what CAMS itself uses internally, and for project consistency it should be the default for FLEXPART runs.
- **Validation is documented and accessible.** CAMS publishes routine validation reports + monthly statistics at <https://atmosphere.copernicus.eu/quality-evaluation-information> and via AeroVal at <https://aeroval.met.no/>. The project should consult these to understand known biases (e.g. CAMS Global tends to underestimate winter PM in central/eastern Europe by ~10–30% — Cluj is squarely in this affected region; the ENSEMBLE corrects this somewhat via the data assimilation).
- **License is fully open Copernicus.** Free for any use including commercial. Attribution per the citation phrasing above is required.
- **Domain sizing for downloads.** CAMS files are dense — a single ENSEMBLE PM2.5 file over the European domain at all 96 forecast hours is several hundred MB; the same plus all pollutants is multi-GB. For Cluj-focused work, **always subset to a regional bounding box** (±~2° is usually sufficient for the warning chain's needs) at the API level rather than downloading the full domain. Reduces ingest time and storage by 100×.

---
