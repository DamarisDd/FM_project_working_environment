# Dataset metadata — Sentinel-3 OLCI + SYNergy AOD

Companion documentation to the Stage 1 input-data table.
This file describes the Sentinel-3 Ocean and Land Colour Instrument (OLCI)
products feeding the Cluj-Napoca aerosol early-warning system. **Scope:** the
OLCI Level-1B Earth Observation Full Resolution (TOA reflectance, 300 m) and
the OLCI+SLSTR SYNergy Level-2 Aerosol Optical Depth product (4.5 km).

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 8. Sentinel-3 OLCI — Ocean and Land Colour Instrument + SYN AOD

### Summary

| Field | Value |
|---|---|
| Instrument | **OLCI** (Ocean and Land Colour Instrument) — medium-resolution push-broom imaging spectrometer with **21 spectral bands** ranging 400–1020 nm (visible + near-IR), using a 5-camera fan to deliver a wide 1270 km swath. Native ground sampling: **300 m**. Heritage from Envisat MERIS, with extended spectral range and improved calibration. Swath is tilted 12.6° westwards relative to nadir to mitigate sun-glint contamination. Field of view fully overlaps with SLSTR — enabling the synergy retrievals below. |
| Network / Agency | **ESA + EUMETSAT** (joint Copernicus operation). ESA handles the L1B production for **land** products, EUMETSAT handles L1B production for **marine** products and the operational dissemination. Atmosphere products (incl. SY_2_AOD) are produced by ESA. |
| Platforms (currently operational, May 2026) | **Sentinel-3A** (launched 16 Feb 2016, EOL nominally December 2026 per CEOS database — nearing end of mission but still nominal). **Sentinel-3B** (launched 25 Apr 2018, operational). The two fly in the same orbit 140° apart, giving OLCI 2-day global coverage at the equator. **Sentinel-3C** is scheduled for launch in **September 2026** from Kourou on Vega-C — not yet operational; **Sentinel-3D** in 2028. The docx mentions Sentinel-3 as a single entry; **the table should note A + B as the current operational constellation.** |
| Products used | **(a) OL_1_EFR — OLCI Earth Observation Full Resolution Level-1B.** Calibrated, orthorectified, geolocated TOA radiances at 300 m for all 21 bands, with per-pixel per-band uncertainties (from ESA processing baseline OL_L1_.003.03.00 and later). Used as the per-band reflectance input for GRASP-style synergy retrievals. **(b) SY_2_AOD — SYNergy Aerosol Optical Depth Level-2** (OLCI + SLSTR combined). Aerosol optical depth at 440, 550, 670, 985, 1600, 2250 nm at 4.5 km "super-pixel" resolution, plus single-scattering albedo, fine-mode AOD, Ångström parameter (550–865 nm), dust AOD, aerosol absorption optical depth, atmospherically corrected nadir surface directional reflectance. Used by FLEXPART / HYSPLIT as column-AOD constraint. |
| Important nomenclature correction | The docx labels the 4.5 km AOD row as "OLCI". **This is technically the OLCI+SLSTR SYNergy product** (`SY_2_AOD`), not OLCI alone. Algorithmically it relies primarily on **SLSTR** (both nadir and oblique views, all channels except S4 at 1.37 µm which is reserved for cloud detection) plus **one OLCI channel** (Oa3 at 442.5 nm). So calling it "OLCI AOD" is misleading — the table should label it `SY_2_AOD (OLCI+SLSTR)` for technical accuracy, even though the row stays under the OLCI group. |
| Current collection / baseline | OLCI L1B processing baseline `OL_L1_.003.03.00` (ESA-side, deployed 25 July 2023 for S3A; 18 July 2023 for S3B) and `OL_L1_.002.25.00` (EUMETSAT-side). New baseline deployed **7 April 2025** for both satellites for OLCI L1, SLSTR L1, and SY products — bug fixes + auxiliary data updates. SY_2_AOD operational since 8 April 2021 (sensing data from 6 April 2021); historical back to 19 February 2020 in the archive. |
| Processing level | OL_1_EFR is **Level-1B** (calibrated geolocated TOA radiances). SY_2_AOD is **Level-2** (geophysical retrieval). |
| File format | **Sentinel-SAFE folder** delivered as a `.SEN3` archive (typically `.zip` or `.tar`), containing **NetCDF4 (.nc)** measurement files plus an XML manifest. One `.nc` file per spectral band for OL_1_EFR plus separate files for geolocation, tie-points, and quality flags. For SY_2_AOD, a single measurement `.nc` plus annotation files. CF-compliant; opens with `netCDF4`, `xarray`, or ESA's SNAP toolbox. **This is genuinely NetCDF**, in contrast to the JP2-based Sentinel-2 SAFE — the docx's NRT/format hints for OLCI are correct. |
| Filename pattern | `S3<X>_OL_1_EFR____<START>_<STOP>_<CREATION>_<INSTANCE>_<CYCLE>_<RELORBIT>_<FRAME>_<CENTRE>_O_<TIMELINESS>_<BASELINE>.SEN3` — e.g. `S3B_OL_1_EFR____20260518T091534_20260518T091834_20260518T120119_0179_096_321_2160_PS2_O_NR_004.SEN3`. The timeliness suffix is **`NR`** (NRT), **`ST`** (Short Time Critical), or **`NT`** (Non-Time Critical). SY_2_AOD analogous with `SY_2_AOD____` token; SY_2_AOD is **NT only** (no NRT variant). |
| Cluj coverage | OLCI swath is 1270 km wide — Cluj is covered by every Sentinel-3 daytime descending pass over central Europe. With S3A + S3B together, OLCI overflies Cluj at roughly **9:30–10:00 local time** roughly every 1–2 days (weather permitting). One useful daytime overpass per platform per orbit cycle through Cluj's longitude band. |
| NRT availability (different per product!) | **OL_1_EFR: YES, NRT in <3 hours.** The same scene is later reprocessed as NTC (~24–48 h) with consolidated orbit + analysis ECMWF auxiliaries; the L1 radiance values are identical between NRT and NTC. **SY_2_AOD: NO NRT — NTC only**, delivered ~24–48 h after acquisition. Atmosphere processing requires consolidated auxiliaries (precise orbits, full ECMWF analysis fields). The docx implies generic "OLCI NRT yes" — needs splitting per product. |
| Authentication | **CDSE account** (free) for ESA-distributed products, **EUMETSAT EO Portal account** (separate free registration) for EUMETSAT-distributed products. Many products are available from both portals; the SY_2_AOD is on CDSE. OLCI L1B is dual-distributed. OAuth 2.0 access tokens (same Keycloak flow as for Sentinel-2). |
| Programmatic access | YES — multiple paths: **CDSE OData** (`https://catalogue.dataspace.copernicus.eu/odata/v1/Products`), **CDSE STAC** (`https://stac.dataspace.copernicus.eu/`), **EUMETSAT Data Store API** (`https://api.eumetsat.int/data/`), **EUMETCast** (push-based broadcast, hardware required), **EUMDAC** Python library (`pip install eumdac` — convenient wrapper for the EUMETSAT API). For a research/operational pipeline at Cluj, CDSE OData or STAC is the simpler choice. |
| Layer destination | **L2:** GRASP (per-band OLCI TOA reflectance for synergy with AERONET — the table's "Reflectanță" sub-row). FLEXPART (SY_2_AOD column-integrated constraint for transport modeling). HYSPLIT (SY_2_AOD context for transport diagnostics — the table's "AOD 4.5 km" sub-row). **L3:** Knowledge Graph **NOT consumed** for AOD (4.5 km too coarse for urban-scale GUI). The L1B reflectance could in principle feed visual evidence in the GUI but at 300 m it's coarser than Sentinel-2 MSI (10 m) — MSI is the better source for visual KG inputs. |

