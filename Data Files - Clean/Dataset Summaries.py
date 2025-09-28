import pandas as pd

combined_file = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv"
df = pd.read_csv(combined_file)
print("=== Crime Summary ===")
print(df["TotalCrimes"].describe())

print("\n=== Liquor License Summary ===")
print(df["license_count"].describe())

print("\n=== Hospitalisations Summary ===")
print(df["Rate_per_100k"].describe())