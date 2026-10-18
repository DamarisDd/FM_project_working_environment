# Datasets metadata — Aerosol early-warning system, Cluj-Napoca

Companion documentation to the Stage 1 input-data table.
For each instrument/dataset row of the table, this document records:
reference + DOI, NRT status (with latency note), host/server, file format,
programmatic download method (or manual download instructions when no API
exists), and any caveats relevant for downstream processing layers (L1, L2, L3).

Layer routing legend (per project architecture):
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (model input/output: GRASP, FLEXPART, HYSPLIT, etc.)
- **L3** — display-ready data fed to the GUI (and/or the Knowledge Graph)

---

## 1. AERONET — Sun photometer (CIMEL CE-318)

### Summary

| Field | Value |
|---|---|
| Instrument | CIMEL Electronique CE-318 automatic sun/sky scanning spectral radiometer |
| Network / Agency | NASA AERONET (AErosol RObotic NETwork), co-managed with PHOTONS (Univ. Lille / CNES / CNRS-INSU) |
| Local site (Cluj) | `CLUJ_UBB` — Babeș-Bolyai University, Faculty of Environmental Science and Engineering, Cluj-Napoca (46.768° N, 23.551° E, 405 m a.s.l.); operational since July 2010 |
| Products used | AOD (multi-wavelength, 340–1640 nm); Almucantar sky radiance; Hybrid scan sky radiance; Inversion retrievals (SSA, size distribution, refractive index, asymmetry parameter, phase function, etc.) |
| Processing levels | L1.0 (unscreened) · **L1.5 (cloud-screened, automated NRT QC — V3)** · L2.0 (quality-assured, post-calibration only — **NOT NRT**) |
| File format | ASCII / plain text (`.txt`), tabular comma-separated; bulk archives delivered as `.tar.gz` |
| NRT availability | **YES for L1.5.** V3 algorithm (since 2018) applies fully automated cloud screening + instrument-anomaly QC to the NRT stream. Typical latency: minutes to ~1 h after measurement, depending on instrument telemetry path (geostationary DCS or direct internet). **L2.0 is NOT NRT** — released only after annual calibration at LOA (Lille), typically months later. |
| Authentication | None — public access, no login or token required |
| Programmatic access | YES — HTTP GET via AERONET Web Data Service (wget / curl / `requests`) |
| Layer destination | **L2:** GRASP (AOD + radiances + inversions); FLEXPART (inversion-derived aerosol typing); HYSPLIT (TBD — to be confirmed; not in original table). **L3:** Knowledge Graph (AOD as ground-truth reference). |

### References

