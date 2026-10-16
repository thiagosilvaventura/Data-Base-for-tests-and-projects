import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker with Brazilian locale for realistic names and addresses
fake = Faker('pt_BR')

def generate_credit_risk_data(num_records=1000):
    """
    Generates a realistic mock database for Credit Risk and Personal Finance.
    Includes logical correlations between income, debt, age, and default probability.
    """
    data = []
    
    for _ in range(num_records):
        # 1. Demographics
        customer_id = fake.uuid4()
        full_name = fake.name()
        
        # Age distribution weighted towards working adults
        age = int(np.random.normal(loc=38, scale=12))
        age = max(18, min(age, 85))
        
        # 2. Financial Profile
        # Income (Log-normal distribution for realistic income skewness)
        monthly_income = round(np.random.lognormal(mean=8.5, sigma=0.7), 2)
        monthly_income = max(1412.0, monthly_income) # Minimum wage floor
        
        # Employment length correlates somewhat with age
        max_emp_length = age - 18
        employment_years = min(max_emp_length, int(np.random.exponential(scale=6)))
        
        home_ownership = np.random.choice(['RENT', 'OWN', 'MORTGAGE'], p=[0.45, 0.25, 0.30])
        
        # 3. Loan Details
        # Loan intent
        loan_intent = np.random.choice(
            ['PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOME_IMPROVEMENT', 'DEBT_CONSOLIDATION'],
            p=[0.3, 0.1, 0.1, 0.1, 0.15, 0.25]
        )
        
        # Loan amount is usually a function of income but has variance
        loan_amount = int(np.random.normal(loc=monthly_income * 3, scale=monthly_income))
        loan_amount = max(1000, min(loan_amount, 150000))
        
        # Interest rate (higher risk = higher rate)
        interest_rate = round(random.uniform(5.0, 25.0), 2)
        
        # 4. Credit History & Risk Metrics
        credit_history_years = max(1, age - 18 - random.randint(0, 5))
        
        # Debt-to-Income (DTI) ratio
        existing_debt_payments = random.uniform(0, monthly_income * 0.6)
        dti = round(existing_debt_payments / monthly_income, 2)
        
        # Number of previous defaults
        # Higher DTI increases chance of having previous defaults
        prev_defaults_prob = 0.05 + (dti * 0.2)
        previous_defaults = 1 if random.random() < prev_defaults_prob else 0
        if previous_defaults == 1 and random.random() < 0.2:
            previous_defaults += random.randint(1, 3)
            
        # 5. Target Variable: Default (Inadimplência)
        # Default probability logic based on DTI, Income, and Interest Rate
        base_default_prob = 0.05
        if dti > 0.4: base_default_prob += 0.15
        if interest_rate > 15.0: base_default_prob += 0.10
        if previous_defaults > 0: base_default_prob += 0.25
        if monthly_income < 3000: base_default_prob += 0.05
        
        # Cap probability at 90%
        final_default_prob = min(base_default_prob, 0.90)
        
        # Simulating the actual default event (1 = Default, 0 = Non-Default)
        is_default = 1 if random.random() < final_default_prob else 0
        
        # Adjust credit score based on default status and history
        if is_default == 1 or previous_defaults > 0:
            credit_score = int(np.random.normal(loc=500, scale=80))
        else:
            credit_score = int(np.random.normal(loc=720, scale=60))
            
        credit_score = max(300, min(credit_score, 850))

        # Compile row data
        data.append({
            "Customer_ID": customer_id,
            "Full_Name": full_name,
            "Age": age,
            "Employment_Years": employment_years,
            "Home_Ownership": home_ownership,
            "Monthly_Income_BRL": monthly_income,
            "Credit_Score": credit_score,
            "Credit_History_Years": credit_history_years,
            "Loan_Intent": loan_intent,
            "Loan_Amount_BRL": loan_amount,
            "Interest_Rate_APR": interest_rate,
            "DTI_Ratio": dti,
            "Previous_Defaults": previous_defaults,
            "Default_Status": is_default
        })

    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    return df

if __name__ == "__main__":
    # Generating 1000 rows as requested
    print("Generating Credit Risk database...")
    credit_df = generate_credit_risk_data(num_records=1000)
    
    # Export to CSV for Data Science studies
    output_filename = "mock_credit_risk_db.csv"
    credit_df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Database successfully generated and saved as '{output_filename}'.")
