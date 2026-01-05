import pandas as pd
import re
import os

#===============================
# DATA CLEANER & MERGER
# ==============================

RAW_PATH = "data/raw"
OUTPUT_PATH = "data/processed"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ------------------------------
# Helper functions
# ------------------------------

def clean_country_names(series):
    return (
        series
        .str.replace(r"\[.*?\]", "", regex=True)  # remove footnotes [1]
        .str.strip()
    )

def clean_numeric(series):
    return (
        series.astype(str)
        .str.replace(r"[^\d.]", "", regex=True)  # keep digits & decimals only
        .replace("", pd.NA)
        .astype(float)
    )

# ------------------------------
# Load raw datasets
# ------------------------------

gdp = pd.read_csv(f"{RAW_PATH}/data_raw_gdp.csv")
life = pd.read_csv(f"{RAW_PATH}/data_raw_life_expectancy.csv")
literacy = pd.read_csv(f"{RAW_PATH}/data_raw_literacy.csv")

# ------------------------------
# Standardize column names
# ------------------------------

gdp = gdp.rename(columns={
    gdp.columns[0]: "Country",
    gdp.columns[1]: "GDP_per_capita"
})

life = life.rename(columns={
    life.columns[0]: "Country",
    life.columns[1]: "Life_expectancy"
})

literacy = literacy.rename(columns={
    literacy.columns[0]: "Country",
    literacy.columns[1]: "Literacy_rate"
})

# ------------------------------
# Clean country names
# ------------------------------

gdp["Country"] = clean_country_names(gdp["Country"])
life["Country"] = clean_country_names(life["Country"])
literacy["Country"] = clean_country_names(literacy["Country"])

# ------------------------------
# Clean numeric values
# ------------------------------

gdp["GDP_per_capita"] = clean_numeric(gdp["GDP_per_capita"])
life["Life_expectancy"] = clean_numeric(life["Life_expectancy"])
literacy["Literacy_rate"] = clean_numeric(literacy["Literacy_rate"])

# ------------------------------
# Merge datasets
# ------------------------------

master_df = (
    gdp
    .merge(life, on="Country", how="inner")
    .merge(literacy, on="Country", how="inner")
)

# ------------------------------
# Save Master CSV
# ------------------------------

output_file = f"{OUTPUT_PATH}/master_country_stats.csv"
master_df.to_csv(output_file, index=False)

print("Data cleaning & merging complete!")
print(f"Master file saved to: {output_file}")
print(master_df.head())
