# Dataset metadata — ATLID on EarthCARE

Companion documentation to the Stage 1 input-data table.
This file describes the **Atmospheric Lidar (ATLID)** products on the
**EarthCARE** satellite — the closest space-based cousin to the project's
ground-based EARLINET Raman lidar at Cluj (file `dataset_metadata_earlinet_lidar.md`).

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

ATLID is **the only space-based aerosol vertical profile source in the
entire input table.** All other satellite sources are nadir-viewing
column-integrated (total-column AOD, total-column trace gases) or
imagery-based. ATLID provides height-resolved aerosol backscatter,
extinction, and depolarization at the 355 nm wavelength that matches the
Raymetrics lidar at Cluj — making it the natural ground/space
intercomparison node in the warning chain.

---

## 15. ATLID — EarthCARE atmospheric lidar (355 nm HSRL)

### Summary

| Field | Value |
|---|---|
| Instrument | **ATLID** (ATmospheric LIDar) — **High Spectral Resolution Lidar (HSRL)** operating at **354.8 nm** (commonly rounded to 355 nm), the **first space-based HSRL targeting clouds and aerosols with publicly released data.** Single-wavelength ultraviolet lidar with linear depolarization measurement capability. **Three receiver channels**: (1) **Mie co-polarized** (parallel particulate backscatter), (2) **Mie cross-polarized** (depolarization), (3) **Rayleigh** (molecular backscatter — separated from the Mie signal by a Fabry-Pérot etalon, which is the defining HSRL technique). Built by **Airbus DS** (instrument prime) with detector subsystem developed at **Leonardo / former Selex-Galileo** (Florence, Italy). |
| Network / Agency | **ESA + JAXA** joint mission. ESA is responsible for ATLID, MSI (multi-spectral imager), and BBR (broadband radiometer); JAXA provides CPR (cloud profiling radar). EarthCARE is part of ESA's **Earth Explorer programme** — a research/demonstration mission, not an operational meteorology mission. The Copernicus Atmosphere Monitoring Service (CAMS) and the climate research community are key downstream users. |
| Platform | **EarthCARE** (Earth Cloud, Aerosol and Radiation Explorer). Launched **28 May 2024** on a **SpaceX Falcon 9** from **Vandenberg Space Force Base** (California). Sun-synchronous orbit at altitude **~393 km** (low, by LEO standards — chosen for lidar/radar signal strength). **Local crossing time: 14:00 ascending node.** 25-day repeat ground track cycle. **3-year nominal mission lifetime** with possible extensions (typical for Earth Explorers, which often run 5–10+ years past nominal). |
| Status (May 2026) | **OPERATIONAL — public data flowing routinely.** First operational ATLID L2 data covers approximately **September 2024 onwards** (post-commissioning). Data is currently in active reprocessing — ESA has released multiple algorithm baseline versions (AE, AF, AG, BA, BB, BC) throughout 2024–2025 as the L2 processors mature. The "BC" series is the most recent baseline at time of writing. **Important context: a CPR (radar) anomaly occurred 2 May 2026 and was resolved 13 May 2026** — that anomaly affected the radar instrument; ATLID was unaffected, but if the project pipeline ingests L2b synergistic (ATLID+CPR) products, the May 2026 outage window should be flagged. |
| Products (ATLID L2a — single-instrument) | **A-AER** (`ATL_AER_2A`) — aerosol products including aerosol optical depth profile, attenuated backscatter, depolarization ratio at 355 nm. **A-EBD** (`ATL_EBD_2A`) — Extinction, Backscatter, and Depolarization profiles (the most directly comparable to EARLINET ground lidar output). **A-TC** (`ATL_TC_2A`) — Target Classification: feature-by-feature labelling as aerosol, cloud, cloud-and-aerosol mixture, clear sky, surface. **A-ICE** (`ATL_ICE_2A`) — ice cloud microphysics. **A-FM** (`ATL_FM_2A`) — feature mask. **A-CTH** (`ATL_CTH_2A`) — cloud top height. **A-ALD** (`ATL_ALD_2A`) — Aerosol Layer Description (layer-resolved properties). The **A-EBD product is the project-priority deliverable** for the warning chain's vertical-distribution layer. |
| Products (L2b synergistic — multi-instrument) | **AC-TC**, **AC-CLD** (ATLID+CPR), **AM-CLD** (ATLID+MSI), **ACM-CAP** (ATLID+CPR+MSI cloud-aerosol-precipitation), **BMA-FLX** (broadband flux). Synergistic products provide higher-confidence retrievals but **depend on all participating instruments being operational** — sensitivity to the CPR anomaly applies. |
| Resolution | **Vertical: ~100 m** from surface up to 20 km altitude; **~500 m** from 20 km up to 40 km altitude (covering full troposphere + lower-to-mid stratosphere). **Horizontal: ~285 m along-track** sampling distance, with on-board averaging of 2 laser shots from the 51 Hz PRF; **single-shot footprint <30 m** on the ground from the 393 km altitude. **3° off-nadir pointing** (offset to avoid specular reflections from horizontally-oriented ice cloud surfaces that would saturate detectors). |
| Coverage geometry | **Narrow nadir-like curtain** — ATLID samples a single point-trail along the satellite ground track, NOT a swath. This is fundamentally different from MODIS / OLCI / FCI / TROPOMI which all observe wide swaths. **An ATLID measurement is a curtain (along-track vertical slice), not an image.** This shapes how the project ingests the data: each ATLID file represents one orbit's worth of curtain measurements, with the user picking the segment where the ground track passes near Cluj. |
| Cluj overpass cadence | EarthCARE has a 25-day repeat ground track, so an exact ATLID overpass directly over Cluj happens **roughly once per 25 days**. However, the ATLID curtain is narrow (~30 m footprint), so "near-Cluj overpasses within X km" are more frequent — for a 100 km radius around Cluj, expect **a few overpasses per week**; for a 200 km radius, daily-to-near-daily. The project's pipeline should ingest ATLID data within a generous radius (e.g. ±200 km of Cluj) and let the warning chain decide whether a particular curtain is close enough for the use case. |
| Day + night | **YES — both daytime and nighttime overpasses** (some at ~14:00 local ascending, some at ~02:00 local descending). Night overpasses have lower solar background noise → typically cleaner aerosol profiles, particularly above the boundary layer. |
| NRT availability | **NRT (Near Real Time)**: ESA distributes ATLID L1B within hours of acquisition through the EarthCARE Online Dissemination Service. L2 products typically follow within 24 hours. **Not as fast as the geostationary imagers** (sub-minute for FCI/SEVIRI), but adequate for the warning chain's vertical-distribution layer which doesn't need real-time refresh anyway. |
| Processing level | **L0** (annotated raw instrument source packets, restricted), **L1B** (calibrated geolocated radiances/backscatter — public), **L2a** (single-instrument geophysical products — public), **L2b** (synergistic multi-instrument products — public), **L1D** (Joint Standard Grid co-locating all 4 instruments with ECMWF meteorology — useful for downstream synergy work). |
| File format | **NetCDF4 (CF-compliant)** with the ESA Earth Explorer file naming convention. Each L1B/L2 product is a single NetCDF file per orbit segment (~1 orbit = ~1.5 hours = one file). |
| Filename pattern | `ECA_EXAA_<PRODUCT-TYPE>__<VERSION>_<SENSING_START>_<SENSING_END>_<ORBIT>_<FRAME>.h5` (ATLID products use `.h5` extension in some baselines, `.nc` in others — both are netCDF4 with HDF5 backing). For example: `ECA_EXAA_ATL_EBD_2A_20260301T120000Z_20260301T133000Z_05432A_E_BC.nc`. |
| Authentication | **ESA EO Sign In** account (free, separate from EUMETSAT credentials used elsewhere in the project). **This is a NEW credential path** for the pipeline — not the EUMETSAT EO Portal account that handles SEVIRI/FCI/SLSTR/Sentinel-5/Sentinel-4. Account setup is straightforward (institutional email + email verification). |
| Programmatic access | YES — via **ESA Earth Online Dissemination Service** (OData + HTTP), via the **MAAP STAC catalogue** with API access tokens, and via **FTP** for bulk downloads. Python: the `ectools` library by Shannon Mason (ECMWF), or generic `xarray.open_dataset()` on the NetCDF files directly. |
| Layer destination | **L2:** FLEXPART (aerosol layer height + extinction profiles as vertical constraint for emission source attribution); HYSPLIT (layer-resolved attribution for back-trajectories — much richer than the column-AOD-only signal from TROPOMI/MODIS); **L2 synergy with GRASP**: ATLID L1B can in principle be ingested as a vertical-profile constraint for GRASP retrievals, though this is research-level integration, not operational. **L3:** Knowledge Graph (ATLID vertical curtains visualised as "atmospheric slices" — periodic but high-information-content overlays showing the actual stratification of aerosol layers above Cluj when EarthCARE passes overhead). |

