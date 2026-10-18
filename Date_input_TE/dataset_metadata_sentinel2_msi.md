# Dataset metadata — Sentinel-2 MSI (Copernicus / ESA)

Companion documentation to the Stage 1 input-data table.
This file describes the Sentinel-2 Multispectral Instrument (MSI) products
feeding the Cluj-Napoca aerosol early-warning system. **Scope:** Level-1C
TOA radiance / 10 m visible imagery (for GUI evidence and source attribution)
and Level-2A BOA reflectance (for GRASP-style synergy with the AERONET
ground-based retrievals).

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 7. Sentinel-2 MSI — Copernicus optical high-resolution

### Summary

| Field | Value |
|---|---|
| Instrument | **MSI** (Multispectral Instrument) — push-broom optical imager with **13 spectral bands** spanning the visible (incl. coastal aerosol B01), near-infrared, and shortwave-infrared (B02–B12) regions. Spatial resolution per band: 4 bands at **10 m** (B02, B03, B04, B08 — Blue, Green, Red, NIR), 6 bands at **20 m** (red-edge + SWIR), 3 bands at **60 m** (B01 coastal-aerosol, B09 water vapour, B10 cirrus). |
| Network / Agency | **ESA / European Commission** — Copernicus Earth Observation programme. Operated by ESA, products distributed centrally through the **Copernicus Data Space Ecosystem (CDSE)** since 2023 (replacing the legacy SciHub / Open Access Hub). |
| Platforms (currently operational, May 2026) | **Sentinel-2B** (launched March 2017) and **Sentinel-2C** (launched September 2024, operational). **Sentinel-2A** (launched June 2015) was maneuvered into a phased orbit in March 2025 for a one-year transition campaign with the new 3-satellite constellation; nominal end of the campaign was March 2026, after which the constellation returns to 2 satellites (S2B + S2C). The docx mentions only "Sentinel 2" generically — **the table should be updated to reflect the S2A → S2C succession.** |
| Products used | **(a) Level-1C** — Top-of-Atmosphere (TOA) reflectance, orthorectified, tiled in MGRS / UTM. Used for the 10 m visible-band imagery feeding the GUI / Knowledge Graph (visual evidence of pollution sources, smoke plumes, dust events). **(b) Level-2A** — Bottom-of-Atmosphere (BOA) reflectance, atmospherically corrected by ESA-run **Sen2Cor**. Used as the per-band reflectance input for GRASP-style synergy retrievals with ground-based AERONET / lidar. L1B (TOA radiance) exists but is expert-only on request — not used. |
| Current collection | **Collection 1** (processing baseline 05.xx and later). Pre-Collection-1 data (baseline ≤ 03.01) are still in the archive but should be filtered out for new ingest. |
| Processing level | L1C and L2A (both released to users). |
| File format | **SAFE** folder structure (Standard Archive Format for Europe), delivered as a `.zip`. Each band is a **JPEG 2000** (`.jp2`) raster file inside `GRANULE/<granule_id>/IMG_DATA/<resolution>/`; metadata is XML conforming to the published XSD schemas. **This is NOT NetCDF** — the docx's "netcdf file" label is incorrect. Open with `rasterio` / `gdal` / `xarray` (via `rioxarray`) or the dedicated `sentinel-2-tools` / `sentinelhub-py` packages. Sentinel Hub's Process API can also deliver subsets as GeoTIFF (COG), PNG, or JPEG on-the-fly without downloading the full SAFE archive. |
| Filename / tile | **Compact filename:** `S2<X>_MSIL1C_<DATATAKE>_N<BASELINE>_R<ORBIT>_T<MGRS>_<PROCDATE>.SAFE` (e.g. `S2B_MSIL2A_20260518T091559_N0511_R094_T34TFR_20260518T120432.SAFE`). **Cluj coverage:** the MGRS tile **`T34TFR`** covers Cluj-Napoca (UTM zone 34, latitude band T, MGRS 100 km square FR). Worth verifying once on the CDSE Browser before pipeline ingest — Cluj sits near the edge of `T34TFR` and an overlap with `T34TFQ` or `T35TKL` is possible depending on the swath geometry. |
| Cluj revisit | With S2B + S2C (post-March 2026): nominal **5-day revisit** at the equator, slightly better at Cluj's mid-latitude due to swath overlap. During the 3-satellite transition campaign (March 2025 – March 2026): ~3–5 days. Each visit is daytime only and subject to cloud cover; the air-quality literature typically gets ~30–40 % usable acquisitions per year at Cluj's latitude. |
| NRT availability | **No formal NRT stream**, but products become available **typically within 3–12 hours of acquisition** (matches the original docx's "between 3 and 12 hours"). For the early-warning chain this is fast enough to confirm a developing event but not fast enough to drive the first alert — the role of S2 is **corroborative / source-attribution**, not first-detection. |
| Authentication | **CDSE account required** (free registration). For programmatic access, **OAuth 2.0 access tokens** obtained from the CDSE Keycloak endpoint. Two concurrent downloads per user; rate-limited. |
| Programmatic access | YES — multiple APIs: **(1) OData REST API** for catalog query + product download; **(2) OpenSearch** for legacy-style catalog queries; **(3) STAC API** at `https://stac.dataspace.copernicus.eu/` (modern, recommended for new pipelines); **(4) Sentinel Hub Process API** for in-cloud subsetting / mosaicking / band-math, returning COG/PNG/etc. without downloading the full SAFE. |
| Layer destination | **L2:** GRASP (per-band TOA / BOA reflectance for synergy retrievals with AERONET — the table assigns this to the L2A "Reflectanță" sub-row). **L3:** Knowledge Graph (10 m true-colour imagery as visual evidence — the table assigns this to the L1C "VIS 10 m" sub-row). HYSPLIT (per the original table — the 10 m visual feeds HYSPLIT-product visualizations in the GUI alongside trajectory outputs, rather than HYSPLIT itself consuming pixel data). FLEXPART not used. |

### References

**Primary mission reference:**
- Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F., & Bargellini, P. (2012). Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services. *Remote Sensing of Environment*, 120, 25–36. DOI: [10.1016/j.rse.2011.11.026](https://doi.org/10.1016/j.rse.2011.11.026)

**Atmospheric-correction / Sen2Cor reference (cite when L2A is used):**
- Main-Knorn, M., Pflug, B., Louis, J., Debaecker, V., Müller-Wilm, U., & Gascon, F. (2017). Sen2Cor for Sentinel-2. *Proc. SPIE 10427, Image and Signal Processing for Remote Sensing XXIII*, 1042704. DOI: [10.1117/12.2278218](https://doi.org/10.1117/12.2278218)

**Dataset DOIs (ESA-issued for Copernicus Sentinel-2 products):**
- **L1C TOA reflectance, Collection 1:** Copernicus Sentinel-2 (processed by ESA), 2021, *MSI Level-1C TOA Reflectance Product. Collection 1.* European Space Agency. DOI: [10.5270/S2_-742ikth](https://doi.org/10.5270/S2_-742ikth) (verify against the current CDSE product page before publication — ESA's DOI tagging is occasionally updated)
- **L2A BOA reflectance, Collection 1:** Copernicus Sentinel-2 (processed by ESA), 2021, *MSI Level-2A BOA Reflectance Product. Collection 1.* European Space Agency.

For citation in publications, ESA's standard form is: *"Contains modified Copernicus Sentinel data [YEAR]"* alongside the DOI.

### Host / Server

- **Main portal (GUI + docs):** <https://dataspace.copernicus.eu/>
- **Browser (interactive map + product selector):** <https://browser.dataspace.copernicus.eu/>
- **API documentation:** <https://documentation.dataspace.copernicus.eu/>
- **STAC catalog:** <https://stac.dataspace.copernicus.eu/> · <https://browser.stac.dataspace.copernicus.eu/>
- **OData endpoint:** `https://catalogue.dataspace.copernicus.eu/odata/v1/Products`
- **OpenSearch endpoint:** `https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json`
- **OAuth token endpoint:** `https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token`
- **Sentinel Hub Process API (alternative cloud-processing path):** <https://services.sentinel-hub.com/api/v1/process>
- **ESA SentiWiki product reference:** <https://sentiwiki.copernicus.eu/web/s2-products>

### Programmatic download

**Step 1 — Get an OAuth access token (the same token works for OData, STAC, and Sentinel Hub APIs):**

```bash
export CDSE_USER="your.email@example.org"
export CDSE_PASS="your_cdse_password"

TOKEN=$(curl -s -X POST \
  "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "username=${CDSE_USER}" \
  -d "password=${CDSE_PASS}" \
  -d "client_id=cdse-public" \
  | jq -r '.access_token')

echo "$TOKEN" | head -c 80; echo ...
```

**Step 2 — Search for recent L2A products covering Cluj via OData:**

```bash
# Last 7 days, low cloud cover, tile T34TFR
TODAY=$(date -u +%Y-%m-%dT00:00:00.000Z)
WEEK_AGO=$(date -u -d '7 days ago' +%Y-%m-%dT00:00:00.000Z)

curl -s -H "Authorization: Bearer ${TOKEN}" \
  "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?\$filter=Collection/Name%20eq%20%27SENTINEL-2%27%20and%20contains(Name,%27MSIL2A%27)%20and%20contains(Name,%27T34TFR%27)%20and%20ContentDate/Start%20gt%20${WEEK_AGO}%20and%20ContentDate/Start%20lt%20${TODAY}&\$orderby=ContentDate/Start%20desc&\$top=10" \
  | jq '.value[] | {Id, Name, ContentDate}'
```

**Step 3 — Download a specific product by ID (Product UUID from the previous query):**

```bash
PRODUCT_ID="<uuid from previous response>"
curl -L -H "Authorization: Bearer ${TOKEN}" \
  "https://zipper.dataspace.copernicus.eu/odata/v1/Products(${PRODUCT_ID})/\$value" \
  -o "${PRODUCT_ID}.zip"
```

**Python — minimal pattern using `requests`:**

```python
import os
import requests
from datetime import datetime, timedelta, timezone

CDSE_USER = os.environ["CDSE_USER"]
CDSE_PASS = os.environ["CDSE_PASS"]

def get_token():
    r = requests.post(
        "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        data={"grant_type": "password", "username": CDSE_USER,
              "password": CDSE_PASS, "client_id": "cdse-public"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]

def search_cluj_l2a(days_back=7, max_cloud=20):
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    flt = (
        f"Collection/Name eq 'SENTINEL-2' "
        f"and contains(Name,'MSIL2A') "
        f"and contains(Name,'T34TFR') "
        f"and ContentDate/Start gt {start} "
        f"and ContentDate/Start lt {end} "
        f"and Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/Value lt {max_cloud:.1f})"
    )
    r = requests.get(
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
        params={"$filter": flt, "$orderby": "ContentDate/Start desc", "$top": 20},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["value"]

def download_product(product_id, token, out_path):
    url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
    with requests.get(url, headers={"Authorization": f"Bearer {token}"},
                      stream=True, timeout=600) as resp:
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(1 << 20):  # 1 MB
                f.write(chunk)

if __name__ == "__main__":
    token = get_token()
    products = search_cluj_l2a(days_back=7, max_cloud=20)
    for p in products[:3]:
        out = f"{p['Name']}.zip"
        print("Downloading", out)
        download_product(p["Id"], token, out)
```

**Alternative — STAC API (modern, cleaner for new pipelines):**

```python
import pystac_client

cat = pystac_client.Client.open("https://stac.dataspace.copernicus.eu/")
search = cat.search(
    collections=["sentinel-2-l2a"],
    intersects={"type": "Point", "coordinates": [23.55, 46.77]},  # Cluj
    datetime="2026-05-01/2026-05-18",
    query={"eo:cloud_cover": {"lt": 20}},
)
items = list(search.items())
for item in items:
    print(item.id, item.properties["datetime"], item.properties["eo:cloud_cover"])
    # `item.assets` gives signed/unsigned URLs to individual band JP2s — can stream just the
    # bands you need with rasterio.open() rather than downloading the whole SAFE
```

**Reading a downloaded SAFE archive (Python):**

```python
import rioxarray as rxr

# Path to a single 10 m band's JP2 inside the SAFE
b04 = rxr.open_rasterio(
    "S2B_MSIL2A_20260518T091559_N0511_R094_T34TFR_20260518T120432.SAFE/"
    "GRANULE/L2A_T34TFR_A025814_20260518T091557/IMG_DATA/R10m/"
    "T34TFR_20260518T091559_B04_10m.jp2"
)
print(b04.shape, b04.rio.crs)   # native UTM zone 34N (EPSG:32634)
```

### Manual download (interactive web UI)

- **CDSE Browser (Cluj pre-filtered):** <https://browser.dataspace.copernicus.eu/?zoom=11&lat=46.7869&lng=23.5547&datasetId=S2_L2A_CDAS&themeId=DEFAULT-THEME>
- **Bulk catalog query:** <https://dataspace.copernicus.eu/explore-data>
- **STAC Browser:** <https://browser.stac.dataspace.copernicus.eu/collections/sentinel-2-l2a>

### Notes / caveats

- **File format correction.** The original docx labels Sentinel-2 data as "netcdf file". This is incorrect — Sentinel-2 products are delivered as **SAFE folders containing JPEG 2000 (`.jp2`) band rasters and XML metadata**, packaged as `.zip`. There is no NetCDF in the standard distribution. (Some derived analytics services emit NetCDF or COG, but the canonical product is SAFE/JP2.)
- **Constellation needs updating.** The docx mentions only "Sentinel 2" as a single platform. The current operational reality is: **S2B + S2C** (May 2026 onward), with **S2A** in transition phase Mar 2025 – Mar 2026. The 3-satellite period gave temporarily improved revisit; expect a return to the 5-day standard revisit from now. The Cluj input table should list both S2B and S2C explicitly.
- **MSI does not directly retrieve AOD** in the standard ESA processing chain. Its role in this project is two-fold: **(a)** the 10 m visible-band imagery provides high-detail visual evidence of pollution sources (industrial stacks, fires, urban dust events, snow cover affecting albedo) — this is what feeds the GUI / KG. **(b)** The per-band reflectance (L1C TOA or L2A BOA) is a candidate input for synergy retrievals with GRASP, alongside ground-based AERONET / lidar measurements; some research-grade aerosol retrievals using S2 reflectance have been published (e.g. MAJA, S2-MAJA, S2-AC4SR), but these are not standard CDSE products.
- **MGRS tile placement.** Cluj-Napoca falls in MGRS tile **T34TFR**. Worth verifying once before locking the pipeline (the city sits ~30 km from the tile centre, so the entire urban area is well within one tile, but the project's wider AOI may need T34TFQ or T34TGR depending on extent). The Sentinel-2 tile-grid KML from ESA is the authoritative source.
- **Sentinel Hub vs. raw OData.** For an operational warning chain that needs **only a small AOI** (Cluj-Napoca + surroundings, ~20 × 20 km), the **Sentinel Hub Process API** route is dramatically cheaper than downloading full ~1 GB SAFE products — you submit a JS-based "evalscript" describing the pixels you want, and the response is a few-MB GeoTIFF or PNG. The Process API is part of CDSE and the basic tier is free, with quotas. Worth evaluating for L3 pipeline design.
- **No L1B for users.** The Level-1B product (TOA radiance, un-orthorectified) is internal/expert-only. If your GRASP synergy retrieval needs radiance rather than reflectance, you'll need to convert L1C reflectance back to radiance using the metadata factors — straightforward, but not always documented for non-ESA workflows.
- **Cloud screening cost.** Sentinel-2 over Cluj is cloud-rejected ~50–70 % of the time across a year (Cluj is in a temperate-continental zone with frequent cloud cover, especially in winter). The pipeline must tolerate long gaps and not flag a missing S2 acquisition as a failure mode.
- **Per-tile UTM CRS.** T34TFR is in EPSG:32634 (UTM Zone 34N / WGS-84). Pixels are square in metres at this CRS. For mosaicking with other data sources on a global lat/lon grid, expect a single reprojection step at ingest; for any quantitative analysis (zonal stats, parcel-level aggregation), prefer working in the native UTM CRS rather than Web Mercator.
- **Migration from old SciHub.** Legacy users may have scripts pointing at `scihub.copernicus.eu` — that service is **deprecated as of 2023**. All new pipelines must use the CDSE endpoints listed above. Some third-party libraries (older versions of `sentinelsat`) still default to SciHub and will fail silently; pin recent versions or migrate to `sentinelhub-py` / `pystac-client`.
- **EU citation policy.** Open data under the Copernicus regulation. Required attribution: *"Contains modified Copernicus Sentinel data [YEAR]"* plus a DOI when available.

---
