# Dataset metadata — MODIS aerosol products (Terra + Aqua)

Companion documentation to the Stage 1 input-data table.
This file describes the MODIS aerosol products feeding the Cluj-Napoca
aerosol early-warning system. **Scope (per project decision):** MAIAC AOD
1 km (MCD19A2) and Dark Target AOD 3 km (M[OY]D04_3K). The Dark Target
10 km product (M[OY]D04_L2) is **not used** in this project.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 5. MODIS — Terra + Aqua aerosol products

### Summary

| Field | Value |
|---|---|
| Instrument | **MODIS** (Moderate Resolution Imaging Spectroradiometer) — 36-band spectroradiometer on the sun-synchronous polar-orbiting **Terra** (equatorial crossing ~10:30 local, descending) and **Aqua** (~13:30, ascending) platforms. |
| Network / Agency | **NASA** (mission), distributed by **EOSDIS** through two complementary services: **LAADS DAAC** (Level 1 and Atmosphere Archive & Distribution System, standard products) and **LANCE NRT3** (Land, Atmosphere Near real-time Capability for Earth observation). MAIAC products are co-distributed by the **LP DAAC** (Land Processes DAAC). |
| Products used | **(a) MAIAC AOD 1 km — MCD19A2** (combined Terra + Aqua, daily L2G gridded). **(b) Dark Target AOD 3 km — MOD04_3K** (Terra) and **MYD04_3K** (Aqua), 5-minute L2 swath. |
| Current collection | **Collection 6.1 (C6.1)** for both products. C6 is deprecated; C6.1 introduced bug fixes (notably for urban areas in DT) and improved radiometric calibration upstream. |
| Processing level | Both are **Level 2** (geophysical retrievals from individual overpasses). MAIAC is additionally L2G (gridded into the MODIS sinusoidal tile system). |
| File format | **HDF4 / HDF-EOS2** — **not HDF5** as stated in the original docx. This matters for downstream code: use `pyhdf` (Python) or `xarray` with the `netcdf4` engine via the HDF-EOS interface, **not** `h5py`. Some new C6.1 cloud-product files have moved to NetCDF4, but the aerosol L2 products remain HDF4. |
| Filename patterns | **MAIAC standard:** `MCD19A2.AYYYYDDD.hHHvVV.061.YYYYDDDHHMMSS.hdf` (e.g. `MCD19A2.A2025135.h19v04.061.2025136120300.hdf`). **MAIAC NRT:** `MCD19A2N.AYYYYDDD.hHHvVV.061.NRT.hdf` — distributed through LANCE NRT3. **DT 3 km standard:** `M[OY]D04_3K.AYYYYDDD.HHMM.061.YYYYDDDHHMMSS.hdf` (5-min swath segments, no tiling). **DT 3 km NRT:** `M[OY]D04_3K.AYYYYDDD.HHMM.061.NRT.hdf`. |
| Cluj coverage | Cluj-Napoca (46.77° N, 23.55° E) falls in **MODIS sinusoidal tile `h19v04`** for the gridded MAIAC product. Daily, two overpasses (Terra mid-morning + Aqua early afternoon) yield 2 useful AOD retrievals per day, weather permitting. The swath-based DT 3 km product covers Cluj when the satellite track passes over Romania (most days, but not always for both platforms). |
| NRT availability | **YES.** Both products have NRT collections delivered through **LANCE NRT3** with typical latency **60–125 minutes after the satellite observation** (per NASA's LANCE service-level statement). Standard (post-processed, validated) versions follow a few days later through LAADS / LP DAAC and replace the NRT files for retrospective analysis. |
| Authentication | **NASA Earthdata Login (EDL) required** — free, single account for all NASA DAACs + LANCE. For LAADS programmatic access, an **App Key** must additionally be generated from the user's Earthdata profile and passed as a Bearer token. LANCE NRT3 also accepts the same Bearer token. |
| Programmatic access | YES — multiple options: **(1)** the official `earthaccess` Python library (recommended for standard products via CMR / Earthdata Cloud); **(2)** the LAADS DAAC HTTP archive with `wget`/`curl` + App Key; **(3)** the LANCE NRT3 archive at `https://nrt3.modaps.eosdis.nasa.gov/` for NRT files. |
| Layer destination | **L2:** FLEXPART (column-AOD constraint for transport-model emission inversion). HYSPLIT (column-AOD context for transport diagnostics, source attribution). **L3:** Knowledge Graph (MAIAC 1 km only — its fine resolution makes it suitable for the urban-scale GUI display; DT 3 km not routed to KG per the original table). GRASP not consumed (synergy-only with ground-based lidar + sun photometer). |

### References

**Primary algorithm references (cite when products are used):**

- **MAIAC (MCD19A2):** Lyapustin, A., Wang, Y., Korkin, S., & Huang, D. (2018). MODIS Collection 6 MAIAC algorithm. *Atmospheric Measurement Techniques*, 11(10), 5741–5765. DOI: [10.5194/amt-11-5741-2018](https://doi.org/10.5194/amt-11-5741-2018)
- **Dark Target 3 km (MOD04_3K / MYD04_3K):** Remer, L. A., Mattoo, S., Levy, R. C., & Munchak, L. A. (2013). MODIS 3 km aerosol product: algorithm and global perspective. *Atmospheric Measurement Techniques*, 6(7), 1829–1844. DOI: [10.5194/amt-6-1829-2013](https://doi.org/10.5194/amt-6-1829-2013)
- **Dark Target Collection 6 over land/ocean (broader DT reference):** Levy, R. C., Mattoo, S., Munchak, L. A., Remer, L. A., Sayer, A. M., Patadia, F., & Hsu, N. C. (2013). The Collection 6 MODIS aerosol products over land and ocean. *Atmospheric Measurement Techniques*, 6(11), 2989–3034. DOI: [10.5194/amt-6-2989-2013](https://doi.org/10.5194/amt-6-2989-2013)

**Dataset DOIs (C6.1, citable for data deliverables):**

- **MCD19A2 V6.1:** Lyapustin, A., & Wang, Y. (2022). MODIS/Terra+Aqua Land Aerosol Optical Depth Daily L2G Global 1km SIN Grid V061. NASA EOSDIS Land Processes DAAC. DOI: [10.5067/MODIS/MCD19A2.061](https://doi.org/10.5067/MODIS/MCD19A2.061)
- **MOD04_3K V6.1:** Levy, R., & Hsu, C. (2017). MODIS/Terra Aerosol 5-Min L2 Swath 3km. NASA MODIS Adaptive Processing System, Goddard Space Flight Center, USA. DOI: [10.5067/MODIS/MOD04_3K.061](https://doi.org/10.5067/MODIS/MOD04_3K.061)
- **MYD04_3K V6.1:** Levy, R., & Hsu, C. (2017). MODIS/Aqua Aerosol 5-Min L2 Swath 3km. NASA MODIS Adaptive Processing System, Goddard Space Flight Center, USA. DOI: [10.5067/MODIS/MYD04_3K.061](https://doi.org/10.5067/MODIS/MYD04_3K.061)

### Host / Server

- **LAADS DAAC (standard products):** <https://ladsweb.modaps.eosdis.nasa.gov/>
- **LANCE NRT MODIS portal:** <https://www.earthdata.nasa.gov/data/instruments/modis/near-real-time-data>
- **LANCE NRT3 archive root:** <https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/>
  - MAIAC NRT: `https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/MCD19A2N/`
  - DT 3 km NRT Terra: `https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/MOD04_3K/`
  - DT 3 km NRT Aqua: `https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/MYD04_3K/`
- **Earthdata Search (GUI):** <https://search.earthdata.nasa.gov/>
- **Earthdata Login (account registration + App Key):** <https://urs.earthdata.nasa.gov/>
- **`earthaccess` Python library docs:** <https://earthaccess.readthedocs.io/>
- **MAIAC User Guide (V6.1):** <https://lpdaac.usgs.gov/documents/1500/MCD19_User_Guide_V61.pdf>

### Programmatic download

**Recommended for standard products: `earthaccess` Python library.** Handles Earthdata Login, CMR search, and cloud/on-prem download in a few lines.

```bash
pip install earthaccess
```

```python
import earthaccess

# 1. Authenticate — first run prompts for EDL username/password and caches them in ~/.netrc
earthaccess.login(strategy="interactive", persist=True)

# 2. Search for MAIAC 1 km over Cluj for a date range
#    bbox = (lon_min, lat_min, lon_max, lat_max). A 0.5° box around Cluj is plenty.
cluj_bbox = (23.0, 46.3, 24.1, 47.2)

maiac_granules = earthaccess.search_data(
    short_name="MCD19A2",
    version="061",
    bounding_box=cluj_bbox,
    temporal=("2026-05-01", "2026-05-18"),
)
print(f"{len(maiac_granules)} MAIAC granules")

dt3k_terra = earthaccess.search_data(
    short_name="MOD04_3K",
    version="061",
    bounding_box=cluj_bbox,
    temporal=("2026-05-01", "2026-05-18"),
)
dt3k_aqua = earthaccess.search_data(
    short_name="MYD04_3K",
    version="061",
    bounding_box=cluj_bbox,
    temporal=("2026-05-01", "2026-05-18"),
)
print(f"{len(dt3k_terra)} Terra DT 3 km, {len(dt3k_aqua)} Aqua DT 3 km")

# 3. Download (or stream from S3 if running in AWS us-west-2)
earthaccess.download(maiac_granules, local_path="./data/maiac/")
earthaccess.download(dt3k_terra + dt3k_aqua, local_path="./data/dt3k/")
```

**For NRT (LANCE NRT3) — `earthaccess` does not currently cover LANCE, so use direct HTTP with an App Key:**

```bash
# Get an App Key:
# 1) log in to https://urs.earthdata.nasa.gov/profile
# 2) Generate Token  →  copy the long Bearer token string
# 3) export it to your shell environment as below
export EDL_TOKEN="<paste long bearer token here>"

# List today's MAIAC NRT files (UTC day-of-year)
DOY=$(date -u +%j); Y=$(date -u +%Y)
curl -s -H "Authorization: Bearer ${EDL_TOKEN}" \
  "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/61/MCD19A2N/${Y}/${DOY}/" \
  | jq .   # the LAADS-style archive API returns JSON for content listings

# Download a specific tile (e.g. Cluj h19v04) for today
curl -s -H "Authorization: Bearer ${EDL_TOKEN}" -O \
  "https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/MCD19A2N/${Y}/${DOY}/MCD19A2N.A${Y}${DOY}.h19v04.061.NRT.hdf"

# Download all of today's Terra DT 3 km granules (5-min swath segments)
curl -s -H "Authorization: Bearer ${EDL_TOKEN}" \
  "https://nrt3.modaps.eosdis.nasa.gov/api/v2/content/archives/allData/61/MOD04_3K/${Y}/${DOY}/" \
  | jq -r '.[].name' \
  | grep '\.NRT\.hdf$' \
  | xargs -I {} curl -s -H "Authorization: Bearer ${EDL_TOKEN}" -O \
      "https://nrt3.modaps.eosdis.nasa.gov/archive/allData/61/MOD04_3K/${Y}/${DOY}/{}"
```

**Reading HDF4 in Python** (since these are not HDF5):

```python
# pip install pyhdf
from pyhdf.SD import SD, SDC

f = SD("MCD19A2.A2025135.h19v04.061.2025136120300.hdf", SDC.READ)
print(f.datasets().keys())  # list SDS layers
aod_550 = f.select("Optical_Depth_055")[:]   # blue/green AOD layer
qa = f.select("AOD_QA")[:]
f.end()
```

Or, with xarray (which can transparently open HDF-EOS via the netCDF4 engine on most systems):

```python
import xarray as xr
ds = xr.open_dataset(
    "MCD19A2.A2025135.h19v04.061.2025136120300.hdf",
    engine="netcdf4",   # works on systems with HDF4 support compiled in
)
print(ds.data_vars)
```

### Manual download (interactive web UI)

- **Earthdata Search GUI** (standard products, bbox+time filters, login): <https://search.earthdata.nasa.gov/search?q=MCD19A2>
- **LAADS DAAC product browser:** <https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MCD19A2> · <https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MOD04_3K> · <https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MYD04_3K>
- **LANCE NRT3 archive (folder listing for current DOY):** the URLs in the original docx point to a fixed historical DOY; use the dynamic pattern shown in the bash example above to pull today's files.

### Notes / caveats

- **HDF4, not HDF5.** The original docx lists MODIS aerosol products as "hdf 5" — this is wrong. Collection 6.1 atmosphere L2 products are HDF-EOS2 (HDF4). Use `pyhdf`, not `h5py`. The MOD04 cloud-mask products and some C6.1 cloud products did move to NetCDF4, but **MCD19A2**, **MOD04_3K**, and **MYD04_3K** remain HDF4.
- **MAIAC vs. DT in the same chain.** The two products are complementary, not redundant: MAIAC uses time-series + multi-angle context and works much better over bright urban surfaces (which is exactly where Cluj-Napoca lives, mid-latitude continental urban), while DT 3 km is the air-quality-community workhorse with a longer heritage and tighter validation. For the project: route **MAIAC** to the GUI/KG (1 km is the right scale for an urban early warning), route **DT 3 km** to FLEXPART/HYSPLIT for transport-model constraints (its swath geometry pairs cleanly with model-grid resampling).
- **Tile vs. swath.** MAIAC is delivered as **daily gridded SIN tiles**; one Cluj-relevant tile (`h19v04`) per day is enough. DT 3 km is delivered as **5-min swath segments**; multiple granules per day, possibly empty for Cluj if the swath happens to miss. The pipeline needs to handle these two geometries differently.
- **NRT vs. standard.** NRT files have the `.NRT.hdf` suffix and are processed with the best available ancillary data at the time of observation; they're typically within ~0.01–0.02 AOD of the standard product. For the warning chain ingest NRT and **overwrite with standard** when it appears (typically 2–7 days later). The `earthaccess` library queries the standard collection; for live NRT you need the direct LANCE NRT3 HTTP path shown above.
- **Authentication two-step.** EDL username/password works for `earthaccess` and the GUI. **Programmatic** HTTP downloads from LAADS or LANCE need a separately generated **App Key** (Bearer token) from the EDL profile page. Tokens have a configurable lifetime (default 60 days) — rotate before expiry.
- **Cloud screening sensitivity.** Cluj winters have frequent thin/broken clouds; both MAIAC and DT will reject many retrievals as cloud-contaminated. Expected useful retrievals: roughly 40–60 % of overpasses on an annual basis at mid-latitudes, lower in winter. The downstream chain should tolerate gaps and not flag missing satellite AOD as an anomaly.
- **Terra–Aqua bias.** Across the Collection 6 era, Terra (MOD04) reports systematically ~13 % higher global mean AOD than Aqua (MYD04), with seasonal modulation. If you average across platforms, document the bias; for event detection (anomaly relative to baseline) the bias is less critical.
- **Citation per NASA policy.** All MODIS data are open with no restrictions on reuse. The MAIAC + DT 3 km algorithm papers (Lyapustin 2018, Remer 2013) should be cited along with the dataset DOIs above when the products are used in deliverables or publications.

---