### Why ATLID matters for the project specifically

ATLID and the Cluj EARLINET Raman lidar are **the most physically similar instruments in the entire input table**:

| Property | EARLINET at Cluj (CLOP) | **ATLID on EarthCARE** |
|---|---|---|
| Wavelength (aerosol) | 355 nm elastic + 387 nm Raman + 532 nm elastic + 607 nm Raman + 1064 nm elastic | **355 nm (only)** |
| Depolarization channels | 355 nm + 532 nm | **355 nm** |
| Extinction retrieval method | Raman inversion at 355 + 532 | **HSRL inversion at 355** (independent of lidar-ratio assumption) |
| Vertical resolution | ~7.5 m raw, gridded to ~30–100 m | **~100 m (0–20 km), ~500 m (20–40 km)** |
| Geometric viewing | Vertical / zenith-pointing fixed | **3° off-nadir, moving (~7 km/s ground speed)** |
| Daytime operation | Limited (Raman channels SNR-impacted) | **YES (HSRL works day and night)** |
| Spatial domain | Single ground site (Cluj) | **Global, along-track curtain** |
| Temporal cadence | On-demand campaigns (~weekly typical) | **Cluj-area overpass every few days** |
| Data latency | Hours-to-days (manual processing via SCC) | **Hours (NRT L1B), 24h (L2)** |
| Mission lifetime | Indefinite (ground station) | **3-year nominal, likely extensions** |

