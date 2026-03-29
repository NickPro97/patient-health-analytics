import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame | None:
    """Load a CSV file into a DataFrame.
    
    Args:
        file_path: Path to the CSV file.
        
    Returns:
        DataFrame if file exists, None if not found.
    """
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Loaded {len(df)} rows from {file_path}")
        return df

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
def load_mimic_data(data_dir: str) -> dict[str, pd.DataFrame]:
    """Load all MIMIC-III datasets.
    
    Args:
        data_dir: Path to the data folder.
        
    Returns:
        Dictionary with patients, chartevents, d_items DataFrames.
        Empty dict if any file fails to load.
    """
    patients = load_csv(f"{data_dir}/PATIENTS.csv")
    chartevents = load_csv(f"{data_dir}/CHARTEVENTS.csv")
    d_items = load_csv(f"{data_dir}/D_ITEMS.csv")

    if patients is None or chartevents is None or d_items is None:
        print("Failed to load one or more MIMIC-III files.")
        return{}
    
    return {
        "patients": patients,
        "chartevents": chartevents,
        "d_items": d_items
    }

def get_patient_vitals(patient_id: int, chartevents: pd.DataFrame, vital_ids: list) -> pd.DataFrame:
    """Get vital sign readings for a specific patient.
    
    Args:
        patient_id: The patient's subject ID.
        chartevents: The chartevents DataFrame.
        vital_ids: List of vital sign item IDs to filter.
        
    Returns:
        DataFrame with the patient's vital sign readings.
    """
    patient_vitals = chartevents[
        (chartevents["subject_id"] == patient_id) &
        (chartevents["itemid"].isin(vital_ids))
    ]

    patient_vitals = patient_vitals.copy()
    return patient_vitals

def calculate_vital_stats(patient_vitals: pd.DataFrame, item_names: dict) -> dict:
    """Calculate statistics for each vital sign.
    
    Args:
        patient_vitals: DataFrame with patient's vital readings.
        item_names: Dict mapping itemid to readable name.
        
    Returns:
        Dict with stats (mean, min, max, count) for each vital sign.
    """
    stats = {}

    for item_id, name in item_names.items():
        readings = patient_vitals[patient_vitals["itemid"] == item_id]["valuenum"]

        if len(readings) > 0:
            stats[name] = {
                "mean": round(readings.mean(), 2),
                "min": readings.min(),
                "max": readings.max(),
                "count": readings.count()
            }
    
    return stats

def count_vitals_by_type(patient_vitals: pd.DataFrame) -> dict:
    """counts vitals types by id's

    Args:
        patient_vitals (pd.DataFrame): DataFrame with patient's 
        vital readings.

    Returns:
        dict: dict showing how many readings exist for 
        each itemid.
    """
    return patient_vitals["itemid"].value_counts().to_dict()

def get_multiple_patients_vitals(patient_ids: list[int], chartevents: pd.DataFrame, vital_ids: list[int]) -> pd.DataFrame:
    """Get vital sign readings for multiple patients.
    
    Args:
        patient_ids: List of patient subject IDs.
        chartevents: The chartevents DataFrame.
        vital_ids: List of vital sign item IDs to filter.
        
    Returns:
        DataFrame with vital readings for all specified patients.
    """
    patient_vitals = chartevents[
        (chartevents["subject_id"].isin(patient_ids)) &
        (chartevents["itemid"].isin(vital_ids))
    ]

    patient_vitals = patient_vitals.copy()
    return patient_vitals
    
if __name__ == "__main__":
    datasets = load_mimic_data("data")

    VITAL_IDS = [211, 220045, 618, 220210, 646, 220277]

    ITEM_NAMES = {
        211: "Heart Rate (CareVue)",
        220045: "Heart Rate (MetaVision)",
        618: "Respiratory Rate (CareVue)",
        220210: "Respiratory Rate (MetaVision)",
        646: "SpO2 (CareVue)",
        220277: "SpO2 (MetaVision)"
    }

    vitals = get_patient_vitals(40124, datasets["chartevents"], VITAL_IDS)
    print(f"\nPatient 40124 has {len(vitals)} vital sign readings")
    
    stats = calculate_vital_stats(vitals, ITEM_NAMES)
    for vital_name, vital_stats in stats.items():
        print(f"\n{vital_name}")
        print(f" Average: {vital_stats['mean']}, Min: {vital_stats['min']}, Max: {vital_stats['max']}, Count: {vital_stats['count']}")

    vital_counts = count_vitals_by_type(vitals)
    print(f"\nReadings per vital type: {vital_counts}")

    sample_ids = datasets["chartevents"]["subject_id"].unique()[:3].tolist()
    print(f"\nSample patient ID:s {sample_ids}")

    multi_vitals = get_multiple_patients_vitals(sample_ids, datasets["chartevents"], VITAL_IDS)
    print(f"\nTotal readings for {len(sample_ids)} patients: {len(multi_vitals)}")