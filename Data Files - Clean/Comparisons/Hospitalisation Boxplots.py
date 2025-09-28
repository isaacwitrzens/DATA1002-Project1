import matplotlib.pyplot as plt
import pandas as pd

#loading file
combined_file = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv"
df = pd.read_csv(combined_file)

##boxplots of hospitalisation rates in 10 individual bins of liquor license counts
bins = [1, 26, 51, 76, 101, 126, 151, 176, 201, 226]
labels = ["1–25","26–50","51–75","76–100","101–125", "126–150","151–175","176–200","201–225"]
df["license_bin"] = pd.cut(df["license_count"], bins=bins, labels=labels, right=False)
plt.figure(figsize=(10,6))
df.boxplot(column="Rate_per_100k", by="license_bin", grid=False)
plt.title("Hospitalisation Rates by Liquor License Count")
plt.suptitle("")
plt.xlabel("License Count")
plt.ylabel("Hospitalisation Rate per 100k")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()