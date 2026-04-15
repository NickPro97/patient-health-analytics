"""NumPy operations for patient vital sign analysis."""
import numpy as np

heart_rates = np.array([72, 85, 91, 68, 110, 78, 95, 88, 76, 102])

print(f"Heart rates: {heart_rates}")
print(f"Mean: {np.mean(heart_rates)}")
print(f"Min: {np.min(heart_rates)}")
print(f"Max: {np.max(heart_rates)}")

# --- NumPy array vs Python list ---
python_list = [72, 85, 91, 68, 110]
numpy_array = np.array([72, 85, 91, 68, 110])

# Try multiplying everything by 2
print(f"\nPython list * 2: {python_list * 2}")
print(f"NumPy array * 2: {numpy_array * 2}")

# --- Z-score anomaly detection ---
def detect_anomalies(readings: np.ndarray, threshold: float = 2.0) -> np.ndarray:
    """Flag readings that are abnormally high or low using z-scores.
    
    Args:
        readings: Array of vital sign values.
        threshold: Z-score above which a reading is flagged (default 2.0).
    
    Returns:
        Boolean array — True where reading is anomalous.
    """
    mean = np.mean(readings)
    std = np.std(readings)
    z_scores = (readings - mean) / std
    return np.abs(z_scores) > threshold

# --- Test with an extreme value ---
sick_patient = np.array([72, 85, 91, 68, 110, 78, 95, 88, 76, 180])
anomalies2 = detect_anomalies(sick_patient)
print(f"\nWith sick patient: {sick_patient}")
print(f"Anomalies:         {anomalies2}")
print(f"Flagged values:    {sick_patient[anomalies2]}")

# --- Boolean indexing exercises ---
temps = np.array([97.2, 98.6, 101.3, 99.1, 103.8, 98.4, 100.5])

# Exercise 1: Get only temperatures above 100 (fever)
fevers = temps[temps > 100]
print(f"\nAll temps: {temps}")
print(f"Fevers (>100): {fevers}")

# Exercise 2: Get only normal temps (between 97 and 99)
normal = temps[(temps >= 97) & (temps <= 99)]
print(f"Normal temps: {normal}")

spo2 = np.array([98, 95, 88, 97, 92, 85, 99, 91, 84, 96])

critical_readings = spo2[spo2 < 90]
print(f"Critical readings: {critical_readings}")

concerning_readings = spo2[(spo2 >= 90) & (spo2 <= 94)]
print(f"Concerning readings: {concerning_readings}")
count_critical = np.sum(spo2 < 90)
print(f"Count Critical readings: {count_critical}")