The combination is naturally synergistic:
1. **Direct ground-truth validation of ATLID:** Cluj is one of the EARLINET stations capable of providing the multi-wavelength + Raman reference profiles that ATLID L2 retrievals are validated against. TROPOS (which operates the PollyXT mobile lidars used for cal/val) is one of the lead validators. **The Cluj station can be a contributing validation site, which is a project-publication opportunity.**
2. **Cross-platform aerosol typing:** EARLINET's multi-wavelength capability (Ångström exponent from 355 / 532 / 1064; lidar ratio at multiple wavelengths) gives stronger aerosol-type discrimination than ATLID alone. Combined ATLID + EARLINET intercepts during overpass windows give the best-of-both: vertical coverage (ATLID, globally) plus rich spectral typing (EARLINET, at the ground site).
3. **Spatial context for ground observations:** EARLINET sees aerosols above Cluj vertically; ATLID extends the picture along the orbit track, showing the spatial extent of layers (e.g. is the Saharan dust event observed at Cluj a local enhancement or part of a continental-scale layer extending hundreds of kilometres?).
4. **355 nm depolarization is the shared anchor:** both instruments measure depolarization at 355 nm, and depolarization at this UV wavelength is particularly sensitive to non-spherical particles (dust, ice). **This is the cleanest possible direct comparison signal** between the two systems.

### References

