# Dataset metadata — Air quality monitoring stations (RNMCA)

Companion documentation to the Stage 1 input-data table.
This file describes the in-situ ground-level air quality measurements
from the Romanian National Air Quality Monitoring Network feeding the
Cluj-Napoca aerosol early-warning system.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

---

## 4. Air-quality stations — RNMCA (Rețeaua Națională de Monitorizare a Calității Aerului)

### Summary

| Field | Value |
|---|---|
| Instrument | Automatic monitoring stations equipped with reference-method analysers for criteria pollutants (e.g. Thermo TEOM 1405-DF / Derenda APM-2 for PM10/PM2.5, UV-fluorescence for SO₂, chemiluminescence for NOₓ, IR absorption for CO, UV absorption for O₃). Configuration varies per station; all instruments comply with EU reference methods per the Air Quality Directive (2008/50/EC). |
| Network / Agency | **RNMCA** — Rețeaua Națională de Monitorizare a Calității Aerului. Administered by **ANMAP** (Agenția Națională pentru Mediu și Arii Protejate; formerly ANPM), specifically through the **Centrul de Evaluare a Calității Aerului (CECA)**. County-level data validation is performed by the local APM (Agenția pentru Protecția Mediului) offices. |
| Local sites (Cluj) | Four official RNMCA stations in Cluj-Napoca, classified by site type per EU AQ Directive: **CJ-1** (traffic), **CJ-2** (urban background), **CJ-3** (suburban background), **CJ-4** (industrial). Additional 3 analysers added in Cluj county under the 2022 RNMCA expansion programme. **County network identifier in the API: `APM_CJ` / `EPA_CJ`.** |
| Products used | Hourly concentrations: **PM₁₀**, **PM₂.₅**, **SO₂**, **NOₓ (NO + NO₂)**, **O₃**, **CO**. (RNMCA also produces C₆H₆, NH₃, H₂S, formaldehyde where applicable, plus heavy metals — Pb, Cd, Ni, As, Hg — and PAHs from PM₁₀ filters in county labs; not currently used in this project.) Romanian-legislation air quality indices (specific per pollutant + general per location) are computed centrally and also retrievable via the API. |
| Processing levels | **Raw** (real-time from data loggers in stations, available immediately). **Validated** (county-level APM validation, typically next working day). **Certified** (national-level ANMAP certification, in multi-month batches). The same database table is updated in place — when raw → validated → certified, the higher-quality value replaces the lower-quality one. |
| File format | **JSON** via the REST API (with Unix-epoch-ms timestamps, UTC). **XLS / XLSX tables** via the manual Reports interface. (The docx originally mentioned only XLS — the API + JSON path is a significant upgrade not previously documented.) |
| NRT availability | **YES, ~1 h cadence.** Hourly averages are pushed to the public API a few times per hour as raw data. Validation lags by ~1 working day; certification lags by months. For the early-warning chain, **raw hourly data is the operational input**; validated data should be used to correct retrospective analyses. |
| Authentication | **YES — HTTP Basic Auth (RFC 7617) required.** Free credentials are obtained by emailing the contact form at <https://www.calitateaer.ro/public/contact-page/?__locale=ro> with: full name, institutional email, justification, requested API module(s), preferred language (RO/EN). Note that the API is officially in "public testing" phase — functionality may change. |
| Programmatic access | YES — REST API at **`https://calitateaer.ro:8443/`**, with Swagger UI and OpenAPI 3 JSON spec. Rate-limited per-account (per 10 s / minute / hour / day, plus concurrent-request cap). Three modules available; you specify which on registration. |
| Layer destination | **L2:** FLEXPART (boundary-layer concentrations for validation of model dispersion + emission inversion). **L3:** Knowledge Graph (ground-truth in-situ confirmation of aerosol/pollution events flagged by remote-sensing layers). Per the original table, GRASP and HYSPLIT do not consume this dataset. |

### References

**Primary legal / regulatory reference (governs measurement methods, limit values, alert thresholds, station siting):**
- *Legea nr. 104 din 15 iunie 2011 privind calitatea aerului înconjurător.* Publicată în Monitorul Oficial al României, Partea I, nr. 452 din 28 iunie 2011 (cu modificările şi completările ulterioare). Romanian transposition of EU Air Quality Directive 2008/50/EC. Available at <https://legislatie.just.ro/Public/DetaliiDocument/129642>.

