# Dataset metadata — Sentinel-4 UVN on MTG-S1 (Meteosat-13)

Companion documentation to the Stage 1 input-data table.
This file describes the Sentinel-4 UVN spectrometer products on the
**MTG-S1 (Meteosat-13) / Sentinel-4A** satellite — the **first
geostationary atmospheric composition mission over Europe**, currently in
commissioning following its 1 July 2025 launch.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

This is the third of three entries on hyperspectral nadir DOAS-class
instruments: **(a)** TROPOMI on Sentinel-5P (LEO afternoon, two files
back), **(b)** UVNS on Sentinel-5 / MetOp-SG-A (LEO morning, previous
file), **(c)** UVN on Sentinel-4 / MTG-S (geostationary, this file).
**Sentinel-4 is uniquely positioned in the project as the only source
providing hourly observations of Cluj.**

---

## 12. Sentinel-4 UVN — MTG-S1 geostationary atmospheric composition

### Summary

| Field | Value |
|---|---|
| Instrument | **UVN** (Ultraviolet / Visible / Near-Infrared imaging spectrometer) — pushbroom hyperspectral spectrometer. **3 spectral bands** (no SWIR, unlike Sentinel-5 UVNS): **UV-1** (305–400 nm), **VIS** (400–500 nm), **NIR** (750–775 nm). Spectral resolution 0.5 nm in UV/VIS, 0.12 nm in NIR. **First geostationary UVN mission in the world** — uniquely positioned vs the polar-orbiting TROPOMI/UVNS family and complementary to NASA's TEMPO (North America) and KARI's GEMS (Asia) which form the global geostationary air-quality constellation. Built by Airbus Defence and Space under ESA contract. |
| Network / Agency | **ESA** (developed UVN under Copernicus contract with Airbus) + **EUMETSAT** (operates the MTG-S host platform, develops ground segment, distributes data) + **European Commission** (programmatic owner via Copernicus). Operationally aligned with the **Copernicus Atmosphere Monitoring Service (CAMS)**. |
| Platform (May 2026) | **MTG-S1** (Meteosat Third Generation – Sounder 1), officially designated **Meteosat-13** upon entering operational service. **Geostationary orbit** at approximately **0° longitude**, altitude **~35,786 km**. Launched **1 July 2025 at 21:04 UTC** on a **SpaceX Falcon 9** (B1085) from **Kennedy Space Center LC-39A**. LEOP successfully concluded 18 July 2025; handed over to EUMETSAT operations from the Fucino Space Centre, Italy. **Currently in commissioning phase** as of May 2026 — first preliminary Sentinel-4 images were released by ESA in **October 2025** showing NO₂, SO₂, and O₃, including a distinct **SO₂ plume from Mount Etna** and clear NO₂ pollution hotspots along the Mediterranean coast and central Europe. CEOS lists current EOL **March 2036** (~10-year operational lifetime). |
| Status for this project (IMPORTANT) | **Pre-operational — commissioning data only.** First-light qualitative imagery is public (Oct 2025), but operational L2 product distribution has not started. **Expected first operational data: H2 2026**, with typical commissioning duration of 9–12 months from launch already approaching its end. **Plan the pipeline to ingest from H2 2026 onwards.** Until then, treat as a high-priority placeholder. |
| Products planned (per ESA Sentinel-4 Mission Handbook) | **NO₂** (total + tropospheric subcolumn), **O₃** (total column + tropospheric subcolumn), **SO₂** (total column), **HCHO** (formaldehyde), **CHOCHO** (glyoxal — same new product as Sentinel-5), **AOD** (Aerosol Optical Depth), **ALH** (Aerosol Layer Height), **UV Aerosol Index** (UVAI), **Surface BRDF** (Bidirectional Reflectance Distribution Function), **Cloud properties** (fraction, height, optical thickness). |
| Sentinel-4A vs Sentinel-4B | **Sentinel-4A** on MTG-S1 (this entry — launched July 2025). **Sentinel-4B** on MTG-S2, planned for launch ~2034. Together they will provide ~17 years of operational Europe air-quality data continuity. |
| Resolution | **8 × 8 km² nominal spatial sampling at the reference point (45°N, 0°E).** At Cluj-Napoca (46.77°N, 23.55°E), the view angle from the subsatellite point (0°N, 0°E) is ~50° (combined latitude + longitude offset), so the actual pixel footprint at Cluj is somewhat elongated — **roughly 8 × 10–12 km² depending on the exact slit orientation**. Coarser than TROPOMI (5.5 × 3.5 km²) and the same as Sentinel-5 UVNS (7 × 7 km²) in approximate area, but the order-of-magnitude faster revisit fully outweighs the spatial-resolution loss for warning-chain purposes. |
| Coverage area | **Europe + North Africa.** The "Geo-Coverage Area" extends from ~30°W to ~45°E in longitude and ~30°N to ~65°N in latitude (the full reference daily-coverage box), with daily-observed area shifting seasonally to follow solar illumination. **Cluj-Napoca is well within the daily observed area year-round.** |
| Revisit / temporal resolution | **~60 minutes (hourly) East-to-West scan repeat cycle.** Achieved by continuous E/W scanning of a N/S-oriented slit field-of-view (FOV ~4° N/S) over a field-of-regard of ~11° E/W. Each repeat cycle = one full coverage of the area, followed by fast W/E retrace. **Daytime only** (no observations at night — solar reflectance measurement). For Cluj: roughly **14 hourly observations per day** in summer (~05:00–19:00 local time), **6–8 hourly observations per day** in winter (Cluj's December daylight is ~08:30–16:30 local). |
| Processing level | **L0** (instrument source packets), **L1B** (geolocated calibrated radiances), **L2** (geophysical retrievals). For this project: L1B is the GRASP synergy input; L2 trace-gas columns feed the warning chain. |
| File format | **NetCDF4 (CF-compliant)** — same family as TROPOMI and Sentinel-5 UVNS, EUMETSAT EPS-SG / MTG-style conventions. Specific schema details will be confirmed at first operational release. |
| Filename pattern | Expected to follow MTG-S conventions, broadly: `W_xx-eumetsat-darmstadt,SAT,MTI<n>+S4-UVN_C_EUMP_<TIMESTAMP>_<TYPE>.nc`. Exact pattern public at operational release. |
| NRT availability | **Operational NRT planned with sub-hourly latency** — the geostationary architecture allows continuous downlink, so L2 products should be available within tens of minutes of the end of each hourly scan cycle (best of any DOAS product in the project). |
| Authentication | **EUMETSAT EO Portal / Data Store account** (free) — same auth path as SLSTR SL_2_AOD and Sentinel-5 UVNS. EUMETCast direct broadcast also planned. CDSE mirror layer expected. |
| Programmatic access | YES (planned, will mirror SLSTR / Sentinel-5 pattern) — **EUMETSAT Data Store API + EUMDAC Python library**, plus EUMETCast direct broadcast. The auth, search, and download code can directly reuse what was developed for SLSTR `SL_2_AOD`. |
| Layer destination | **L2:** **GRASP (PRIMARY — direct algorithmic relevance)** — GRASP Earth is the operational AOD and BRDF retrieval team for Sentinel-4 UVN (algorithms originally developed under the Sentinel-5P Innovation project, now ported to S4). The project's GRASP layer is the most natural downstream consumer of Sentinel-4. FLEXPART (NO₂, SO₂, CO₂ proxy + glyoxal for emission tracers; ALH for vertical constraints — hourly cadence enables tracking morning rush-hour vs midday plume evolution). HYSPLIT (column gases + UVAI for transport context). **L3:** Knowledge Graph (**hourly updates** for NO₂, SO₂, O₃, UVAI, UV Index, AOD — this is the project's highest-cadence atmospheric-composition layer, by an order of magnitude). |

