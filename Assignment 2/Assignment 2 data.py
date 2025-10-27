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

print(f"✅ Cleaned and merged dataset saved to: {output_path}")
print(merged.head(10))
