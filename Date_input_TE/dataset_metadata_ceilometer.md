# Dataset metadata — Ceilometer (ACTRIS Cloudnet)

Companion documentation to the Stage 1 input-data table.
This file describes the ceilometer data stream feeding the Cluj-Napoca
aerosol early-warning system through the ACTRIS Cloudnet data portal.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 2. Ceilometer — ACTRIS Cloudnet

### Summary

| Field | Value |
|---|---|
| Instrument | **Lufft CHM 15k** — single-wavelength (1064 nm Nd:YAG) elastic-backscatter ceilometer / aerosol lidar, vertical resolution ~15 m, range up to ~15 km, native NetCDF output. Manufacturer: G. Lufft Mess- und Regeltechnik (now OTT HydroMet). Cloudnet instrument id: `chm15k`. |
| Network / Agency | ACTRIS — Cloud remote sensing data centre Unit (**CLU**), Centre for Cloud Remote Sensing (**CCRES**); operated for ACTRIS by the Finnish Meteorological Institute (FMI). |
| Local site (Cluj) | `cluj` (Cloudnet site identifier — confirmed registered: <https://cloudnet.fmi.fi/site/cluj>). Hosted under the **CARO** (Cluj Atmospheric Remote sensing Observatory) infrastructure at Babeș-Bolyai University, part of ACTRIS-RO. **Status (as of May 2026):** the ceilometer is operational; only the cloud radar is offline (sent to INOE Bucharest for calibration / co-location measurements under the BASTA CCRES campaign). Radar data is not used in this project, so radar downtime does not affect this dataset stream. |
| Products used | **Raw / L1b** attenuated backscatter coefficient (`beta`), range-corrected signal (RCS); screened backscatter (`beta_smooth`). For this project, only the ceilometer-only (single-instrument) products are needed — radar+MWR synergy products (target classification, categorize, IWC/LWC) are **not** used. |
| Processing levels | **L1b** (single-instrument, daily NetCDF, harmonized via CloudnetPy `LufftCeilo` reader). L2 synergy products not used. |
| File format | **NetCDF** end-to-end. The Lufft CHM 15k writes its **raw** output as native NetCDF (one `.nc` per day, daily files named e.g. `<date>_<site>_CHM<serial>.nc`), which is then converted to the Cloudnet L1b NetCDF (CF-compliant, `format: "HDF5 (NetCDF4)"` or `"NetCDF3"` per CLU processing). Directly readable by `xarray`/`netCDF4` without per-vendor adapters. |
| NRT availability | **YES.** Cloudnet tags every file with an official ACTRIS `timeliness`: `rrt` (real real-time), `nrt` (near real-time), or `scheduled`. Filtering on `timeliness in {rrt, nrt}` retrieves only the operationally fresh files. For a CHM 15k with a working data link to FMI, ceilometer L1b products are normally available within minutes of measurement. The original table's "Yes if raw" matches: raw + L1b stream is NRT. |
| Authentication | None for read/download — public, no account required. (Upload requires HTTP Basic auth with station credentials; not relevant for our consumer-side use.) |
| Programmatic access | YES — full REST API at `https://cloudnet.fmi.fi/api/` + official Python client `cloudnet-api-client`. |
| Layer destination | **L2:** GRASP (aerosol layer / PBL height context for column inversions), FLEXPART (vertical aerosol distribution for source attribution). **L3:** Knowledge Graph (aerosol layer presence + PBL height). HYSPLIT: not used in the original table. |

### References

**Primary Cloudnet reference (required for any Cloudnet-derived product):**
- Illingworth, A. J., Hogan, R. J., O'Connor, E. J., Bouniol, D., Brooks, M. E., Delanoë, J., Donovan, D. P., Eastment, J. D., Gaussiat, N., Goddard, J. W. F., Haeffelin, M., Klein Baltink, H., Krasnov, O. A., Pelon, J., Piriou, J.-M., Protat, A., Russchenberg, H. W. J., Seifert, A., Tompkins, A. M., van Zadelhoff, G.-J., Vinit, F., Willén, U., Wilson, D. R., & Wrench, C. L. (2007). Cloudnet: Continuous Evaluation of Cloud Profiles in Seven Operational Models Using Ground-Based Observations. *Bulletin of the American Meteorological Society*, 88(6), 883–898. DOI: [10.1175/BAMS-88-6-883](https://doi.org/10.1175/BAMS-88-6-883)

**CloudnetPy processing software reference (cite when L1b/L2 products are used):**
- Tukiainen, S., O'Connor, E., & Korpinen, A. CloudnetPy — Python package for Cloudnet data processing. Software DOI: [10.5281/zenodo.15261153](https://doi.org/10.5281/zenodo.15261153) (latest version at time of writing; resolve the Zenodo concept DOI for current version).

**Dataset DOI / persistent identifier policy:** Cloudnet does **not** issue a single network-level dataset DOI. Instead:
- Each individual file receives a Handle PID (e.g. `https://hdl.handle.net/21.12132/1.<uuid>`) once it transitions from `volatile` to stable.
- Each instrument receives a separate Handle PID (e.g. `https://hdl.handle.net/21.12132/3.<uuid>`) with its own citation block (provided in the instrument metadata response).
- Multi-station campaign collections may be assigned Zenodo or PANGAEA DOIs (e.g. the ACTRIS/Cloudnet 12-station Jan–May 2020 collection).
- For deliverable citation: cite Illingworth 2007 + Tukiainen et al. (CloudnetPy DOI) + the instrument PID + the file PID(s) of the actual data used.

### Host / Server

- Main portal: <https://cloudnet.fmi.fi/>
- Cluj site landing page: <https://cloudnet.fmi.fi/site/cluj>
- REST API base URL: <https://cloudnet.fmi.fi/api/>
- API documentation: <https://docs.cloudnet.fmi.fi/api/data-portal.html>
- Python client (recommended): <https://github.com/actris-cloudnet/cloudnet-api-client>
- Processing toolkit: <https://github.com/actris-cloudnet/cloudnetpy>
- ACTRIS vocabulary for timeliness: <https://vocabulary.actris.nilu.no/actris_vocab/timeliness>

### Programmatic download

**Recommended: official Python client (`cloudnet-api-client`).** Handles pagination, retries, async downloads, and PID resolution.

```bash
pip install cloudnet-api-client
```

```python
from cloudnet_api_client import APIClient
from datetime import date

client = APIClient()

# Sanity check — confirm Cluj site is registered and get coordinates
site = client.site("cluj")
print(site)

# Resolve the actual Cluj CHM 15k UUID
# (DO NOT reuse the docs-example UUID d6bf209b-... from the cloudnet-api-client README)
cluj_instruments = client.raw_files(site_id="cluj", instrument_id="chm15k", date="2026-05-01")
# any returned record carries the instrument metadata + PID; capture it once and reuse
print({(r.instrument.uuid, r.instrument.pid) for r in cluj_instruments})

# Fetch L1b ceilometer files for Cluj for a given UTC date
files = client.files(
    site_id="cluj",
    date=date.today().isoformat(),
    product_id=["lidar"],   # "lidar" is the Cloudnet product id for ceilometer L1b
)
print(f"{len(files)} file(s) found")

# Download into ./data/
paths = client.download(files, "data/")
print(paths)

# For NRT filtering, inspect each file's `timeliness` attribute and keep nrt/rrt
nrt_files = [f for f in files if f.timeliness in ("rrt", "nrt")]
client.download(nrt_files, "data_nrt/")
```

**Alternative: raw HTTP via curl** (REST endpoint, no auth):

```bash
# 1. Query metadata for today's Cluj lidar (ceilometer L1b) files
DATE=$(date -u +%Y-%m-%d)
curl -s "https://cloudnet.fmi.fi/api/files?site=cluj&date=${DATE}&product=lidar" \
  | jq '.[] | {uuid, filename, downloadUrl, timeliness, format}'

# 2. Pull each file's downloadUrl and fetch it
curl -s "https://cloudnet.fmi.fi/api/files?site=cluj&date=${DATE}&product=lidar" \
  | jq -r '.[].downloadUrl' \
  | xargs -n1 curl -sO
```

**Raw (un-processed) files** — if the use case requires the original Lufft CHM 15k NetCDF rather than the homogenized Cloudnet L1b:

```bash
curl -s "https://cloudnet.fmi.fi/api/raw-files?site=cluj&date=${DATE}&instrument=chm15k" \
  | jq -r '.[].downloadUrl' \
  | xargs -n1 curl -sO
```

(The Lufft CHM 15k's native NetCDF is already very close to a Cloudnet-compatible format, so for this project the L1b stream from `/api/files?product=lidar` is normally the right entry point; the raw stream is mainly useful as a fallback if a given day fails central processing.)

**Processing raw → L1b locally with CloudnetPy** (fallback if central processing has a gap on a given day):

```python
from cloudnetpy.instruments import ceilo2nc

# CloudnetPy auto-detects the instrument family (Vaisala / Lufft / Campbell)
# from the file structure; for the Cluj CHM 15k it uses cloudnetpy.instruments.lufft.LufftCeilo.
# The site altitude is required; calibration_factor is optional but recommended.
uuid = ceilo2nc(
    "CHM<serial>_20260518.nc",            # native Lufft CHM 15k daily NetCDF
    "cluj_lidar_l1b_20260518.nc",         # Cloudnet-compliant L1b output
    {
        "name": "Cluj-Napoca",
        "altitude": 405,                  # m a.s.l. — UBB rooftop
        "calibration_factor": 2.3e-12,    # placeholder; use the CARO-calibrated value
    },
)
```

### Manual download (interactive web UI)

- Cluj site overview + file browser: <https://cloudnet.fmi.fi/site/cluj>
- Generic search/filter UI: <https://cloudnet.fmi.fi/search/data?site=cluj>
- Instrument detail page (replace UUID with the **actual** Cluj ceilometer UUID once confirmed):
  `https://cloudnet.fmi.fi/instrument/<INSTRUMENT_UUID>`

### Notes / caveats

- **UUID flag (open action item).** The original docx points to instrument UUID `d6bf209b-c48b-48a4-bbfb-fed713b27832`. **This same UUID appears verbatim as the placeholder example in the official `cloudnet-api-client` README** (`client.instrument("d6bf209b-c48b-48a4-bbfb-fed713b27832")`), which strongly suggests it was copied from the docs rather than retrieved for the actual Cluj CHM 15k. The correct UUID + PID should be pulled from `https://cloudnet.fmi.fi/api/raw-files?site=cluj&instrument=chm15k` (any record carries the instrument's UUID and Handle PID under `instrument.uuid` / `instrument.pid`) and recorded once, then reused. Quick fix, but worth doing before any production code references the UUID.
- **Station status (May 2026).** The ceilometer is operational at the CARO / ACTRIS-Cluj facility (Babeș-Bolyai University, rooftop, ~405 m a.s.l.). The cloud radar is offline — currently at INOE Bucharest for the BASTA CCRES calibration / co-location campaign — but this project does **not** consume radar data, so the radar's absence does not affect this stream.
- **Volatile vs. stable files.** Cloudnet marks recently processed files as `volatile: true` — they may be re-processed and updated. For NRT ingestion this is acceptable, but downstream code should re-fetch updated `volatile` files (e.g. for a few days following measurement) until they stabilize (drop to `volatile: false` and receive a Handle PID).
- **CF-compliant NetCDF.** Cloudnet L1b files follow the Climate and Forecast conventions on a time–height grid (UTC, one file per UTC day, midnight-to-midnight). Directly readable by `xarray.open_dataset` / `netCDF4` without per-instrument adapters.
- **CCRES nominal grid.** ACTRIS-compatible cloud-profiling stations target 30 s × 60 m time/height resolution as nominal — useful as the canonical grid for any downstream resampling.
- **Acknowledgment.** Cloudnet data are free for non-commercial / scientific use; co-authorship is offered by data providers when their data is used substantially. Acknowledgment paragraph required in publications; provided per-file by the portal.

---
