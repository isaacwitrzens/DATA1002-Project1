import pandas as pd
df = pd.read_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Raw\CrimeRawData.csv")
df = df[[
    "Suburb", "Offence category", "Subcategory",
    "Jan 2022","Feb 2022","Mar 2022","Apr 2022","May 2022","Jun 2022",
    "Jul 2022","Aug 2022","Sep 2022","Oct 2022","Nov 2022","Dec 2022",
    "Jan 2023","Feb 2023","Mar 2023","Apr 2023","May 2023","Jun 2023",
    "Jul 2023","Aug 2023","Sep 2023","Oct 2023","Nov 2023","Dec 2023"
]]
df.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\CrimeClean.csv", index=False)