**Mission overview paper:**
- Eisinger, M., Marnas, F., Wallace, K., Kubota, T., Tomiyama, N., Ohno, Y., Tanaka, T., Tomita, E., Wehr, T., & Bernaerts, D. (2024). The EarthCARE mission: science data processing chain overview. *Atmospheric Measurement Techniques*, 17, 839–862. DOI: [10.5194/amt-17-839-2024](https://doi.org/10.5194/amt-17-839-2024)
- Wehr, T., Kubota, T., Tzeremes, G., Wallace, K., Nakatsuka, H., Ohno, Y., Koopman, R., Rommen, B., Donovan, D., et al. (2023). The EarthCARE Mission – Science and System Overview. *Atmospheric Measurement Techniques*, 16, 3581–3608. DOI: [10.5194/amt-16-3581-2023](https://doi.org/10.5194/amt-16-3581-2023)

**ATLID algorithm reference (A-PRO processor):**
- Donovan, D. P., van Zadelhoff, G.-J., & Wang, P. (2024). The EarthCARE lidar cloud and aerosol profile processor (A-PRO): the A-AER, A-EBD, A-TC and A-ICE products. *Atmospheric Measurement Techniques* (discussion paper, published 2024). See <https://amt.copernicus.org/> for the latest published version.

**JAXA ATLID L2 algorithm:**
- Nishizawa, T., Okamoto, H., Sugimoto, N., Kudo, R., et al. (2026). Algorithms to retrieve aerosol optical properties using lidar measurements on board the EarthCARE satellite. *Atmospheric Measurement Techniques*, 19, 729-…. DOI: [10.5194/amt-19-729-2026](https://doi.org/10.5194/amt-19-729-2026)

**EarthCARE concept and rationale:**
- Illingworth, A. J., Barker, H. W., Beljaars, A., Ceccaldi, M., Chepfer, H., Clerbaux, N., Cole, J., Delanoë, J., Domenech, C., Donovan, D. P., et al. (2015). The EarthCARE Satellite: The next step forward in global measurements of clouds, aerosols, precipitation, and radiation. *Bulletin of the American Meteorological Society*, 96(8), 1311–1332. DOI: [10.1175/BAMS-D-12-00227.1](https://doi.org/10.1175/BAMS-D-12-00227.1)

**Citation format for ATLID products** (per ESA Earth Online collection DOIs):
- Example for the A-EBD product: *European Space Agency, 2025, "EarthCARE ATLID EBD Level 2A" (version BC), DOI: 10.57780/eca-d00d438* — version letter must be tracked, since reprocessing baselines change throughout the mission. Always cite the specific version DOI you actually used, not the generic mission paper.

### Host / Server

- **EarthCARE Online Dissemination Service** (primary download portal): <https://ec-pdgs-dissemination1.eo.esa.int/> (link active May 2026; check ESA Earth Online for current URL)
- **ESA Earth Online mission page:** <https://earth.esa.int/eogateway/missions/earthcare>
- **EarthCARE L1 product collection page** (with DOIs): <https://earth.esa.int/eogateway/catalog/earthcare-l1-products>
- **EarthCARE L2 product collection page** (with DOIs): <https://earth.esa.int/eogateway/catalog/earthcare-esa-l2-products>
- **ESA MAAP STAC catalogue** (modern API access): <https://earth.esa.int/eogateway/tools/maap>
- **EarthCARE Imagery Portal** (McGill, interactive visualisation): <https://earth.esa.int/eogateway/tools/earthcare-imagery-portal>
- **Orbit Prediction and Overpass Tool (OPOT)** (predict Cluj overpasses): <https://evdc.esa.int/orbit/>
- **ectools Python library** (Shannon Mason / ECMWF): see ESA Earth Online tools page for current repository link

### Programmatic download

**Step 1 — Account setup (one-time):**

1. Register at ESA EO Sign In: <https://eosso.esa.int/>
2. Sign the EarthCARE data access terms (sent by email after registration)
3. Wait for activation (typically 1–2 business days)
4. Generate API access token via the MAAP catalogue interface

**Step 2 — Programmatic search and download:**

```python
import requests
from datetime import datetime, timedelta, timezone

# ESA EarthCARE Dissemination Service — OData query interface
# (verify current endpoint URL against ESA Earth Online — endpoints may evolve)
BASE_URL = "https://ec-pdgs-dissemination1.eo.esa.int/oads/data/EarthCARE/ESA/Open"

# Authentication: HTTP Basic with EO Sign In credentials,
# or Bearer token via OAuth (recommended for production)
auth_headers = {"Authorization": f"Bearer {os.environ['ESA_EARTHCARE_TOKEN']}"}

# Search for A-EBD (Extinction, Backscatter, Depolarization) products
# within ±200 km of Cluj (46.77°N, 23.55°E) over the last 30 days
now = datetime.now(timezone.utc)
search_params = {
    "$filter": (
        f"Sensing_Start ge {(now - timedelta(days=30)).isoformat()} and "
        f"Sensing_Start le {now.isoformat()} and "
        f"Product_Type eq 'ATL_EBD_2A' and "
        # Spatial filter — OGC-style intersects polygon around Cluj ±~2° (~200 km):
        f"OData.CSC.Intersects(Footprint, "
        f"geography'POLYGON((21.5 44.7, 25.5 44.7, 25.5 48.8, 21.5 48.8, 21.5 44.7))')"
    ),
    "$top": 50,
}

r = requests.get(BASE_URL + "/Products", params=search_params, headers=auth_headers)
r.raise_for_status()
products = r.json()["value"]
for p in products:
    print(p["Name"], p["Sensing_Start"], p["Footprint"])
    # Download the product file:
    download_url = f"{BASE_URL}/Products({p['Id']})/$value"
    with requests.get(download_url, headers=auth_headers, stream=True) as resp:
        with open(p["Name"], "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
```

**Step 3 — Reading and extracting Cluj-window data with xarray:**

```python
import xarray as xr
import numpy as np

ds = xr.open_dataset("ECA_EXAA_ATL_EBD_2A_20260301T120000Z_20260301T133000Z_05432A_E_BC.nc")

# ATLID curtain variables (names per A-PRO documentation):
# - 'particle_backscatter_coefficient_355nm' (along-track × height)
# - 'particle_extinction_coefficient_355nm'
# - 'particle_linear_depol_ratio_355nm'
# - 'classification' (target type per pixel)
# - 'latitude', 'longitude' along track
# - 'height' along profile

# Find profiles where ground track passes within 200 km of Cluj
cluj_lat, cluj_lon = 46.77, 23.55
dist_km = np.hypot(
    (ds['latitude']  - cluj_lat) * 111.0,
    (ds['longitude'] - cluj_lon) * 111.0 * np.cos(np.radians(cluj_lat)),
)
near_cluj_mask = dist_km < 200.0
near_cluj_profiles = ds.isel({ds['latitude'].dims[0]: near_cluj_mask})

print(f"Profiles within 200 km of Cluj this orbit: {near_cluj_mask.sum().item()}")
# Plot the curtain:
import matplotlib.pyplot as plt
near_cluj_profiles['particle_backscatter_coefficient_355nm'].plot(
    x='along_track', y='height', cmap='Spectral_r', vmin=0, vmax=5e-6,
)
plt.title(f"ATLID 355nm particulate backscatter — Cluj overpass {ds.attrs['sensing_start']}")
```

**MAAP STAC catalogue alternative** (recommended for production — STAC is a more modern API standard):

```python
from pystac_client import Client
catalog = Client.open("https://earth.esa.int/eogateway/maap/stac/v1",
                      headers={"Authorization": f"Bearer {os.environ['ESA_EARTHCARE_TOKEN']}"})
search = catalog.search(
    collections=["earthcare-atlid-ebd-l2a"],
    bbox=(21.5, 44.7, 25.5, 48.8),  # Cluj ±~2°
    datetime=(now - timedelta(days=30), now),
)
for item in search.items():
    print(item.id, item.assets["data"].href)
```

### Manual download (interactive web UI)

- **ESA Earth Online EarthCARE catalog**: <https://earth.esa.int/eogateway/catalog/earthcare-esa-l2-products> → use the "Search and Download" interface, filter by Product Type = `ATL_EBD_2A` (or other ATLID products), draw bounding box around Cluj, select date range.
- **EarthCARE Imagery Portal (McGill)**: <https://earth.esa.int/eogateway/tools/earthcare-imagery-portal> — visual browse of ATLID + CPR curtains, useful for quickly inspecting whether a particular overpass passes near Cluj before committing to download.
- **OPOT (Orbit Prediction and Overpass Tool)**: <https://evdc.esa.int/orbit/> — plan future overpasses (e.g. "next 30 days, which orbits pass within 100 km of Cluj?"). Useful for campaign planning + coordinating with the ground EARLINET schedule.

### Notes / caveats

- **ATLID is the project's only space-based vertical profiler.** Every other satellite in the input table is either a wide-swath imager (MODIS, VIIRS, MSI, OLCI, FCI, SEVIRI) or a nadir column-DOAS sounder (TROPOMI, UVNS, UVN, OLCI, SLSTR). ATLID alone gives **altitude-resolved aerosol** at ~100 m vertical resolution. For the project's "what altitude is the smoke / dust layer at?" question, ATLID is the unique answer from space — everything else either misses vertical info entirely or provides only a single layer-height retrieval (TROPOMI ALH).
- **Single wavelength only — 355 nm, period.** No 532 nm (CALIPSO/CALIOP territory), no 1064 nm (CALIPSO again, plus ground EARLINET), no Raman channels. This is the major specification limit vs the Cluj ground lidar which spans 355/387/532/607/1064 nm. ATLID's HSRL design partly compensates by providing independent extinction without lidar-ratio assumption, but **aerosol-type discrimination from spectral information is limited** — relying instead on the lidar-ratio + depolarization-ratio combination at the single 355 nm wavelength, classifying via lookup tables of pre-characterised aerosol types. **For aerosol typing, multi-wavelength EARLINET ground data at Cluj is significantly more discriminating; ATLID complements with spatial coverage.**
- **Curtain not swath.** Critically important to remember: a single ATLID file does NOT cover Europe — it covers a single along-track strip ~30 m wide × tens of degrees of latitude long. The "Cluj near-pass" is when the orbit ground track happens to come within X km of the city; **direct overhead passes are once per ~25 days,** and "useful nearby passes" within 200 km are more like a few per week. **Plan the data ingest cadence accordingly** — this is not a continuous source.
- **HSRL is the key innovation vs CALIPSO/CALIOP.** CALIPSO's CALIOP lidar (2006–2023, EOL) was elastic-only at 532/1064 nm. To convert backscatter to extinction it had to assume a lidar ratio per aerosol type, which is the dominant error source. ATLID's HSRL technique uses the Fabry-Pérot etalon to **directly separate molecular from particulate backscatter** — and the molecular signal serves as an internal calibration target with known attenuation. This gives **direct, calibration-independent extinction profiles** at 355 nm. It is the same physics-of-retrieval that the EARLINET Raman channels provide on the ground; ATLID delivers it from space for the first time, publicly.
- **Active reprocessing — version letters matter.** ESA has released ATLID L2 baselines AE → AF → AG → BA → BB → BC throughout 2024–2025, reflecting iterative algorithm improvements during commissioning and early operations. **When citing ATLID data in publications, always cite the specific version DOI** (e.g. `10.57780/eca-d00d438` for the BC A-EBD baseline) rather than the generic mission paper. **In the pipeline, design ingest code to flag the data baseline version and re-trigger reprocessing of any cached products when a new ESA baseline appears.**
- **Earth Explorer = research mission, not operational continuity.** Unlike SEVIRI/FCI/TROPOMI/Sentinel-4/Sentinel-5 which are operational with multi-decade replacement programmes, EarthCARE has a **3-year nominal lifetime** (2024–2027) with possible extensions (Aeolus, the previous lidar-bearing Earth Explorer, was extended to 4.8 years; CryoSat-2 has run 15+ years). There is **no committed follow-on mission for ATLID specifically.** AOS (the NASA Aerosol and Cloud, Convection and Precipitation mission, planned launch ~2031) may carry an HSRL successor, but it is not yet flying. **Plan the warning chain to treat ATLID as a high-quality but time-bounded data source** — design the architecture so that the pipeline degrades gracefully (to TROPOMI ALH, surface PM, and EARLINET ground profiles) if/when ATLID is decommissioned.
- **CPR anomaly May 2026 — operational lesson learned.** The Cloud Profiling Radar (CPR) had a critical anomaly on 2 May 2026 and was returned to nominal operation on 13 May 2026 after a joint JAXA/ESA investigation. **ATLID was unaffected**, but L2b synergistic products (ATLID+CPR) had a ~11-day gap. For the warning chain: prefer **L2a ATLID-only products** over L2b synergistic when the use case allows, since L2a is robust to single-instrument anomalies elsewhere on the satellite.
- **Authentication is separate from EUMETSAT.** ESA EO Sign In is a **separate credential** from the EUMETSAT EO Portal account used for SEVIRI, FCI, SLSTR, Sentinel-5 UVNS, Sentinel-4 UVN. The pipeline must hold both sets. This is the **only data source in the input table requiring this credential** so far — manage it accordingly.
- **3° off-nadir pointing has a subtle consequence.** ATLID points 3° off-nadir specifically to avoid the specular reflection from horizontally-oriented ice crystals, which would otherwise saturate the lidar detectors. The trade-off: **the ground track centre is offset by ~20 km from the satellite ground track for an instrument at 393 km altitude.** When computing "is this orbit near Cluj?", use the corrected ATLID footprint geolocation in the L1B/L2 product files — do not approximate using the satellite nadir position.
- **Direct EARLINET → ATLID validation publication is feasible.** The Cluj station (CLOP) has the technical capability for cal/val: 355 nm elastic + Raman, depolarization. The lidar group could submit a campaign-based validation paper comparing simultaneous Cluj ground profiles with ATLID overpasses, contributing to the EarthCARE Cal/Val community alongside TROPOS/PollyNET. **This is a publication opportunity adjacent to the warning-chain deliverable, not part of it — but worth flagging.**

---
