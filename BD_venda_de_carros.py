import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker with Brazilian locale for realistic localized data (names, CEP, cities)
fake = Faker('pt_BR')

def generate_vehicle_sales_data(num_records=500):
    """
    Generates a realistic mock database for vehicle sales.
    Includes the requested fields and expands with logically related financial 
    and vehicle specification metrics commonly found in real CRM/ERP systems.
    """
    
    # Pre-defined realistic vehicle data to ensure consistency between Make, Model, and Base Price
    vehicle_catalog = [
        {"make": "Toyota", "model": "Corolla", "base_price": 120000, "category": "Sedan"},
        {"make": "Honda", "model": "Civic", "base_price": 135000, "category": "Sedan"},
        {"make": "Volkswagen", "model": "Nivus", "base_price": 115000, "category": "SUV"},
        {"make": "Volkswagen", "model": "Polo", "base_price": 85000, "category": "Hatchback"},
        {"make": "Chevrolet", "model": "Tracker", "base_price": 130000, "category": "SUV"},
        {"make": "Chevrolet", "model": "Onix", "base_price": 82000, "category": "Hatchback"},
        {"make": "Jeep", "model": "Compass", "base_price": 180000, "category": "SUV"},
        {"make": "Fiat", "model": "Toro", "base_price": 150000, "category": "Pickup"},
        {"make": "Hyundai", "model": "Creta", "base_price": 125000, "category": "SUV"},
        {"make": "Hyundai", "model": "HB20", "base_price": 78000, "category": "Hatchback"}
    ]

    data = []
    
    # Define a date range for the sales (e.g., last 3 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365)

    for _ in range(num_records):
        # 1. Customer Demographics
        customer_id = fake.uuid4()
        full_name = fake.name()
        email = f"{full_name.replace(' ', '.').lower()}@{fake.free_email_domain()}"
        phone = fake.cellphone_number()
        
        # Address details
        address = fake.street_address()
        zip_code = fake.postcode()
        city = fake.city()
        state = fake.state_abbr()
        
        # 2. Vehicle Details
        vehicle = random.choice(vehicle_catalog)
        is_new = np.random.choice([True, False], p=[0.4, 0.6]) # 40% new, 60% used
        
        # Depreciate price if used (between 10% and 40% cheaper)
        year_modifier = random.randint(2015, 2024) if not is_new else 2024
        price_multiplier = 1.0 if is_new else random.uniform(0.6, 0.9)
        total_price = round(vehicle["base_price"] * price_multiplier, 2)
        
        vin_number = fake.vin() # Vehicle Identification Number
        mileage_km = random.randint(15, 200) if is_new else random.randint(15000, 150000)

        # 3. Transaction & Financial Details
        sale_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Realistic down payment: 10% to 60% of the total price
        down_payment_pct = random.uniform(0.10, 0.60)
        down_payment = round(total_price * down_payment_pct, 2)
        
        # Calculate financed amount
        financed_amount = round(total_price - down_payment, 2)
        
        # Installment logic: standard auto loan terms (12, 24, 36, 48, 60, 72 months)
        installments = random.choice([12, 24, 36, 48, 60, 72])
        
        # Apply realistic annual interest rate (e.g., 12% to 25% APR)
        annual_interest_rate = random.uniform(0.12, 0.25)
        monthly_interest_rate = annual_interest_rate / 12
        
        # Standard compound interest formula for monthly payments (Amortization)
        if financed_amount > 0:
            monthly_payment = (financed_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** installments)) / (((1 + monthly_interest_rate) ** installments) - 1)
            monthly_payment = round(monthly_payment, 2)
        else:
            monthly_payment = 0.0

        # Sales metadata
        salesperson_id = f"EMP-{random.randint(100, 150)}"
        payment_method = np.random.choice(
            ["Bank Transfer", "Pix", "Financing", "Credit Card"], 
            p=[0.15, 0.20, 0.60, 0.05]
        )

        # Append row to data list
        data.append({
            "Transaction_ID": fake.unique.hexify(text='TRX-^^^^^^^^'),
            "Customer_ID": customer_id,
            "Customer_Name": full_name,
            "Email": email,
            "Phone": phone,
            "Address": address,
            "City": city,
            "State": state,
            "Zip_Code": zip_code,
            "Sale_Date": sale_date,
            "Salesperson_ID": salesperson_id,
            "Vehicle_Make": vehicle["make"],
            "Vehicle_Model": vehicle["model"],
            "Vehicle_Category": vehicle["category"],
            "Vehicle_Year": year_modifier,
            "Condition": "New" if is_new else "Used",
            "Mileage_KM": mileage_km,
            "VIN": vin_number,
            "Total_Price_BRL": total_price,
            "Down_Payment_BRL": down_payment,
            "Financed_Amount_BRL": financed_amount,
            "Installments": installments,
            "Monthly_Payment_BRL": monthly_payment,
            "Interest_Rate_APR": round(annual_interest_rate, 4),
            "Payment_Method": payment_method
        })

    # Convert to pandas DataFrame for easy export and manipulation
    df = pd.DataFrame(data)
    
    # Sort chronologically by sale date to simulate standard DB indexing
    df = df.sort_values(by="Sale_Date").reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Generate 1000 rows of vehicle sales data
    print("Generating database...")
    sales_df = generate_vehicle_sales_data(num_records=1000)
    
    # Display the first 5 rows to verify the structure
    print("\nSample Data:")
    print(sales_df.head())
    
    # Export to CSV for Data Science studies
    output_filename = "mock_vehicle_sales_database.csv"
    sales_df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nDatabase successfully generated and saved as '{output_filename}'.")
    print(f"Total Rows: {len(sales_df)} | Total Columns: {len(sales_df.columns)}")
