# Dataset metadata — Raman lidar (ACTRIS EARLINET)

Companion documentation to the Stage 1 input-data table.
This file describes the EARLINET multi-wavelength Raman + depolarization lidar
data stream feeding the Cluj-Napoca aerosol early-warning system.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 3. Raman lidar — ACTRIS EARLINET

### Summary

| Field | Value |
|---|---|
| Instrument | **Raymetrics LR231-D300** multi-wavelength Raman + depolarization lidar. Emitter: Continuum INLITE II-30 Nd:YAG laser, 30 Hz repetition rate. **Elastic channels:** 355, 532, 1064 nm. **Raman channels:** 387 nm and 607 nm (rotational-vibrational N₂ Raman, used to derive extinction independently of backscatter). **Depolarization channels:** 355 nm and 532 nm (volume + particle linear depolarization ratio — recent upgrade adds 355 nm to the original 532 nm channel, enabling spectrally-resolved depolarization for improved aerosol typing). |
| Network / Agency | ACTRIS — Centre for Aerosol Remote Sensing (**CARS**) / EARLINET. Data are processed centrally by the **EARLINET Single Calculus Chain (SCC)**, operated by CNR-IMAA (Potenza, Italy). |
| Local site (Cluj) | EARLINET station code **`CLOP`** (Cluj-Napoca, Babeș-Bolyai University, Faculty of Environmental Science and Engineering; co-located with the AERONET `CLUJ_UBB` and the Cloudnet `cluj` ceilometer at 46.768° N, 23.551° E, 405 m a.s.l.). Operational since 2009. Local PIs: N. Ajtai, H. Ștefănie (UBB). |
| Products used | **Level 1:** range-corrected signal (RCS) time series, high-resolution attenuated backscatter, volume depolarization ratio (355, 532 nm). **Level 2:** aerosol particle backscatter coefficient profiles (at 355/532/1064 nm), particle extinction coefficient profiles (at 355/532 nm, Raman method, nighttime only), lidar ratio, Ångström exponent, particle linear depolarization ratio (PLDR) at **355 and 532 nm**, planetary boundary layer / aerosol layer height. |
| Processing levels | **L0** (raw vendor binary, internal). **L1** (pre-processed RCS, CF-compliant NetCDF, SCC ELPP/HiRELPP modules). **L2** (aerosol optical products, CF-compliant NetCDF, SCC ELDA module). |
| File format | **NetCDF**, CF-compliant. One file per product / per measurement window. (Raw L0 is a vendor format and not normally distributed.) |
| NRT availability | **NOT NRT by default.** Operation is manual: the instrument runs on the EARLINET climatological schedule (1 daytime measurement on Monday around noon for a well-developed PBL; 2 nighttime measurements on Monday and Thursday for Raman extinction with low background light). Eye safety + operator presence rules out unattended NRT operation. **On-demand / event-driven NRT is possible** for known incoming events: an operator can trigger measurements, submit raw data to the SCC, and have Level 1/Level 2 products available end-to-end within ~12 h (consistent with the EARLINET 72-h NRT operativity exercises and the COVID-19 intensive campaign). For this project's early-warning chain, treat the Raman lidar as a **reactive / on-demand** validation source rather than a routine NRT input. |
| Authentication | **Asymmetric — upload vs. download.** The CLOP operator confirms credentials are required for **submitting raw data** to EARLINET (necessary for SCC ingestion + central QC). For **downloading already-processed L1/L2 products** from `data.earlinet.org`, access appears to be open / non-site-specific in most cases — the EARLINET documentation is internally inconsistent on this and the project team flags it as something to verify empirically before finalising the operational pipeline. **SCC processing:** registration required; for ACTRIS stations (including CLOP) the account is auto-provisioned once the ACTRIS lidar code is assigned. |
| Programmatic access | YES — REST API at `https://data.earlinet.org/api/` (Swagger UI at `/api/swagger-ui/`). THREDDS / OPeNDAP at `https://login.earlinet.org:8443/thredds`. SCC has its own GUI + API (`https://scc.imaa.cnr.it/`). |
| Layer destination | **L2:** GRASP (synergy with AERONET via GARRLiC inversions; combined sun-photometer–lidar retrievals), FLEXPART (vertical aerosol distribution + source attribution for transported plumes). **L3:** Knowledge Graph (event-driven evidence of aerosol layers and typing at altitude). HYSPLIT: not used in the original table. |

