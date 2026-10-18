# Dataset metadata — SEVIRI on Meteosat Second Generation (MSG)

Companion documentation to the Stage 1 input-data table.
This file describes the SEVIRI imager products on EUMETSAT's Meteosat
Second Generation (MSG) satellites feeding the Cluj-Napoca aerosol
early-warning system.

**Important architectural note before reading further:** SEVIRI has been
superseded by **FCI on MTG-I1 (Meteosat-12)** which is fully operational
since December 2024 and offers significantly higher spatial and temporal
resolution. The "Recommended addition" section at the end of this file
proposes adding FCI as a separate input-table row, since the project
should ingest the modern instrument as primary and treat SEVIRI as a
graceful-degradation backup.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 13. SEVIRI — Meteosat Second Generation (MSG) imager

### Summary

| Field | Value |
|---|---|
| Instrument | **SEVIRI** (Spinning Enhanced Visible and Infrared Imager) — spin-stabilised passive optical/IR imager. **12 spectral channels**: 11 at 3 km nadir sampling distance (4 visible/near-IR for cloud + surface reflectance applications; 7 mid- and thermal-IR for cloud-top, surface temperature, water vapour, ozone, CO₂); plus **1 broadband High Resolution Visible (HRV) channel at 1 km nadir sampling**. The instrument scans by rotating with the satellite (~100 rpm), with a S-N scan mirror progressing line-by-line through 1250 (full resolution) or 3750 (HRV) scan lines per cycle. Built by Astrium (now Airbus) under ESA contract. |
| Network / Agency | **EUMETSAT** (operational owner, distributor) + **ESA** (developed the MSG satellite + SEVIRI under contract). MSG was a generation of 4 spin-stabilised geostationary satellites, the last MSG launching in 2015. |
| Platforms (currently operational, May 2026) | **Meteosat-10** (MSG-3, launched July 2012): currently provides the **prime full-disc service from 0° longitude** with 15-minute repeat (this is the primary SEVIRI feed for Europe). **Meteosat-11** (MSG-4, launched July 2015): provides the **Rapid Scan Service (RSS) from 9.5°E** with 5-minute repeat over the northern third of the Earth disc (covering Europe + N. Africa + adjacent seas). **Meteosat-9** (MSG-2, launched 2005): provides the **Indian Ocean Data Coverage (IODC) service from 45.5°E** with 15-minute repeat — relevant to the project only as a backup or for dust events traveling westwards from Asia/Middle East across into Europe. **Meteosat-8** retired October 2022. Periodic role swaps between Meteosat-10 and Meteosat-11 may occur (EUMETSAT has scheduled position/role exchanges); always check EUMETSAT's current operational configuration. |
| Products used (per docx label) | **"RGB 5.5 km nat/hrit"** — referring to multi-channel RGB composites generated from SEVIRI L1.5 imagery in native EUMETSAT (`.nat`) or HRIT format. The "5.5 km" label corresponds approximately to the **off-nadir resolution at Cluj's latitude** (Cluj ≈ 46.8°N; nadir is 0°N, so view-angle elongation pushes pixel size from 3 × 3 km at sub-satellite point to roughly 5 × 5 km at Cluj for the standard channels, and from 1 × 1 km nadir to ~1.7 × 1.7 km at Cluj for HRV). |
| RGB composites relevant to the aerosol warning chain | RGB composites are not native SEVIRI products — they are built from channel combinations. The aerosol-relevant ones: **Dust RGB** (IR12.0–IR10.8, IR10.8–IR8.7, IR10.8) — colours dust plumes pink/magenta against cooler grey backgrounds, very effective for Saharan and Aeolian dust events; **Ash RGB** (IR12.0–IR10.8, IR10.8–IR8.7, IR10.8 with tuned scaling) — volcanic ash detection, relevant for aviation alerts; **Natural Colour RGB** (NIR1.6, VIS0.8, VIS0.6) — daytime overview, vegetation green / desert sandy / clouds white. The Dust RGB is the highest-value composite for an aerosol early-warning system because **it works on thermal channels, so it operates at night** (unlike daytime-only AOD products). |
| Resolution at Cluj | Standard channels: ~5 × 5 km² (effective pixel size off-nadir at Cluj's latitude). HRV channel: ~1.7 × 1.7 km². The docx's "5.5 km" is correct for standard-channel display use. |
| Coverage | **Europe + Africa + Middle East + Atlantic Ocean** (full disc visible from 0° longitude). Cluj is well within the full-disc area; the RSS Europe-only scan from Meteosat-11 also covers Cluj. |
| Revisit / temporal resolution | **Meteosat-10 full disc: 15 minutes** (standard prime service from 0°). **Meteosat-11 Rapid Scan: 5 minutes** over Europe. The 5-minute RSS is the more operationally useful cadence for the warning chain. |
| Processing level | **L1.5** is the standard distributed product — geolocated calibrated radiances. L2 products (aerosols, clouds, dust mask, etc.) are produced by EUMETSAT's Satellite Application Facilities (SAFs), particularly **NWC SAF** (nowcasting), **AC SAF** (atmospheric composition), and **CM SAF** (climate monitoring). |
| File format | **HRIT** (High Rate Image Transmission, segment-based, the EUMETCast broadcast format) or **`.nat`** (EUMETSAT Native — single file with all channels and metadata, used by EUMETSAT Data Store for offline downloads). Both are XRIT-derived binary formats with documented headers; opens with `satpy` (Python — recommended) or proprietary tools like McIDAS / SNAP. **Note:** these are *not* NetCDF — distinct from FCI which uses NetCDF (see "Recommended addition" below). |
| Filename pattern | HRIT segment files: `H-000-MSG<n>__-MSG<n>________-<CHANNEL>-<SEGMENT>__-<YYYYMMDDHHMM>-<C/D>` (one file per channel per segment). Native file: `MSG<n>-SEVI-MSG15-0100-NA-<YYYYMMDDHHMMSS>.<MILLISEC>Z-NA.nat`. |
| Cluj coverage cadence | 15-min full disc (Meteosat-10) → 96 observations per day. 5-min RSS (Meteosat-11) → 288 observations per day. **Day and night both** — the IR channels do not require sunlight, so SEVIRI is the only entry in the input table (apart from the ceilometer and lidar) that observes Cluj continuously through the night. |
| NRT availability | **YES — sub-minute latency on EUMETCast** (direct broadcast). EUMETSAT Data Store also delivers within minutes. **This is the fastest data source in the entire project** for any satellite product. |
| Authentication | **EUMETSAT EO Portal / Data Store account** (free) — same as for SLSTR, Sentinel-5 UVNS, Sentinel-4 UVN. For real-time broadcast via EUMETCast Terrestrial / Satellite: separate institutional registration + DVB-S receiver hardware required. |
| Programmatic access | YES — **EUMETSAT Data Store API + EUMDAC** Python library (same toolchain reused), or direct EUMETCast for institutional users. For Python-based parsing of HRIT/`.nat` data, the canonical tool is **`satpy`** (PyTroll project) — handles SEVIRI L1.5 directly, generates RGB composites with one-line API calls, and resamples to user-specified projections. |
| Layer destination | **L2:** FLEXPART (UVAI-equivalent dust/ash flag + cloud top context for transport modelling); HYSPLIT (dust/ash/smoke flag overlay on trajectory visualisations). GRASP: not consumed (SEVIRI radiances at coarse spatial resolution provide limited value vs ground-based + LEO synergy already in the chain). **L3:** Knowledge Graph (**Dust RGB and natural-colour imagery for the GUI** — fast-refresh hourly background layer; the highest-cadence visual layer in the entire warning chain at 5-min refresh during dust events). |

### References

**Primary instrument reference:**
- Schmetz, J., Pili, P., Tjemkes, S., Just, D., Kerkmann, J., Rota, S., & Ratier, A. (2002). An introduction to Meteosat Second Generation (MSG). *Bulletin of the American Meteorological Society*, 83(7), 977–992. DOI: [10.1175/1520-0477(2002)083<0977:AITMSG>2.3.CO;2](https://doi.org/10.1175/1520-0477(2002)083%3C0977:AITMSG%3E2.3.CO;2)

**RGB composite recipes (EUMETSAT operational guides):**
- EUMETSAT "Best Practices for RGB Compositing" series — see <https://resources.eumetrain.org/> for the Dust RGB, Ash RGB, Natural Colour, Day Microphysics quick guides (well-illustrated, intended for operational forecasters).
- Lensky, I. M., & Rosenfeld, D. (2008). Clouds-Aerosols-Precipitation Satellite Analysis Tool (CAPSAT). *Atmospheric Chemistry and Physics*, 8, 6739–6753 — methodology underpinning many of the operational RGB recipes.

**EUMETSAT documentation:**
- SEVIRI instrument overview: <https://www.eumetsat.int/seviri>
- MSG operations & services: <https://www.eumetsat.int/msg-services>
- HRIT/Native L1.5 Data Guide: <https://user.eumetsat.int/resources/user-guides/msg-high-rate-seviri-level-1-5-data-guide>

**Citation format**: *"Source: EUMETSAT"* or *"Meteosat data © EUMETSAT [YEAR]"*. EUMETSAT data are openly available for non-commercial use under the EUMETSAT data policy.

### Host / Server

- **EUMETSAT Data Store** (primary path for archived + recent data): <https://data.eumetsat.int/>
- **EUMETCast** (live broadcast — fastest possible delivery): <https://www.eumetsat.int/eumetcast>
- **EUMETSAT Product Navigator:** <https://navigator.eumetsat.int/>
- **MSG SEVIRI L1.5 collection** in Data Store: search for `EO:EUM:DAT:MSG:HRSEVIRI` (15-min full disc) or `EO:EUM:DAT:MSG:HRSEVIRI-RSS` (5-min Rapid Scan)
- **EUMDAC Python library:** <https://gitlab.eumetsat.int/eumetlab/data-services/eumdac>
- **satpy (Python toolkit for SEVIRI L1.5 processing + RGB compositing):** <https://satpy.readthedocs.io/>

### Programmatic download

**EUMDAC pattern (same auth flow as for SLSTR SL_2_AOD, Sentinel-5 UVNS, Sentinel-4 UVN):**

```python
import eumdac
import os
from datetime import datetime, timedelta, timezone

token = eumdac.AccessToken((os.environ["EUMETSAT_KEY"],
                            os.environ["EUMETSAT_SECRET"]))
datastore = eumdac.DataStore(token)

# 15-minute full disc (Meteosat-10 at 0°E)
collection_fd = datastore.get_collection("EO:EUM:DAT:MSG:HRSEVIRI")

# 5-minute Rapid Scan Service (Meteosat-11 at 9.5°E)
collection_rss = datastore.get_collection("EO:EUM:DAT:MSG:HRSEVIRI-RSS")

# Pull last hour of RSS data covering Cluj
now = datetime.now(timezone.utc)
products = collection_rss.search(
    bbox=(23.0, 46.3, 24.1, 47.2),
    dtstart=(now - timedelta(hours=1)).isoformat(),
    dtend=now.isoformat(),
)

for p in products:
    print(p, p.sensing_start)
    with p.open() as src, open(f"{p}.nat", "wb") as dst:
        dst.write(src.read())
```

**Processing a downloaded `.nat` file into Dust RGB with satpy:**

```bash
pip install satpy
```

```python
from satpy import Scene
from satpy.utils import debug_on
import matplotlib.pyplot as plt

# Load the .nat file
scn = Scene(reader="seviri_l1b_native", filenames=["MSG3-SEVI-MSG15-0100-NA-20260518T100000.nat"])
scn.load(["dust"])    # the 'dust' composite is a registered RGB recipe

# Resample to a local Cluj-centred area definition
from pyresample import create_area_def
cluj_area = create_area_def(
    "cluj_area",
    {"proj": "stere", "lat_0": 46.77, "lon_0": 23.55, "ellps": "WGS84"},
    width=600, height=600,
    area_extent=(-150e3, -150e3, 150e3, 150e3),   # ±150 km around Cluj
)
local = scn.resample(cluj_area)
local.save_dataset("dust", filename="cluj_dust_rgb.png")
```

**EUMETCast direct broadcast** (for institutional users needing sub-minute latency): requires DVB-S receiver hardware and EUMETCast subscription. Beyond the scope of a Python-only ingestion pipeline; typically only deployed at meteorological agencies. The EUMETSAT Data Store API is sufficient for sub-5-minute latency in normal pipelines.

### Manual download (interactive web UI)

- **EUMETSAT Data Store** search: <https://data.eumetsat.int/> → filter Mission = "Meteosat Second Generation"
- **EUMETSAT Viewer** (real-time browse): <https://view.eumetsat.int/>
- **NWC SAF / NWCSAF Geo software** (offline RGB + nowcasting products generation from L1.5 data): <https://www.nwcsaf.org/>

### Notes / caveats

- **Day + night coverage is unique.** SEVIRI is the only satellite source in the entire project that observes Cluj **24 hours a day**. The IR channels (Dust RGB, Ash RGB) work at night; only the visible + HRV channels are daytime-restricted. For an early-warning chain, this matters: night-time dust events arriving from the Sahara overnight can be detected and tracked, whereas a daily-LEO-only chain would only catch them at the next morning overpass.
- **Resolution at Cluj is the binding limitation.** SEVIRI standard channels at Cluj's latitude resolve at ~5 km — coarse compared to MODIS (1 km), MSI (10 m), and even Sentinel-5 UVNS (7 km). It is **fundamentally a synoptic-scale instrument, not an urban-scale one.** Cluj appears as a 1-pixel "smudge" in standard channels; the HRV channel does considerably better at ~1.7 km. SEVIRI cannot resolve urban-scale gradients within Cluj.
- **EUMETCast vs Data Store.** EUMETCast is the broadcast service (sub-minute latency, DVB-S hardware). Data Store is the HTTP / API service (few-minute latency, no hardware needed). For a software-only pipeline at a research institute, Data Store via EUMDAC is the practical choice. EUMETCast is only justified if your operations require absolute sub-minute latency (e.g. severe-weather alerts feeding into a public warning system).
- **HRIT vs Native format choice.** Native (`.nat`) is one file per repeat cycle with all channels — simpler for batch processing, what the Data Store delivers. HRIT is segment-based (one file per channel per scan-segment) — what EUMETCast broadcasts in real time. `satpy` reads both; for `.nat` files use `reader="seviri_l1b_native"`, for HRIT use `reader="seviri_l1b_hrit"`.
- **No native aerosol product, only RGB composites.** SEVIRI's "aerosol detection" capability is qualitative — it relies on RGB composites that exploit channel differences to highlight dust, ash, or smoke. **Quantitative AOD products from SEVIRI exist** (e.g. AERUS-GEO, CM SAF / SAF on Land Surface Analysis aerosol products, ICARE / AERONET-extension products), but the docx framing focuses on RGB imagery and the Knowledge Graph visualization. The 5-minute RSS Dust RGB is what most operationally-focused users care about.
- **Don't confuse Meteosat-10 with Meteosat-11.** The two are operationally distinct and provide different services. Periodic swaps occur. Always programmatically query the Data Store for the correct *current* operational satellite if your pipeline depends on a specific position/cadence; do not hard-code satellite IDs.
- **Reference paper is from 2002.** Schmetz et al. 2002 BAMS is the standard SEVIRI reference and remains valid; for newer applications/algorithms, cite SAF-specific publications.

---

