import pandas as pd
df = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\HospitalisationsRawData.csv")
df = df[df["Period"] == "22/23"]
df = df[["LGA", "Period", "Rate per 100,000 population"]]
df = df.rename(columns={"Rate per 100,000 population": "Rate_per_100k"})
df.to_csv("HospitalisationsClean.csv", index=False)