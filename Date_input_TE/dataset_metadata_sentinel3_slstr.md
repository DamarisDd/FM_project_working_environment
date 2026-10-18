# Dataset metadata — Sentinel-3 SLSTR (SL_2_AOD NRT)

Companion documentation to the Stage 1 input-data table.
This file describes the Sentinel-3 Sea and Land Surface Temperature
Radiometer (SLSTR) standalone aerosol product (SL_2_AOD, NRT only, 9.5 km
super-pixel) feeding the Cluj-Napoca aerosol early-warning system.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

This is the natural NRT complement to the OLCI+SLSTR SYNergy product
(`SY_2_AOD`, NTC-only, 4.5 km) documented in the previous file.

---

## 9. Sentinel-3 SLSTR — Sea and Land Surface Temperature Radiometer (SL_2_AOD)

### Summary

| Field | Value |
|---|---|
| Instrument | **SLSTR** (Sea and Land Surface Temperature Radiometer) — **dual-view** conical scanning imaging radiometer. Successor to ENVISAT's AATSR series, with rotated 180° dual-view orientation, extended swath widths, and a **new SWIR channel at 2.25 µm** added vs. AATSR. **9 spectral channels** total: **6 solar channels (S1–S6)** spanning 0.55 → 2.25 µm at 500 m native resolution (channel S4 at 1.375 µm is dedicated to cirrus/cloud detection only), **3 thermal IR (S7–S9)** at 1 km, plus **2 dedicated fire channels (F1, F2)**. Dual-view = same surface seen near-simultaneously from **nadir** and **oblique (~55°)** — the geometric basis for SLSTR's atmospheric correction strength. |
| Network / Agency | **ESA** (instrument provider + L1B Land production) + **EUMETSAT** (operational dissemination + L1B Marine + L2 AOD/FRP production). The SL_2_AOD product is produced and distributed **exclusively by EUMETSAT** — it is *not* on Copernicus Data Space Ecosystem (CDSE). Access path differs from OLCI L1 and SY_2_AOD on that point. |
| Platforms | Same as OLCI: **Sentinel-3A** + **Sentinel-3B**, both flying SLSTR (designated SLSTR-A and SLSTR-B). The swath fully overlaps with OLCI's, enabling the synergy retrievals. |
| Product used | **SL_2_AOD** — SLSTR-only L2 NRT Aerosol Optical Depth, EUMETSAT Data Store collection `EO:EUM:DAT:0416`. Released in second half of 2020. Single measurement file `NRT_AOD.nc` inside the `.SEN3` archive. Includes AOD at multiple SLSTR solar wavelengths (all except S4), AOD uncertainty, fine/coarse mode parameters, surface reflectance contribution, quality flags, geolocation. |
| Resolution | **9.5 km × 9.5 km super-pixel** near nadir (correct in the docx). Native SLSTR L1B grid (500 m solar / 1 km thermal) is binned to super-pixels to satisfy the dual-view co-registration and signal-to-noise requirements of the retrieval. |
| Processing level | **Level-2** geophysical retrieval (aerosol optical properties). |
| File format | **Sentinel-SAFE folder** delivered as `.SEN3` archive (typically `.tar` or `.zip`). Contains a single `NRT_AOD.nc` measurement file (NetCDF4, CF-compliant) plus XML manifest and quality reports. Opens with `netCDF4` / `xarray` directly. |
| Filename pattern | `S3<X>_SL_2_AOD____<START>_<STOP>_<CREATION>_<INSTANCE>_<CYCLE>_<RELORBIT>______MAR_O_NR_<BASELINE>.SEN3` — e.g. `S3B_SL_2_AOD____20260518T091534_20260518T092034_20260518T112102_0299_096_321______MAR_O_NR_002.SEN3`. The `MAR` token indicates the Marine branch processor (EUMETSAT-operated, despite the product covering global land + ocean). Always `NR` (NRT) — **there is no NT/NTC variant** for SL_2_AOD. |
| Cluj coverage | SLSTR swath is **1420 km wide at nadir** (oblique view is narrower at ~750 km). Cluj is covered by every Sentinel-3 daytime descending pass at roughly 9:30–10:00 local time. With S3A + S3B, ~2 daytime overpasses per day with usable AOD over Cluj, weather permitting. **Daytime only** — retrieval requires solar zenith angle below 80°. |
| NRT availability | **YES, NRT only.** Products are available **in less than 3 hours after the SLSTR observation sensing time** (per EUMETSAT's official service-level statement). **There is no NTC variant** — the equivalent "consolidated" aerosol product is `SY_2_AOD` (OLCI+SLSTR synergy, ESA-produced, NTC-only, 4.5 km). The two products are complementary in timeliness and resolution, not redundant. |
| Authentication | **EUMETSAT EO Portal / Data Store account required** (free registration at <https://eoportal.eumetsat.int/>). API consumer key + secret pair generated at <https://api.eumetsat.int/api-key/>. **Separate registration from CDSE** — you cannot use a CDSE login here. |
| Programmatic access | YES — three paths: **(1) EUMETSAT Data Store REST API** (the recommended programmatic path); **(2) the EUMDAC Python library** (official wrapper for the Data Store API); **(3) EUMETCast Terrestrial / Satellite** (hardware-broadcast push service — for institutional users who need guaranteed delivery; requires DVB-S receiver or NREN multicast subscription). |
| Layer destination | **L2:** FLEXPART (NRT column-AOD constraint for transport modelling — fast-arriving data, fits an early-warning chain). HYSPLIT (NRT context for transport diagnostics and source attribution). **L3:** Knowledge Graph **NOT consumed** (9.5 km too coarse for urban-scale GUI display). GRASP: not used (synergy with ground-based only, doesn't ingest satellite AOD). |

### References

**Primary instrument / mission reference:**
- Donlon, C., Berruti, B., Buongiorno, A., Ferreira, M.-H., Féménias, P., Frerick, J., Goryl, P., Klein, U., Laur, H., Mavrocordatos, C., Nieke, J., Rebhan, H., Seitz, B., Stroede, J., & Sciarra, R. (2012). The Global Monitoring for Environment and Security (GMES) Sentinel-3 mission. *Remote Sensing of Environment*, 120, 37–57. DOI: [10.1016/j.rse.2011.07.024](https://doi.org/10.1016/j.rse.2011.07.024)

**SLSTR aerosol algorithm reference (cite when SL_2_AOD is used):**
- Pearson, K., North, P., Heckel, A., Hornero, A., Kinne, S., Popp, T., Sogacheva, L., & Griesfeller, J. (2025). Atmospheric aerosol measurements from the ATSR-SLSTR series of dual-view satellite instruments 1995–2022. *Scientific Data*, 12, 410. DOI: [10.1038/s41597-025-04694-6](https://doi.org/10.1038/s41597-025-04694-6)
- Algorithm: SDV (SLSTR Dual View) / SSV (SLSTR Single View) — joint development by Swansea University (Prof. Peter North) and EUMETSAT, building on FMI's earlier ADV algorithm for the (A)ATSR predecessors. Algorithm Theoretical Basis Document (ATBD): Kolmonen, P., Virtanen, T. H., Sogacheva, L., & Lipponen, A. (2024). ATBD Annex A2 SLSTR Dual and Single View Algorithm. Copernicus C3S2_312a_Lot2 (v4.1). Available via: <https://dast.data.compute.cci2.ecmwf.int/documents/satellite-aerosol-properties/>

**EUMETSAT product documentation:**
- SL_2_AOD product page: <https://www.eumetsat.int/S3-AOD>
- SARP study (SLSTR AOD retrieval performance): <https://www.eumetsat.int/SARP>
- ACES study (algorithm improvements): <https://www.eumetsat.int/aerosol-copernicus-eumetsat-swansea-aces>
- SentiWiki SLSTR products reference: <https://sentiwiki.copernicus.eu/web/slstr-products>

**ESA dataset citation format** (per Copernicus regulation): *"Contains modified Copernicus Sentinel-3 data [YEAR], processed by EUMETSAT"*. **Note the "by EUMETSAT" attribution** for SL_2_AOD — this differs from the "processed by ESA" attribution used for OLCI L1B and SY_2_AOD.

### Host / Server

- **EUMETSAT Data Store (browser):** <https://data.eumetsat.int/>
- **SL_2_AOD collection (direct):** <https://data.eumetsat.int/data/map/EO:EUM:DAT:0416>
- **Data Store API:** `https://api.eumetsat.int/data/`
- **API documentation:** <https://user.eumetsat.int/resources/user-guides/data-store-detailed-guide>
- **EUMDAC Python library:** <https://gitlab.eumetsat.int/eumetlab/data-services/eumdac>
- **API key generation:** <https://api.eumetsat.int/api-key/>
- **EUMETCast information (hardware-broadcast path):** <https://www.eumetsat.int/eumetcast>

### Programmatic download

**Setup — generate API credentials once:**

```bash
# 1) Register at https://eoportal.eumetsat.int/  (free)
# 2) Visit https://api.eumetsat.int/api-key/  and generate a "Consumer Key" + "Consumer Secret"
# 3) Store these as environment variables (do NOT commit to source control)
export EUMETSAT_KEY="your_consumer_key"
export EUMETSAT_SECRET="your_consumer_secret"
```

**Recommended path — EUMDAC Python library:**

```bash
pip install eumdac
```

```python
import eumdac
import os
from datetime import datetime, timedelta, timezone

# Auth
token = eumdac.AccessToken((os.environ["EUMETSAT_KEY"],
                            os.environ["EUMETSAT_SECRET"]))
datastore = eumdac.DataStore(token)

# SL_2_AOD collection
collection = datastore.get_collection("EO:EUM:DAT:0416")

# Search recent SL_2_AOD over Cluj
now = datetime.now(timezone.utc)
products = collection.search(
    bbox=(23.0, 46.3, 24.1, 47.2),  # Cluj small bbox
    dtstart=(now - timedelta(days=3)).isoformat(),
    dtend=now.isoformat(),
)

for p in products:
    print(p)            # filename
    print(p.sensing_start, p.sensing_end)
    # Download as a .zip archive
    with p.open() as src, open(f"{p}.zip", "wb") as dst:
        dst.write(src.read())
```

**Alternative — direct REST API with curl** (handy for shell scripts or operator debugging):

```bash
# 1) Get a Bearer token
TOKEN=$(curl -s -d "grant_type=client_credentials" \
  --user "${EUMETSAT_KEY}:${EUMETSAT_SECRET}" \
  "https://api.eumetsat.int/token" | jq -r '.access_token')

# 2) Search recent products covering Cluj
curl -s -H "Authorization: Bearer ${TOKEN}" \
  "https://api.eumetsat.int/data/search-products/1.0.0/os" \
  --data-urlencode 'pi=EO:EUM:DAT:0416' \
  --data-urlencode 'bbox=23.0,46.3,24.1,47.2' \
  --data-urlencode "dtstart=$(date -u -d '3 days ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --data-urlencode "dtend=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --data-urlencode 'format=json' \
  -G | jq '.features[] | {id: .id, sensing: .properties.date}'

# 3) Download a specific product by ID (replace PRODUCT_ID)
PRODUCT_ID="<id from search above>"
curl -L -H "Authorization: Bearer ${TOKEN}" \
  "https://api.eumetsat.int/data/download/1.0.0/collections/EO:EUM:DAT:0416/products/${PRODUCT_ID}" \
  -o "${PRODUCT_ID}.zip"
```

**Reading a SL_2_AOD file (Python):**

```python
import xarray as xr

# Inside the unzipped .SEN3 folder
prod_dir = "S3B_SL_2_AOD____20260518T091534_..._MAR_O_NR_002.SEN3"

ds = xr.open_dataset(f"{prod_dir}/NRT_AOD.nc")
print(ds.data_vars)
# Key variables include:
#   AOD_550  (or similar; check the netCDF metadata) — AOD at 550 nm super-pixel
#   AOD_550_uncertainty
#   quality flag fields
#   latitude / longitude per super-pixel

# Spatial subset to Cluj
lat = ds["latitude"].values
lon = ds["longitude"].values
mask = (lat > 46.3) & (lat < 47.2) & (lon > 23.0) & (lon < 24.1)
print(f"Super-pixels over Cluj: {mask.sum()}")  # typically 1-2 super-pixels for Cluj's footprint
```

### Manual download (interactive web UI)

- **Data Store browser (SL_2_AOD pre-filtered):** <https://data.eumetsat.int/data/map/EO:EUM:DAT:0416>
- **Search interface:** <https://data.eumetsat.int/search?query=SL_2_AOD>
- **Generic Data Store entry:** <https://data.eumetsat.int/> → filter Mission = Sentinel-3, Product type = "Aerosol Optical Depth"

### Notes / caveats

- **SL_2_AOD vs SY_2_AOD — pick the right one for the right job.** These two are not redundant. **SL_2_AOD** (this row): NRT-only (<3 h), 9.5 km, SLSTR-only, EUMETSAT-produced, distributed exclusively via EUMETSAT Data Store and EUMETCast. **SY_2_AOD** (OLCI row): NTC-only (~24–48 h), 4.5 km, OLCI+SLSTR synergy, ESA-produced, distributed via CDSE. For the early-warning chain, **SL_2_AOD is the Sentinel-3 first-alert source** (only NRT path); SY_2_AOD is the consolidation pass for retrospective analysis or higher-resolution validation.
- **Maturity status warning.** Per the official EUMETSAT product notice: SL_2_AOD **over ocean is "pre-operational"** and **over land is "demonstrational"** (as of last published baseline). This is a more cautious maturity label than e.g. MODIS Collection 6.1 DT or VIIRS V2.1. Translation for the project: use SL_2_AOD as **fast-but-coarse anomaly detection** rather than as quantitative ground truth. For absolute AOD values, prefer MODIS/VIIRS DT or SY_2_AOD with proper validation against AERONET CLUJ_UBB.
- **Known SLSTR vs MODIS bias.** SL_2_AOD(550 nm) is **systematically lower than MODIS Terra/Aqua DT Ocean C6.1 by 0.03–0.05** AOD units. After the v2.0 processor update (radiometric calibration correction + log-AOD fitting), this bias was slightly amplified by another 0.01–0.03 in open-ocean regions. Over thick Saharan dust plumes the new processor *reduces* AOD by up to 0.04 vs the old. For Cluj's continental urban-aerosol regime, expect a similar undershoot relative to MODIS — characterise once empirically before locking in absolute thresholds.
- **No CDSE distribution.** Important operational point: SL_2_AOD is **NOT on Copernicus Data Space Ecosystem**. The pipeline needs a separate EUMETSAT account + API key pair, in addition to the CDSE credentials used for Sentinel-2 MSI and Sentinel-3 OLCI L1/SY_2_AOD. Build credential rotation for **both** Keycloak (CDSE) and API-key (EUMETSAT) auth into the pipeline maintenance plan.
- **Daytime-only retrieval.** SZA < 80° gating means: at Cluj's latitude (~47° N), winter coverage drops noticeably — only the ~5 h around local noon is usable, December may have only one of the two daily Sentinel-3 passes qualifying. Account for this in expected granule counts.
- **Bonus product on the same instrument: SL_2_FRP (Fire Radiative Power).** Although the docx doesn't list it, SLSTR also produces an **NRT Fire Radiative Power product** (EUMETSAT-distributed, ~1 km hotspot detection), identifying location and radiative power of fires on land and ocean surfaces. **This is highly relevant to an aerosol warning chain** — wildfires are major regional aerosol sources, and an FRP detection upstream of Cluj (e.g. in the Balkans, Ukraine, or southern Romania) gives advance warning of an incoming smoke plume hours before the AOD anomaly arrives. Consider adding SL_2_FRP to the input list in a future revision of the table. EUMETSAT Data Store collection ID: `EO:EUM:DAT:0417`.
- **Why dual-view matters.** Conventional single-view AOD retrievals over land struggle because surface reflectance and atmospheric scattering are entangled in one TOA measurement. SLSTR's dual view (nadir + oblique 55°) gives two near-simultaneous measurements of the same surface with very different atmospheric path lengths, which lets the SDV algorithm separate surface from atmosphere without strong a-priori assumptions. **This is SLSTR's structural advantage over MODIS/VIIRS over bright urban surfaces** — which makes it especially relevant for an urban project like Cluj's. The 9.5 km resolution is the cost of the dual-view geometric registration.
- **No GRASP feed.** Despite the dual-view radiance information being theoretically valuable for GRASP synergy retrievals, the docx (correctly) doesn't route SLSTR to GRASP. GRASP at the project level uses ground-based AERONET + lidar synergy, and bringing SLSTR L1B radiances in would require a substantial additional integration effort beyond the Stage 1 scope.
- **EU citation policy.** Open data. Required attribution: *"Contains modified Copernicus Sentinel-3 data [YEAR], processed by EUMETSAT"* plus the algorithm reference (Pearson et al. 2025) when the AOD is used in publications or formal reports.

---