### References

**Primary mission reference:**
- Donlon, C., Berruti, B., Buongiorno, A., Ferreira, M.-H., Féménias, P., Frerick, J., Goryl, P., Klein, U., Laur, H., Mavrocordatos, C., Nieke, J., Rebhan, H., Seitz, B., Stroede, J., & Sciarra, R. (2012). The Global Monitoring for Environment and Security (GMES) Sentinel-3 mission. *Remote Sensing of Environment*, 120, 37–57. DOI: [10.1016/j.rse.2011.07.024](https://doi.org/10.1016/j.rse.2011.07.024)

**SYNergy AOD validation reference (cite when SY_2_AOD is used):**
- Sogacheva, L., Popp, T., Sayer, A. M., Dubovik, O., Garay, M. J., Heckel, A., Hsu, N. C., Jethva, H., Kahn, R. A., Kolmonen, P., Kosmale, M., de Leeuw, G., Levy, R. C., Litvinov, P., Lyapustin, A., North, P., Torres, O., & Arola, A. (2022). Extended validation and evaluation of the OLCI–SLSTR SYNERGY aerosol product (SY_2_AOD) on Sentinel-3. *Atmospheric Measurement Techniques*, 15(17), 5289–5314. DOI: [10.5194/amt-15-5289-2022](https://doi.org/10.5194/amt-15-5289-2022)

**OLCI product technical references:**
- ESA Sentinel-3 OLCI Marine User Handbook: <https://earth.esa.int/eogateway/documents/20142/1564943/Sentinel-3-OLCI-Marine-User-Handbook.pdf>
- ESA Sentinel-3 Product Notice SY_2_AOD: <https://sentinel.esa.int/documents/d/sentinel/s3-pn-syn-aod-02-i1r0-syn-aod-l2-aod_ntc-002-08-01->
- SentiWiki OLCI Products: <https://sentiwiki.copernicus.eu/web/olci-products>

**ESA dataset citation format** (per Copernicus regulation): *"Contains modified Copernicus Sentinel-3 data [YEAR], processed by ESA/EUMETSAT"*

### Host / Server

**ESA / Copernicus side:**
- Copernicus Data Space Ecosystem: <https://dataspace.copernicus.eu/>
- Browser: <https://browser.dataspace.copernicus.eu/>
- STAC catalog (OLCI L1 EFR NTC): <https://browser.stac.dataspace.copernicus.eu/collections/sentinel-3-olci-1-efr-ntc>
- OData endpoint: `https://catalogue.dataspace.copernicus.eu/odata/v1/Products`
- ESA OLCI technical docs: <https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-olci>

**EUMETSAT side:**
- EUMETSAT Data Store: <https://data.eumetsat.int/>
- Data Store API documentation: <https://user.eumetsat.int/data/data-store-search-and-download>
- Product Navigator (OLCI L1 EFR NRT): <https://navigator.eumetsat.int/product/EO:EUM:DAT:SENTINEL-3:OL_1_EFR___NRT>
- EUMDAC Python library: <https://gitlab.eumetsat.int/eumetlab/data-services/eumdac>

### Programmatic download

**OAuth token (CDSE — same flow as for Sentinel-2):**

```bash
export CDSE_USER="your.email@example.org"
export CDSE_PASS="your_cdse_password"

TOKEN=$(curl -s -X POST \
  "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" -d "username=${CDSE_USER}" \
  -d "password=${CDSE_PASS}" -d "client_id=cdse-public" \
  | jq -r '.access_token')
```

**Search recent OLCI L1 EFR + SY_2_AOD products over Cluj (OData):**

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

def search_s3_over_cluj(short_pattern: str, days_back: int = 3):
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end   = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # Cluj bbox (small to limit hits)
    cluj_wkt = "POLYGON((23.0 46.3,24.1 46.3,24.1 47.2,23.0 47.2,23.0 46.3))"
    flt = (
        f"Collection/Name eq 'SENTINEL-3' "
        f"and contains(Name,'{short_pattern}') "
        f"and OData.CSC.Intersects(area=geography'SRID=4326;{cluj_wkt}') "
        f"and ContentDate/Start gt {start} "
        f"and ContentDate/Start lt {end}"
    )
    r = requests.get(
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
        params={"$filter": flt, "$orderby": "ContentDate/Start desc", "$top": 50},
        timeout=60); r.raise_for_status()
    return r.json()["value"]

# OLCI L1 Full Resolution (NRT only — 'NR' in name)
efr_nrt = search_s3_over_cluj("OL_1_EFR")  # matches all timeliness; filter further by name
# SYNergy AOD (NTC only)
syn_aod = search_s3_over_cluj("SY_2_AOD")
print(f"{len(efr_nrt)} OL_1_EFR / {len(syn_aod)} SY_2_AOD")
```

**Download a product (same OData pattern as Sentinel-2):**

```python
def download_product(product_id, token, out_path):
    url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
    with requests.get(url, headers={"Authorization": f"Bearer {token}"},
                      stream=True, timeout=900) as resp:
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(1 << 20):
                f.write(chunk)
```

**Alternative — EUMETSAT EUMDAC for OLCI L1 (often simpler if you only need L1):**

```bash
pip install eumdac
```

```python
import eumdac

# Get credentials at https://api.eumetsat.int/api-key/
token = eumdac.AccessToken(("CONSUMER_KEY", "CONSUMER_SECRET"))
ds = eumdac.DataStore(token)
coll = ds.get_collection("EO:EUM:DAT:SENTINEL-3:OL_1_EFR___NRT")

products = coll.search(
    bbox=(23.0, 46.3, 24.1, 47.2),
    dtstart="2026-05-15T00:00:00",
    dtend="2026-05-18T23:59:59",
)
for p in products:
    print(p)
    with p.open() as src, open(f"{p}.zip", "wb") as dst:
        dst.write(src.read())
```

**Reading an OLCI L1 EFR product (Python):**

```python
import xarray as xr

# Inside the unzipped .SEN3 folder
prod_dir = "S3B_OL_1_EFR____20260518T091534_..._O_NR_004.SEN3"

# Each band is its own NetCDF; load Oa08 (665 nm, useful for true-colour)
oa08 = xr.open_dataset(f"{prod_dir}/Oa08_radiance.nc")
geo  = xr.open_dataset(f"{prod_dir}/geo_coordinates.nc")

print(oa08.data_vars)              # Oa08_radiance + uncertainty
print(geo["latitude"].shape)       # full image grid lat/lon
```

**Reading a SY_2_AOD product (Python):**

```python
import xarray as xr

prod_dir = "S3B_SY_2_AOD____20260517T090432_..._O_NT_005.SEN3"
ds = xr.open_dataset(f"{prod_dir}/NTC_AOD.nc")
print(ds.data_vars)   # AOD at 440/550/670/985/1600/2250 nm + uncertainties + ancillary

# Spatial subset to Cluj
mask = ((ds["latitude"] > 46.3) & (ds["latitude"] < 47.2) &
        (ds["longitude"] > 23.0) & (ds["longitude"] < 24.1))
aod_550_cluj = ds["T550"].where(mask)   # T550 = AOD at 550 nm in the SY_2_AOD product
```

### Manual download (interactive web UI)

- **CDSE Browser (Cluj pre-filtered, OLCI L1):** <https://browser.dataspace.copernicus.eu/?datasetId=S3OLCI_L1_EFR&zoom=10&lat=46.77&lng=23.55>
- **CDSE STAC Browser:** <https://browser.stac.dataspace.copernicus.eu/collections/sentinel-3-olci-1-efr-ntc>
- **EUMETSAT Data Store:** <https://data.eumetsat.int/> (search for OL_1_EFR or SY_2_AOD with bbox filter)

### Notes / caveats

- **OLCI vs. SY_2_AOD nomenclature.** The 4.5 km AOD product in the docx's "OLCI" row is the **OLCI+SLSTR synergy** (`SY_2_AOD`), not a stand-alone OLCI retrieval. Algorithmically it's mostly SLSTR (both views, all solar bands) + one OLCI blue channel (Oa3, 442.5 nm). The label "OLCI AOD" is conventional but technically inaccurate; for clarity in the updated table, consider re-labelling as `SY_2_AOD (OLCI+SLSTR synergy)` while leaving the row position unchanged.
- **NRT split per product.** OL_1_EFR has a proper <3 h NRT stream; SY_2_AOD does not — only NTC (~24–48 h). For the early-warning chain, this means **Sentinel-3 cannot be a first-alert source for AOD events** — its role is corroborative / event-confirmation, not detection. The 300 m TOA reflectance can serve as faster visual evidence (still 3 h), but at 300 m it's coarser than Sentinel-2 MSI (10 m), so it's secondary for visual KG inputs.
- **NRT vs NTC radiometry equivalence.** Per the ESA / EUMETSAT joint product notice (S3.PN-OLCI-L1.11), **there is no difference in radiance values** between NRT and NTC at L1. The differences are purely in auxiliary data (forecast vs analysis ECMWF, predicted vs precise orbits) and uncertainty estimates. So if your pipeline ingests NRT, the values will not change when NTC arrives — only the metadata. Safe to overwrite or simply discard the NTC duplicate for L1 EFR.
- **Sun-glint avoidance and the 12.6° tilt.** OLCI's swath is tilted westwards by 12.6° relative to nadir. This affects the geometric viewing angles in the SAFE metadata. Most users don't need to think about it, but if you're doing radiative-transfer matching with model output or with simulations (e.g. into a GRASP synergy), the viewing geometry from the tie-point grid must be respected.
- **Per-pixel uncertainties.** The ESA-side L1 baseline (`OL_L1_.003.03.00`+) includes per-pixel per-band radiance uncertainties; the EUMETSAT-side does not yet. For uncertainty-aware downstream pipelines (e.g. GRASP error propagation), prefer the ESA path via CDSE. Note that the uncertainty is **encoded on a log scale** and is not decoded automatically by SNAP — you need to apply the decoding factor from the netCDF attributes.
- **SY_2_AOD super-pixel construction.** Each 4.5 km super-pixel aggregates 15 × 15 = 225 native 300 m L1c pixels. Retrieval is attempted only if the super-pixel is ≥ 50 % free of cloud, ice, and snow. **Cluj's frequent cloudiness in winter will cause many empty super-pixels** — expect retrieval yield comparable to MODIS DT and lower in DJF.
- **Constellation status (May 2026).** S3A + S3B both operational; S3A is nominally near end-of-life (CEOS lists EOL Dec 2026) but no end-of-mission announcement yet. S3C launch scheduled for September 2026 (Vega-C from Kourou) — when it commissions, the constellation will return to two satellites if S3A is decommissioned, or briefly run as three. Project should monitor ESA / EUMETSAT mission announcements during 2026 H2 for transition impacts on data continuity.
- **Why pair with SLSTR row separately?** The next entry (SLSTR — AOD 9.5 km) covers the **standalone SLSTR aerosol product (`SL_2_AOD`)**, which is **NRT-only** (the complement of SY_2_AOD's NTC-only). The two AOD products are not redundant: SL_2_AOD gives a faster, coarser AOD (NRT, 9.5 km); SY_2_AOD gives a higher-quality, finer (4.5 km) but slower (NTC) retrieval. For the warning chain, SL_2_AOD plays the first-alert role from Sentinel-3; SY_2_AOD plays the confirmation role.
- **EU citation policy.** Open data. Required attribution: *"Contains modified Copernicus Sentinel-3 data [YEAR], processed by ESA/EUMETSAT"* plus the SY_2_AOD validation paper (Sogacheva 2022) when the AOD is used.

---
