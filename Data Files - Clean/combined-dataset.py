import pandas as pd
crime_file = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean_LGA_CrimeCounts.csv'
liquor_file = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean_LGA_Counts.csv'
hosp_file  = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\HospitalisationsClean.csv'
out_file   = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv'

crime = pd.read_csv(crime_file)
liquor = pd.read_csv(liquor_file)
hosp = pd.read_csv(hosp_file)

crime['LGA'] = crime['LGA'].str.strip()
liquor['LGA'] = liquor['LGA'].str.replace(" LGA", "", regex=False).str.strip()
hosp['LGA'] = hosp['LGA'].str.replace(" LGA", "", regex=False).str.strip()

hosp = hosp.drop(columns=['Period'])

merged = crime.merge(liquor, on="LGA", how="outer")
merged = merged.merge(hosp, on="LGA", how="outer")

merged.to_csv(out_file, index=False)