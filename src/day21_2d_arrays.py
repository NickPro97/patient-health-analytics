import numpy as np

# --- 2D arrays: patient vitals matrix ---
# 5 patients, 3 vitals each: [heart_rate, bp_systolic, spo2]
vitals = np.array([
    [72, 120, 98],   # Patient P001
    [85, 135, 95],   # Patient P002
    [91, 128, 88],   # Patient P003
    [68, 118, 97],   # Patient P004
    [110, 145, 92],  # Patient P005
])

print("Vitals matrix:")
print(vitals)
print(f"\nShape: {vitals.shape}")
print(f"Number of dimensions: {vitals.ndim}")
print(f"Total values: {vitals.size}")

# --- Accessing a single value ---
# Format: vitals[row, column]
print(f"\nPatient P003's heart rate: {vitals[2, 0]}") # row 2, col 0
print(f"Patient P001's SpO2: {vitals[0, 2]}") # row 0, col 2

# --- Accessing a whole row (one patient's vitals) ---
print(f"\nAll vitals for P005: {vitals[4]}")
# or more explicit:
print(f"All vitals for P005: {vitals[4, :]}") # : means "all columns"

# --- Accessing a whole column (one vital across all patients) ---
print(f"\nAll heart rates: {vitals[:, 0]}") # all rows, column 0
print(f"All BP readings:  {vitals[:, 1]}")   # all rows, column 1
print(f"All SpO2 values:  {vitals[:, 2]}")   # all rows, column 2

print(f"Value: {vitals[3, 2]}")

# --- Axis operations ---

# First, what happens WITHOUT specifying axis?
print("\n--- No axis (flattens everything) ---")
print(f"Mean of ALL values: {np.mean(vitals)}")
# Gives ONE number — the average of all 15 values mashed together. Usually not what you want.

# --- axis=0: collapse DOWN the rows (one result per column) ---
print("\n--- axis=0 (average each VITAL across all patients) ---")
print(f"Average per vital: {np.mean(vitals, axis=0)}")
# Gives 3 numbers: [avg HR, avg BP, avg SpO2]

# --- axis=1: collapse ACROSS the columns (one result per row) ---
print("\n--- axis=1 (average each PATIENT across their vitals) ---")
print(f"Average per patient: {np.mean(vitals, axis=1)}")
# Gives 5 numbers: one average per patient

# --- You can use axis= with many functions ---
print(f"\nMax HR across patients: {np.max(vitals[:, 0])}")
print(f"Max of each vital: {np.max(vitals, axis=0)}")
print(f"Max vital per patient: {np.max(vitals, axis=1)}")
print(f"Sum of each vital: {np.sum(vitals, axis=0)}")

print(f"Lowest vital per patient:      {np.min(vitals, axis=1)}")
print(f"Lowest per vital (across pts): {np.min(vitals, axis=0)}")

# --- np.where: vectorized if/else ---

heart_rates = np.array([72, 85, 91, 68, 110, 78, 95, 88, 76, 102])

# Label each heart rate as "HIGH" (>100) or "OK"
labels = np.where(heart_rates > 100, "HIGH", "OK")
print(f"Heart rates: {heart_rates}")
print(f"Labels: {labels}")

# Clip heart rates: if HR > 100, cap at 100. Otherwise keep as-is.
capped = np.where(heart_rates > 100, 100, heart_rates)
print(f"Original: {heart_rates}")
print(f"Capped: {capped}")

# Find the POSITIONS (indices) of all high heart rates
positions = np.where(heart_rates > 100)
print(f"Positions of HIGH readings: {positions}")

# --- Your turn: label oxygen saturation readings ---
spo2 = np.array([98, 95, 88, 97, 92, 85, 99, 91, 84, 96])

# TODO 1: Create an array of labels where:
#   - spo2 < 90  -> "CRITICAL"
#   - otherwise  -> "OK"
# Store it in a variable called `spo2_labels`.
spo2_labels = np.where(spo2 < 90, "CRITICAL", "OK")

# TODO 2: Print the spo2 array and the labels side by side.
print(f"Original spo2: {spo2}")
print(f"spo2 labels: {spo2_labels}")

# TODO 3 (harder): Replace any CRITICAL reading (< 90) with the value 90,
#                  and keep the OK readings unchanged.
#                  Store in `spo2_clipped`. Print it.
spo2_clipped = np.where(spo2 < 90, 90, spo2)
print(f"spo2 clipped: {spo2_clipped}")