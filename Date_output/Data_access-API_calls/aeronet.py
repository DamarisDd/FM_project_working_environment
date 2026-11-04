import csv
import io
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


def download_text(url):
    with urlopen(url, timeout=120) as response:
        return response.read().decode("utf-8-sig")


# Resolve the exact site identifier from NASA's catalogue.
catalogue = download_text(
    "https://aeronet.gsfc.nasa.gov/aeronet_locations_v3.txt"
)

sites = [
    row[0].strip()
    for row in csv.reader(io.StringIO(catalogue))
    if row and "cluj" in row[0].lower()
]

print("Cluj sites in NASA's catalogue:", sites)

site = next(
    (name for name in sites if name.casefold() == "cluj_ubb"),
    None,
)

if site is None:
    raise RuntimeError(
        "Could not resolve CLUJ_UBB. Check the printed site names."
    )

# Request a historical month, including explicit start and end dates.
parameters = {
    "site": site,
    "year": 2025,
    "month": 6,
    "day": 1,
    "year2": 2025,
    "month2": 6,
    "day2": 30,
    "AOD15": 1,
    "AVG": 10,
    "if_no_html": 1,
}

url = (
    "https://aeronet.gsfc.nasa.gov/cgi-bin/print_web_data_v3?"
    + urlencode(parameters)
)

print("Requesting:", url)
text = download_text(url)

# Measurement rows contain a date followed by a time.
observations = [
    line
    for line in text.splitlines()
    if re.search(
        r"(?:^|,)\d{2}:\d{2}:\d{4},\d{2}:\d{2}:\d{2}(?:,|$)",
        line,
    )
]

if not observations:
    print("\nServer response:\n", text[:3000])
    raise RuntimeError(
        "No observation rows returned. No measurement file was saved."
    )

output = Path(__file__).resolve().parent / "cluj_aod15_202506.txt"
output.write_text(text, encoding="utf-8")

print(f"Downloaded {len(observations)} observation rows.")
print(f"Saved to: {output}")