import re

text = "Patient ID: 40124, admitted on 03/15/2026"

# re.search() looks for a pattern in text
# \d means "any digit"
# \d+ means "one or more digits"

result = re.search(r"\d+", text)
print(result)
print(result.group())

results = re.findall(r"\d+", text)
print(results)

text = "Patient BP: 120/80, HR: 82bpm, SpO2: 97%, admitted 03/15/2026"

# \d = one digit, \d+ = one or more digits
print("1:", re.findall(r"\d+", text))

# \d{2} = exactly 2 digits
print("2:", re.findall(r"\d{2}", text))

# \d{2}/\d{2}/\d{4} = date pattern: XX/XX/XXXX
print("3:", re.findall(r"\d{2}/\d{2}/\d{4}", text))

# \w = any word character (letter, digit, underscore)
# \w+ = one or more word characters
text2 = "Diagnosis: I50.9 (Heart Failure), Code: E11.65"

print("1:", re.findall(r"[A-Z]\d{2}\.\d+", text2))

# What this pattern says:
# [A-Z] = one uppercase letter
# \d{2} = two digits
# \. = a literal dot (not "any character")
# \d+ = one or more digits

text3 = "BP: 120/80, BP: 135/90, BP: 110/70"

# Parentheses () create capture groups
matches = re.findall(r"(\d+)/(\d+)", text3)
print(matches)

# re.sub(pattern, replacement, text)
note = "Patient SSN: 123-45-6789, DOB: 03/15/1985"

# HIPAA: mask the SSN!
cleaned = re.sub(r"\d{3}-\d{2}-\d{4}", "***-**-****", note)
print(cleaned)

note = "HR: 82, BP: 120/80, SpO2: 97%, Temp: 98.6F, RR: 18"

# Extract the vital name and its value
# Expected output: [('HR', '82'), ('BP', '120/80'), ('SpO2', '97'), ('Temp', '98.6'), ('RR', '18')]

matches = re.findall(r"(\w+): ([\d/.]+)", note)
print(matches)

text = "Contact dr.smith@hospital.com or nurse_jones@clinic.org for patient info"

# Expected: ['dr.smith@hospital.com', 'nurse_jones@clinic.org']
matches = re.findall(r"[\w.]+\w@\w+\.\w+", text)
print(matches)

note = "Refer PT40124 to cardiology. PT99881 needs follow-up. Room PT3 is empty."

# Expected: ['PT40124', 'PT99881']  (NOT PT3 — that's only 1 digit)
matches = re.findall(r"PT\d{5}", note)
print(matches)

note = "Refer PT40124 to cardiology. PT99881 needs follow-up."

cleaned = re.sub(r"PT\d{5}", "PT*****", note)
print(cleaned)
# Expected: "Refer PT***** to cardiology. PT***** needs follow-up."

notes = """
Patient vitals recorded:
HR: 82 (normal: 60-100)
BP: 155/95 (normal: below 140/90)
SpO2: 88% (normal: above 95%)
Temp: 98.6F (normal: 97.0-99.5)
RR: 22 (normal: 12-20)
"""

# Step 1: Extract all vital names and values using your earlier pattern
vitals = re.findall(r"(\w+): ([\d./]+)", notes)
print(vitals)

vitals = [(name, val) for name, val in vitals if name != "normal"]
print(vitals)

for name, value in vitals:
    if name == "HR":
        hr = int(value)
        if hr < 60 or hr > 100:
            print(f"⚠️ {name}: {value} — ABNORMAL")
        else:
            print(f"✅ {name}: {value} — normal")
    if name == "SpO2":
        sp = int(value)
        if sp < 95:
            print(f"⚠️ {name}: {value} — ABNORMAL")
        else:
            print(f"✅ {name}: {value} — normal")
    if name == "RR":
        rr = int(value)
        if rr < 12 or rr > 20:
            print(f"⚠️ {name}: {value} — ABNORMAL")
        else:
            print(f"✅ {name}: {value} — normal")
    if name == "BP":
        parts = value.split("/")
        systolic = int(parts[0])
        diastolic = int(parts[1])
        if systolic > 140 or diastolic > 90:
            print(f"⚠️ {name}: {value} — ABNORMAL")
        else:
            print(f"✅ {name}: {value} — normal")