### Why Sentinel-4 matters for an urban early-warning system

Sentinel-4 is structurally different from every other satellite source in this project, and the difference is exactly what an urban early-warning system needs most:

| Aspect | TROPOMI (S5P) / UVNS (S5) | UVN (S4) |
|---|---|---|
| Orbit | LEO sun-synchronous polar | Geostationary at 0°E |
| Cluj observations per day | 1 (S5P @ 12:30 local) or 2 (S5 + S5P) | **~14 in summer, 6–8 in winter** |
| Latency between observations | ~24 hours or ~3 hours | **~60 minutes** |
| Resolution at Cluj | 5.5 × ~5 km² (TROPOMI) | 8 × 10–12 km² |
| Detects rush-hour buildup? | No (single snapshot/day) | **Yes (hourly NO₂ evolution)** |
| Detects intra-day pollution event? | Marginal (1–2 snapshots) | **Yes (tracks event from start to dissipation)** |
| Forecast-relevant for next-hour alerts? | No (next overpass tomorrow) | **Yes (nowcasting capable)** |

For a first-responder GUI in Cluj, the value of hourly geostationary data over daily polar-orbit data is similar to the value of weather radar over once-daily satellite imagery — fundamentally different operational use cases, despite measuring similar variables.

### References

**Instrument design references:**
- Gulde, S. T., Kolm, M. G., Smith, D. J., Maurer, R., Bazalgette Courrèges-Lacoste, G., Sallusti, M., & Bagnasco, G. (2017). Sentinel-4: a geostationary imaging UVN spectrometer for air quality monitoring: status of design, performance and development. *Proc. SPIE 10563, International Conference on Space Optics — ICSO 2014*, 1056341. DOI: [10.1117/12.2304099](https://doi.org/10.1117/12.2304099)
- Gulde et al. follow-on papers (2018, 2021) for design-update overviews — see the SPIE Optical Engineering proceedings series.

**Algorithm references (heritage from TROPOMI — same algorithm developer ecosystem):**
- AOD + BRDF: **GRASP Earth** (Dubovik et al.) — operational algorithm port from Sentinel-5P Innovation to Sentinel-4. See GRASP project page: <https://www.grasp-earth.com/portfolio/sentinel-5p-innovation>
- NO₂, CO, AAI, ALH: KNMI heritage (van Geffen, Stein Zweers, Nanda) — algorithm papers cited in the TROPOMI metadata file (`dataset_metadata_sentinel5p_tropomi.md`)
- SO₂, HCHO, O₃: BIRA-IASB + DLR heritage (Theys, De Smedt) — same as TROPOMI

**Mission overview (peer-reviewed paper expected post-commissioning):** No comprehensive peer-reviewed mission paper has been published yet (the satellite is in commissioning at time of writing). Use the Gulde 2017 SPIE proceedings as the citation until the mission paper appears in *Remote Sensing of Environment* or similar.

**Citation format** (once operational): *"Contains modified Copernicus Sentinel-4 data [YEAR], processed by EUMETSAT"*.

### Host / Server (planned)

- **EUMETSAT Data Store** (primary path): <https://data.eumetsat.int/>
- **EUMETCast** (real-time push): <https://www.eumetsat.int/eumetcast>
- **Copernicus Data Space Ecosystem mirror** (planned): <https://dataspace.copernicus.eu/>
- **EUMDAC Python library**: <https://gitlab.eumetsat.int/eumetlab/data-services/eumdac>
- **API key generation**: <https://api.eumetsat.int/api-key/>
- **ESA Sentinel-4 mission page**: <https://sentinel.esa.int/web/sentinel/missions/sentinel-4>
- **ESA Copernicus Sentinel-4 page**: <https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-4>
- **EUMETSAT MTG-S1 / Sentinel-4 page**: <https://www.eumetsat.int/meteosat-third-generation-sounder-1-and-copernicus-sentinel-4>
- **MTG-S1 commissioning status updates**: <https://www.eumetsat.int/mtg> (check periodically for first-data-release announcements)

### Programmatic download (template — will be confirmed at operational release)

**Expected pattern (using EUMDAC, identical to SLSTR SL_2_AOD and Sentinel-5 UVNS):**

```python
import eumdac
import os
from datetime import datetime, timedelta, timezone

token = eumdac.AccessToken((os.environ["EUMETSAT_KEY"],
                            os.environ["EUMETSAT_SECRET"]))
datastore = eumdac.DataStore(token)

# Collection IDs to be confirmed — placeholder pattern (based on MTG-S/Meteosat conventions):
# EO:EUM:DAT:MTG-S:S4-L2__NO2___
# EO:EUM:DAT:MTG-S:S4-L2__SO2___
# EO:EUM:DAT:MTG-S:S4-L2__O3____
# EO:EUM:DAT:MTG-S:S4-L2__HCHO__
# EO:EUM:DAT:MTG-S:S4-L2__CHOCHO  (NEW vs TROPOMI)
# EO:EUM:DAT:MTG-S:S4-L2__AER_AI_
# EO:EUM:DAT:MTG-S:S4-L2__AER_LH_
# EO:EUM:DAT:MTG-S:S4-L2__AOD_____
# EO:EUM:DAT:MTG-S:S4-L2__BRDF____  (GRASP-produced)
# EO:EUM:DAT:MTG-S:S4-L2__CLOUD___

# Once IDs are public:
# collection = datastore.get_collection("EO:EUM:DAT:MTG-S:S4-L2__NO2___")
# products = collection.search(
#     bbox=(23.0, 46.3, 24.1, 47.2),  # Cluj
#     dtstart=(datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),  # last 2 hours
#     dtend=datetime.now(timezone.utc).isoformat(),
# )
# Expect roughly 1-2 hourly granules per query (vs 1 per day for TROPOMI)
```

**Reading + spatial subsetting (expected pattern — TROPOMI-class):**

```python
import xarray as xr
# Once operational filenames are known:
# ds = xr.open_dataset("W_xx-eumetsat-darmstadt,SAT,MTI1+S4-UVN____*.nc", group="PRODUCT")
# Variables expected to mirror TROPOMI: nitrogendioxide_tropospheric_column, qa_value, ...
# Spatial subset to Cluj will yield 1-3 pixels per hourly scan depending on the exact tile geometry
```

### Manual download (interactive web UI)

- **EUMETSAT Data Store** (once products published): <https://data.eumetsat.int/>
- **EUMETSAT Product Navigator**: <https://navigator.eumetsat.int/>
- **ESA Sentinel-4 latest news / commissioning updates**: <https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-4>

### Notes / caveats

- **NOT YET OPERATIONAL** (May 2026). MTG-S1 / Sentinel-4A is **in commissioning**. First preliminary images were released October 2025 (NO₂, SO₂, O₃ maps incl. Etna SO₂ plume), demonstrating instrument health. Operational L2 distribution expected H2 2026. Plan ingestion infrastructure now, switch on data ingest when EUMETSAT announces first-product release.
- **Hourly cadence is the project superpower.** All other satellite sources in this table provide 1 (S5P, MSI), 2 (MODIS Terra+Aqua), or up to 5 (full LEO stack with NOAA-21) observations of Cluj per day. **Sentinel-4 alone provides ~14 summer / ~6–8 winter daytime hourly observations per day.** For an urban early-warning system this is transformative — the difference between "we got one snapshot at noon" and "we tracked the plume evolution hour-by-hour from morning rush hour through midday photochemistry to evening dispersal". The GUI's NO₂ / UVAI / AOD layers should be designed to refresh hourly, not daily, with Sentinel-4 as the primary data source once operational.
- **Geostationary trade-offs.** Sentinel-4 trades **spatial resolution** (8 × 10–12 km² at Cluj, coarser than TROPOMI's ~5 × 5 km²) for **temporal resolution** (hourly vs daily). At Cluj's view angle from 0° subsatellite point (~50° combined off-nadir), the pixel is elongated in the E-W direction. The Cluj urban core fits in roughly 1 Sentinel-4 pixel, so the GUI will show Cluj as a single "hot pixel" rather than a multi-pixel urban structure. Sub-urban gradients within Cluj will not be resolvable — TROPOMI/UVNS at sharper resolution remains the source for any urban-internal detail (still at daily cadence).
- **GRASP intersection is direct and operational.** This is the most algorithmically integrated row in the entire input table with the project's L2 GRASP layer: **GRASP Earth (the spin-off from the original Dubovik GRASP group at Université de Lille)** is the operational retrieval team for Sentinel-4 AOD and surface BRDF, with algorithms originally developed under the ESA-funded "Sentinel-5P Innovation" project and ported to Sentinel-4 operations. **The project's GRASP layer will receive Sentinel-4 AOD/BRDF L2 products natively** — no algorithmic mismatch to bridge, just an ingest connection.
- **Daytime only — and Cluj's winter daylight matters.** Solar reflectance measurement means **no observations at night** and **observations only when SZA < ~80°**. At Cluj's latitude, December–January daylight is roughly 08:30–16:30 local time, giving only **6–8 useful hourly scans per day in winter**, compared to ~14 in summer. The warning chain should expect this seasonal cycle in data availability.
- **3 bands, no SWIR.** Unlike TROPOMI (8 bands incl. SWIR) and Sentinel-5 UVNS (7 bands incl. SWIR), Sentinel-4 UVN has only 3 bands (305–500 nm + 750–775 nm). The lack of SWIR means **no CO and no CH₄ retrievals** from Sentinel-4 — those species can only come from TROPOMI/UVNS in this project. Sentinel-4's strengths are NO₂, SO₂, O₃, HCHO, glyoxal, aerosols, UV index — all of which depend on UV-VIS absorption.
- **Part of a global geostationary air-quality constellation.** Sentinel-4 is the European member of a worldwide network: **GEMS** (Geostationary Environment Monitoring Spectrometer, KARI / South Korea, operational since 2020, monitors Asia), **TEMPO** (Tropospheric Emissions: Monitoring of Pollution, NASA, operational since April 2023, monitors North America), and now **Sentinel-4** (Europe + N Africa). The three together provide quasi-continuous geostationary air-quality monitoring of the northern-hemisphere industrial belt — relevant for cross-continental smoke/dust transport tracking and for cross-instrument validation. **If the project ever wants to track e.g. North American wildfire smoke or Saharan dust arriving at Cluj, the upstream observations are already available from TEMPO and GEMS plus Sentinel-4.**
- **EUMETSAT-only distribution path (with planned CDSE mirror).** Same auth as SLSTR SL_2_AOD and Sentinel-5 UVNS — no new credential setup beyond what's already in the pipeline.
- **Algorithm continuity from TROPOMI.** Same algorithm developer ecosystem (KNMI, DLR, BIRA, GRASP Earth) — until Sentinel-4-specific ATBDs are released post-commissioning, cite the TROPOMI algorithm papers for L2 products.
- **Don't confuse the naming.** **Sentinel-4** = the instrument (UVN spectrometer). **MTG-S1** = the satellite hosting it. **Meteosat-13** = the operational designation MTG-S1 receives after commissioning. **Sentinel-4A** = the specific S4 instrument flight model on MTG-S1 (Sentinel-4B will be on MTG-S2 in ~2034). All four names refer to the same hardware in current orbit.
- **EU citation policy**: *"Contains modified Copernicus Sentinel-4 data [YEAR], processed by EUMETSAT"*. Cite the Gulde 2017 SPIE proceedings for the instrument until a peer-reviewed mission paper appears post-commissioning. For AOD and BRDF specifically, also cite the GRASP algorithm references (Dubovik et al. 2014 ATMOS).

---