**Primary network reference (always required by AERONET data policy):**
- Holben, B. N., Eck, T. F., Slutsker, I., Tanré, D., Buis, J. P., Setzer, A., Vermote, E., Reagan, J. A., Kaufman, Y. J., Nakajima, T., Lavenu, F., Jankowiak, I., & Smirnov, A. (1998). AERONET — A Federated Instrument Network and Data Archive for Aerosol Characterization. *Remote Sensing of Environment*, 66(1), 1–16. DOI: [10.1016/S0034-4257(98)00031-5](https://doi.org/10.1016/S0034-4257(98)00031-5)

**Version 3 / NRT QC algorithm reference (cite for L1.5 NRT data):**
- Giles, D. M., Sinyuk, A., Sorokin, M. G., Schafer, J. S., Smirnov, A., Slutsker, I., Eck, T. F., Holben, B. N., Lewis, J. R., Campbell, J. R., Welton, E. J., Korkin, S. V., & Lyapustin, A. I. (2019). Advancements in the Aerosol Robotic Network (AERONET) Version 3 database — automated near-real-time quality control algorithm with improved cloud screening for Sun photometer aerosol optical depth (AOD) measurements. *Atmospheric Measurement Techniques*, 12(1), 169–209. DOI: [10.5194/amt-12-169-2019](https://doi.org/10.5194/amt-12-169-2019)

**Dataset DOI:** AERONET does **not** issue a single canonical persistent DOI for the network's data products. Citation is done via the two papers above plus the network acknowledgment text. The repository is registered in re3data.org under ID [r3d100011742](https://www.re3data.org/repository/r3d100011742).

### Host / Server

- Main portal: <https://aeronet.gsfc.nasa.gov/>
- Web Data Service (direct sun / AOD): <https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3>
- Web Data Service (inversion products): <https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_inv_v3>
- API help (direct sun): <https://aeronet.gsfc.nasa.gov/print_web_data_help_v3.html>
- API help (inversions): <https://aeronet.gsfc.nasa.gov/print_web_data_help_v3_inv.html>
- Site name list: <https://aeronet.gsfc.nasa.gov/aeronet_locations_v3.txt>

### Programmatic download

**Key Web Data Service parameters** (case-sensitive):

| Parameter | Meaning |
|---|---|
| `site` | AERONET site code (e.g. `CLUJ_UBB`) — must match catalog exactly |
| `year`, `month`, `day` | Start date (and optional `year2`, `month2`, `day2` for end) |
| `AVG` | `10` = all points; `20` = daily average |
| `AOD10` / `AOD15` / `AOD20` | Direct-sun AOD at Level 1.0 / 1.5 / 2.0 |
| `ALM10` / `ALM15` / `ALM20` | Almucantar inversion at Level 1.0 / 1.5 / 2.0 (inversion endpoint only) |
| `HYB10` / `HYB15` / `HYB20` | Hybrid scan inversion at Level 1.0 / 1.5 / 2.0 (inversion endpoint only) |
| `product` | For inversion endpoint: `SSA`, `SIZ`, `VOL`, `PFN`, etc. |
| `if_no_html` | `1` = strip HTML wrapper (recommended for scripting) |

**Bash / curl — pull today's NRT AOD L1.5 for CLUJ_UBB:**

```bash
#!/usr/bin/env bash
Y=$(date -u +%Y); M=$(date -u +%-m); D=$(date -u +%-d)
OUT="cluj_aod15_$(date -u +%Y%m%d).txt"
curl -s -k -o "$OUT" \
  "https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3?site=CLUJ_UBB&year=${Y}&month=${M}&day=${D}&AOD15=1&AVG=10&if_no_html=1"
```

**Bash / curl — pull Almucantar L1.5 SSA inversions for CLUJ_UBB:**

```bash
curl -s -k -o cluj_alm15_ssa_$(date -u +%Y%m%d).txt \
  "https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_inv_v3?site=CLUJ_UBB&year=${Y}&month=${M}&day=${D}&product=SSA&AVG=10&ALM15=1&if_no_html=1"
```

**Python — minimal AOD downloader (uses `requests`):**

```python
import requests
from datetime import date, timedelta

def fetch_aeronet_aod(site="CLUJ_UBB", day=None, level="1.5", out_path=None):
    """Fetch AERONET direct-sun AOD for one site and one UTC day."""
    if day is None:
        day = date.today()
    code = {"1.0": "AOD10", "1.5": "AOD15", "2.0": "AOD20"}[level]
    url = "https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3"
    params = {
        "site": site,
        "year": day.year, "month": day.month, "day": day.day,
        code: 1, "AVG": 10, "if_no_html": 1,
    }
    r = requests.get(url, params=params, timeout=60, verify=False)
    r.raise_for_status()
    out_path = out_path or f"{site}_AOD{level.replace('.', '')}_{day.isoformat()}.txt"
    with open(out_path, "wb") as f:
        f.write(r.content)
    return out_path

if __name__ == "__main__":
    print(fetch_aeronet_aod(day=date.today() - timedelta(days=1)))
```

**Off-the-shelf community tools** (worth evaluating before writing custom code):
- `aeraod.py` — configurable AERONET batch downloader, published on Zenodo. DOI: [10.5281/zenodo.13242332](https://doi.org/10.5281/zenodo.13242332)
- `dad_download_aeronet_data` — Python script for direct-sun + inversion bulk download. Repo: <https://github.com/inciteleal/dad_download_aeronet_data>

### Manual download (interactive web UI)

Pre-filtered for the Cluj station — useful as a fallback or for quick visual inspection:
- AOD (direct sun): <https://aeronet.gsfc.nasa.gov/cgi-bin/webtool_aod_v3?stage=3&region=Europe&state=Romania&site=CLUJ_UBB&place_code=10&if_polarized=0>
- Almucantar radiance, Hybrid radiance, inversion products: <https://aeronet.gsfc.nasa.gov/cgi-bin/webtool_inv_v3?stage=3&region=Europe&state=Romania&site=CLUJ_UBB&place_code=10&if_polarized=0>

### Notes / caveats

- **Level 1.5 is the only NRT-usable level.** L2.0 requires post-deployment recalibration of the instrument (annual cycle, performed at LOA Lille for European sites including CLUJ_UBB), so L2.0 lags by months to a year. For the early-warning chain, ingest L1.5; reserve L2.0 for retrospective validation.
- **Calibration gaps.** Expect 2–3 month gaps in the CLUJ_UBB time series each year while the instrument is at the calibration facility. The system should handle these gracefully (degrade to satellite-only nowcasting during gaps).
- **Daytime / clear-sky only.** Photometer is passive solar; no measurements at night or under overcast conditions. Inversion products additionally require sky-radiance scans with enough valid scattering angles, so they are much sparser than AOD.
- **Site-name case sensitivity.** `CLUJ_UBB` exactly — `cluj_ubb` or `Cluj_UBB` will return wrong/empty data without an error.
- **No persistent dataset DOI.** Required citation = Holben 1998 + Giles 2019 + the AERONET acknowledgment paragraph (see <https://aeronet.gsfc.nasa.gov/new_web/data_usage.html>).
- **HYSPLIT routing TBD.** Original table marks HYSPLIT as `-` for all AERONET products; user has flagged this as possibly changing. Decision should be recorded once the L2 pipeline is finalized.

---
