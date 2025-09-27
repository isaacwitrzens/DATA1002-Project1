import os
import pandas as pd

# --- Functions ---

def load_and_clean_crime(raw_path, clean_path):
    """Load raw crime data, select needed columns, save clean version."""
    df = pd.read_csv(raw_path)
    df = df[[
        "Suburb", "Offence category", "Subcategory",
        "Jan 2022","Feb 2022","Mar 2022","Apr 2022","May 2022","Jun 2022",
        "Jul 2022","Aug 2022","Sep 2022","Oct 2022","Nov 2022","Dec 2022",
        "Jan 2023","Feb 2023","Mar 2023","Apr 2023","May 2023","Jun 2023",
        "Jul 2023","Aug 2023","Sep 2023","Oct 2023","Nov 2023","Dec 2023"
    ]]
    df.dropna(subset=["Suburb"], inplace=True)
    df.to_csv(clean_path, index=False)
    return df

def load_liquor(path):
    """Load liquor license data."""
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

def report_unmatched(merged):
    """Show suburbs with no LGA match."""
    unmatched = merged[merged["LGA"].isna()]["Suburb"].unique()
    print("❌ Suburbs with no LGA match:", unmatched)
    return unmatched

def compare_suburb_sets(crime, liquor):
    """Compare suburb coverage between datasets."""
    crime_suburbs = set(crime["Suburb"].unique())
    liq_suburbs   = set(liquor["Suburb"].unique())
    extra_in_liq = liq_suburbs - crime_suburbs
    print(f"Total suburbs in liquor data: {len(liq_suburbs)}")
    print(f"Total suburbs in crime data: {len(crime_suburbs)}")
    print(f"Liquor-only suburbs: {len(extra_in_liq)}")
    for s in extra_in_liq:
        print(s)
    return extra_in_liq

def drop_missing_lga(merged):
    """Remove rows where LGA is missing."""
    return merged.dropna(subset=["LGA"])


# --- Main script ---

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
report_unmatched(crime_with_lga)
compare_suburb_sets(df, liq)

crime_with_lga = drop_missing_lga(crime_with_lga)

# ⬇️ Override CrimeClean.csv instead of making a new file
crime_with_lga.to_csv(clean_crime, index=False)
print("✅ Finished: CrimeClean.csv has been updated with LGA")

