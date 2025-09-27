import pandas as pd
df = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\LiqourLicenseRawData.csv")
df = df[df["Licence type"] == "Liquor - packaged liquor licence"]
df = df[["Licence type", "Suburb", "LGA"]]
df.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\LiquorLicenseClean.csv", index=False)
