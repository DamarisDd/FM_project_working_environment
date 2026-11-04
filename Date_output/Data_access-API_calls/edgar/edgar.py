from pathlib import Path
from urllib.request import urlopen
import shutil
import zipfile

url = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/"
    "datasets/v81_FT2022_AP_new/NOx/TRO/emi_nc/"
    "v8.1_FT2022_AP_NOx_2022_TRO_emi_nc.zip"
)

output = Path("edgar_data")
output.mkdir(exist_ok=True)

archive = output / "NOx_2022_TRO.zip"

print("Downloading from JRC...")
with urlopen(url, timeout=120) as response, archive.open("wb") as file:
    shutil.copyfileobj(response, file)

with zipfile.ZipFile(archive) as zip_file:
    if zip_file.testzip() is not None:
        raise RuntimeError("Downloaded ZIP failed its integrity check.")

    for member in zip_file.infolist():
        if member.filename.lower().endswith(".nc"):
            target = output / Path(member.filename).name
            with zip_file.open(member) as source, target.open("wb") as file:
                shutil.copyfileobj(source, file)
            print("Saved:", target)
