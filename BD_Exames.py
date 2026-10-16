import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker with Brazilian locale for realistic demographic data
fake = Faker('pt_BR')

def generate_medical_exam_data(num_records=500):
    """
    Generates a highly realistic mock database for medical exam results.
    Includes Urine, Cardiac, and Hormonal tests with clinical logic, 
    reference ranges, and status comparisons.
    """
    data = []
    
    # Date range for exams (last 12 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    for _ in range(num_records):
        # ==========================================
        # 1. Demographics & General Info
        # ==========================================
        sex = random.choice(["Male", "Female"])
        # Generate names based on sex for consistency
        full_name = fake.name_male() if sex == "Male" else fake.name_female()
        
        # Age distribution weighted towards older adults who take more exams
        age = int(np.random.normal(loc=45, scale=18))
        age = max(18, min(age, 90)) # Clamp between 18 and 90 years old
        
        address = fake.street_address()
        zip_code = fake.postcode()
        city = fake.city()
        state = fake.state_abbr()
        exam_date = fake.date_between(start_date=start_date, end_date=end_date)
        patient_id = fake.unique.hexify(text='PAT-^^^^^^^^')

        # ==========================================
        # 2. Urine Exam (Urinalysis)
        # ==========================================
        # Simulate a 15% chance of having a Urinary Tract Infection (UTI) or abnormality
        has_uti = random.random() < 0.15 
        
        # Leukocytes (Reference: < 10,000 /mL)
        urine_leukocytes = random.randint(15000, 100000) if has_uti else random.randint(0, 9000)
        leukocytes_ref = "< 10000 /mL"
        leukocytes_status = "Altered" if urine_leukocytes >= 10000 else "Normal"

        # Erythrocytes / Hemácias (Reference: < 10,000 /mL)
        urine_erythrocytes = random.randint(12000, 50000) if has_uti else random.randint(0, 8000)
        erythrocytes_ref = "< 10000 /mL"
        erythrocytes_status = "Altered" if urine_erythrocytes >= 10000 else "Normal"

        # Protein (Reference: < 15 mg/dL)
        urine_protein = round(random.uniform(20.0, 100.0), 1) if has_uti else round(random.uniform(0.0, 14.0), 1)
        protein_ref = "< 15.0 mg/dL"
        protein_status = "Altered" if urine_protein >= 15.0 else "Normal"

        # ==========================================
        # 3. Cardiac Exam
        # ==========================================
        # BPM (Reference: 60 - 100 bpm)
        bpm = int(np.random.normal(loc=75, scale=12))
        bpm = max(40, min(bpm, 140)) # Clamp extreme outliers
        bpm_ref = "60 - 100 bpm"
        bpm_status = "Altered" if bpm < 60 or bpm > 100 else "Normal"

        # Blood Pressure (Systolic Reference: < 120, Diastolic Reference: < 80)
        # BP naturally correlates with age in this mock logic
        age_factor = (age - 30) * 0.4 if age > 30 else 0
        systolic = int(np.random.normal(loc=115 + age_factor, scale=10))
        diastolic = int(np.random.normal(loc=75 + (age_factor * 0.6), scale=8))
        
        bp_ref = "< 120/80 mmHg"
        bp_status = "Altered" if systolic >= 130 or diastolic >= 85 else "Normal" # Using clinical hypertension threshold

        # ==========================================
        # 4. Hormonal Exam
        # ==========================================
        # TSH - Thyroid (Reference: 0.4 - 4.0 mIU/L for both sexes)
        tsh = round(np.random.lognormal(mean=0.5, sigma=0.8), 2)
        tsh = max(0.1, min(tsh, 10.0))
        tsh_ref = "0.4 - 4.0 mIU/L"
        tsh_status = "Altered" if tsh < 0.4 or tsh > 4.0 else "Normal"

        # Testosterone (Sex-specific reference ranges)
        if sex == "Male":
            # Men: 300 - 1000 ng/dL (decreases slightly with age)
            testosterone = int(np.random.normal(loc=600 - (age - 30)*3, scale=150))
            testo_ref = "300 - 1000 ng/dL"
            testo_status = "Altered" if testosterone < 300 or testosterone > 1000 else "Normal"
        else:
            # Women: 15 - 70 ng/dL
            testosterone = int(np.random.normal(loc=40, scale=15))
            testo_ref = "15 - 70 ng/dL"
            testo_status = "Altered" if testosterone < 15 or testosterone > 70 else "Normal"

        # Compile the row data
        data.append({
            "Patient_ID": patient_id,
            "Patient_Name": full_name,
            "Sex": sex,
            "Age": age,
            "Address": address,
            "Zip_Code": zip_code,
            "City": city,
            "State": state,
            "Exam_Date": exam_date,
            
            # Urine
            "Urine_Leukocytes_mL": urine_leukocytes,
            "Leukocytes_Ref": leukocytes_ref,
            "Leukocytes_Status": leukocytes_status,
            "Urine_Erythrocytes_mL": urine_erythrocytes,
            "Erythrocytes_Ref": erythrocytes_ref,
            "Erythrocytes_Status": erythrocytes_status,
            "Urine_Protein_mg_dL": urine_protein,
            "Protein_Ref": protein_ref,
            "Protein_Status": protein_status,
            
            # Cardiac
            "Heart_Rate_BPM": bpm,
            "BPM_Ref": bpm_ref,
            "BPM_Status": bpm_status,
            "BP_Systolic": systolic,
            "BP_Diastolic": diastolic,
            "BP_Ref": bp_ref,
            "BP_Status": bp_status,
            
            # Hormonal
            "TSH_mIU_L": tsh,
            "TSH_Ref": tsh_ref,
            "TSH_Status": tsh_status,
            "Testosterone_ng_dL": max(0, testosterone), # Ensure no negative values
            "Testosterone_Ref": testo_ref,
            "Testosterone_Status": testo_status
        })

    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Sort chronologically by exam date
    df = df.sort_values(by="Exam_Date").reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Generate 500 rows to easily surpass the 250 minimum requirement
    print("Generating medical records database...")
    medical_df = generate_medical_exam_data(num_records=500)
    
    # Preview the data specifically highlighting the clinical comparisons
    print("\nSample Data (Cardiac & Hormonal):")
    cols_to_show = ['Patient_Name', 'Age', 'Sex', 'BP_Systolic', 'BP_Status', 'Testosterone_ng_dL', 'Testosterone_Status']
    print(medical_df[cols_to_show].head())
    
    # Export to CSV
    output_filename = "mock_medical_exams_db.csv"
    medical_df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nDatabase successfully generated and saved as '{output_filename}'.")
    print(f"Total Rows: {len(medical_df)} | Total Columns: {len(medical_df.columns)}")
