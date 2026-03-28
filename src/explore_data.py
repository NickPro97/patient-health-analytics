import pandas as pd

# patients = pd.read_csv("data/PATIENTS.csv")
# print(f"Total patients: {len(patients)}")
# print(f"\nColumns: {list(patients.columns)}")
# print("\nFirst 5 patients:")
# print(patients.head())

# print("\n--- CHARTEVENTS (Vital Signs) ---")
# chartevents = pd.read_csv("data/CHARTEVENTS.csv")
# print(f"Total vital sign records: {len(chartevents)}")
# print(f"\nColumns: {list(chartevents.columns)}")
# print("\nFirst 5 rows:")
# print(chartevents.head())

# print("\n--- D_ITEMS (Dictionary) ---")
# d_items = pd.read_csv("data/D_ITEMS.csv")
# print(f"Total items in dictionary: {len(d_items)}")
# print(f"\nColumns: {list(d_items.columns)}")
# print("\nFirst 5 items:")
# print(d_items.head())

# print("\n--- All DB Sources ---")
# print(d_items["dbsource"].unique())

# heart_rate_items = d_items[d_items["label"].str.contains("Heart Rate", na=False)]
# bp_items = d_items[d_items["label"].str.contains("Blood Pressure", na=False)]
# spo2_items = d_items[d_items["label"].str.contains("SpO2", na=False)]

# print("\n--- Heart Rate codes ---")
# print(heart_rate_items[["itemid", "label", "dbsource"]])
# print("\n--- Blood Pressure codes ---")
# print(bp_items[["itemid", "label", "dbsource"]])
# print("\n--- SpO2 codes ---")
# print(spo2_items[["itemid", "label", "dbsource"]])

# VITAL_SIGNS = ["Heart Rate", "Blood Pressure", "SpO2"]

# for vital in VITAL_SIGNS:
#     matches = d_items[d_items["label"].str.contains(vital, na=False)]
#     print(f"\n--- {vital} codes ---")
#     print(matches[["itemid", "label", "dbsource"]])

# spo2_check = d_items[d_items["label"].str.contains("SpO2|O2 sat|Oxygen sat", case=False, na=False)]
# print("\n--- SpO2 expanded search ---")
# print(spo2_check[["itemid", "label", "dbsource"]])

# Load data
patients = pd.read_csv("data/PATIENTS.csv")
chartevents = pd.read_csv("data/CHARTEVENTS.csv")
d_items = pd.read_csv("data/D_ITEMS.csv")

# VITAL SIGN ITEM IDS (verified from D_ITEMS)
VITAL_SIGN_IDS = {
    "heart_rate": [211, 220045],
    "bp_systolic": [220050, 220179],
    "bp_diastolic": [220051, 220180],
    "spo2": [646, 220277],
}

all_vital_ids = []
for ids in VITAL_SIGN_IDS.values():
    all_vital_ids.extend(ids)

print(f"Tracking {len(all_vital_ids)} vital sign codes: {all_vital_ids}")

# STEP 2: Get one patient's vital signs

patient_id = 40124

# Filter: keep only rows where subject_id matches AND itemid is one of our vital signs
patient_vitals = chartevents[
    (chartevents["subject_id"] == patient_id) &
    (chartevents["itemid"].isin(all_vital_ids))
]

print(f"\nPatient {patient_id} vital sign records: {len(patient_vitals)}")
print(patient_vitals[["charttime", "itemid", "valuenum", "valueuom"]].head(10))

# STEP 3: Make it readable — replace itemid with names

ITEM_NAMES = {
    211: "Heart Rate",
    220045: "Heart Rate",
    220050: "BP Systolic",
    220179: "BP Systolic",
    220051: "BP Diastolic",
    220180: "BP Diastolic",
    646: "SpO2",
    220277: "SpO2",
}

patient_vitals = patient_vitals.copy()
patient_vitals["vital_name"] = patient_vitals["itemid"].map(ITEM_NAMES)

print(f"\n--- Patient {patient_id} Vital Signs (Readable) ---")
print(patient_vitals[["charttime", "vital_name", "valuenum", "valueuom"]].head(10))