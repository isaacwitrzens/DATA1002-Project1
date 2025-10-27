import pandas as pd

# --------------------------
# File paths
# --------------------------
crime_path = r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2\Suburb_CrimeCounts.csv"
liquor_path = r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2\LiquorLicenseClean.csv"
output_path = r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2\Cleaned.csv"

# --------------------------
# Load data
# --------------------------
crime = pd.read_csv(crime_path)
liquor = pd.read_csv(liquor_path)

# --------------------------
# Clean and normalise suburb names
# --------------------------
crime["Suburb"] = crime["Suburb"].str.strip().str.upper()
liquor["Suburb"] = liquor["Suburb"].str.strip().str.upper()

# Clean and normalise licence types
liquor["Licence type"] = liquor["Licence type"].str.strip().str.lower()

# --------------------------
# Focus on the six known licence types
# --------------------------
valid_licences = [
    "liquor - hotel licence",
    "liquor - club licence",
    "liquor - packaged liquor licence",
    "liquor - on-premises licence",
    "liquor - producer wholesaler licence",
    "liquor - limited licence"
]
liquor = liquor[liquor["Licence type"].isin(valid_licences)]

# --------------------------
# Count licences by suburb
# --------------------------
licence_counts = (
    liquor.groupby(["Suburb", "Licence type"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# --------------------------
# Rename licence columns to clean format
# --------------------------
rename_map = {
    "liquor - hotel licence": "Hotel_Licences",
    "liquor - club licence": "Club_Licences",
    "liquor - packaged liquor licence": "Packaged_Licences",
    "liquor - on-premises licence": "OnPremises_Licences",
    "liquor - producer wholesaler licence": "ProducerWholesaler_Licences",
    "liquor - limited licence": "Limited_Licences"
}
licence_counts = licence_counts.rename(columns=rename_map)

# Calculate total number of licences per suburb
licence_counts["Total_Licences"] = licence_counts[
    [
        "Hotel_Licences",
        "Club_Licences",
        "Packaged_Licences",
        "OnPremises_Licences",
        "ProducerWholesaler_Licences",
        "Limited_Licences"
    ]
].sum(axis=1)

# --------------------------
# Merge crime + liquor data
# --------------------------
merged = crime.merge(licence_counts, on="Suburb", how="inner")

# --------------------------
# Save clean merged dataset for modelling
# --------------------------
merged.to_csv(output_path, index=False)

from sklearn.model_selection import train_test_split

df = pd.read_csv("Cleaned.csv")
X = df[[
    "Hotel_Licences",
    "Club_Licences",
    "Packaged_Licences",
    "OnPremises_Licences",
    "ProducerWholesaler_Licences",
    "Limited_Licences",
    "Total_Licences"
]]
y = df["TotalCrimes"]

# 75% training, 25% temporary
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.25, random_state=42)

# Split the temporary set: 15% validation, 10% test overall
X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, test_size=0.4, random_state=42)

train = pd.concat([X_train, y_train], axis=1)
valid = pd.concat([X_valid, y_valid], axis=1)
test = pd.concat([X_test, y_test], axis=1)

train.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2\train.csv", index=False)
valid.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2\valid.csv", index=False)
test.to_csv(r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2\test.csv", index=False)

