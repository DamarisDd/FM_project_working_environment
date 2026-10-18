# Dataset metadata — FCI on MTG-I1 / Meteosat-12

Companion documentation to the Stage 1 input-data table.
This file describes the **Flexible Combined Imager (FCI)** products on
**MTG-I1 (Meteosat-12)** — the modern geostationary imaging successor to
SEVIRI, operational since December 2024.

This entry is a **new row added to the input table** following the user
recommendation in the SEVIRI file. FCI is to be ingested as the **primary
geostationary imaging source**; the SEVIRI entry remains as a parallel
backup/legacy time-series source (see SEVIRI file `dataset_metadata_seviri.md`).

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 14. FCI — Meteosat Third Generation Imager 1 (Meteosat-12)

### Summary

| Field | Value |
|---|---|
| Instrument | **FCI** (Flexible Combined Imager) — pushbroom optical/IR imager on the 3-axis-stabilised MTG-I platform (a fundamental architectural change from SEVIRI's spin-stabilised geometry). **16 spectral channels** total: **8 solar bands** (0.4–2.2 µm) at **1 km spatial sampling at nadir** + **8 thermal bands** (3.8–13.3 µm) at **2 km spatial sampling at nadir**. Additionally, an **HRFI mode** (High Resolution Fast Imagery) delivers **4 selected channels at 500 m solar / 1 km thermal** spatial sampling. The IR 3.8 µm channel has an extended dynamic range dedicated to fire monitoring (up to ~900 K). Built by **Thales Alenia Space** under ESA contract as the MTG prime. |
| Network / Agency | **EUMETSAT** (operates the satellite + ground segment + distributes data) + **ESA** (developed MTG + FCI under contract). MTG is a 6-satellite programme: 4 MTG-I imager satellites + 2 MTG-S sounder satellites, ensuring continuity through ~2045. |
| Platform (May 2026) | **MTG-I1**, officially designated **Meteosat-12** since 4 December 2024 when L1 data was declared operational. Launched **13 December 2022 at 20:30 UTC** on an **Ariane 5** from Kourou. **Geostationary orbit at 0° longitude**, altitude ~35,786 km. **Nominal lifetime 8.5 years; fuel for 10.7+ years.** First of the MTG-I series; MTG-I2 expected launch 2026, MTG-I3 and MTG-I4 to follow. **3-axis stabilised** (vs SEVIRI's spinning platform), which is the key architectural change enabling the higher spatial resolution and faster scan times. |
| Status | **OPERATIONAL** — L1 data declared operational on **4 December 2024**, MTG-I1 officially renamed Meteosat-12 at the same time. This is one of only a few entries in the entire input table that is fully operational AND already producing routinely-distributable L1 data, alongside SEVIRI, TROPOMI, MODIS, VIIRS, OLCI, etc. **A commissioning anomaly is known and disclosed** (see Notes/caveats below) but does not affect end-user data quality. |
| HRFI channels (the 500 m / 1 km set) | **4 channels**: **VIS 0.64 µm** (red, 500 m), **NIR 2.25 µm** (SWIR cloud/aerosol, 500 m), **IR 3.8 µm** (fire detection with extended dynamic range, 1 km), **IR 10.5 µm** (cloud top temperature, 1 km). These four channels are sufficient for many real-time nowcasting applications (cloud + fire detection at sub-km resolution over Europe) and are the basis of the most operationally-useful FCI fast-imagery products. |
| Full 16-channel set (FDHSI — Full Disc High Spectral Imagery) | **Solar bands** (1 km at nadir): VIS 0.44 µm (blue, NEW vs SEVIRI), VIS 0.51 µm (green, NEW), VIS 0.64 µm (red), VIS 0.86 µm (NIR vegetation), NIR 0.91 µm (water vapour, NEW), NIR 1.38 µm (cirrus + high-altitude aerosol, NEW), NIR 1.61 µm (cloud phase), NIR 2.25 µm (cloud phase/aerosol). **Thermal bands** (2 km at nadir): IR 3.8 µm (fire), WV 6.3 µm (water vapour), WV 7.35 µm (water vapour), IR 8.7 µm (cloud phase), IR 9.66 µm (ozone), IR 10.5 µm (window/cloud top), IR 12.3 µm (window), IR 13.3 µm (CO₂). The four **NEW** channels relative to SEVIRI (VIS 0.44, VIS 0.51, NIR 0.91, NIR 1.38) significantly enhance aerosol and cloud microphysics retrieval capability. |
| Resolution at Cluj | **Standard FDHSI**: ~1.7 × 1.7 km² for solar bands, ~3.4 × 3.4 km² for thermal bands (off-nadir at 46.8°N latitude scales pixel by ~1.7×). **HRFI**: ~0.85 × 0.85 km² for VIS 0.64 + NIR 2.25; ~1.7 × 1.7 km² for IR 3.8 + IR 10.5. **The Cluj urban area is resolved by ~30–50 HRFI pixels in the visible**, a qualitative leap from SEVIRI's ~1-pixel "smudge". |
| Coverage | **Europe + Africa + Atlantic + Middle East + Indian Ocean rim** (full disc from 0° longitude). Cluj is well within both Full Disc and RSS Europe-only coverage. **The Q4 RSS mode covers Europe + Mediterranean + N. Africa** in 2.5 minutes. |
| Revisit / temporal resolution | **FDSS (Full Disc Scanning Service): 10 minutes** (the primary cadence — vs 15 min for SEVIRI). **RSS (Rapid Scanning Service via HRFI mode): 2.5 minutes over Europe** (vs 5 min for SEVIRI RSS). The 2.5-minute RSS is **the highest-cadence Earth observation in the entire input table** by an order of magnitude over the LEO satellites. |
| Processing level | **L1c** is the standard distributed product — calibrated, geolocated, rectified radiances on a regular reference grid in NetCDF4. L2 products in development at EUMETSAT Central Facility: **Optimal Cloud Analysis (OCA)**, atmospheric instability, fire detection, atmospheric motion vectors (AMV), all-sky radiances. L2 products are being released progressively post-commissioning. |
| File format | **NetCDF4 (CF-compliant)** — major improvement over SEVIRI's proprietary HRIT / .nat formats. Each repeat cycle is split into a series of **body chunks + 1 trailer chunk** (~70 body chunks per Full Disc nominal; chunk count varies). Each body chunk = one strip ~278 rows × 11136 columns (1 km grid) or 22272 columns (500 m HRFI grid). The trailer chunk contains end-of-cycle quality/metadata. |
| Filename pattern | `W_xx-eumetsat-darmstadt,IMG+SAT,MTI1+FCI-1C-RRAD-<MODE>-<BODY/TRAIL>-<CHANNEL_OR_ALL>-<RES>-<CHK_INDEX>_C_EUMT_<TIMESTAMP>_<INST_TIMESTAMPS>_<TYPE>.nc`. Modes are `FDHSI` (full disc high spectral, 1 km), `HRFI` (full disc high spatial, 500 m), `Q4HRFI` (RSS over Europe Q4 quadrant in HRFI mode), `AF` (Africa-only dissemination mode). |
| Cluj coverage cadence | **FDSS: 144 observations per day** (10-min full disc). **RSS Q4: 576 observations per day** (2.5-min Europe). **Day and night both** (IR channels work at night). The 2.5-minute RSS over Europe is the **single highest-cadence atmospheric observation** in the entire warning chain. |
| NRT availability | **YES — sub-minute latency on EUMETCast**; few-minute latency on EUMETSAT Data Store. Effectively real-time for any practical warning-chain application. |
| Authentication | **EUMETSAT EO Portal / Data Store account** (free) — **same auth path as SEVIRI, SLSTR, Sentinel-5 UVNS, Sentinel-4 UVN**. No new credentials needed; reuse the existing EUMETSAT EUMDAC client. EUMETCast direct broadcast requires institutional DVB-S hardware (separate). |
| Programmatic access | YES — **EUMETSAT Data Store API + EUMDAC** Python library (same toolchain). For Python-based L1c parsing + RGB compositing + reprojection, the canonical tool is **`satpy`** (PyTroll) with reader `fci_l1c_nc` — handles FDHSI, HRFI, RSS (Q4), and AF modes. |
| Layer destination | **L2:** FLEXPART (fire pixel detection + dust/ash flag from new channel combinations as emission tracer inputs); HYSPLIT (dust/ash/smoke overlay for trajectory visualisations). GRASP: limited intersection (GRASP is more naturally tied to Sentinel-4 UVN AOD/BRDF; FCI L1c can in principle be used as a GRASP synergy input, but no operational pipeline exists). **L3:** Knowledge Graph (**Dust RGB, True-Colour RGB, Fire Temperature RGB at 2.5-min refresh** — this is the highest-cadence visual layer in the entire warning chain GUI; primary background imagery for the operational dashboard). |

### References

**Primary mission reference:**
- Holmlund, K., Grandell, J., Schmetz, J., Stuhlmann, R., Bojkov, B., Munro, R., Lekouara, M., Coppens, D., Viticchie, B., August, T., Theodore, B., Watts, P., Dobber, M., Fowler, G., Bojinski, S., Schmid, A., Salonen, K., Tjemkes, S., Aminou, D., & Blythe, P. (2021). Meteosat Third Generation (MTG): Continuation and innovation of observations from geostationary orbit. *Bulletin of the American Meteorological Society*, 102(5), E990–E1015. DOI: [10.1175/BAMS-D-19-0304.1](https://doi.org/10.1175/BAMS-D-19-0304.1)

**Calibration anomaly + vicarious calibration workaround:**
- Mousivand, A., Wagner, S., Debaecker, V., Shandhag, R., Burini, A., Hewison, T., & Lekouara, M. (2025). In-Flight Calibration of Geostationary Meteorological Imagers Using Alternative Methods: MTG-I1 FCI Case Study. *Remote Sensing*, 17(14), 2369. DOI: [10.3390/rs17142369](https://doi.org/10.3390/rs17142369)
- Mousivand et al. (2024). Monitoring radiometric performance of EUMETSAT operational missions: MSG/SEVIRI, MTG-I/FCI, and Sentinel-3/OLCI&SLSTR. *Proc. SPIE 13143, Earth Observing Systems XXIX*, 131430X. DOI: [10.1117/12.3028195](https://doi.org/10.1117/12.3028195) (conference proceedings, supplementary).

**RGB composite recipes (EUMETSAT operational guides — many are extensions of SEVIRI recipes with new FCI channels added):**
- EUMETSAT Best Practices for RGB Compositing series at <https://resources.eumetrain.org/>
- **Fire Temperature RGB** — new for FCI, exploits IR 3.8 µm extended dynamic range + NIR channels for high-confidence fire detection (relevant for upstream biomass-burning detection feeding into the smoke component of the warning chain).
- **True-Colour RGB** — native to FCI via VIS 0.44 + 0.51 + 0.64 (not possible with SEVIRI's single broadband HRV channel).

**EUMETSAT documentation:**
- FCI L1c Data Guide: <https://user.eumetsat.int/resources/user-guides/mtg-fci-level-1c-data-guide>
- FCI L1 Product User Guide (PUG): <https://user.eumetsat.int/s3/eup-strapi-media/pdf_mtg_fci_l1_pug_8235cb71d9.pdf>
- FCI instrument overview: <https://www.eumetsat.int/mtg-flexible-combined-imager-fci>
- MTG mission overview: <https://www.eumetsat.int/mtg>

**Citation format:** *"Source: EUMETSAT"* or *"Meteosat data © EUMETSAT [YEAR]"*. EUMETSAT data are openly available for non-commercial use under the EUMETSAT data policy.

### Host / Server

- **EUMETSAT Data Store** (primary): <https://data.eumetsat.int/>
- **EUMETCast** (live broadcast, sub-minute latency): <https://www.eumetsat.int/eumetcast>
- **EUMETSAT Product Navigator** (find collection IDs): <https://navigator.eumetsat.int/>
- **EUMDAC Python library:** <https://gitlab.eumetsat.int/eumetlab/data-services/eumdac>
- **satpy (Python toolkit for FCI L1c processing + RGB compositing):** <https://satpy.readthedocs.io/>

**Key Data Store collection IDs** (confirmed from EUMETSAT Data Store, May 2026):
- **`EO:EUM:DAT:0665`** — FCI L1c High Resolution Image Data (HRFI), Full Disc, 0° service
- **`EO:EUM:DAT:0662`** — FCI L1c Image Data (FDHSI, all 16 channels), Full Disc — verify ID against the live Data Store catalog before locking pipeline code
- **`EO:EUM:DAT:MTG:FCI-1C-RRAD-Q4`** — pattern for Q4 RSS mode (Europe rapid scan) — verify collection ID in the Product Navigator; the public catalog ID may differ
- Africa Dissemination mode collections — for users of the EUMETCast Africa service

**Always validate collection IDs against the current Product Navigator** before hard-coding into pipeline scripts — EUMETSAT periodically reorganises the catalogue.

### Programmatic download

**EUMDAC pattern (identical auth flow to SEVIRI, SLSTR, Sentinel-5 UVNS, Sentinel-4 UVN):**

```python
import eumdac
import os
from datetime import datetime, timedelta, timezone

token = eumdac.AccessToken((os.environ["EUMETSAT_KEY"],
                            os.environ["EUMETSAT_SECRET"]))
datastore = eumdac.DataStore(token)

# HRFI Full Disc (500m visible/NIR, 1km IR)
collection_hrfi = datastore.get_collection("EO:EUM:DAT:0665")

# Pull last full repeat cycle (~10 min for FDSS, ~2.5 min for Q4 RSS) covering Cluj
# Note: FCI files are body+trailer chunks — typically all chunks for a cycle are needed
# for the full disc image; for a Cluj subset, only chunks covering Cluj's latitude band
# are strictly necessary, but easiest is to download all chunks for a single repeat cycle.
now = datetime.now(timezone.utc)
products = collection_hrfi.search(
    dtstart=(now - timedelta(minutes=15)).isoformat(),
    dtend=now.isoformat(),
)

for p in products:
    print(p, p.sensing_start, p.sensing_end)
    # Each "product" entry in the Data Store typically returns a complete repeat cycle
    # (~70 body chunks + 1 trailer chunk for Full Disc HRFI = ~700 MB compressed)
    with p.open() as src, open(f"{p}.zip", "wb") as dst:
        dst.write(src.read())
```

**Processing a downloaded FCI L1c repeat cycle into True Colour RGB with satpy:**

```bash
pip install satpy
```

```python
from satpy import Scene
from glob import glob

# Unzip the downloaded archive first; you get a directory of body chunk .nc files
# and a trailer .nc file
files = sorted(glob("/path/to/repeat_cycle_dir/*BODY*.nc")) + \
        glob("/path/to/repeat_cycle_dir/*TRAIL*.nc")

scn = Scene(reader="fci_l1c_nc", filenames=files)
scn.load(["true_color"])    # native true-colour RGB recipe using VIS 0.44 + 0.51 + 0.64

# Resample to a local Cluj-centred area definition
from pyresample import create_area_def
cluj_area = create_area_def(
    "cluj_area",
    {"proj": "stere", "lat_0": 46.77, "lon_0": 23.55, "ellps": "WGS84"},
    width=600, height=600,
    area_extent=(-150e3, -150e3, 150e3, 150e3),   # ±150 km around Cluj
)
local = scn.resample(cluj_area)
local.save_dataset("true_color", filename="cluj_fci_truecolor.png")

# Other useful composites:
# scn.load(["dust", "ash", "fire_temperature", "natural_color", "night_microphysics"])
```

**For the Q4 RSS rapid scan**, swap reader filenames to `*_Q4HRFI*` files; the satpy reader auto-detects mode from filename. Cadence is then 2.5 minutes per cycle.

**EUMETCast direct broadcast** (institutional users only): same setup as for SEVIRI (DVB-S hardware + EUMETCast subscription). Beyond the scope of a research-institute pipeline; Data Store API is sufficient for sub-5-minute latency.

### Manual download (interactive web UI)

- **EUMETSAT Data Store search:** <https://data.eumetsat.int/> → filter Mission = "Meteosat Third Generation" → Sensor = "FCI"
- **EUMETView** (live browse of FCI imagery): <https://view.eumetsat.int/> — single-channel and basic-RGB visualisations updated in near-real-time
- **NWC SAF / NWCSAF Geo software** (offline RGB + nowcasting products generation from L1c data; FCI support added 2024): <https://www.nwcsaf.org/>

### Notes / caveats

- **Operational since 4 December 2024.** MTG-I1 was renamed Meteosat-12 on that date when L1c data was declared operational. This is one of the most mature data sources in the warning chain (alongside SEVIRI, TROPOMI, MODIS, VIIRS, OLCI). Routine production has been running for ~17 months as of May 2026, so the data quality and operational reliability are well established.
- **2.5-minute Europe RSS cadence is the project's single fastest-refresh data source.** No other entry in the input table comes close. For comparison: Sentinel-4 UVN (hourly), SEVIRI RSS (5 min), AERONET (15 min — but ground point-data, not imagery), ceilometer (continuous but vertical 1D). The 2.5-minute FCI Q4 mode is what makes high-cadence visual tracking of evolving plumes possible at city scale over Cluj.
- **The COM anomaly (full transparency disclosure).** On 13 January 2024, during commissioning, the Calibration and Obturation Mechanism (COM) experienced a critical failure. The COM is used for in-flight radiometric calibration via an onboard reference target. EUMETSAT's response: **(1)** Permanently disable use of the COM to preserve operational instrument safety, and **(2)** Implement a vicarious calibration approach called **MICMICS** (Multi-Mission Solution for Level-1 Radiometric Calibration Monitoring) which uses inter-comparison with collocated observations from other satellite missions (S3/OLCI, S3/SLSTR, MSG/SEVIRI). The result: L1c data quality and stability are operationally acceptable, but recovery from any future calibration outage (e.g. decontamination event) takes **~12 hours of accumulated inter-comparison data** to re-converge gains — vs near-instant recovery from a working onboard calibrator. **For end users: this is invisible at the L1c level.** L1c data is delivered with full quality metadata. The user does not need to handle MICMICS internals. Mentioning the anomaly here only because it is publicly documented in peer-reviewed literature (Mousivand 2024/2025) and would be discoverable by external reviewers of the project deliverable.
- **Continuity through ~2045.** The MTG programme is designed for **20+ years of operations** via successive satellite launches: **MTG-I1 (this satellite, 2022)** → **MTG-I2 (expected 2026)** → **MTG-I3** → **MTG-I4**. Each MTG-I has 8.5-year nominal life with fuel for ~10.7+ years. By the time MTG-I4 reaches end-of-life in the late 2030s/early 2040s, the EUMETSAT next-generation programme will be active. **From an infrastructure-planning perspective for the warning chain, FCI is a multi-decade commitment** — safe to design around.
- **NetCDF4 vs HRIT/.nat.** A practical workflow improvement: **FCI L1c is NetCDF4**, easily parsed by `xarray.open_dataset()` for simple field extraction or by `satpy` for full RGB pipelines. **SEVIRI L1.5 is HRIT or .nat**, both proprietary EUMETSAT formats requiring specialised libraries. **Ingest pipeline complexity drops significantly** when switching primary source from SEVIRI to FCI.
- **Body chunks + trailer chunks.** FCI L1c is not delivered as a single file per repeat cycle — instead, ~70 body chunk files + 1 trailer chunk file per Full Disc cycle (the structure is needed because the on-board data rate is too high to buffer the entire image and downlink it in one chunk). Each chunk is one strip of rows across the entire disc width. `satpy` reads the stack transparently when all chunks for a cycle are present; **make sure to download the entire chunk set + trailer for each repeat cycle**, otherwise satpy reports missing data.
- **HRFI vs FDHSI choice.** **HRFI = 4 channels at 500 m** (visible + NIR + IR), best for visual/RGB applications and fire detection at urban scale. **FDHSI = all 16 channels at 1–2 km**, best for full atmospheric/cloud/aerosol product generation. For the project's GUI background imagery + fire-detection layers, HRFI is the right choice. For aerosol/dust/cloud chemistry overlays, FDHSI is needed. **Probably want to ingest both**, with HRFI driving the GUI background refresh and FDHSI feeding the dust/aerosol RGB overlays.
- **Africa Dissemination (AF) mode.** EUMETSAT distributes a special African subset via EUMETCast Africa (each file = full disc masked to a single channel). Not relevant to Cluj operations, but flagged here because users of the EUMETCast Africa service or African collaborators on the project would receive FCI L1c in this format.
- **GRASP intersection (limited).** Unlike Sentinel-4 UVN — where GRASP Earth is the operational AOD/BRDF retrieval team — there is no comparable operational GRASP role for FCI at present. The FCI L1c radiances could in principle be processed by GRASP, but no operational pipeline currently does this. The project's GRASP layer should treat FCI as an optional/experimental synergy input, not a primary data flow.
- **Aerosol detection enhancements over SEVIRI.** Per EUMETSAT FCI training materials, the four new solar channels (VIS 0.44, VIS 0.51, NIR 0.91, NIR 1.38) enable improved aerosol detection vs SEVIRI:
  - **VIS 0.44** (blue): standard wavelength for aerosol optical depth retrievals (analogous to MODIS Band 3 at 470 nm). First time a Meteosat instrument has a true blue channel.
  - **VIS 0.51** (green): aids true-colour discrimination and aerosol type classification.
  - **NIR 0.91** (water vapour): improves cloud screening + water vapour correction for aerosol retrievals.
  - **NIR 1.38** (cirrus): originally designed for thin cirrus detection but also detects high-altitude aerosols (e.g. volcanic stratospheric plumes, lofted dust). **This is the most important new channel for the project's vertical-distribution awareness.**
- **Native true-colour RGB.** SEVIRI cannot make a real true-colour RGB (its HRV channel is broadband panchromatic). FCI can, using VIS 0.44 + 0.51 + 0.64. For public-facing GUI imagery, this matters: a true-colour view of Cluj and surrounding regions is qualitatively more interpretable for first responders and the general public than the false-colour Natural Colour RGB from SEVIRI.
- **Same auth path as SEVIRI / SLSTR / Sentinel-5 UVNS / Sentinel-4 UVN.** No new EUMETSAT credentials needed for FCI; the existing pipeline EUMETSAT API key works directly. Switching primary geostationary source from SEVIRI to FCI is a 1-day pipeline change: swap collection IDs, swap satpy reader, validate output. The end-to-end warning chain logic stays the same.

---
