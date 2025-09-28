import pandas as pd
import matplotlib.pyplot as plt

#loading file
combined_file = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv"
df = pd.read_csv(combined_file)

#total crimes boxplot count vs lga
plt.figure(figsize=(8,6))
ax = df.boxplot(column="TotalCrimes", vert=False)
plt.scatter(df["TotalCrimes"], [1]*len(df), alpha=0.6, color="blue")
plt.title("Total Crimes by LGA")
plt.xlabel("Total Crimes")
plt.yticks([])
plt.grid(False)
plt.show()

# Licenses boxplot count vs lga
plt.figure(figsize=(8,6))
ax = df.boxplot(column="license_count", vert=False)
plt.scatter(df["license_count"], [1]*len(df), alpha=0.6, color="green")
plt.title("Liquor License Count by LGA")
plt.xlabel("License Count")
plt.yticks([])
plt.grid(False)
plt.show()

# Hospitalisations rate vs lga box plot
plt.figure(figsize=(8,6))
ax = df.boxplot(column="Rate_per_100k", vert=False)
plt.scatter(df["Rate_per_100k"], [1]*len(df), alpha=0.6, color="red")
plt.title("Hospitalisation Rates by LGA")
plt.xlabel("Rate per 100k")
plt.yticks([])
plt.grid(False)
plt.show()

#summary stats - made a function to filter though the databases easily
def summary_stats(series, name):
    print(f"\n=== {name} Summary ===")
    print(f"N = {series.count()}")
    print(f"Mean = {series.mean():.2f}")
    print(f"Median = {series.median():.2f}")
    print(f"Range = {series.min()} – {series.max()}")
    print(f"Standard Deviation = {series.std():.2f}")
    print(f"IQR = {series.quantile(0.75) - series.quantile(0.25):.2f}")

    # top & bottom 5 LGAs
    print("\nTop 5 LGAs:")
    print(df.loc[series.nlargest(5).index, ["LGA", series.name]])
    print("\nBottom 5 LGAs:")
    print(df.loc[series.nsmallest(5).index, ["LGA", series.name]])

# Crime
summary_stats(df["TotalCrimes"], "Total Crimes")

# Liquor Licenses
summary_stats(df["license_count"], "Liquor License Count")

# Hospitalisations
summary_stats(df["Rate_per_100k"], "Hospitalisations per 100k")