**EU Directive transposed:**
- *Directive 2008/50/EC of the European Parliament and of the Council of 21 May 2008 on ambient air quality and cleaner air for Europe* (the "Air Quality Directive"). Consolidated text: <https://eur-lex.europa.eu/eli/dir/2008/50>.
- *Directive (EU) 2024/2881* (the recast Air Quality Directive, replacing 2008/50/EC by 2030); transposition into Romanian law is in progress at the time of writing and may change downstream products.

**Dataset DOI:** RNMCA does not mint a network-level DOI. Data are citable by network name, URL, and access date. EEA Air Quality e-Reporting (which mirrors Romanian data) provides versioned annual collections with PIDs on the EEA portal but no DOI for the live stream.

### Host / Server

- **Public website (HTML, manual access):** <https://www.calitateaer.ro/>
- **REST API base URL:** <https://calitateaer.ro:8443/>
- **Swagger UI (interactive API docs):** <https://calitateaer.ro:8443/swagger-ui/index.html?configUrl=/api-docs/swagger-config>
- **OpenAPI 3 JSON spec:** <https://calitateaer.ro:8443/api-docs>
- **API access request / contact form:** <https://www.calitateaer.ro/public/contact-page/?__locale=ro>
- **Privacy policy (must agree):** <https://www.calitateaer.ro/export/sites/default/.galleries/Legislation/Politica-de-Confidentialitate.pdf_2063068895.pdf>
- **API terms & conditions (must agree):** <https://www.calitateaer.ro/export/sites/default/.galleries/Legislation/Termeni-si-conditii.pdf_2063068895.pdf>
- **Manual report download (the URL in the original docx):** <https://www.calitateaer.ro/public/monitoring-page/reports-reports-page/?__locale=ro>
- **EEA mirror (backup, no auth, slower update cadence):** <https://discomap.eea.europa.eu/App/AQViewer/index.html?fqn=Airquality_Dissem.b2g.AirQualityStatistics>

### API structure

The RNMCA API exposes three modules, all under `https://calitateaer.ro:8443/`. Each request needs HTTP Basic Auth. The right module for an early-warning use-case is the **Simplified Data API** (or the **Main Measurement Data API** if accurate replicas of the database are needed for retrospective analysis):

| Module | Use case | Lookback |
|---|---|---|
| **Simplified Data API** | Human-friendly recent values + AQ indices | Up to 7 days |
| **Main Measurement Data API** | Optimised bulk transfer, full history | Arbitrary; versioned mode for incremental sync |
| **Air Quality Index API** | Legal AQ indices (specific + general) | Recent or arbitrary |

Workflow for any module: (1) fetch the **configuration** (lists networks, locations, parameters, measurement values) — versioned, only re-pulled when version changes; (2) fetch **available cache intervals**; (3) request **data** by network, location, or measurement-value id, for a given interval.

Key endpoints (Main module):
- `GET /main/measurements/recent/config/all` — full config (versioned)
- `GET /main/measurements/recent/data/availableIntervals` — interval codes
- `GET /main/measurements/recent/data/network?networkId=&intervalCode=` — all data for a network (e.g. Cluj county)
- `GET /main/measurements/recent/data/location?locationId=&intervalCode=` — all data for one station
- `GET /main/measurements/recent/data/measurementValue?measurementValueId=&intervalCode=` — single parameter+station
- `POST /main/measurements/arbitrary/data/measurementValues` — historical with arbitrary date range
- `POST /main/measurements/versioned/data/measurementValues` — incremental updates for DB replication

### Programmatic download

**Bash / curl — minimal sanity check (after credentials are issued):**

```bash
USER="your_rnmca_user"
PASS="your_rnmca_pass"

# 1. Fetch the simplified data config — gives the location ids for Cluj stations
curl -s -u "${USER}:${PASS}" -H "Accept-Encoding: gzip" \
  "https://calitateaer.ro:8443/airquality/simplified/recent/config/all" | jq .

# 2. List available cache intervals
curl -s -u "${USER}:${PASS}" \
  "https://calitateaer.ro:8443/main/measurements/recent/data/availableIntervals" | jq .
```

**Python — minimal NRT poller for the Cluj county network:**

