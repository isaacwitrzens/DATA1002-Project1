import pandas as pd
df = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\HospitalisationsRawData.csv")
df = df[df["Period"] == "22/23"]
df = df[["LGA", "Period", "Rate per 100,000 population"]]
df = df.rename(columns={"Rate per 100,000 population": "Rate_per_100k"})
df.to_csv("HospitalisationsClean.csv", index=False)

crime = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\CrimeRawData.csv")
crime = crime[[
    "Suburb", "Offence category", "Subcategory",
    "Jan 2022","Feb 2022","Mar 2022","Apr 2022","May 2022","Jun 2022",
    "Jul 2022","Aug 2022","Sep 2022","Oct 2022","Nov 2022","Dec 2022",
    "Jan 2023","Feb 2023","Mar 2023","Apr 2023","May 2023","Jun 2023",
    "Jul 2023","Aug 2023","Sep 2023","Oct 2023","Nov 2023","Dec 2023"
]]

crime["Suburb"] = crime["Suburb"].str.strip().str.upper()

crime_with_lga = crime.merge(
    df[["LGA"]].drop_duplicates(),
    how="left",
    left_on="Suburb",
    right_on="LGA"  # might need a mapping if Suburb != LGA
)

unmatched = crime_with_lga[crime_with_lga["LGA"].isna()]["Suburb"].unique()
print("Suburbs with no LGA match:", unmatched)

crime_with_lga.to_csv(
    r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeWithHospitalisations.csv",
    index=False
)
