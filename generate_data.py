import pandas as pd
import random
from datetime import datetime, timedelta

print("Initializing Healthcare Data Synthesizer Engine...")

# Configuration constants
NUM_RECORDS = 10000
SYMPTOMS = ["Chest Pain", "Difficulty Breathing", "Severe Headache", "Deep Laceration", "Minor Cut", "Sore Throat"]
LOCATIONS = ["North ER", "South ER", "Pediatric Triage", "Trauma Bay Assessment"]

data = []

# Generate 10,000 professional-grade clinical data vectors
for i in range(NUM_RECORDS):
    # Simulate realistic time dispersion over a 30-day period
    random_days = random.randint(0, 30)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    arrival_time = datetime(2026, 6, 1) + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
    
    symptom = random.choice(SYMPTOMS)
    
    # Establish realistic physiological bounds based on chief complaint
    if symptom in ["Chest Pain", "Difficulty Breathing"]:
        hr = random.randint(90, 140)
        sbp = random.randint(85, 190)
        rr = random.randint(20, 28)
        base_wait = random.randint(5, 20) # Red/Yellow cases get seen instantly
    else:
        hr = random.randint(60, 100)
        sbp = random.randint(110, 140)
        rr = random.randint(12, 20)
        base_wait = random.randint(45, 180) # Green cases wait longer
        
    data.append({
        "Patient_ID": f"PT-{100000 + i}",
        "Arrival_Timestamp": arrival_time,
        "Chief_Complaint": symptom,
        "Heart_Rate_BPM": hr,
        "Systolic_BP_mmHg": sbp,
        "Respiratory_Rate": rr,
        "Wait_Time_Minutes": base_wait,
        "Triage_Zone": random.choice(LOCATIONS)
    })

# Convert structured dictionary array into a Pandas DataFrame
df = pd.DataFrame(data)

# Sort chronologically to mimic streaming real-time hospital logs
df = df.sort_values(by="Arrival_Timestamp").reset_index(drop=True)

# Export to a production-ready CSV data layer
df.to_csv("er_patient_data.csv", index=False)
print(f"Success! Generated {NUM_RECORDS} operational data vectors and exported to 'er_patient_data.csv'.")