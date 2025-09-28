import pandas as pd
import matplotlib.pyplot as plt

combined_file = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv"
df = pd.read_csv(combined_file)


print("=== Crime Summary ===")
print(df["TotalCrimes"].describe())
df.boxplot(column="TotalCrimes")
plt.title("boxplot of total crimes")
plt.ylabel("total crime")
plt.show()

print("\n=== Liquor License Summary ===")
print(df["license_count"].describe())
df.boxplot(column="license_count")
plt.title("boxplot of license_count")
plt.ylabel("license_count")
plt.show()

print("\n=== Hospitalisations Summary ===")
print(df["Rate_per_100k"].describe())
df.boxplot(column="Rate_per_100k")
plt.title("boxplot of Rate_per_100k")
plt.ylabel("Rate_per_100k")
plt.show()