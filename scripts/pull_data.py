"""Download the raw data files into data/raw/<source>/.

Run from the project root:  uv run python scripts/pull_data.py

Existing files are replaced with the latest versions.
"""

from pathlib import Path

import requests

# Folder locations, worked out from where this script lives
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
RAW_DATA_FOLDER = PROJECT_FOLDER / "data" / "raw"

# Where to save each file (inside data/raw/), and where to download it from
FILES_TO_DOWNLOAD = {
    "NOAA/co2_mm_mlo.csv": "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv",
    "NASA/GLB.Ts+dSST.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv",
    "Our_World_in_Data/owid_co2.csv": "https://catalog.ourworldindata.org/emissions/owid_co2/owid_co2.csv",
    "Our_World_in_Data/owid_co2.codebook.csv": "https://catalog.ourworldindata.org/emissions/owid_co2/owid_co2.codebook.csv",
    "Our_World_in_Data/owid_energy.csv": "https://catalog.ourworldindata.org/energy/owid_energy/owid_energy.csv",
    "Our_World_in_Data/owid_energy.codebook.csv": "https://catalog.ourworldindata.org/energy/owid_energy/owid_energy.codebook.csv",
}

# Give up on a server that hasn't responded after this many seconds
TIMEOUT_SECONDS = 120


def download(save_as: str, url: str) -> None:
    """Download one file and save it inside data/raw/."""
    save_path = RAW_DATA_FOLDER / save_as

    # Create the folder (e.g. data/raw/NOAA/) if it doesn't exist yet
    save_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {save_as} ...", end=" ", flush=True)
    response = requests.get(url, timeout=TIMEOUT_SECONDS)

    # Stop with an error if the server sent an error page instead of the file
    response.raise_for_status()

    save_path.write_bytes(response.content)

    size_in_mb = len(response.content) / 1_000_000
    print(f"{size_in_mb:.1f} MB")


def main() -> None:
    for save_as, url in FILES_TO_DOWNLOAD.items():
        download(save_as, url)


if __name__ == "__main__":
    main()
