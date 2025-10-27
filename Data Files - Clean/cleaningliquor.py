import pandas as pd
df = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\LiqourLicenseRawData.csv")
#getting rid of unused columns
df = df[["Licence type", "Suburb"]]
df.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean.csv", index=False)

#counting license by lga
#LQ = r'C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean.csv'
#liq = pd.read_csv(LQ)
#liq["LGA"] = liq["LGA"].astype(str).str.strip()
#lga_counts = liq.groupby("LGA", as_index=False).size().rename(columns={"size": "license_count"})
#ga_counts = lga_counts.sort_values("license_count", ascending=False)
#out1 = LQ.replace(".txt", "_LGA_Counts.csv").replace(".csv", "_LGA_Counts.csv")
#lga_counts.to_csv(out1, index=False)