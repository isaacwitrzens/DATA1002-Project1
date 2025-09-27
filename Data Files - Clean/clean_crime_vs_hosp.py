import pandas as pd

CLEAN_HOSP  = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\HospitalisationsClean.csv"
CLEAN_CRIME = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean.csv"
OUT_FILE    = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeWithHospitalisations.csv"

def main():
    hosp = pd.read_csv(CLEAN_HOSP)
    crime = pd.read_csv(CLEAN_CRIME)

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

    crime_with_hosp.to_csv(OUT_FILE, index=False)
    print(f"✅ Saved merged dataset: {OUT_FILE}")

if __name__ == "__main__":
    main()
