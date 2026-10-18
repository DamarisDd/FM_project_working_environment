# Dataset metadata — Sentinel-5P TROPOMI

Companion documentation to the Stage 1 input-data table.
This file describes the Sentinel-5P TROPOMI products feeding the
Cluj-Napoca aerosol early-warning system. **Scope:** the seven products
listed in the input table — Level-1B TOA reflectance plus six Level-2
geophysical retrievals (NO₂, SO₂, CO, O₃, UV Aerosol Index, Aerosol Layer
Height).

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

This is the first of three closely-related entries on hyperspectral
nadir DOAS-class instruments: **(a)** TROPOMI on Sentinel-5P (this file),
**(b)** UVNS on Sentinel-5 / MetOp-SG-A (LEO operational successor, next
file), **(c)** UVN on Sentinel-4 / MTG-S (geostationary, third file).
Cross-reference the three when reading.

---

## 10. Sentinel-5P TROPOMI — Atmospheric composition (NRT + offline)

### Summary

| Field | Value |
|---|---|
| Instrument | **TROPOMI** (TROPOspheric Monitoring Instrument) — hyperspectral nadir-viewing pushbroom imaging spectrometer. Four physical spectrometers, **eight spectral bands** total: **UV** (270–320 nm), **UVIS** (310–405 nm), **VIS** (400–499 nm), **NIR** (685–775 nm), **SWIR-1** (1590–1675 nm), **SWIR-3** (2305–2385 nm), each split into two bands per detector. Heritage from SCIAMACHY, OMI, and GOME-2; designed to bridge the gap between OMI/Aura (still flying) and the future Copernicus Sentinel-4/Sentinel-5 operational missions. Swath: **2600 km (~108°)**, giving daily global coverage at latitudes |φ| > 7°. |
| Network / Agency | **ESA + Netherlands Space Office (NSO)** for the satellite + instrument. **KNMI** (Royal Netherlands Meteorological Institute) is the principal scientific institute and produces NO₂, CO, CH₄, AAI, ALH, O₃ profile (the "NL-L2" suite). **DLR** (Germany) produces SO₂, HCHO, O₃ total column, cloud, O₃ tropospheric (the "UPAS" suite). **BIRA-IASB** (Belgium) leads SO₂ algorithm and HCHO. Distribution via the **Copernicus Data Space Ecosystem (CDSE)**. |
| Platform (May 2026) | **Sentinel-5P (S5P)** — single satellite, launched **13 October 2017** from Plesetsk on a Rockot. Sun-synchronous orbit, **13:30 local ascending equator crossing**, in loose formation with **Suomi-NPP** (to share VIIRS cloud mask for the CH₄ retrieval). **Past 7-year design life** (nominal end Oct 2024) — operating under extended-mission grant. CEOS database lists current **EOL September 2027**. ESA/EUMETSAT are managing the transition to **Sentinel-5/UVNS on MetOp-SG-A1** (LEO operational successor, launching ~2026–2027). |
| Products used (7) | (1) **Reflectance** — L1B TOA reflectance from all 8 bands (`S5P_L1B_RA_BD<n>`). (2) **NO₂** — `L2__NO2___` total and tropospheric vertical column. (3) **SO₂** — `L2__SO2___` total column. (4) **CO** — `L2__CO____` total column. (5) **O₃** — `L2__O3____` total column (and optionally `L2__O3__PR` profile / `L2__O3_TCL` tropospheric column). (6) **UV AAI** — `L2__AER_AI` Absorbing Aerosol Index (UVAI). (7) **ALH** — `L2__AER_LH` Aerosol Layer Height. |
| Resolution | **5.5 × 3.5 km² since 6 August 2019** (was 7 × 3.5 km² before that date — operations scenario change improved along-track sampling). The docx lists "5.5 km" — that's the along-track dimension only. **At Cluj's latitude** (~47°N), pixel size is roughly **5.5 km along-track × ~4–5 km across-track** at the centre of the swath. SWIR products (CO, CH₄) at slightly coarser native resolution. |
| Processing level | All seven products are **L1B (reflectance) or L2** geophysical retrievals. No L3 gridded products in this row; gridding to a regular lat/lon grid is left to the user (typically with `harpconvert` — recommended ESA tool). |
| File format | **NetCDF4** (CF-compliant), one `.nc` file per orbit per product. Orbit granules cover ~50 minutes of sensing time. Variables follow the CCI/CF conventions: e.g. `nitrogendioxide_tropospheric_column`, `carbonmonoxide_total_column`, `aerosol_index_354_388`, `aerosol_mid_pressure` (for ALH). Quality flags as `qa_value` (0–1 scale, 0.5–0.75 is the recommended NO₂ threshold per van Geffen 2022). |
| Filename pattern | `S5P_<TIMELINESS>_L2__<PRODUCT>_<START>_<STOP>_<ORBIT>_<COLLECTION>_<PROCESSOR>_<PROCDATE>.nc` — e.g. `S5P_OFFL_L2__NO2____20260518T091534_20260518T105704_34812_03_020700_20260520T011242.nc`. **Timeliness tokens**: `NRTI` (Near Real Time), `OFFL` (Offline), `RPRO` (Reprocessed). |
| Cluj coverage | One usable daytime overpass per day at approximately **11:00–12:00 local time**. The 2600 km swath means Cluj is in the central portion of multiple consecutive orbits per day, but only the orbit closest in longitude gives an over-Cluj measurement at minimum zenith. ~365 useful daytime granules per year; cloud screening reduces this to roughly 150–200 useful retrievals per year for column-amount products (NO₂, SO₂, CO), more for UVAI (which is cloud-tolerant — see notes below). |
| NRT availability | **YES — NRTI in <3 hours** for all listed products except CH₄ (CH₄ is OFFL-only — not in this project's list). Offline (OFFL) reprocessing follows ~5–7 days later with consolidated calibration + auxiliaries. Periodic full-mission reprocessing campaigns (RPRO) align historical data with the current OFFL baseline. |
| Authentication | **CDSE account** (free) — same OAuth 2.0 / Keycloak flow as for Sentinel-2 MSI and Sentinel-3 OLCI. **Alternative path: AWS Open Data** at `s3://meeo-s5p` — no Earthdata-style auth, pay-by-egress for download (cheap for small AOI). |
| Programmatic access | YES — multiple paths: **(1) CDSE OData / OpenSearch** (the canonical Copernicus path); **(2) CDSE STAC API** at `https://stac.dataspace.copernicus.eu/` (Sentinel-5P collections); **(3) AWS Open Data S3** via `boto3` or `s3fs` (Sentinel-5P data are mirrored in S3 since 2020, also as Cloud-Optimized GeoTIFF for NRTI from 2020+); **(4) `harp` / `harpconvert`** — the official ESA atmospheric data conversion tool, handles L2-to-L3 gridding cleanly and is used by Google Earth Engine for its S5P collections. |
| Layer destination | **L2:** GRASP (Reflectance L1B for radiance synergy with AERONET — but mostly secondary to OLCI L1; AAI for absorbing-aerosol context); FLEXPART (NO₂, SO₂, CO as emission tracers for transport-model emission inversion; ALH as vertical-distribution constraint); HYSPLIT (column gases + UVAI as transport context). **L3:** Knowledge Graph (NO₂, SO₂, CO, O₃, UVAI for air-quality dashboard layers — at 5.5 km, fine enough to distinguish Cluj from surrounding rural areas in the GUI, but not enough for sub-urban resolution). |

### Per-product detail

| Product | Short name | Algorithm lead | Variable of interest | Cloud-tolerant? | Why used |
|---|---|---|---|---|---|
| Reflectance | `S5P_L1B_RA_BD<n>` (n=1..8) | KNMI | per-band TOA radiance / reflectance | n/a | Synergy reflectance for GRASP-style retrievals; cross-validation against OLCI |
| NO₂ | `L2__NO2___` | KNMI (van Geffen / Eskes) | `nitrogendioxide_tropospheric_column` | Cloud-sensitive (use `qa_value > 0.75`) | Urban traffic + industrial emissions; daily NO₂ maps over Cluj are a leading indicator |
| SO₂ | `L2__SO2___` | DLR/BIRA (Theys) | `sulfurdioxide_total_vertical_column` | Cloud-sensitive | Industrial point sources (regional power stations); volcanic ash plume monitoring (relevant for aviation alerts) |
| CO | `L2__CO____` | SRON (Borsdorff) | `carbonmonoxide_total_column` | More cloud-tolerant (SWIR sees through thin cirrus) | Biomass-burning tracer; long-range smoke transport from regional fires |
| O₃ | `L2__O3____` | DLR (Garane) | `ozone_total_vertical_column` | Cloud-sensitive | UV radiation health context; stratospheric vs tropospheric partitioning if profile product is also ingested |
| UV AAI | `L2__AER_AI` | KNMI (Stein Zweers / Tilstra) | `aerosol_index_354_388`, `aerosol_index_340_380`, `aerosol_index_335_367` (since v2.4) | **Yes — UVAI works through clouds.** | Dust + smoke + volcanic-ash flag at daily global coverage; complements MODIS DT/MAIAC AOD (cloud-rejected) |
| ALH | `L2__AER_LH` | KNMI (Nanda) | `aerosol_mid_pressure`, `aerosol_mid_height` | Cloud-sensitive | **Critical for the warning chain**: tells you whether a smoke plume is at surface (impacts air quality at Cluj) or aloft (transport only) |

### References

**Mission reference (cite TROPOMI in any deliverable):**
- Veefkind, J. P., Aben, I., McMullan, K., Förster, H., de Vries, J., Otter, G., Claas, J., Eskes, H. J., de Haan, J. F., Kleipool, Q., van Weele, M., Hasekamp, O., Hoogeveen, R., Landgraf, J., Snel, R., Tol, P., Ingmann, P., Voors, R., Kruizinga, B., Vink, R., Visser, H., & Levelt, P. F. (2012). TROPOMI on the ESA Sentinel-5 Precursor: A GMES mission for global observations of the atmospheric composition for climate, air quality and ozone layer applications. *Remote Sensing of Environment*, 120, 70–83. DOI: [10.1016/j.rse.2011.09.027](https://doi.org/10.1016/j.rse.2011.09.027)

**Per-product algorithm references (cite when each product is used):**
- **NO₂:** van Geffen, J., Eskes, H., Compernolle, S., Pinardi, G., Verhoelst, T., Lambert, J.-C., Sneep, M., ter Linden, M., Ludewig, A., Boersma, K. F., & Veefkind, J. P. (2022). Sentinel-5P TROPOMI NO₂ retrieval: impact of version v2.2 improvements and comparisons with OMI and ground-based data. *Atmospheric Measurement Techniques*, 15, 2037–2060. DOI: [10.5194/amt-15-2037-2022](https://doi.org/10.5194/amt-15-2037-2022)
- **SO₂:** Theys, N., De Smedt, I., Yu, H., Danckaert, T., van Gent, J., Hörmann, C., Wagner, T., Hedelt, P., Bauer, H., Romahn, F., Pedergnana, M., Loyola, D., & Van Roozendael, M. (2017). Sulfur dioxide retrievals from TROPOMI onboard Sentinel-5 Precursor: algorithm theoretical basis. *Atmospheric Measurement Techniques*, 10, 119–153. DOI: [10.5194/amt-10-119-2017](https://doi.org/10.5194/amt-10-119-2017)
- **CO:** Borsdorff, T., aan de Brugh, J., Hu, H., Aben, I., Hasekamp, O., & Landgraf, J. (2018). Measuring carbon monoxide with TROPOMI: First results and a comparison with ECMWF-IFS analysis data. *Geophysical Research Letters*, 45, 2826–2832. DOI: [10.1002/2018GL077045](https://doi.org/10.1002/2018GL077045)
- **O₃ total column:** Garane, K., Koukouli, M.-E., Verhoelst, T., et al. (2019). TROPOMI/S5P total ozone column data: global ground-based validation and consistency with other satellite missions. *Atmospheric Measurement Techniques*, 12, 5263–5287. DOI: [10.5194/amt-12-5263-2019](https://doi.org/10.5194/amt-12-5263-2019)
- **UV AAI (UVAI):** Stein Zweers, D. C. (2024). TROPOMI ATBD of the UV Aerosol Index. S5P-KNMI-L2-0008-RP, v2.2.0. Available via the ESA TROPOMI document library.
- **ALH:** Nanda, S., de Graaf, M., Veefkind, J. P., Sneep, M., ter Linden, M., Sun, J., & Levelt, P. F. (2020). A first comparison of TROPOMI aerosol layer height (ALH) to CALIOP data. *Atmospheric Measurement Techniques*, 13, 3043–3059. DOI: [10.5194/amt-13-3043-2020](https://doi.org/10.5194/amt-13-3043-2020)

**ESA dataset citation format**: *"Contains modified Copernicus Sentinel-5P data [YEAR], processed by ESA/KNMI/DLR"*.

### Host / Server

- **Copernicus Data Space Ecosystem (canonical path):** <https://dataspace.copernicus.eu/>
- **CDSE Sentinel-5P documentation:** <https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel5P.html>
- **CDSE Browser:** <https://browser.dataspace.copernicus.eu/?datasetId=S5P_NO2>
- **CDSE STAC catalog:** <https://stac.dataspace.copernicus.eu/> (Sentinel-5P collections under `sentinel-5p-l2-...`)
- **TROPOMI mission site (algorithm + validation):** <https://www.tropomi.eu/>
- **S5P Mission Performance Centre product readme files:** <https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-5p-tropomi/document-library>
- **S5P L2 Quality Control portal:** <https://mpc-l2qc.tropomi.eu/>
- **S5P Validation Data Analysis Facility:** <https://mpc-vdaf.tropomi.eu/>
- **AWS Open Data (S3 bucket, no auth for read):** `s3://meeo-s5p/` — see <https://meeo-s5p.s3.amazonaws.com/index.html>
- **NASA GES DISC alternative mirror** (a subset of products): <https://disc.gsfc.nasa.gov/datasets?keywords=S5P_TROPOMI>

### Programmatic download

**CDSE OData (recommended — same auth as Sentinel-2/Sentinel-3):**

```python
import os, requests
from datetime import datetime, timedelta, timezone

CDSE_USER = os.environ["CDSE_USER"]; CDSE_PASS = os.environ["CDSE_PASS"]

def get_token():
    r = requests.post(
        "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        data={"grant_type": "password", "username": CDSE_USER,
              "password": CDSE_PASS, "client_id": "cdse-public"},
        timeout=30); r.raise_for_status()
    return r.json()["access_token"]

def search_s5p(product_short: str, timeliness: str = "OFFL",
               days_back: int = 3, max_results: int = 50):
    """product_short like 'L2__NO2___', 'L2__AER_AI', 'L2__AER_LH', etc."""
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end   = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    cluj_wkt = "POLYGON((23.0 46.3,24.1 46.3,24.1 47.2,23.0 47.2,23.0 46.3))"
    flt = (
        f"Collection/Name eq 'SENTINEL-5P' "
        f"and contains(Name,'{product_short}') "
        f"and contains(Name,'{timeliness}') "
        f"and OData.CSC.Intersects(area=geography'SRID=4326;{cluj_wkt}') "
        f"and ContentDate/Start gt {start} "
        f"and ContentDate/Start lt {end}"
    )
    r = requests.get(
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
        params={"$filter": flt, "$orderby": "ContentDate/Start desc",
                "$top": max_results},
        timeout=60); r.raise_for_status()
    return r.json()["value"]

# Pull NO2 NRTI over Cluj for the last 24 hours
no2_nrti = search_s5p("L2__NO2___", "NRTI", days_back=1)
print(f"{len(no2_nrti)} NO2 NRTI granules")

# Pull all seven products as OFFL for the last week
products = ["L1B_RA_BD3", "L2__NO2___", "L2__SO2___", "L2__CO____",
            "L2__O3____", "L2__AER_AI", "L2__AER_LH"]
for p in products:
    hits = search_s5p(p, "OFFL", days_back=7)
    print(f"{p:18s}: {len(hits):4d}")
```

**Download (same OData pattern as Sentinel-2/3):**

```python
def download_s5p(product_id, token, out_path):
    url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
    with requests.get(url, headers={"Authorization": f"Bearer {token}"},
                      stream=True, timeout=600) as resp:
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(1 << 20):
                f.write(chunk)
```

**Alternative — AWS Open Data S3 (no CDSE auth needed):**

```python
import s3fs
fs = s3fs.S3FileSystem(anon=True)

# List today's NO2 OFFL files
today = "2026/05/18"   # YYYY/MM/DD
files = fs.ls(f"s3://meeo-s5p/OFFL/L2__NO2___/{today}/")
print(f"{len(files)} files")

# Stream / download one
with fs.open(files[0], "rb") as src, open("no2.nc", "wb") as dst:
    dst.write(src.read())
```

**Reading + spatial subsetting (Python):**

```python
import xarray as xr
import numpy as np

# NO2 L2 file
ds = xr.open_dataset("S5P_OFFL_L2__NO2____20260518T091534_..._020700_....nc",
                     group="PRODUCT")

print(ds.data_vars)  # nitrogendioxide_tropospheric_column, qa_value, ...

# Coordinates are stored as 2-D arrays (scanline × ground_pixel)
lat = ds["latitude"].values     # shape (n_scanlines, n_ground_pixels)
lon = ds["longitude"].values
no2 = ds["nitrogendioxide_tropospheric_column"].values
qa  = ds["qa_value"].values

# Spatial mask to Cluj
mask = ((lat > 46.3) & (lat < 47.2) &
        (lon > 23.0) & (lon < 24.1) &
        (qa > 0.75))   # KNMI-recommended quality threshold for NO2
cluj_no2 = no2[mask]
print(f"Cluj NO2 retrievals: {cluj_no2.size}  mean = {np.nanmean(cluj_no2):.3e} mol/m^2")
```

**Convert L2 to a regular L3 lat/lon grid with harpconvert (recommended ESA tool):**

```bash
pip install harp
```

```bash
harpconvert --format netcdf \
  -a 'tropospheric_NO2_column_number_density_validity > 75; \
       derive(datetime_stop {time}); \
       bin_spatial(91, 46.3, 0.01, 121, 23.0, 0.01); \
       keep(NO2_column_number_density, tropospheric_NO2_column_number_density)' \
  S5P_OFFL_L2__NO2____*.nc \
  cluj_no2_gridded.nc
# Output: regular 0.01° grid covering 46.3-47.2 N, 23.0-24.2 E
```

### Manual download (interactive web UI)

- **CDSE Browser (S5P NO2 over Cluj):** <https://browser.dataspace.copernicus.eu/?datasetId=S5P_L2_NO2&zoom=10&lat=46.77&lng=23.55>
- **TROPOMI Monitoring Portal:** <https://mpc-l1cal.tropomi.eu/>
- **AWS Open Data S3 browser:** <https://meeo-s5p.s3.amazonaws.com/index.html#OFFL/L2__NO2___/>

### Notes / caveats

- **Resolution clarification.** The docx labels all S5P products at "5.5 km". This is the **along-track** dimension only; the actual pixel size is **5.5 × 3.5 km²** since the operations scenario change of **6 August 2019** (was 7 × 3.5 km² before that date). For pre-2019-08-06 data the along-track sampling is coarser — relevant only if the project ingests historical data for retrospective analysis or trend studies.
- **Satellite past design life — succession planning matters.** Sentinel-5P was designed for 7 years and is now in year 9 (May 2026). CEOS lists current EOL as September 2027, but instrument or platform anomalies could shorten that. The operational successor is **Sentinel-5/UVNS on MetOp-SG-A1** (next file), expected to launch in 2026–2027 with full operational data flowing shortly after commissioning. There may be a continuity gap. The project should plan a transition window where both data streams are tracked, and ingest code is parameterised on instrument-source rather than hard-coded for TROPOMI.
- **NRTI vs OFFL.** All seven products in this row have both NRTI (<3 h) and OFFL (5–7 days later) versions, except for CH₄ which is OFFL-only (and not in this project's list). NRTI uses preliminary calibration + forecast ECMWF; OFFL uses consolidated calibration + analysis ECMWF. **Differences are typically small for NO₂, SO₂, CO, UVAI; can be larger for ALH** because the ALH retrieval is more sensitive to surface-albedo and absorbing-aerosol assumptions that are refined in OFFL. Recommended pipeline pattern: ingest NRTI for the live warning chain, overwrite with OFFL when it arrives.
- **AAI is uniquely cloud-tolerant — this matters operationally.** The UV Aerosol Index works on **wavelength-dependent residuals in Rayleigh scattering**, not on direct AOD retrieval. It functions in the presence of clouds, gives daily global coverage, and detects UV-absorbing aerosols (dust, smoke, volcanic ash). For Cluj this means **UVAI is the only "real-time aerosol detector" from S5P that survives cloudy days** — critical for the warning chain. The downside: UVAI is qualitative (a residual index, not an optical depth), and is positively correlated with both AOD and aerosol layer height. So a high UVAI tells you "absorbing aerosol is present somewhere in the column"; the **AAI + ALH combination** disambiguates whether the plume is at surface (health-relevant) or aloft (transport-relevant). Use both together.
- **ALH limitations.** Per Nanda 2020 validation against CALIOP, TROPOMI ALH retrieves typical biases of ±0.5–1 km vs CALIOP for opaque biomass-burning plumes over ocean, and is **considerably worse over bright land surfaces** (Cluj's mid-latitude continental terrain falls in this category). The product is best treated as a coarse indicator rather than a precise height — use it for "near-surface vs elevated" binary classification, not for precise injection-height estimation.
- **qa_value thresholds matter and vary per product.** Standard recommended thresholds: NO₂ `qa_value > 0.75`, SO₂ `qa_value > 0.5`, CO `qa_value > 0.5`, O₃ `qa_value > 0.5`, AAI generally no strict threshold (it's robust), ALH `qa_value > 0.5`. Apply these at ingest; downstream code should not assume all delivered pixels are equally trustworthy.
- **Format and tooling.** All products are NetCDF4 in CF conventions, but in a **two-level group structure**: the main data group is `/PRODUCT/`, with `/PRODUCT/SUPPORT_DATA/` and `/METADATA/` siblings. `xarray.open_dataset(..., group="PRODUCT")` is the correct call. **`harp` / `harpconvert`** (an ESA-funded tool) is the canonical way to convert L2 to a regular L3 grid — Google Earth Engine's S5P L3 collections are produced this way. Don't reinvent the gridding wheel.
- **CDSE replaced s5phub.** Some older documentation still references the legacy "Sentinel-5P Pre-Operations Data Hub" at `https://s5phub.copernicus.eu/` — that service was retired and migrated to CDSE. Update any pipeline code that points to `s5phub`.
- **AWS Open Data as a backup path.** S3 bucket `s3://meeo-s5p/` mirrors all S5P L2 products without authentication. Useful as a fallback if CDSE has an outage, or for cloud-native pipelines running in AWS. NRTI from 2020 onwards is also available as Cloud-Optimized GeoTIFF in addition to NetCDF.
- **Suomi-NPP synergy is for CH₄, not for AAI/ALH.** The S5P orbit is phased behind Suomi-NPP specifically so that VIIRS's cloud mask can be used by the CH₄ retrieval algorithm. This synergy does not affect the seven products in this row.
- **EU citation policy.** Open data. Required attribution: *"Contains modified Copernicus Sentinel-5P data [YEAR], processed by ESA / KNMI / DLR"* (use the institutional acknowledgement appropriate to each product — KNMI for NL-L2 suite, DLR/BIRA for UPAS suite).

---
