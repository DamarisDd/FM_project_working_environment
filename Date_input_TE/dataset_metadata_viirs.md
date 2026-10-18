# Dataset metadata — VIIRS aerosol products (SNPP + NOAA-20 + NOAA-21)

Companion documentation to the Stage 1 input-data table.
This file describes the VIIRS Dark Target aerosol products feeding the
Cluj-Napoca aerosol early-warning system. **Scope:** the Level-2 Dark
Target Aerosol 6 km product family, across all three currently operational
VIIRS platforms.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 6. VIIRS — Suomi NPP + NOAA-20 + NOAA-21 Dark Target aerosols

### Summary

| Field | Value |
|---|---|
| Instrument | **VIIRS** (Visible Infrared Imaging Radiometer Suite) — 22-band scanning radiometer designed as the operational successor to MODIS. Sun-synchronous polar orbits, ~13:30 local ascending equator crossing. Native moderate-resolution ("M-band") pixel size ~750 m at nadir; the L2 aerosol product averages 8 × 8 M-band pixels into a single 6 km × 6 km retrieval. |
| Network / Agency | **NASA** (Dark Target algorithm + product distribution, via the **VIIRS Atmosphere SIPS** at SSEC, University of Wisconsin-Madison). Distributed through **LAADS DAAC** (standard) and **LANCE** (NRT). |
| Platforms (currently operational in 2026) | **(1) Suomi NPP (SNPP)** — launched Oct 2011, still operational. **(2) NOAA-20 (JPSS-1)** — launched Nov 2017. **(3) NOAA-21 (JPSS-2)** — launched Nov 2022, **first DT aerosol product released Dec 2025** (V2.1 is its initial public collection). NOAA-21 was not yet producing aerosol data when the original docx was written; it should be added to the input list for the project. |
| Product family | Dark Target Aerosol L2 6-min swath, 6 km at nadir. Per-platform short names: **`AERDT_L2_VIIRS_SNPP`** · **`AERDT_L2_VIIRS_NOAA20`** · **`AERDT_L2_VIIRS_NOAA21`**. NRT counterparts: **`AERDT_L2_VIIRS_SNPP_NRT`** · **`AERDT_L2_VIIRS_NOAA20_NRT`** · (NOAA-21 NRT to follow). |
| Current collection | **V2.1** (December 2025) for all three platforms. V2.0 still archived but superseded. V2.1 introduces cross-platform calibration coefficients (so SNPP, NOAA-20, NOAA-21 are now properly inter-comparable), improved ocean cloud filter, a new `Dust_Flag_Ocean` SDS for enhanced dust detection, revised urban surface-reflectance correction, and updated GMAO ancillary (GEOS-IT replacing GEOS-FPIT). |
| Processing level | **Level 2** geophysical retrievals from individual overpasses, organised into 6-minute swath segments. ~130 granules per platform per UTC day (daylight only). |
| File format | **NetCDF4** (CF-compliant), file extension `.nc`. NetCDF4 is built on the HDF5 binary layer, so technically these files can also be opened by `h5py`, but the canonical tool is `netCDF4` / `xarray` / `xarray.open_dataset(..., engine="netcdf4")`. **This is different from MODIS C6.1 atmosphere products (which are HDF4)** — same agency, same Dark Target algorithm family, different on-disk format. The original docx labels VIIRS as "hdf 5"; the correct label is "NetCDF4". |
| Filename patterns | **Standard:** `AERDT_L2_VIIRS_<PLATFORM>.AYYYYDDD.HHMM.021.<PROCDATE>.nc` (e.g. `AERDT_L2_VIIRS_NOAA20.A2026138.1124.021.2026138165422.nc`). **NRT:** same root, with the `_NRT` suffix on the short-name (`AERDT_L2_VIIRS_SNPP_NRT.AYYYYDDD.HHMM.021.<PROCDATE>.nc`). |
| Cluj coverage | Each platform overflies Cluj-Napoca with one usable daytime pass per day. With three platforms there are up to **3 useful AOD swaths per day over Cluj** — significantly better revisit than the MODIS-only era (Terra + Aqua = 2 passes). Combined with MODIS, the project gets up to **5 daytime satellite AOD opportunities per day** over the city. |
| NRT availability | **YES, ~3 h latency.** LANCE-distributed NRT product is generally available **within ~3 hours of observation** (per NASA's April 2025 announcement) — slower than the MODIS NRT path (60–125 min) but still fast enough for the early-warning chain. Standard products replace the NRT files a few days later. |
| Authentication | **NASA Earthdata Login (EDL) required** — same account as for MODIS. For programmatic LAADS / LANCE access, also a Bearer App Key generated in the EDL profile (single key works for all NASA atmosphere products). |
| Programmatic access | YES — same toolchain as MODIS: `earthaccess` Python library for standard products (CMR-based search), or direct HTTPS with Bearer auth against LAADS / LANCE NRT3 for swath-by-swath NRT pulls. |
| Layer destination | **L2:** FLEXPART (column-AOD constraint for transport modelling, complementary to MODIS DT 3 km). HYSPLIT (transport diagnostics / source attribution). **L3:** Knowledge Graph **NOT consumed** (per original table) — 6 km resolution is too coarse for urban-scale GUI display compared with MAIAC 1 km. GRASP: not used (ground-based-synergy only). |

### References

**Primary algorithm reference for VIIRS DT (cite when products are used):**
- Sawyer, V., Levy, R. C., Mattoo, S., Cureton, G., Shi, Y., & Remer, L. A. (2020). Continuing the MODIS Dark Target Aerosol Time Series with VIIRS. *Remote Sensing*, 12(2), 308. DOI: [10.3390/rs12020308](https://doi.org/10.3390/rs12020308)

**Recent algorithm-update / multi-platform evaluation reference (V2.1 era):**
- Sawyer, V., Levy, R. C., Mattoo, S., Shi, Y. R., Kim, M., Remer, L. A., & Cureton, G. (2025). An updated VIIRS dark target aerosol product for continuity with MODIS: assessing regional aerosol trends. *Frontiers in Environmental Science*, 13. DOI: [10.3389/fenvs.2025.1602145](https://doi.org/10.3389/fenvs.2025.1602145)

**Foundational MODIS DT reference (relevant since the VIIRS algorithm is a direct port):**
- Levy, R. C., Mattoo, S., Munchak, L. A., Remer, L. A., Sayer, A. M., Patadia, F., & Hsu, N. C. (2013). The Collection 6 MODIS aerosol products over land and ocean. *Atmospheric Measurement Techniques*, 6(11), 2989–3034. DOI: [10.5194/amt-6-2989-2013](https://doi.org/10.5194/amt-6-2989-2013)

**Note on the docx's original reference [6]:** The Hsu et al. 2013 *Enhanced Deep Blue* paper cited in the docx is the canonical reference for the **Deep Blue** algorithm, not Dark Target. The docx itself flags this in a footnote. **Replace with Sawyer 2020 + 2025 above** for the VIIRS Dark Target products actually used in this project. (If the project ever ingests Deep Blue from VIIRS — `AERDB_L2_VIIRS_*` — then Hsu 2013 becomes the right reference for that stream.)

**Dataset DOIs (V2.1, citable for data deliverables):**

- **SNPP V2.1:** VIIRS Atmosphere Science Team / SSEC (2025). SNPP VIIRS Dark Target Aerosol Level-2 6-Minute Swath 6 km. NASA LAADS DAAC. DOI: [10.5067/VIIRS/AERDT_L2_VIIRS_SNPP.021](https://doi.org/10.5067/VIIRS/AERDT_L2_VIIRS_SNPP.021)
- **NOAA-20 V2.1:** VIIRS Atmosphere Science Team / SSEC (2025). NOAA20 VIIRS Dark Target Aerosol Level-2 6-Minute Swath 6 km. NASA LAADS DAAC. DOI: `10.5067/VIIRS/AERDT_L2_VIIRS_NOAA20.021` (per the SNPP / NOAA-21 DOI pattern; verify on LAADS landing page before publication).
- **NOAA-21 V2.1 (new):** VIIRS Atmosphere Science Team / SSEC (2025). NOAA21 VIIRS Dark Target Aerosol Level-2 6-Minute Swath 6 km. NASA LAADS DAAC. DOI: [10.5067/VIIRS/AERDT_L2_VIIRS_NOAA21.021](https://doi.org/10.5067/VIIRS/AERDT_L2_VIIRS_NOAA21.021)
- **NOAA-20 NRT V2:** NASA VIIRS Atmosphere Science Team / SSEC (2023). VIIRS/NOAA20 Dark Target Aerosol L2 6-Min Swath 6 km (NRT). NASA VIIRS Atmosphere SIPS. DOI: [10.5067/VIIRS/AERDT_L2_VIIRS_NOAA20_NRT.002](https://doi.org/10.5067/VIIRS/AERDT_L2_VIIRS_NOAA20_NRT.002)

### Host / Server

- **LAADS DAAC product pages:**
  - SNPP: <https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/AERDT_L2_VIIRS_SNPP/>
  - NOAA-20: <https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/AERDT_L2_VIIRS_NOAA20/>
  - NOAA-21: <https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/AERDT_L2_VIIRS_NOAA21/>
- **LANCE NRT VIIRS portal:** <https://www.earthdata.nasa.gov/data/instruments/viirs/near-real-time-data>
- **LANCE NRT3 archive root:** <https://nrt3.modaps.eosdis.nasa.gov/archive/allData/5200/> (VIIRS uses archive set `5200`, distinct from MODIS's `61`)
- **Atmosphere SIPS at SSEC:** <https://sips.ssec.wisc.edu/>
- **Earthdata Search (GUI):** <https://search.earthdata.nasa.gov/> (CMR collection concept IDs from the docx are still resolvable but pin to V2.0; V2.1 has new concept IDs — re-query CMR for the latest)
- **Earthdata Login (account + App Key):** <https://urs.earthdata.nasa.gov/>
- **Dark Target team page:** <https://darktarget.gsfc.nasa.gov/>

### Programmatic download

**Recommended for standard products: `earthaccess` Python library** (same setup as for MODIS — credentials cached in `~/.netrc` after first login):

```python
import earthaccess

earthaccess.login(strategy="interactive", persist=True)  # one-time

cluj_bbox = (23.0, 46.3, 24.1, 47.2)
window = ("2026-05-01", "2026-05-18")

snpp = earthaccess.search_data(
    short_name="AERDT_L2_VIIRS_SNPP", version="021",
    bounding_box=cluj_bbox, temporal=window,
)
noaa20 = earthaccess.search_data(
    short_name="AERDT_L2_VIIRS_NOAA20", version="021",
    bounding_box=cluj_bbox, temporal=window,
)
noaa21 = earthaccess.search_data(
    short_name="AERDT_L2_VIIRS_NOAA21", version="021",
    bounding_box=cluj_bbox, temporal=window,
)
print(f"{len(snpp)} SNPP / {len(noaa20)} NOAA-20 / {len(noaa21)} NOAA-21 granules")

earthaccess.download(snpp + noaa20 + noaa21, local_path="./data/viirs_dt/")
```

**For NRT (LANCE) — direct HTTPS with Bearer token:**

```bash
export EDL_TOKEN="<paste long bearer token from urs.earthdata.nasa.gov/profile>"

Y=$(date -u +%Y); DOY=$(date -u +%j)

# List today's SNPP NRT files (JSON index)
curl -s -H "Authorization: Bearer ${EDL_TOKEN}" \
  "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5200/AERDT_L2_VIIRS_SNPP_NRT/${Y}/${DOY}/" \
  | jq .

# Pull all of today's NOAA-20 NRT granules
curl -s -H "Authorization: Bearer ${EDL_TOKEN}" \
  "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/5200/AERDT_L2_VIIRS_NOAA20_NRT/${Y}/${DOY}/" \
  | jq -r '.[].name' \
  | grep '\.nc$' \
  | xargs -I {} curl -s -H "Authorization: Bearer ${EDL_TOKEN}" -O \
      "https://nrt3.modaps.eosdis.nasa.gov/archive/allData/5200/AERDT_L2_VIIRS_NOAA20_NRT/${Y}/${DOY}/{}"
```

**Reading a VIIRS DT file in Python:**

```python
import xarray as xr

ds = xr.open_dataset(
    "AERDT_L2_VIIRS_NOAA20.A2026138.1124.021.2026138165422.nc",
    engine="netcdf4",
)
print(ds.data_vars)              # 37 geophysical SDSs + 8 geolocation
aod_550 = ds["Optical_Depth_Land_And_Ocean"]
qa = ds["Land_Ocean_Quality_Flag"]
```

**Spatial subsetting to Cluj at ingest time** (each 6-min swath covers a huge area — extract only the relevant pixels):

```python
import numpy as np

lat = ds["latitude"].values
lon = ds["longitude"].values
mask = (lat > 46.3) & (lat < 47.2) & (lon > 23.0) & (lon < 24.1)
aod_cluj = ds["Optical_Depth_Land_And_Ocean"].values[mask]
qa_cluj = qa.values[mask]
# keep only high-quality retrievals
good = aod_cluj[qa_cluj == 3]
```

### Manual download (interactive web UI)

- **Earthdata Search:** <https://search.earthdata.nasa.gov/search?q=AERDT_L2_VIIRS> (filter by platform, date, bbox)
- **LAADS DAAC product browser:** product-specific pages linked above
- **LANCE NRT3 (browse):** `https://nrt3.modaps.eosdis.nasa.gov/archive/allData/5200/AERDT_L2_VIIRS_<PLATFORM>_NRT/<YYYY>/<DDD>/` — replace placeholders and open in browser (will prompt for EDL credentials)

### Notes / caveats

- **NetCDF4, not HDF4.** Important to call out: the VIIRS aerosol L2 products are NetCDF4 — different from MODIS C6.1 atmosphere products (HDF4). The same `xarray` open call works for both (with `engine="netcdf4"`), but the underlying SDS-versus-variable conventions are slightly different, and naive HDF4 code (`pyhdf`) will not work on the VIIRS files. The original docx labels these as "hdf 5"; the correct label is "NetCDF4".
- **NOAA-21 is brand new.** First public VIIRS DT aerosol data from NOAA-21 became available **December 2025** (V2.1). This was not yet available when the original docx was written, so the input table should be updated to add NOAA-21 alongside SNPP and NOAA-20. The cross-platform calibration in V2.1 explicitly aligns all three platforms, so they're now genuinely inter-comparable in the same retrieval framework.
- **Cross-platform offsets are documented.** Even with the V2.1 cross-calibration, each VIIRS instrument carries a small, relatively stable offset from the others (and from MODIS — see Sawyer 2025). For event detection (anomaly relative to baseline) this is negligible; for absolute AOD comparisons (e.g. matching against AERONET CLUJ_UBB ground truth), the offset should be characterised once for the Cluj-area pixels and either applied as a per-platform correction or absorbed into a multi-platform consensus value.
- **NRT vs. standard latency.** NRT is ~3 h after observation (slower than MODIS at 60–125 min). The standard (final) product is available 2–7 days later through LAADS. The pipeline should ingest NRT for the live warning chain and overwrite with standard for retrospective analyses.
- **Authentication shared with MODIS.** A single Earthdata Login account + App Key serves MODIS *and* VIIRS *and* most other NASA atmosphere products. Token rotation policy is the same — default 60-day lifetime.
- **Cloud screening.** Like MODIS DT, VIIRS DT rejects cloud-contaminated pixels aggressively; expect 40–60 % retrieval yield on annual average at mid-latitudes, lower in winter. Use the `Land_Ocean_Quality_Flag` to keep only the highest-quality retrievals (QA = 3) for science-grade work; for event-detection screening (warning chain), QA ≥ 2 may be acceptable to maximise sampling.
- **Why three platforms.** From a project perspective, the value of the three-platform stack is **temporal coverage**, not redundancy: SNPP + NOAA-20 + NOAA-21 all sit on the same ~13:30-local orbital plane (NOAA-21 ~50 min ahead of NOAA-20, SNPP between them), so they give three closely-spaced passes per day rather than three independent looks. Combined with MODIS Terra (~10:30) and Aqua (~13:30), the project sees Cluj at roughly 10:30, 13:00, 13:30, 14:00 local time on a typical clear day.
- **Citation per NASA policy.** Open data, no restrictions. Cite the algorithm paper(s) and the dataset DOI(s) above; the V2.1 acknowledgment text is recommended to include the SSEC ASIPS facility.

---
