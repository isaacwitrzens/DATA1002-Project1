import os
import pandas as pd

def load_and_clean_crime(raw_path, clean_path):
    df = pd.read_csv(raw_path)
    month_cols = [
        "Jan 2022", "Feb 2022", "Mar 2022", "Apr 2022", "May 2022", "Jun 2022",
        "Jul 2022", "Aug 2022", "Sep 2022", "Oct 2022", "Nov 2022", "Dec 2022",
        "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023",
        "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023"
    ]
    df = df[["Suburb", "Offence category", "Subcategory"] + month_cols]
    df.dropna(subset=["Suburb"], inplace=True)

    df["TotalCrimes"] = df[month_cols].sum(axis=1)

    df = df.drop(columns=month_cols)

    df.to_csv(clean_path, index=False)
    return df

def load_liquor(path):
    return pd.read_csv(path)

def normalize_suburbs(df, col="Suburb"):
    """Standardize suburb names: strip + uppercase."""
    df[col] = df[col].str.strip().str.upper()
    return df

def apply_manual_map(df, manual_map, col="Suburb"):
    """Apply manual suburb corrections."""
    df[col] = df[col].replace(manual_map)
    return df

def merge_crime_liquor(crime, liquor):
    """Merge liquor LGA info into crime data."""
    merged = crime.merge(
        liquor[["Suburb", "LGA"]].drop_duplicates(),
        on="Suburb",
        how="left"
    )
    return merged

def drop_missing_lga(merged):
    return merged.dropna(subset=["LGA"])

raw_crime = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\CrimeRawData.csv"
clean_crime = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean.csv"
clean_liquor = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean.csv"

manual_map = {
    "WESTDALE":"WESTDALE (SNOWY VALLEYS)",
    "CARRINGTON":"CARRINGTON (NEWCASTLE)",
    "FLEMINGTON":"HOMEBUSH WEST",
    "PUNCHBOWL":"PUNCHBOWL (CANTERBURY-BANKSTOWN)",
    "SUMMER HILL":"SUMMER HILL (INNER WEST)",
    "SILVERWATER":"SILVERWATER (PARRAMATTA)",
    "GRANVILLE SOUTH":"GRANVILLE",
    "ST CLAIR":"ST CLAIR (PENRITH)",
    "DURAL":"DURAL (HORNSBY)",
    "KINGSWOOD":"KINGSWOOD (PENRITH)",
    "DARLINGTON":"DARLINGTON (SYDNEY)",
    "WOODBURN": "WOODBURN (SHOALHAVEN)",
    "THE ROCKS":"THE ROCKS (SYDNEY)",
    "HILL TOP":"HILL TOP (WINGECARRIBEE)",
    "LILLI PILLI":"LILLI PILLI (SUTHERLAND SHIRE)",
    "GREEN POINT":"GREEN POINT (CENTRAL COAST)",
    "ENMORE":"ENMORE (INNER WEST)",
    "MARYLAND":"MARYLAND (NEWCASTLE)",
    "SPRINGFIELD":"SPRINGFIELD (CENTRAL COAST)",
    "CROA":"CRONULLA",
    "BARANGAROO SYDNEY": "BARANGAROO",
}

# Run pipeline
df = load_and_clean_crime(raw_crime, clean_crime)
liq = load_liquor(clean_liquor)

df = normalize_suburbs(df)
liq = normalize_suburbs(liq)

df = apply_manual_map(df, manual_map)
liq = apply_manual_map(liq, manual_map)

crime_with_lga = merge_crime_liquor(df, liq)

crime_with_lga = drop_missing_lga(crime_with_lga)

# ⬇️ Override CrimeClean.csv instead of making a new file
crime_with_lga.to_csv(clean_crime, index=False)


CR = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean.csv'
crime = pd.read_csv(CR)
month_cols = [c for c in crime.columns if "2022" in c or "2023" in c]
crime["TotalCrimes"] = crime[month_cols].sum(axis=1)
lga_crimes = (
    crime.groupby("LGA", as_index=False)["TotalCrimes"]
         .sum()
         .sort_values("TotalCrimes", ascending=False)
)
out = CR.replace(".txt", "_LGA_CrimeCounts.csv").replace(".csv", "_LGA_CrimeCounts.csv")
lga_crimes.to_csv(out, index=False)