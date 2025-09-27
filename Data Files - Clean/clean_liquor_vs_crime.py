import os
import pandas as pd

df = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\CrimeRawData.csv")
df = df[[
    "Suburb", "Offence category", "Subcategory",
    "Jan 2022","Feb 2022","Mar 2022","Apr 2022","May 2022","Jun 2022",
    "Jul 2022","Aug 2022","Sep 2022","Oct 2022","Nov 2022","Dec 2022",
    "Jan 2023","Feb 2023","Mar 2023","Apr 2023","May 2023","Jun 2023",
    "Jul 2023","Aug 2023","Sep 2023","Oct 2023","Nov 2023","Dec 2023"
]]
df.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean.csv", index=False)

liq = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean.csv")
df["Suburb"] = df["Suburb"].str.strip().str.upper()
liq["Suburb"] = liq["Suburb"].str.strip().str.upper()

crime_with_lga = df.merge(
    liq[["Suburb", "LGA"]].drop_duplicates(),
    on="Suburb",
    how="left"
)
unmatched = crime_with_lga[crime_with_lga["LGA"].isna()]["Suburb"].unique()
print("❌ Suburbs with no LGA match:", unmatched)

crime_suburbs = set(df["Suburb"].unique())
liq_suburbs   = set(liq["Suburb"].unique())
extra_in_liq = liq_suburbs - crime_suburbs
print(f"Total suburbs in liquor data: {len(liq_suburbs)}")
print(f"Total suburbs in crime data: {len(crime_suburbs)}")
print(f"Liquor-only suburbs: {len(extra_in_liq)}")
for s in extra_in_liq:
    print(s)

manual_map = {
    "WESTDALE"
    "CARRINGTON"
    "FLEMINGTON"
    "PUNCHBOWL"
    "SUMMER HILL"
    "SILVERWATER"
    "DALWOOD"
    "MAYFIELD"
    "GRANVILLE SOUTH"
    "ST CLAIR"
    "DURAL"
    "KINGSWOOD"
    "DARLINGTON":"DARLINGTON (SYDNEY)",
    "WOODBURN"
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



crime_with_lga.to_csv(
    r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeWithLGA.csv",
    index=False
)

