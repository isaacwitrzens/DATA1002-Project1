import pandas as pd
RAW_HOSP = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\HospitalisationsRawData.csv"
CLEAN_HOSP = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\HospitalisationsClean.csv"

#getting rid of the unused columns
def main():
    hosp = pd.read_csv(RAW_HOSP)
    hosp = hosp[hosp["Period"] == "22/23"]
    hosp = hosp[["LGA", "Period", "Rate per 100,000 population"]]
    hosp = hosp.rename(columns={"Rate per 100,000 population": "Rate_per_100k"})
    hosp.to_csv(CLEAN_HOSP, index=False)

if __name__ == "__main__":
    main()