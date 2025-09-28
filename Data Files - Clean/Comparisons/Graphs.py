import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from scipy.stats import false_discovery_control

combined_file = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv"
df = pd.read_csv(combined_file)

#plt.scatter(df["TotalCrimes"], df["license_count"])
#plt.xlabel("Total Crimes")
#plt.ylabel("license_count")
#plt.title("Total Crimes vs license_count")
#plt.show()

#plt.scatter(df["Rate_per_100k"], df["license_count"])
#plt.xlabel("Hospitalisation Rate per 100k")
#plt.ylabel("license_count")
#plt.title("license_count vs Hospitalisation Rate")
#plt.show()

subset = df[df["LGA"] != "SYDNEY"]
#plt.scatter(subset["TotalCrimes"], subset["license_count"])
#plt.xlabel("Total Crimes")
#plt.ylabel("license_count")
#plt.title("Total Crimes vs license_count")
#plt.show()

#x = subset["TotalCrimes"]
#y = subset["license_count"]
#m, b = np.polyfit(x, y, 1)
#plt.scatter(x, y)
#plt.plot(x, m*x + b, color="red")  # add trendline
#plt.xlabel("Total Crimes")
#plt.ylabel("license_count")
#plt.title("Scatter with Linear Trendline")
#plt.show()


data = df[["license_count", "TotalCrimes"]]
bins = [1, 26, 51, 76, 101, 126, 151, 176, 201, 226]
labels = ["1–25","26–50","51–75","76–100","101–125","126–150","151–175","176–200","201–225"]
df["license_bin"] = pd.cut(df["license_count"], bins=bins, labels=labels, right=False)
grouped = df.groupby("license_bin", observed=False)["TotalCrimes"].sum()
grouped.plot(kind="bar", edgecolor="black")

plt.xlabel("License Count (binned)")
plt.ylabel("Total Crimes")
plt.title("Total Crimes by License Count Bin")
plt.xticks(rotation=45, ha="right")  # rotate labels and align right
plt.tight_layout()                   # auto-adjust layout so nothing is cut off
plt.show()
