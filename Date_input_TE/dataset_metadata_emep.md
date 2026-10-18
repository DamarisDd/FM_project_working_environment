# Dataset metadata — EMEP (European Monitoring and Evaluation Programme)

Companion documentation to the Stage 1 input-data table.
This file describes **EMEP** — the **European Monitoring and Evaluation
Programme** under the UNECE **Convention on Long-Range Transboundary
Air Pollution (CLRTAP)**. EMEP is the European-focused counterpart to
the globally-scoped EDGAR emission inventory, and the closing entry in
the project's emission-inventory cluster.

Layer routing legend:
- **L1** — raw ingestion + initial processing
- **L2** — intermediate products (GRASP, FLEXPART, HYSPLIT)
- **L3** — display-ready data fed to the GUI / Knowledge Graph

**EMEP is multifaceted** — unlike most other entries, it spans:
1. A **gridded emissions database** (CEIP, Vienna) of European national submissions
2. A **chemistry-transport model** (MSC-W, Oslo) — one of the 11 models in the CAMS European ENSEMBLE
3. A **ground-based observation network** (EBAS, hosted by NILU, Norway) — out of scope for this metadata file
4. An **annual Status Report** series describing the state of transboundary pollution

This file focuses on the gridded emissions and the MSC-W model, the two
EMEP components that feed directly into the project's L2 layer.

**The unique value of EMEP for the project:** for emissions over the
European source region affecting Cluj, EMEP provides the
**politically-validated, nationally-submitted** inventory — including
Romania's official emission data submitted by **ANMAP** (Agenția
Națională pentru Mediu și Arii Protejate). EDGAR is an independent JRC
estimate; EMEP is the official record. Cross-comparison between the two
is operationally informative.

---

## 23. EMEP — gridded emissions (CEIP) + MSC-W chemistry-transport model

### Summary

