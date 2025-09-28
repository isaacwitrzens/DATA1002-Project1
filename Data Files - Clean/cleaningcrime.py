import os
import pandas as pd

# selected columns from raw data to created clean data set
# selected only 2022/2023 dates and combined them into a count by crime
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

# using liquor data set to give the crime data set an LGA column so that the datasets will only have the same LGAs
def load_liquor(path):
    return pd.read_csv(path)

#normalising suburb names so theyre all upper case
def normalise_suburbs(df, col="Suburb"):
    df[col] = df[col].str.strip().str.upper()
    return df

#normalising lga names so theyre all upper case
def normalise_lga(df, col="LGA"):
    if col in df.columns:
        df[col] = df[col].str.replace(" LGA", "", regex=False).str.strip().str.upper()
    return df

#function to apply the manual map with name changes
def apply_manual_map(df, manual_map, col="Suburb"):
    df[col] = df[col].replace(manual_map)
    return df

#using the liqour dataset to give the suburbs in the crime data set their LGA
def merge_crime_liquor(crime, liquor):
    lookup = liquor[["Suburb","LGA"]].drop_duplicates()
    merged = crime.merge(lookup, on="Suburb", how="left")
    return merged

#getting rid of suburbs with missing LGA because then they cant be compared with the liquor dataset
def drop_missing_lga(merged):
    return merged.dropna(subset=["LGA"])

#manually changing suburb names in both data sets to make them equal
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
#loading my functions
crime_df = load_and_clean_crime(raw_crime, clean_crime)
liq_df = load_liquor(clean_liquor)
crime_df = normalise_suburbs(crime_df)
liq_df   = normalise_suburbs(liq_df)
crime_df = apply_manual_map(crime_df, manual_map)
liq_df   = apply_manual_map(liq_df, manual_map)

crime_with_lga = merge_crime_liquor(crime_df, liq_df)
crime_with_lga = drop_missing_lga(crime_with_lga)
crime_with_lga = normalise_lga(crime_with_lga, "LGA")

crime_with_lga.to_csv(clean_crime, index=False)

#getting rid of the individual crimes and grouping by LGA
CR = clean_crime
crime = pd.read_csv(CR)
crime = normalise_lga(crime, "LGA")

lga_crimes = (
    crime.groupby("LGA", as_index=False)["TotalCrimes"]
         .sum()
         .sort_values("TotalCrimes", ascending=False)
)

out = os.path.splitext(CR)[0] + "_LGA_CrimeCounts.csv"
lga_crimes.to_csv(out, index=False)