```python
import os, time
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://calitateaer.ro:8443"
AUTH = HTTPBasicAuth(os.environ["RNMCA_USER"], os.environ["RNMCA_PASS"])
HEADERS = {"Accept-Encoding": "gzip"}

def get_json(path, params=None):
    r = requests.get(f"{BASE}{path}", params=params, auth=AUTH,
                     headers=HEADERS, timeout=60)
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 60))
        time.sleep(wait)
        return get_json(path, params)
    r.raise_for_status()
    return r.json()

# 1. Resolve the Cluj county network id (one-off, then cache)
config = get_json("/main/measurements/recent/config/all")
cluj_network = next(n for n in config["networks"] if n["name"] in ("APM_CJ", "EPA_CJ"))
print("Cluj network id:", cluj_network["id"])

# 2. Pick an interval code (e.g. the shortest one — raw hourly)
intervals = get_json("/main/measurements/recent/data/availableIntervals")
shortest = sorted(intervals.keys())[0]

# 3. Pull recent data for all locations in the Cluj county network
data = get_json("/main/measurements/recent/data/network",
                params={"networkId": cluj_network["id"], "intervalCode": shortest})

# `data` contains hourly values for PM10, PM2.5, SO2, NOx, O3, CO across CJ-1..CJ-4
# Timestamps are Unix epoch ms in UTC.
```

**Operational notes for the polling loop:**

- The cache updates **a few times per hour** — polling more often than that wastes rate-limit budget without getting fresher data.
- Always send `Accept-Encoding: gzip` (server supports it; payloads can be large).
- Watch for **HTTP 503** under burst load → retry after a few seconds.
- Watch for **HTTP 429** → respect the `Retry-After` header.
- Use the **versioned** endpoint (not recent) when building a long-term replica DB — it tells you exactly which records changed since the last sync.
- All timestamps mark the **end** of the averaging interval, **in UTC**. Convert to Europe/Bucharest with DST awareness for display.

### Manual download (interactive web UI)

For one-off or audit downloads, no API account required:
- **Reports page (custom date range, station, parameter, output as XLS):** <https://www.calitateaer.ro/public/monitoring-page/reports-reports-page/?__locale=ro> — select location (Cluj-Napoca → CJ-1/2/3/4), date range, pollutants, then export.
- **Station detail (real-time view):** <https://www.calitateaer.ro/public/?__locale=ro> → map → click station.
- **EEA mirror:** Air Quality e-Reporting download service at <https://eeadmz1-cws-wp-air02.azurewebsites.net/> (filter country = Romania; output as parquet / CSV; lags the national source).

### Notes / caveats

- **The original docx undersells the access path.** It lists only "tabel xls — se selectează locația, data, stația, parametrii etc" via the Reports page. The actual situation is much better: a documented REST API exists, with three modules, configurable cache intervals, versioned incremental sync, and per-account rate limits. **Action item:** register an API account (email request to the calitateaer.ro contact form, specifying the project + the modules needed — at minimum the Simplified Data and AQ Index modules). Credentials are free; usually issued within days.
- **Network / agency name has changed.** Older docs (and the original docx Reference [4]) say ANPM. The agency is now **ANMAP** (Agenția Națională pentru Mediu și Arii Protejate). RNMCA is the same network. The bibliographic reference (Law 104/2011) is unchanged.
- **Station classification matters for downstream use.** The four Cluj stations differ in site type (traffic / urban / suburban / industrial). For source attribution work (FLEXPART), the traffic station CJ-1 carries a strong local-source signal and is not directly comparable to the column-integrated AOD from AERONET/satellites without accounting for that. The suburban (CJ-3) and urban background (CJ-2) stations are more representative of regional aerosol load.
- **Validation lag is real.** Raw data is what arrives in NRT; the next-working-day validation step **replaces** the raw value in the same row of the database. The same `measurementValueId` may return a different value tomorrow than it returned today, for the same timestamp. Downstream code should expect this and re-fetch yesterday's data for at least 48 h to absorb the validation cycle. The "versioned" endpoint exists precisely for this.
- **Romanian AQ indices ≠ EU AQI ≠ WHO guidelines.** The indices computed by the API follow the Romanian legislation (Legea 104/2011 + implementing orders). If the GUI presents indices to first responders, use the legal Romanian ones for compliance reporting, but consider also displaying WHO 2021 guideline values as a public-health reference — they are stricter.
- **Recast EU Directive (2024/2881) is coming.** Member-state transposition deadline is December 2026 with stricter limit values from 2030. Some monitoring methods and reporting requirements will change; the API config is versioned for exactly this kind of regulatory drift.
- **Backup data path.** If the calitateaer.ro API is down or rate-limited, the **EEA Air Quality e-Reporting service** mirrors Romanian data with a delay (hours to days). Useful for retrospective gap-filling, less so for NRT.
- **Citation/acknowledgment.** Cite Law 104/2011 + the network ("data provided by RNMCA, via the calitateaer.ro web service, accessed YYYY-MM-DD"). The Terms & Conditions PDF specifies the formal attribution requirements.

---
