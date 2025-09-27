import pandas as pd
hosp = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\HospitalisationsRawData.csv")
hosp = hosp[hosp["Period"] == "22/23"]
hosp = hosp[["LGA", "Period", "Rate per 100,000 population"]]
hosp = hosp.rename(columns={"Rate per 100,000 population": "Rate_per_100k"})
hosp.to_csv("HospitalisationsClean.csv", index=False)

crime = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\CrimeRawData.csv")
crime = crime[[
    "Suburb", "Offence category", "Subcategory",
    "Jan 2022","Feb 2022","Mar 2022","Apr 2022","May 2022","Jun 2022",
    "Jul 2022","Aug 2022","Sep 2022","Oct 2022","Nov 2022","Dec 2022",
    "Jan 2023","Feb 2023","Mar 2023","Apr 2023","May 2023","Jun 2023",
    "Jul 2023","Aug 2023","Sep 2023","Oct 2023","Nov 2023","Dec 2023"
]]

crime["Suburb"] = crime["Suburb"].str.strip().str.upper()
manual_map = {
    "DARLINGTON": "SYDNEY",
    "THE ROCKS": "SYDNEY",
    "HILL TOP": "WINGECARRIBEE",
    "LILLI PILLI": "SUTHERLAND SHIRE",
    "GREEN POINT": "CENTRAL COAST",
    "ENMORE": "INNER WEST",
    "MARYLAND": "NEWCASTLE",
    "SPRINGFIELD": "CENTRAL COAST",
    "BARANGAROO": "SYDNEY",
    "CRONULLA": "SUTHERLAND SHIRE",
}

crime["LGA"] = crime["Suburb"].replace(manual_map)
crime_with_hosp = crime.merge(
    hosp[["LGA", "Rate_per_100k"]],
    on="LGA",
    how="left"
)

unmatched = crime_with_hosp[crime_with_hosp["Rate_per_100k"].isna()]["Suburb"].unique()
print("❌ Suburbs with no hospitalisation LGA match:", unmatched)

crime_with_hosp.to_csv(
    r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeWithHospitalisations.csv",
    index=False
)