### References

**Primary network reference (required for any EARLINET-derived product, per data policy):**
- Pappalardo, G., Amodeo, A., Apituley, A., Comeron, A., Freudenthaler, V., Linné, H., Ansmann, A., Bösenberg, J., D'Amico, G., Mattis, I., Mona, L., Wandinger, U., Amiridis, V., Alados-Arboledas, L., Nicolae, D., & Wiegner, M. (2014). EARLINET: towards an advanced sustainable European aerosol lidar network. *Atmospheric Measurement Techniques*, 7(8), 2389–2409. DOI: [10.5194/amt-7-2389-2014](https://doi.org/10.5194/amt-7-2389-2014)

**Single Calculus Chain (SCC) processing reference (cite when L1/L2 SCC products are used):**
- D'Amico, G., Amodeo, A., Baars, H., Binietoglou, I., Freudenthaler, V., Mattis, I., Wandinger, U., & Pappalardo, G. (2015). EARLINET Single Calculus Chain – overview on methodology and strategy. *Atmospheric Measurement Techniques*, 8(11), 4891–4916. DOI: [10.5194/amt-8-4891-2015](https://doi.org/10.5194/amt-8-4891-2015)

**Dataset DOI:** EARLINET does not currently mint a single network-level DOI for the live operational database. The most widely cited dataset DOI is for the climatological subset:
- EARLINET publishing group (2018). EARLINET Climatology 2000–2015. *World Data Center for Climate (WDCC) at DKRZ.* DOI: [10.1594/WDCC/EARLINET_Climatology_2000-2015](https://doi.org/10.1594/WDCC/EARLINET_Climatology_2000-2015)

For live / NRT-style use, citation = Pappalardo 2014 + D'Amico 2015 + the acknowledgment paragraph from EARLINET's data policy.

### Host / Server

- Main website (information, station list, policy): <https://www.earlinet.org/> (also <https://earlinet.eu/>)
- **Modern data portal (REST API + GUI):** <https://data.earlinet.org/>
- REST API base: <https://data.earlinet.org/api/>
- Swagger UI (interactive API docs): <https://data.earlinet.org/api/swagger-ui/>
- Quicklooks (PNG previews, all stations): <https://quicklooks.earlinet.org/>
- THREDDS / OPeNDAP (legacy / parallel, credentialed): <https://login.earlinet.org:8443/thredds/>
- **SCC (processing):** <https://scc.imaa.cnr.it/>
- SCC documentation: <https://docs.scc.imaa.cnr.it/>
- SCC forum / support: <https://earlinetforum.imaa.cnr.it/>
- Data policy: <https://www.earlinet.org/index.php?id=127>

### Programmatic download

**REST API — list Cluj L2 backscatter files in a date range:**

```bash
# Replace endpoint paths with the live ones from the Swagger UI
# (https://data.earlinet.org/api/swagger-ui/) — the API is evolving and
# the most reliable approach is to discover endpoints there first.
curl -s "https://data.earlinet.org/api/v2/files?station=clop&dateFrom=2026-01-01&dateTo=2026-05-18&productType=backscatter" \
  -H "Accept: application/json" \
  | jq '.[] | {filename, downloadUrl, productType, startTime}'
```

**Python — minimal downloader pattern:**

```python
import requests
from urllib.parse import urljoin

BASE = "https://data.earlinet.org/api/"

def search_clop(date_from, date_to, product="backscatter"):
    """Search the EARLINET data portal for CLOP (Cluj) files."""
    # Endpoint name varies by API version — verify via the Swagger UI before relying on this.
    r = requests.get(
        urljoin(BASE, "v2/files"),
        params={
            "station": "clop",
            "dateFrom": date_from,
            "dateTo": date_to,
            "productType": product,
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()

def download(records, out_dir="./earlinet_clop/"):
    import os
    os.makedirs(out_dir, exist_ok=True)
    for rec in records:
        url = rec["downloadUrl"]
        path = os.path.join(out_dir, rec["filename"])
        with requests.get(url, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            with open(path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
        print(path)

if __name__ == "__main__":
    files = search_clop("2026-01-01", "2026-05-18", product="backscatter")
    download(files)
```

**THREDDS / OPeNDAP — for streaming NetCDF subsets directly with `xarray`** (credentialed):

```python
import xarray as xr
url = "https://login.earlinet.org:8443/thredds/dodsC/<catalog_path>/<filename>.nc"
ds = xr.open_dataset(url)  # OPeNDAP — pulls only the slice you ask for
print(ds)
```

(Exact catalog path is discoverable via the THREDDS catalog UI: <https://login.earlinet.org:8443/thredds/catalog.html>.)

**On-demand event-driven workflow (the operational case for this project):**

1. **Trigger:** another data stream in the pipeline (CAMS forecast, MODIS/VIIRS AOD spike, SEVIRI Dust RGB, AERONET AOD anomaly, or a manual user alert via the GUI) suggests an aerosol event is incoming.
2. **Notify operator:** the system pings the CLOP lidar operator (N. Ajtai / H. Ștefănie) to start a measurement, respecting the 14-day-advance recommendation only as a default — for genuine event responses, shorter notice is operationally accepted.
3. **Measurement:** operator runs a session compatible with the SCC configuration of the station (typical EARLINET windows: 1–2 h continuous).
4. **Upload to SCC:** raw + station configuration submitted to `scc.imaa.cnr.it`; ELPP + ELDA modules run automatically.
5. **Retrieve products:** L1 RCS + L2 optical profiles become available, typically within ~12 h end-to-end depending on SCC queue load.
6. **Ingest:** project pipeline pulls the L2 NetCDF via the REST API and feeds it into the L2 stage (GRASP / FLEXPART).

### Manual download (interactive web UI)

- Search & download GUI: <https://data.earlinet.org/> (filter by station = Cluj-Napoca / `clop`, by product type, by date)
- User registration (if needed for the data portal): <https://data.earlinet.org/earlinet/userRegistration.zul>
- Direct EARLINET database link from the docx (current as of the table submission): <https://data.earlinet.org/earlinet/>
- Quicklook browser (PNG, useful for visual checks before downloading the NetCDF): <https://quicklooks.earlinet.org/>

### Notes / caveats

- **NRT story is operator-bound, not data-stream-bound.** The lidar can't run unattended (Class 4 laser, eye-safety regulations, calibration drift), so the limiting factor for NRT is human availability, not the SCC processing chain. The project should design around event-triggered measurement campaigns rather than continuous ingestion. The realistic latency from "trigger" to "L2 product in the pipeline" is **~12 h** (consistent with EARLINET's documented NRT exercises), but contingent on (a) operator on-site, (b) clear sky, (c) SCC queue not saturated.
- **Daytime vs. nighttime products differ.** Particle **extinction** is reliably derived only from Raman channels at night (387 / 607 nm signals are too weak against the daytime solar background). During the day only **backscatter** is available (Klett–Fernald inversion, requires assumed lidar ratio). For the warning chain, this means: daytime triggers yield less aerosol-typing power than nighttime ones — worth flagging in the GUI.
- **Authentication — asymmetric.** The CLOP operator confirms: **uploading raw data** to EARLINET requires station credentials (used by the operator to submit measurement files for SCC processing). **Downloading already-processed L1/L2 products** is most likely open access without site-specific credentials — but EARLINET's own documentation contradicts itself on this point (one page says "open and credential-free", another says "username/password required"), and the legacy THREDDS server (`login.earlinet.org:8443`) is credentialed. **Action item:** verify empirically (try an unauthenticated GET against `data.earlinet.org/api/v2/files?station=clop&...`) and lock the entry once confirmed. Either way, an institutional account is free and useful for tracking data-policy compliance.
- **Station name confusion.** AERONET calls the Cluj site `CLUJ_UBB`; Cloudnet calls it `cluj`; EARLINET calls the lidar station `CLOP`. All three refer to the same physical facility at Babeș-Bolyai University. Document this mapping in the Knowledge Graph schema.
- **Schedule alignment with CALIPSO/EarthCARE overpasses.** EARLINET coordinates measurements with satellite overpasses by default. This is an opportunity for the project: scheduling an event-driven lidar session to coincide with the next ATLID (EarthCARE) overpass produces simultaneous space–ground vertical profiles, valuable for L3 validation.
- **Acknowledgment text** (mandatory in publications): *"The authors acknowledge EARLINET for providing aerosol LIDAR profiles available at https://data.earlinet.org/"* + cite Pappalardo et al. 2014.

---
