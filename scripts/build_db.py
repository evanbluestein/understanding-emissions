"""Clean the raw data files and save each one as a table in data/emissions.db.

Run from the project root:  uv run python scripts/build_db.py

Tables created:
    owid_co2          one row per country per year   CO2 emissions (million tonnes)
    owid_energy       one row per country per year   Electricity and energy by source
    noaa_co2_monthly  one row per month, 1958-       CO2 in the atmosphere (ppm)
    gistemp_monthly   one row per month, 1880-       Temperature vs. 1951-1980 average (degC)
    gistemp_annual    one row per year, 1880-        Same, yearly average (complete years only)

The database is deleted and rebuilt from scratch every time this runs.
"""

import sqlite3
from pathlib import Path

import pandas as pd

# Folder locations, worked out from where this script lives
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
RAW_DATA_FOLDER = PROJECT_FOLDER / "data" / "raw"
DATABASE_FILE = PROJECT_FOLDER / "data" / "emissions.db"

MONTH_NUMBERS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def load_owid(filename: str) -> pd.DataFrame:
    """Read an Our World in Data file. These are already clean."""
    return pd.read_csv(RAW_DATA_FOLDER / "Our_World_in_Data" / filename)


def load_noaa() -> pd.DataFrame:
    """Read NOAA's monthly Mauna Loa CO2 file."""
    # Lines starting with "#" are notes, not data
    df = pd.read_csv(RAW_DATA_FOLDER / "NOAA" / "co2_mm_mlo.csv", comment="#")

    # Column names with spaces are awkward in SQL
    df = df.rename(columns={"decimal date": "decimal_date"})

    # NOAA writes negative numbers in these three columns to mean "no data".
    # This happens for every month before 1974 and for months NOAA filled in.
    # Record which rows those are, then replace the fake numbers with blanks.
    df["stats_unavailable"] = df["unc"] < 0
    for column in ["ndays", "sdev", "unc"]:
        df.loc[df[column] < 0, column] = None

    return df


def load_gistemp_monthly() -> pd.DataFrame:
    """Read NASA's temperature file as one row per month."""
    df = read_gistemp_file()

    # NASA's file has one row per year, with a column for each month.
    # Reshape it to one row per month: year, month, anomaly_c.
    df = df.melt(
        id_vars="year",
        value_vars=list(MONTH_NUMBERS),
        var_name="month_name",
        value_name="anomaly_c",
    )

    # "Jan" -> 1, "Feb" -> 2, ... so months sort in calendar order
    df["month"] = df["month_name"].map(MONTH_NUMBERS)

    # Months that haven't happened yet have no value
    df = df.dropna(subset=["anomaly_c"])

    df = df[["year", "month", "anomaly_c"]]
    df = df.sort_values(["year", "month"])
    return df


def load_gistemp_annual() -> pd.DataFrame:
    """Read NASA's temperature file as one row per year."""
    df = read_gistemp_file()

    # "J-D" is NASA's January-December average
    df = df[["year", "J-D"]]
    df = df.rename(columns={"J-D": "anomaly_c"})

    # The current year has no annual average until December is in
    df = df.dropna(subset=["anomaly_c"])
    return df


def read_gistemp_file() -> pd.DataFrame:
    """Read NASA's raw file, shared by the monthly and annual loaders."""
    # Line 1 is a title, and NASA writes "***" for missing values
    df = pd.read_csv(
        RAW_DATA_FOLDER / "NASA" / "GLB.Ts+dSST.csv",
        skiprows=1,
        na_values="***",
    )
    return df.rename(columns={"Year": "year"})


def main() -> None:
    tables = {
        "owid_co2": load_owid("owid_co2.csv"),
        "owid_energy": load_owid("owid_energy.csv"),
        "noaa_co2_monthly": load_noaa(),
        "gistemp_monthly": load_gistemp_monthly(),
        "gistemp_annual": load_gistemp_annual(),
    }

    # Start fresh so old data never mixes with new
    DATABASE_FILE.unlink(missing_ok=True)

    with sqlite3.connect(DATABASE_FILE) as connection:
        for table_name, df in tables.items():
            df.to_sql(table_name, connection, index=False)
            print(f"{table_name}: {len(df):,} rows")

        # Indexes make lookups by country and year fast in the two big tables
        connection.execute("CREATE INDEX idx_owid_co2 ON owid_co2 (country, year)")
        connection.execute("CREATE INDEX idx_owid_energy ON owid_energy (country, year)")

    print(f"Saved {DATABASE_FILE}")


if __name__ == "__main__":
    main()
