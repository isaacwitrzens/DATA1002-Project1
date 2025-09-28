import re
import pandas as pd

crime_file = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean_LGA_CrimeCounts.csv'
liquor_file = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean_LGA_Counts.csv'
hosp_file  = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\HospitalisationsClean.csv'
out_file   = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv'

crime  = pd.read_csv(crime_file)
liquor = pd.read_csv(liquor_file)
hosp   = pd.read_csv(hosp_file)

def normalise_lga(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.replace(" LGA", "", regex=False)
    s = s.str.replace(r"\s*\(.*?\)", "", regex=True)  # drop "(...)" like "(INNER WEST)"
    s = s.str.strip().str.upper()
    return s

# --- Normalise LGA keys consistently
for df in (crime, liquor, hosp):
    df["LGA"] = normalise_lga(df["LGA"])

# --- Drop 'Period' if present
if "Period" in hosp.columns:
    hosp = hosp.drop(columns=["Period"])

# --- Clean hospital rate -> float
hosp["Rate_per_100k"] = (
    hosp["Rate_per_100k"].astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("e", "", regex=False)   # fixes things like '37156.7e'
    .str.strip()
)
hosp["Rate_per_100k"] = pd.to_numeric(hosp["Rate_per_100k"], errors="coerce")

# --- Apply rename map AFTER normalising (keys in UPPER)
rename_map = {
    "GUNDAGAI": "COOTAMUNDRA-GUNDAGAI REGIONAL",
    "NAMBUCCA VALLEY": "NAMBUCCA",
}
for df in (crime, liquor, hosp):
    df["LGA"] = df["LGA"].replace(rename_map)

# --- Ensure numeric & aggregate to one row per LGA
# CRIME: if TotalCrimes not present, sum month columns
if "TotalCrimes" not in crime.columns:
    month_cols = [c for c in crime.columns if re.match(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) 20\d{2}$", c)]
    if month_cols:
        crime[month_cols] = crime[month_cols].apply(pd.to_numeric, errors="coerce")
        crime["TotalCrimes"] = crime[month_cols].sum(axis=1)
    else:
        raise ValueError("No TotalCrimes column and no month columns found in crime file.")

crime["TotalCrimes"] = pd.to_numeric(crime["TotalCrimes"], errors="coerce")
crime_agg = crime.groupby("LGA", as_index=False)["TotalCrimes"].sum()

# LIQUOR
if "license_count" not in liquor.columns:
    raise ValueError("Expected 'license_count' column in liquor file.")
liquor["license_count"] = pd.to_numeric(liquor["license_count"], errors="coerce")
liquor_agg = liquor.groupby("LGA", as_index=False)["license_count"].sum()

# --- Diagnostics: check overlap after normalisation/renames
set_crime, set_liquor, set_hosp = set(crime_agg["LGA"]), set(liquor_agg["LGA"]), set(hosp["LGA"])
print("Overlap:",
      "crime∩hosp =", len(set_crime & set_hosp),
      "| liquor∩hosp =", len(set_liquor & set_hosp))

# --- Merge ONTO hospitals (left join) to avoid stray suburbs
merged = (
    hosp[["LGA", "Rate_per_100k"]]
    .merge(crime_agg,  on="LGA", how="left")
    .merge(liquor_agg, on="LGA", how="left")
)

# Optional: see how many NaNs remain and sample a few problem LGAs
print(merged.isna().sum())
missing_crime = merged[merged["TotalCrimes"].isna()]["LGA"].head(10).tolist()
missing_lic   = merged[merged["license_count"].isna()]["LGA"].head(10).tolist()
print("Example LGAs missing crime:", missing_crime)
print("Example LGAs missing liquor:", missing_lic)

merged.to_csv(out_file, index=False)
print(f"Saved {len(merged)} LGAs to {out_file}")