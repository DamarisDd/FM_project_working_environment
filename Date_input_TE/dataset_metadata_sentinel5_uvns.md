# Dataset metadata — Sentinel-5 UVNS on MetOp-SG-A

Companion documentation to the Stage 1 input-data table.
This file describes the Sentinel-5 UVNS spectrometer products on the
**MetOp-SG-A1** satellite (also called Sentinel-5A) — the operational LEO
successor to Sentinel-5P TROPOMI, currently in commissioning following its
13 August 2025 launch.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

This is the second of three entries on hyperspectral nadir DOAS-class
instruments: **(a)** TROPOMI on Sentinel-5P (LEO, afternoon orbit, previous
file), **(b)** UVNS on Sentinel-5 / MetOp-SG-A (LEO, morning orbit, this
file), **(c)** UVN on Sentinel-4 / MTG-S (geostationary, hourly Europe
coverage, next file).

---

## 11. Sentinel-5 UVNS — MetOp-SG-A operational atmospheric composition

### Summary

| Field | Value |
|---|---|
| Instrument | **UVNS** (Ultraviolet / Visible / Near-Infrared / Shortwave-Infrared Spectrometer) — pushbroom hyperspectral imaging spectrometer. **7 spectral bands** total: **UV-1** (270–300 nm), **UV-2** (300–370 nm), **VIS** (370–500 nm), **NIR-1** (685–710 nm), **NIR-2** (745–773 nm), **SWIR-1** (1590–1675 nm), **SWIR-3** (2305–2385 nm). Same spectral concept as TROPOMI but designed for operational continuity (multi-decade) rather than research/precursor. Built by Airbus Defence and Space (Friedrichshafen). |
| Network / Agency | **ESA** (developed UVNS under Copernicus contract with Airbus) + **EUMETSAT** (procures launch service, operates the satellite, develops ground segment, distributes data) + **European Commission** (programmatic owner via Copernicus). Operationally aligned with the **Copernicus Atmosphere Monitoring Service (CAMS)** as the primary downstream user. |
| Platform (May 2026) | **MetOp-SG-A1** (also called Sentinel-5A) — first of three planned A-type satellites in the EUMETSAT Polar System Second Generation (EPS-SG) programme. Launched **13 August 2025** on an **Ariane 6** (62 L6003) from Kourou — the first major Sentinel launch on Ariane 6 (alongside Sentinel-4 which launched July 2025 on a Falcon 9). Sun-synchronous orbit, altitude **823–848 km**, **local crossing time 09:30 descending node** (morning orbit — see notes). **Currently in commissioning phase** as of May 2026 — other onboard instruments have produced first light (MWS, RO end-Aug 2025; 3MI 28 Aug 2025; IASI-NG 30 Sept 2025); UVNS specific first-light status not yet publicly confirmed at time of writing. |
| Status for this project (IMPORTANT) | **Not yet operationally producing data.** Sentinel-5A UVNS is in commissioning. Expected operational data release: **mid-to-late 2026**, possibly slipping to early 2027 — typical commissioning duration for atmospheric composition instruments is 6–12 months. **Until operational, treat this entry as a placeholder** for pipeline architecture planning, not as an active data source. Monitor EUMETSAT announcements (<https://www.eumetsat.int/sentinel-5>) for first product release. |
| Products planned | UVNS will measure the same product suite as TROPOMI **plus glyoxal (CHOCHO) and an explicit UV Index product**: **O₃** (total column + tropospheric + profile), **NO₂**, **SO₂**, **HCHO** (formaldehyde), **CHOCHO** (glyoxal — NEW vs TROPOMI), **CO**, **CH₄**, **aerosol index (UVAI)**, **aerosol layer height (ALH)**, **UV index** (explicit product). The instrument can also be processed for **BrO**, **CO₂**, **OClO**, **H₂O**, **O₂**, **O₄** (per the WMO OSCAR list), although operational L2 products for those are not committed yet. |
| Current collection / baseline | **Pre-operational** — commissioning data only. First operational baseline (Cal/Val 1) expected with the first L2 product releases in 2026–2027. Algorithm baselines inherit heavily from TROPOMI heritage (most algorithm leads — KNMI for NO₂/CO/AAI/ALH, DLR/BIRA for SO₂/HCHO/O₃ — are continuing into Sentinel-5). |
| Processing level | **L0** (instrument source packets), **L1B** (geolocated calibrated radiances/reflectance), **L2** (geophysical retrievals). For this project, L1B reflectance is potential GRASP synergy input; L2 trace-gas columns feed FLEXPART/HYSPLIT/KG (same routing logic as TROPOMI). |
| File format | **NetCDF4 (CF-compliant)**, expected to follow EUMETSAT EPS-SG conventions — broadly similar to the TROPOMI structure (`/PRODUCT/`, `/PRODUCT/SUPPORT_DATA/`, `/METADATA/` groups) but with EPS-SG-specific metadata. Exact schema will be confirmed when operational products are released. |
| Filename pattern | Expected to follow the EPS-SG convention: `W_xx-eumetsat-darmstadt,SAT,SGA1+UVNS_C_EUMP_<TIMESTAMP>_S<SENSING>_E<SENSING>_<PROD>.nc` — exact pattern to be confirmed at first operational release. Likely timeliness suffixes: NRT (<3 h via direct readout), NTC (~24–48 h via global dump). |
| Resolution | **7 × 7 km² at nadir** (per ESA / EUMETSAT mission documentation). **This is coarser than TROPOMI's 5.5 × 3.5 km²** in pixel area (49 km² vs ~19 km²), which is a counterintuitive design choice — but the **7 × 7 spatial sampling is across the full swath**, whereas TROPOMI's finer along-track sampling degrades toward swath edges. The trade was operational reliability + uniformity across swath vs peak resolution at nadir. For Cluj at ~46.8°N, ~30° off the morning-orbit groundtrack centre, expect pixels of roughly 7 × 8–9 km². |
| Swath / coverage | Wide swath, similar to TROPOMI — daily global coverage. Exact swath width depends on operational mode and is not yet finalised in public documentation; the EPS-SG nominal scenario gives global coverage in one day. |
| Cluj coverage | **One usable daytime overpass per day at approximately 09:00–10:00 local time** — distinctly earlier than TROPOMI's ~12:00 local. **This is the key complementarity:** combined with TROPOMI (afternoon), Sentinel-5 (morning) gives **two atmospheric-composition snapshots per day over Cluj** with a ~3-hour gap, enabling tracking of morning rush-hour vs midday photochemistry buildup for NO₂, and morning vs afternoon plume-evolution for AOD events. |
| NRT availability | **Operational NRT planned at <3 hours** (same target as TROPOMI), with NTC at 24–48 h. Direct readout to receiving stations enables the NRT path; global storage dump enables the NTC. Operational timeliness contracts to be confirmed at commissioning completion. |
| Authentication | **EUMETSAT EO Portal / Data Store account** (free) — same auth path as for SLSTR SL_2_AOD. Sentinel-5 data is expected to be primarily distributed via EUMETSAT Data Store + EUMETCast, **with mirroring to CDSE** for European Copernicus users. |
| Programmatic access | YES (planned) — EUMETSAT Data Store API + EUMDAC Python library (same toolchain as SLSTR SL_2_AOD), plus EUMETCast direct broadcast for institutional users. CDSE mirror also planned. Exact API collection IDs (`EO:EUM:DAT:METOP:...`) to be assigned at operational release. |
| Layer destination (planned, mirroring TROPOMI) | **L2:** GRASP (UVNS L1B reflectance — secondary to OLCI); FLEXPART (NO₂, SO₂, CO as emission tracers; ALH for vertical constraint); HYSPLIT (column gases + UVAI as transport context). **L3:** Knowledge Graph (NO₂, SO₂, CO, O₃, UVAI, UV index for air-quality dashboard layers — morning + TROPOMI afternoon gives twice-daily KG refresh). |

### References

**Instrument design / mission reference:**
- Irizar, J., Melf, M., Bartsch, P., Koehler, J., Weiss, S., Greinacher, R., Erdmann, M., Kirschner, V., Perez Albinana, A., & Martin, D. (2019). Sentinel-5/UVNS. *Proc. SPIE 11180, International Conference on Space Optics — ICSO 2018*, 1118004. DOI: [10.1117/12.2535923](https://doi.org/10.1117/12.2535923)

**Predecessor algorithm references** (the Sentinel-5 retrieval algorithms inherit from TROPOMI heritage — cite these until Sentinel-5-specific ATBDs are finalised post-commissioning):
- See TROPOMI references in the previous file (`dataset_metadata_sentinel5p_tropomi.md`): Veefkind 2012 (mission), van Geffen 2022 (NO₂), Theys 2017 (SO₂), Borsdorff 2018 (CO), Garane 2019 (O₃), Stein Zweers 2024 (UVAI), Nanda 2020 (ALH).

**Sentinel-5 official documentation (active during commissioning):**
- ESA Sentinel-5 mission page: <https://sentinel.esa.int/web/sentinel/missions/sentinel-5>
- EUMETSAT EPS-SG Sentinel-5 page: <https://www.eumetsat.int/sentinel-5>
- EUMETSAT UVNS L1B Data Guide (in development): <https://user.eumetsat.int/resources/user-guides/metop-sg-sentinel-5-uvns-l1b-data-guide>
- Copernicus Atmosphere Monitoring Service (downstream user): <https://atmosphere.copernicus.eu/>
- CEOS database mission summary: <https://database.eohandbook.com/database/missionsummary.aspx?missionID=641>

**Citation format** (once operational): *"Contains modified Copernicus Sentinel-5 data [YEAR], processed by EUMETSAT"* — note the **"processed by EUMETSAT"** attribution, distinguishing from TROPOMI's "processed by ESA/KNMI/DLR".

### Host / Server (planned)

- **EUMETSAT Data Store** (primary path): <https://data.eumetsat.int/>
- **EUMETCast** (real-time push, for institutional users with DVB-S receivers or NREN multicast): <https://www.eumetsat.int/eumetcast>
- **Copernicus Data Space Ecosystem mirror** (planned): <https://dataspace.copernicus.eu/>
- **EUMDAC Python library:** <https://gitlab.eumetsat.int/eumetlab/data-services/eumdac>
- **API key generation:** <https://api.eumetsat.int/api-key/>
- **Sentinel-5 Mission Status (commissioning):** <https://sentinel.esa.int/web/sentinel/missions/sentinel-5> (check periodically for first-data-release announcements)

### Programmatic download (template — will be confirmed at operational release)

**Once operational, expected pattern (using EUMDAC, same as SL_2_AOD):**

```python
import eumdac
import os
from datetime import datetime, timedelta, timezone

token = eumdac.AccessToken((os.environ["EUMETSAT_KEY"],
                            os.environ["EUMETSAT_SECRET"]))
datastore = eumdac.DataStore(token)

# Collection IDs to be confirmed — placeholder pattern:
# EO:EUM:DAT:METOP-SG:S5-L2__NO2___
# EO:EUM:DAT:METOP-SG:S5-L2__SO2___
# EO:EUM:DAT:METOP-SG:S5-L2__CO____
# EO:EUM:DAT:METOP-SG:S5-L2__O3____
# EO:EUM:DAT:METOP-SG:S5-L2__HCHO__
# EO:EUM:DAT:METOP-SG:S5-L2__CHOCHO  (NEW)
# EO:EUM:DAT:METOP-SG:S5-L2__AER_AI_
# EO:EUM:DAT:METOP-SG:S5-L2__AER_LH_
# EO:EUM:DAT:METOP-SG:S5-L2__UV_INDX (NEW explicit product)

# Once collection IDs are public:
# collection = datastore.get_collection("EO:EUM:DAT:METOP-SG:S5-L2__NO2___")
# products = collection.search(
#     bbox=(23.0, 46.3, 24.1, 47.2),
#     dtstart=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
#     dtend=datetime.now(timezone.utc).isoformat(),
# )
```

Code structure should mirror what was developed for SLSTR `SL_2_AOD` (file `dataset_metadata_sentinel3_slstr.md`), since the auth, library, and search patterns are identical EUMETSAT-side flows.

**Reading L2 products (expected pattern, same as TROPOMI):**

```python
import xarray as xr

# Once operational filenames are known:
# ds = xr.open_dataset("S5-OPER-L2__NO2_____*.nc", group="PRODUCT")
# Variables expected to mirror TROPOMI: nitrogendioxide_tropospheric_column, qa_value, etc.
```

### Manual download (interactive web UI)

- **EUMETSAT Data Store browser** (filter by mission = MetOp-SG-A1, once products are published): <https://data.eumetsat.int/>
- **EUMETSAT product navigator** (planned collection entries): <https://navigator.eumetsat.int/>

### Notes / caveats

- **NOT YET OPERATIONAL** (May 2026). MetOp-SG-A1 / Sentinel-5A is **in commissioning**. The satellite is alive and other instruments have produced first light, but UVNS L2 products are not yet publicly distributed. For pipeline architecture planning: treat this as a future source, design the ingest code to be parameterised on instrument-source (TROPOMI / UVNS / UVN — three sources with similar product schemas), and monitor EUMETSAT for the first-data-release announcement (expected H2 2026 to H1 2027). **Until then, the project's "morning-orbit" atmospheric composition data has no direct source** (S5P is the only operational nadir DOAS instrument, and it observes only the afternoon orbit).
- **Resolution surprise — 7 × 7 km coarser than TROPOMI in pixel area.** TROPOMI's 5.5 × 3.5 km² covers ~19 km², Sentinel-5 UVNS's 7 × 7 km² covers 49 km² — a factor of ~2.5 larger. This was a deliberate design trade-off favouring **uniform resolution across the full swath + operational signal-to-noise + multi-decade mission stability** over peak-resolution-at-nadir. The functional consequence for Cluj: **somewhat coarser local detail than TROPOMI**. The Cluj urban area (~80 km²) fits in roughly 2 UVNS pixels, comparable to ~4 TROPOMI pixels. For city-scale gradients (urban core vs suburban background) this is on the edge of resolving — expect to see Cluj as a "hot pixel" rather than a multi-pixel structure.
- **Morning orbit (09:30 LTDN) — this is the project win.** Where Sentinel-5 UVNS shines vs TROPOMI: it's a **morning orbit (~09:00–10:00 local at Cluj)** versus TROPOMI's **afternoon (~12:00–13:00 local)**. Combined, you get two atmospheric-composition snapshots per day, ~3 hours apart, which lets the project resolve **morning rush-hour NO₂ build-up vs midday photochemistry processing, and detect smoke plumes arriving in the morning that would be ageing or dispersed by TROPOMI's afternoon pass.** This is the main scientific reason to ingest both: not redundancy, but diurnal coverage.
- **New products vs TROPOMI: glyoxal + explicit UV index.** **Glyoxal (CHOCHO)** is a secondary oxidation product of VOCs (especially biogenic isoprene), giving a marker for biogenic + biomass-burning VOC chemistry — useful for source-attribution work even if not central to an aerosol warning chain. **Explicit UV index product** (surface UV irradiance) is a direct health-relevant variable that complements the warning system's broader public-health-context layer.
- **Operational continuity is the key value-add.** Sentinel-5P was a pre-operational research/precursor mission (designed for 7 years; now in extended mission with EOL ~Sept 2027). **Sentinel-5 is operational** — designed as a 20-year programme with three satellite pairs (MetOp-SG-A1, A2, A3 + B partners), launching in succession, guaranteeing continuous data flow through ~2045. For an operational warning chain at a public agency / first-responder client, this multi-decade guarantee matters: you can build infrastructure on Sentinel-5 with confidence that the data feed won't dry up in 2027.
- **EUMETSAT-only distribution** (with CDSE mirror planned). Like SLSTR SL_2_AOD, Sentinel-5 is distributed by EUMETSAT first, with a CDSE mirror layer on top. The project pipeline already has EUMETSAT credentials from the SLSTR ingest path — reuse the same auth + EUMDAC library. **No new credential rotation needed.**
- **Algorithm continuity.** Most TROPOMI algorithm leads (KNMI for NO₂/CO/AAI/ALH, DLR/BIRA for SO₂/HCHO/O₃) are continuing into the Sentinel-5 era. The L2 retrieval algorithms are direct heritage of TROPOMI ones with operational-readiness improvements. **Until Sentinel-5-specific ATBDs are released (post-commissioning), continue to cite the TROPOMI algorithm papers** (see previous file references).
- **Companion B-type satellite coming.** MetOp-SG-B1 — which carries the scatterometer (SCA), microwave imager (MWI), ice-cloud imager (ICI), and second radio occultation sounder — is scheduled for launch in **2026** to complete the first MetOp-SG pair. **B-type does not carry UVNS**, so it's not directly relevant to this project; mentioned only for the user's awareness of the broader MetOp-SG architecture.
- **Don't confuse Sentinel-5 with Sentinel-5P.** Despite the name, **Sentinel-5 is the operational successor**, not the same satellite. Sentinel-5P ("P" for Precursor) was a pre-operational research mission. The two will fly simultaneously through ~Sept 2027 (S5P EOL), giving a roughly 1–2 year inter-calibration overlap window — valuable for the project's data validation but not affecting the operational warning chain.
- **EU citation policy** (once operational): *"Contains modified Copernicus Sentinel-5 data [YEAR], processed by EUMETSAT"*. Use the Irizar 2019 SPIE paper for the instrument citation until peer-reviewed mission overview papers post-commissioning are published.

---
