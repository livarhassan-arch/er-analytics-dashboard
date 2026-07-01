import sys

class Patient:
    """Represents a patient case during an emergency triage assessment."""
    def __init__(self, symptom: str):
        self.symptom = symptom.strip().lower()
        self.heart_rate = 0
        self.systolic_bp = 0
        self.resp_rate = 0
        self.vitals_risk_score = 0
        self.base_priority = "GREEN (Non-Urgent)"
        self.final_priority = "GREEN (Non-Urgent)"
        self.protocol_action = ""

    def calculate_vitals_risk(self):
        """
        Calculates a clinical risk score based on vital sign deviations.
        A score >= 2 indicates severe physiological distress.
        """
        score = 0
        
        # Evaluate Heart Rate (Normal: 60-100 bpm)
        if self.heart_rate > 120 or self.heart_rate < 50:
            score += 2
        elif self.heart_rate > 100 or self.heart_rate < 60:
            score += 1
            
        # Evaluate Systolic Blood Pressure (Normal: 90-120 mmHg)
        if self.systolic_bp < 90 or self.systolic_bp > 180:
            score += 2
        elif self.systolic_bp > 140:
            score += 1
            
        # Evaluate Respiratory Rate (Normal: 12-20 breaths/min)
        if self.resp_rate > 24 or self.resp_rate < 10:
            score += 2
        elif self.resp_rate > 20 or self.resp_rate < 12:
            score += 1
            
        self.vitals_risk_score = score
        return score


class TriageEngine:
    """Core logic engine that handles clinical databases and triage logic processing."""
    def __init__(self):
        # Master protocol registry mapping symptoms to baseline severity and initial actions
        self.protocol_registry = {
            "chest pain": {
                "level": "RED (Emergent)",
                "action": "Possible cardiac event. Call 911/ALS backup instantly. Administer Aspirin/O2 per local protocol."
            },
            "difficulty breathing": {
                "level": "RED (Emergent)",
                "action": "Severe respiratory distress. Assess ABCs. Prepare BVM/suction and assist with prescribed bronchodilator."
            },
            "severe headache": {
                "level": "YELLOW (Urgent)",
                "action": "Potential neurological event or acute hypertensive crisis. Perform stroke scale screening (FAST)."
            },
            "deep laceration": {
                "level": "YELLOW (Urgent)",
                "action": "Controlled hemorrhage requiring closure. Apply direct pressure, pressure dressing, and tourni-prep if severe."
            },
            "minor cut": {
                "level": "GREEN (Non-Urgent)",
                "action": "Clean wound track, apply topical antibiotic barrier, dress with sterile gauze, and monitor for infection."
            },
            "sore throat": {
                "level": "GREEN (Non-Urgent)",
                "action": "Supportive care, hydration, oral analgesics, and outpatient referral if fever or exudate develops."
            }
        }

    def process_triage(self, patient: Patient):
        """Evaluates baseline clinical protocols against patient vitals to determine final priority."""
        if patient.symptom in self.protocol_registry:
            match = self.protocol_registry[patient.symptom]
            patient.base_priority = match["level"]
            patient.final_priority = match["level"]
            patient.protocol_action = match["action"]
        else:
            patient.base_priority = "YELLOW (Urgent)"
            patient.final_priority = "YELLOW (Urgent)"
            patient.protocol_action = "Unknown etiology. Defaulting to standard primary assessment and immediate secondary vitals sweep."

        # Dynamic Vitals Override Logic
        risk_score = patient.calculate_vitals_risk()
        
        if risk_score >= 3 and patient.final_priority != "RED (Emergent)":
            patient.final_priority = "RED (Emergent) [CRITICAL VITAL SIGNS OVERRIDE]"
            patient.protocol_action = f"CRITICAL CHANGE: Patient upgraded due to physiological instability (Risk Score: {risk_score}). " + patient.protocol_action
        elif risk_score >= 1 and patient.final_priority == "GREEN (Non-Urgent)":
            patient.final_priority = "YELLOW (Urgent) [VITALS OVERRIDE]"
            patient.protocol_action = f"MODERATE CHANGE: Upgraded due to abnormal vitals trend. " + patient.protocol_action


def get_validated_int(prompt: str) -> int:
    """Helper function to catch user input errors and ensure robust integer entry."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("[!] Invalid entry. Please enter a valid numerical value.")


def main():
    print("=" * 60)
    print("   FORDHAM UNIVERSITY EMS (FUEMS) CLINICAL TRIAGE ENGINE   ")
    print("=" * 60)
    
    symptom = input("Enter Patient Chief Complaint (Symptom): ")
    patient = Patient(symptom)
    
    print("\n--- Gather Patient Vitals ---")
    patient.heart_rate = get_validated_int("Enter Heart Rate (BPM): ")
    patient.systolic_bp = get_validated_int("Enter Systolic Blood Pressure (mmHg): ")
    patient.resp_rate = get_validated_int("Enter Respiratory Rate (Breaths/Min): ")
    
    # Run the processing engine
    engine = TriageEngine()
    engine.process_triage(patient)
    
    # Print clean clinical output
    print("\n" + "#" * 60)
    print("                        TRIAGE SUMMARY                         ")
    print("#" * 60)
    print(f"CHIEF COMPLAINT:     {patient.symptom.upper()}")
    print(f"BASELINE PRIORITY:   {patient.base_priority}")
    print(f"VITALS RISK SCORE:   {patient.vitals_risk_score}/6")
    print(f"FINAL ASSIGNED LEVEL:{patient.final_priority}")
    print("-" * 60)
    print(f"STANDING PROTOCOL INSTRUCTIONS:\n{patient.protocol_action}")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    main()