| Field | Value |
|---|---|
| Dataset / Software | **EMEP** comprises (a) the **CEIP gridded emissions database** of national emission submissions and (b) the **EMEP MSC-W chemistry-transport model** code. **CEIP** = Centre on Emission Inventories and Projections at the Federal Environment Agency Austria (Umweltbundesamt, Vienna). **MSC-W** = Meteorological Synthesizing Centre - West at the Norwegian Meteorological Institute (Oslo). Both operate under CLRTAP within the UNECE Air Convention. |
| Producer / Agencies | **CEIP** (Vienna, Austria) — operates the gridded emissions database from national submissions. **MSC-W** (Oslo, Norway) — operates the chemistry-transport model, produces the annual EMEP Status Reports. **EBAS** (NILU, Norway) — operates the EMEP observation network (out of scope here). National emission submissions come from CLRTAP Parties — **for Romania, this is ANMAP (Agenția Națională pentru Mediu și Arii Protejate)**. |
| Status (May 2026) | **OPERATIONAL — open public access, no authentication required.** Gridded emissions updated annually (2025 release covers reporting year 2023, available now). MSC-W model v5.6 released **November 2025** based on the model version used for EMEP Status Report 1/2025. |
| Current versions | **CEIP gridded emissions 2025 release**: annual data for **1990–2023** (continuous time series). **EMEP MSC-W model v5.6** (released 202511, November 2025) — open source under GPLv3 on GitHub. |
| Pollutant species in CEIP gridded emissions | **Air pollutants:** NOx, NMVOC, SOx, NH₃, CO, PM₂.₅, PM₁₀, **PMcoarse** (PM10 minus PM2.5), BC. **Heavy metals (unique to EMEP among the project's inventories):** Cd (cadmium), Hg (mercury), Pb (lead). **Persistent organic pollutants (POPs, also unique to EMEP):** PCDD/PCDF (dioxins+furans), BaP (benzo[a]pyrene), BbF (benzo[b]fluoranthene), BkF (benzo[k]fluoranthene), Indeno (indeno[1,2,3-cd]pyrene), HCB (hexachlorobenzene). **The heavy metals and POPs are NOT in EDGAR Air Pollutants v8.1** — for any analysis involving Cd, Hg, Pb, dioxins, or PAHs over Cluj, EMEP is the primary inventory. |
| Sectoral resolution | **GNFR14** = Gridded Nomenclature For Reporting (14 sectors). **Different from EDGAR's IPCC 2006 codes** — bridge tables between GNFR14 and IPCC are documented in the EMEP/EEA Air Pollutant Emission Inventory Guidebook. GNFR sectors include: A (Public power), B (Industry), C (Other stationary combustion), D (Fugitives), E (Solvents), F (Road transport), G (Shipping), H (Aviation), I (Off-road), J (Waste), K (Agriculture livestock), L (Agriculture other), M (Other), N (Natural). The slightly different sectoral framing reflects EMEP's policy focus (sectoral emission reduction commitments) vs EDGAR's accounting focus (national emission attribution). |
| Spatial resolution | **0.1° × 0.1° regular lat/lon grid (WGS84)** — same resolution as EDGAR v8.1 Air Pollutants and CAMS European ENSEMBLE. Grid mandatory since reporting year 2017 (EMEP/CLRTAP decision ECE/AB.AIR/122/Add.1). **Before 2017, EMEP used a 50×50 km polar stereographic grid** — historical files in that older grid are still available but should not be mixed with the new 0.1° grid without explicit regridding. |
| Spatial coverage | **EMEP domain:** 30°N – 82°N latitude, 30°W – 90°E longitude — covers Europe, North Africa, Middle East to Caspian. **Cluj (46.77°N, 23.55°E) is well within the domain** with substantial margin for back-trajectory source-region analysis covering most of Europe + western Asia + northern Africa. |
| Temporal coverage | **Annual emissions from 1990 to 2023** (1990 onwards continuous; gridded mandatory every 4 years since 2017, in practice produced annually). **No monthly or sub-monthly resolution** in CEIP gridded data — for sub-annual variation, either use EDGAR monthly (where the species overlap) or apply EMEP/EEA Guidebook seasonal/diurnal profiles. |
| Update cadence and latency | **Annual** — typically the 2025 release (delivered ~mid-2025) covers reporting year 2023, so latency is roughly **2 years** from emission year to gridded availability. National submissions arrive in February-March of each year; CEIP processes and publishes the gridded products through mid-year. **Not NRT** — same operational limitation as EDGAR. |
| File format | **NetCDF** (CF-compliant) for gridded files. **CSV** (in ZIP archives) for tabular per-cell data with format `ISO2; YEAR; SECTOR; POLLUTANT; LONGITUDE; LATITUDE; UNIT; EMISSION`. Country totals also available as Excel summary tables. |
| Authentication | **NONE.** Direct download from CEIP website. **Like EDGAR, no credentials are required** — the project's emission-inventory inputs (GFED5, EDGAR, EMEP) all share this no-auth pattern. |
| Programmatic access | YES — direct HTTPS download of per-pollutant per-year files from `https://www.ceip.at/`. No formal API, but the URL structure is regular and predictable, making scripted bulk downloads straightforward. |
| Layer destination | **L2:** FLEXPART (European-domain anthropogenic emission input — alternative or complement to EDGAR; politically-validated source); EMEP MSC-W model (run directly or via CAMS ENSEMBLE member). **L3:** Knowledge Graph (sectoral attribution of European source regions using nationally-reported data — answers "what does Romania officially say about emissions in its territory, and how does this compare to EDGAR's independent estimate?"). |

### Two project-relevant uses of EMEP

#### 23.1 CEIP gridded emissions (the data product)

For project FLEXPART runs over the European source region affecting Cluj, the choice between EDGAR and CEIP gridded EMEP is non-trivial. **Both are at 0.1° resolution**, both cover Europe, both are open and free. **The key differences:**

| Property | **EDGAR v8.1 Air Pollutants** | **EMEP CEIP gridded** |
|---|---|---|
| Origin | JRC independent estimate (top-down from IEA/FAO activity data) | National official submissions (bottom-up from country inventories) |
| Geographic scope | Global | EMEP domain (Europe + North Africa + Middle East + western Asia) |
| Sectoral coding | IPCC 1996/2006 | GNFR14 |
| Temporal | Annual + monthly (2000+) | Annual only |
| Species | CO, NOx, NMVOC, NH₃, SO₂, PM10, PM2.5, BC, OC | NOx, NMVOC, SOx, NH₃, CO, PM2.5, PM10, PMcoarse, BC, **+ heavy metals (Cd, Hg, Pb), + POPs (dioxins, PAHs, HCB)** |
| Politically validated? | No — independent JRC estimate | **Yes — official national submissions** |
| Romania-specific accuracy | Good (uses IEA/FAO data) | **Highest available** (ANMAP submission) |
| Coverage start | 1970 | 1990 |
| Latency | ~2 years | ~2 years |
| Heavy metals + POPs | **NO** | **YES** |

**Project recommendation:** Use **both** in parallel. EDGAR provides global coverage + monthly resolution + longer time series; EMEP provides the politically-validated European baseline + heavy metals + POPs that EDGAR omits. **For any Cluj deliverable to local or EU regulatory audiences, citing EMEP alongside EDGAR is strategically important** — EMEP is the inventory the Romanian government itself submits to CLRTAP, making it the most defensible reference for any emission-related claim in project outputs.

#### 23.2 EMEP MSC-W chemistry-transport model (the model component)

The **EMEP MSC-W** model is a Eulerian chemistry-transport model developed at the Norwegian Meteorological Institute, used for:
- Producing the **annual EMEP Status Reports** on transboundary pollution across Europe
- **Supporting CLRTAP policy assessments** (which sources contribute to which receptors at what magnitude)
- **One of the 11 European-domain models in the CAMS European ENSEMBLE** (see `dataset_metadata_cams.md`) — so the project is **already implicitly using EMEP MSC-W outputs** via the CAMS ENSEMBLE mean

**Current version: v5.6 (released November 2025), GPLv3, open source on GitHub** (<https://github.com/metno/emep-ctm>).

**Project-relevant capabilities of EMEP MSC-W:**
- Detailed European-domain chemistry including full nitrate (ISORROPIA-style) and SOA — comparable chemistry detail to GEOS-Chem (see `dataset_metadata_geoschem.md`)
- Native horizontal resolution: 0.1° × 0.1° over Europe (matches EMEP gridded emissions exactly)
- Driven by ECMWF IFS meteorology (operational analysis or forecast)
- Heavy metals + POPs chemistry — capabilities EDGAR-driven CAMS and MERRA-2 do not have
- Used for the official European source-receptor relationship calculations (which Cluj contributes to / receives from)

**Realistic use cases for the project:**
- **Use case A — implicit via CAMS ENSEMBLE:** the project is already using EMEP MSC-W outputs via the CAMS European ENSEMBLE mean. **No additional infrastructure needed**; this is the default operational use.
- **Use case B — running EMEP MSC-W locally:** open source GPLv3, reproducible builds. **Compute requirement comparable to GEOS-Chem nested 0.1° over Europe (~500-2000 CPU-hours per month-simulated).** Same HPC requirement as GEOS-Chem. **Feasible only with HPC access.**
- **Use case C — referencing EMEP Status Reports:** annual reports synthesise the model's results for the whole European domain, with specific country-level chapters that include Romania. **Useful as a citable reference for project deliverables.**

**Compute alternative — EMEP4UK exists but no EMEP4RO equivalent.** The UK Centre for Ecology and Hydrology in Edinburgh runs a 1-km nested version of EMEP MSC-W over the British Isles (EMEP4UK). A Romanian-specific 1-km nest (EMEP4RO) does not currently exist — **this could be a notable medium-term project opportunity to flag**, as the underlying open-source MSC-W code supports user-defined nesting. Creating an EMEP4RO would mirror EMEP4UK at Cluj's scale and would significantly improve Romanian-domain air-quality modelling capability. Such an effort would require partnership with MSC-W (Oslo) and likely co-funding through the EMEP scientific programme.

### Sectoral codes: GNFR14 reference

GNFR14 (Gridded Nomenclature For Reporting, 14 sectors) used by EMEP gridded emissions:

| GNFR | Name | Cluj relevance |
|---|---|---|
| **A** | Public power | Large CHP/electricity sector — major NOx + SO₂ |
| **B** | Industry | Cement, chemicals, metals — local industrial sources |
| **C** | Other stationary combustion | **Residential heating** + commercial — winter PM peak |
| **D** | Fugitives | Fugitive emissions from fuel handling, mining |
| **E** | Solvents | Industrial + consumer solvent NMVOC |
| **F** | Road transport | **Primary local NOx + PM source** — Cluj urban traffic |
| **G** | Shipping | Negligible at Cluj (landlocked area) |
| **H** | Aviation | Cluj Airport (CLJ) — small but identifiable |
| **I** | Off-road | Off-road vehicles, agricultural machinery |
| **J** | Waste | Landfill, waste burning |
| **K** | Agriculture livestock | **Regional NH₃** — major source for nitrate aerosol formation |
| **L** | Agriculture other | Crop residues, fertilizer application — additional NH₃ + PM |
| **M** | Other | Miscellaneous |
| **N** | Natural | Excluded from anthropogenic inventory; biogenic sources |

**Bridging GNFR14 to EDGAR IPCC 2006 codes:** for project consistency, any layer that compares EMEP and EDGAR sectoral attributions must use the official bridge tables in the EMEP/EEA Air Pollutant Emission Inventory Guidebook (chapter A.7). Rough mapping: GNFR A → IPCC 1A1a (public power); GNFR B → IPCC 1A2 + 2A-2C (industry); GNFR C → IPCC 1A4 (residential + commercial heating); GNFR F → IPCC 1A3b (road transport); GNFR K+L → IPCC 3A+3D (agriculture); etc. **The mapping is not 1:1 in all cases** — flag any cross-inventory comparisons in deliverables.

### References

**EMEP MSC-W model — primary reference (always cite when EMEP model outputs are used or referenced):**
- Simpson, D., Benedictow, A., Berge, H., Bergström, R., Emberson, L. D., Fagerli, H., Flechard, C. R., Hayman, G. D., Gauss, M., Jonson, J. E., Jenkin, M. E., Nyíri, Á., Richter, C., Semeena, V. S., Tsyro, S., Tuovinen, J.-P., Valdebenito, Á., & Wind, P. (2012). The EMEP MSC-W chemical transport model — technical description. *Atmospheric Chemistry and Physics*, 12, 7825–7865. DOI: [10.5194/acp-12-7825-2012](https://doi.org/10.5194/acp-12-7825-2012)

**Annual updates to the model are described in EMEP Status Report updates chapters. Latest:**
- Simpson, D., Hood, C., van Caspel, W., Vieno, M., & Wind, P. (2025). Updates to the EMEP/MSC-W model, 2024–2025. In: *Transboundary particulate matter, photo-oxidants, acidifying and eutrophying components. EMEP Status Report 1/2025*, Norwegian Meteorological Institute, Oslo, Norway, pp. 195–203.

**Chemistry mechanism reference (relevant for any speciated chemistry work):**
- Bergström, R., Hayman, G. D., Jenkin, M. E., & Simpson, D. (2022). Update and comparison of atmospheric chemistry mechanisms for the EMEP MSC-W model system — EmChem19a, EmChem19X, CRIv2R5Em, CB6r2Em, and MCMv3.3Em. *EMEP MSC-W Technical Report* 1/2022, Norwegian Meteorological Institute.
- GenChem package: Bergström, R., et al. (2023). GenChem v1.0: a chemical pre-processor and box-modelling system. *Geoscientific Model Development*, 16, 7433. DOI: [10.5194/gmd-16-7433-2023](https://doi.org/10.5194/gmd-16-7433-2023)

**EMEP Status Report 1/2025 (the latest annual report — the canonical reference for the current state of European transboundary pollution):**
- Fagerli, H., et al. (2025). *Transboundary particulate matter, photo-oxidants, acidifying and eutrophying components. EMEP Status Report 1/2025*. The Norwegian Meteorological Institute, Oslo, Norway. Available at <https://emep.int/publ/reports/2025/>.

**CEIP emissions data citation (per-year):**
- Wankmüller, R., Ullrich, B., Mareckova, K., & Schindlbacher, S. (2025). *Inventory Review 2025: Review of emission data reported under the LRTAP Convention and the NEC Directive*. CEIP Technical Report 4/2025, Umweltbundesamt Vienna. (Annual CEIP reports document the methodology and review of submissions for each release.)

**EMEP/EEA Emission Inventory Guidebook (the methodology bible):**
- EMEP/EEA Air Pollutant Emission Inventory Guidebook — 2023 (with periodic chapter updates). European Environment Agency, EEA Report 6/2023. Available at <https://www.eea.europa.eu/publications/emep-eea-guidebook-2023>.

**EMEP4UK reference (for comparison with the UK nested model — relevant for proposing an EMEP4RO):**
- Vieno, M., Heal, M. R., Williams, M. L., Carnell, E. J., Nemitz, E., Stedman, J. R., & Reis, S. (2016). The sensitivities of emissions reductions for the mitigation of UK PM2.5. *Atmospheric Chemistry and Physics*, 16, 265–276. DOI: [10.5194/acp-16-265-2016](https://doi.org/10.5194/acp-16-265-2016)
- EMEP4UK website: <https://www.emep4uk.ceh.ac.uk/>

**Citation phrasing:** *"This work used the EMEP/MSC-W chemical transport model (Simpson et al., 2012) and the EMEP gridded emissions inventory produced by the Centre on Emission Inventories and Projections (CEIP), Umweltbundesamt, Vienna, in the framework of the UNECE Convention on Long-Range Transboundary Air Pollution."*

### Host / Server

**EMEP umbrella + governance:**
- **EMEP umbrella website:** <https://www.emep.int/>
- **CLRTAP under UNECE:** <https://unece.org/environment/air>
- **EMEP Steering Body documents:** annual decisions, scientific programme

**CEIP — gridded emissions database (the data product):**
- **CEIP main website:** <https://www.ceip.at/>
- **Gridded emissions page (per pollutant):** <https://www.ceip.at/the-emep-grid/gridded-emissions>
- **Country-specific data + grid cell fractions:** <https://www.ceip.at/the-emep-grid>
- **CEIP technical reports + data viewers:** <https://www.ceip.at/ceip-data-viewer> and <https://www.ceip.at/reports>
- **National submissions database (raw country files):** <https://www.ceip.at/data-status>

**EMEP MSC-W model (the chemistry-transport model):**
- **GitHub repository:** <https://github.com/metno/emep-ctm>
- **Read-the-docs documentation:** <https://emep-ctm.readthedocs.io/>
- **Latest release (v5.6, November 2025):** <https://github.com/metno/emep-ctm/releases>
- **GenChem chemistry preprocessor:** <https://github.com/metno/genchem>

**EMEP/EEA Emission Inventory Guidebook (methodology):**
- <https://www.eea.europa.eu/publications/emep-eea-guidebook-2023>

### Programmatic download

**Step 1 — Browse + download CEIP gridded emissions for a specific species and year:**

```python
import requests
import zipfile
import io

# Pattern for CEIP gridded emissions: per pollutant, per release year, per emission year
# 2025 release covers reporting year 2023

# NetCDF format (gridded, sector-specific)
species = "NOx"
emission_year = 2023
release_year = 2025

url = (f"https://www.ceip.at/.../{species}/{species}_{emission_year}_GRID_"
       f"{release_year}_GNFR.nc")
# Note: exact URL structure varies — verify on the CEIP pollutant page first

# CSV format (the tabular alternative, useful for direct database loads)
url_csv = (f"https://www.ceip.at/.../{species}/{species}_{emission_year}_GRID_"
           f"{release_year}_GNFR_csv.zip")

# Download + unzip CSV
response = requests.get(url_csv, stream=True)
response.raise_for_status()
with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
    zf.extractall(f"./emep_{species}_{emission_year}/")
```

**Step 2 — Reading CSV gridded data into pandas:**

```python
import pandas as pd

# CSV format from CEIP: ISO2; YEAR; SECTOR; POLLUTANT; LONGITUDE; LATITUDE; UNIT; EMISSION
df = pd.read_csv(
    f"./emep_NOx_2023/NOx_2023_GRID_2025.csv",
    sep=";",
    comment="#",
    names=["ISO2", "YEAR", "SECTOR", "POLLUTANT", "LON", "LAT", "UNIT", "EMISSION"],
    skiprows=lambda i: i < 4,   # skip header comments; verify with file inspection
)

# Filter to Romania only
ro = df[df["ISO2"] == "RO"]
print(f"Romania NOx emissions, 2023, all GNFR sectors: {ro['EMISSION'].sum():.2f} {ro['UNIT'].iloc[0]}")

# Filter to Cluj region grid cells (0.1° grid: lon 23.5-23.6, lat 46.7-46.8)
cluj = ro[(ro["LON"].between(23.4, 23.7)) & (ro["LAT"].between(46.6, 46.9))]
print(f"NOx emissions in Cluj area cells by sector:")
print(cluj.groupby("SECTOR")["EMISSION"].sum().sort_values(ascending=False))
```

**Step 3 — NetCDF read for FLEXPART/HEMCO ingestion:**

```python
import xarray as xr

ds = xr.open_dataset(f"./emep_NOx_2023/NOx_2023_GRID_2025_GNFR.nc")
# Typical structure:
# - dimensions: sector (14 GNFR sectors), lat, lon
# - variable: emis (kg/cell/year or kg/m²/s depending on the file)
# - global attributes: pollutant, year, release, grid description

# Sum across all sectors for total NOx
total_nox = ds["emis"].sum(dim="sector")

# Subset to broad Romania domain
ro_domain = ds.sel(lat=slice(43, 48.5), lon=slice(20, 30))
ro_per_sector = ro_domain["emis"].sum(dim=["lat", "lon"])
print(ro_per_sector)
```

**Step 4 — Cross-comparison with EDGAR (the operationally interesting analysis):**

```python
# Load both inventories on a common grid (both are at 0.1° — convenient)
emep_nox_ro = ... # from above
edgar_nox_ro = ... # from dataset_metadata_edgar.md workflow

# Compute total NOx for Romania from each inventory
emep_total = emep_nox_ro.sum().item()
edgar_total = edgar_nox_ro.sum().item()
discrepancy = (emep_total - edgar_total) / emep_total * 100

print(f"EMEP (Romania official): {emep_total:.0f} kt NOx/yr")
print(f"EDGAR (JRC independent): {edgar_total:.0f} kt NOx/yr")
print(f"Discrepancy: {discrepancy:+.1f}%")
# Typical discrepancy is 5-20% for OECD countries; >20% indicates an issue
```

**Step 5 — Building the EMEP MSC-W model from source (for use case B):**

```bash
# Clone the model repository
git clone https://github.com/metno/emep-ctm.git
cd emep-ctm
git checkout v5.6

# Download model results + input data using the catalog tool
wget https://raw.githubusercontent.com/metno/emep-ctm/tools/catalog.py
chmod +x catalog.py
./catalog.py     # interactive: pick what to download (~100 GB for meteorology)

# Build (requires NetCDF, MPI, Fortran compiler)
make
# Then submit a run via modrun.sh (the provided run script)
```

### Manual download (interactive web UI)

- **CEIP gridded data per pollutant:** <https://www.ceip.at/the-emep-grid/gridded-emissions> — drill into each pollutant page; download CSV (ZIP) or NetCDF for any year 1990–2023
- **Country totals (Excel) per year:** linked from each pollutant page — useful for quick Romania-specific context
- **EMEP Status Reports archive:** <https://emep.int/publ/reports/> — annual reports going back many years; Status Report 1/2025 is the current canonical reference
- **CEIP Data Viewer 2025:** interactive viewer with country + sector + pollutant filters at <https://www.ceip.at/ceip-data-viewer>

### Notes / caveats

- **EMEP is the politically-validated emission record for Europe; EDGAR is the independent estimate.** **Cite EMEP whenever the audience is European or Romanian regulatory** — EMEP is what national governments submit and is therefore the most defensible source for any emission-related claim in regulatory deliverables. EDGAR adds global coverage + monthly resolution but does not have the political endorsement. **For a Cluj early-warning system serving local authorities and first responders, the EMEP attribution chain is the more directly relevant lineage.**
- **Romania's emission submissions flow ANMAP → CEIP → gridded EMEP product.** The project's RNMCA observations (covered in `dataset_metadata_rnmca.md`) and Romania's EMEP submissions are produced by the same agency (ANMAP). **There is a direct institutional link between the project's ground observations and the EMEP gridded inventory** — both bottom-up products from the same national environmental authority. **Cross-checking RNMCA-observed concentrations against EMEP-estimated emissions over Cluj is operationally informative** and can flag potential under- or over-reporting in either dataset.
- **Heavy metals + POPs are unique to EMEP among the project's inventories.** EDGAR Air Pollutants v8.1 does **not** include Cd, Hg, Pb, dioxins, PAHs, or HCB. For any project deliverable that involves these species (rare for general aerosol warning, but relevant for any health-impact assessment or specific industrial-source attribution), **EMEP is the only inventory option** in the project's input data.
- **Heavy metals from biomass burning are also relevant.** A useful side-note: Cluj's winter PM2.5 (residential heating, wood + coal combustion) carries non-trivial Cd, Pb, BC, and PAH content. EMEP's heavy metals + POPs gridded data over the Cluj region quantifies this; combining it with the EMEP PM2.5 data gives a richer characterisation of "what's in the winter PM" than PM mass alone.
- **GNFR14 vs IPCC 2006 sectoral codes — bridge tables matter.** When comparing EMEP and EDGAR sectoral attributions, use the bridge tables in chapter A.7 of the EMEP/EEA Emission Inventory Guidebook. Direct comparison without translation can produce inconsistencies (e.g. EDGAR "1A4b residential" maps approximately but not exactly to EMEP "GNFR C other stationary combustion").
- **EMEP grid changed in 2017.** Before 2017 the grid was 50×50 km polar stereographic; since 2017 it is 0.1°×0.1° regular lat-lon WGS84. **Files from before 2017 are in the old grid and require careful regridding before comparison with current-grid data.** This is rarely an issue for project use (any recent analysis uses the post-2017 grid), but worth flagging if historical EMEP data is ever consulted.
- **Update cadence is annual.** New CEIP gridded emissions are released around mid-year, covering reporting year ≈ release year minus 2. **The project pipeline should plan an annual update window** to refresh EMEP data + verify reference DOIs.
- **EMEP MSC-W model is GPLv3.** Source code is free under GPLv3 (vs MIT for GEOS-Chem). The GPLv3 viral clause means: any derivative work that is distributed must also be GPLv3. **For the project's internal use this is not constraining**; if the project ever distributes a modified MSC-W model build, the modified code must also be GPLv3 — flag for any partnership planning.
- **EMEP4UK demonstrates the path for a hypothetical EMEP4RO.** The UK Centre for Ecology and Hydrology at Edinburgh runs EMEP4UK as a 1-km nested version over the British Isles, with WRF as the meteorological driver. **A Romanian-domain equivalent (EMEP4RO) does not exist** but is technically feasible with the open-source MSC-W code. Creating it would be a substantial project — typically 2-3 person-years for an experienced atmospheric-chemistry-modelling group — but would significantly enhance Romanian-domain air-quality modelling capability. **Flag this as a medium-term project opportunity** for ACTRIS Cluj / Babeș-Bolyai University in partnership with MSC-W (Oslo).
- **EMEP MSC-W is one of the 11 CAMS European ENSEMBLE models.** The project is **already using EMEP MSC-W outputs via the CAMS ENSEMBLE mean** — no extra ingestion needed for that use case. Running EMEP MSC-W directly (use case B) is a research-grade addition; running it via the CAMS interface (use case A) is the operational default.
- **No authentication needed for any path.** EMEP/CEIP data is fully open under CLRTAP. **EMEP closes out the project's emission-inventory cluster (GFAS, GFED5, EDGAR, EMEP) with the same no-auth open-access pattern** that the project's other authoritative emission sources share.
- **Citation matters for European regulatory credibility.** EMEP is the inventory the **EU references in policy work, the Romanian government references in environmental reporting, and the project should reference whenever Cluj's emission baseline is presented in any official capacity.** Use the JRC-recommended citation phrasing in every project document that involves EMEP data.

---
