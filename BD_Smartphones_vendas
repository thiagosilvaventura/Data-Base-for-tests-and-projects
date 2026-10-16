import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import hashlib

# Initialize Faker with Brazilian locale for realistic addresses and names
fake = Faker('pt_BR')

def generate_cellphone_sales_data(num_records=1000):
    """
    Generates a realistic mock database for cellphone sales.
    Ensures consistency between Manufacturer, Model, OS, and Camera features.
    Includes additional data science features like storage impact on price.
    """
    
    # Pre-defined catalog to maintain logical consistency in the generated data
    device_catalog = [
        {"make": "Apple", "model": "iPhone 15 Pro", "os_type": "iOS", "base_price": 7299.00, "camera": "48MP", "os_versions": ["17.0", "17.1", "17.4"]},
        {"make": "Apple", "model": "iPhone 13", "os_type": "iOS", "base_price": 3899.00, "camera": "12MP", "os_versions": ["15.0", "16.5", "17.0"]},
        {"make": "Samsung", "model": "Galaxy S23 Ultra", "os_type": "Android", "base_price": 6500.00, "camera": "200MP", "os_versions": ["13.0", "14.0"]},
        {"make": "Samsung", "model": "Galaxy A54", "os_type": "Android", "base_price": 1800.00, "camera": "50MP", "os_versions": ["13.0"]},
        {"make": "Motorola", "model": "Edge 40", "os_type": "Android", "base_price": 2700.00, "camera": "50MP", "os_versions": ["13.0"]},
        {"make": "Motorola", "model": "Moto G84", "os_type": "Android", "base_price": 1400.00, "camera": "50MP", "os_versions": ["13.0", "14.0"]},
        {"make": "Xiaomi", "model": "Redmi Note 12", "os_type": "Android", "base_price": 1200.00, "camera": "48MP", "os_versions": ["12.0", "13.0"]},
        {"make": "Xiaomi", "model": "Poco X5 Pro", "os_type": "Android", "base_price": 1950.00, "camera": "108MP", "os_versions": ["12.0", "13.0"]}
    ]

    # Common smartphone colors
    color_options = ["Graphite", "Titanium Blue", "Alpine White", "Phantom Black", "Mint Green", "Rose Gold", "Cosmic Grey"]
    
    # Storage capacities usually affect the final price
    storage_options = [
        {"capacity": "128GB", "price_multiplier": 1.0},
        {"capacity": "256GB", "price_multiplier": 1.15},
        {"capacity": "512GB", "price_multiplier": 1.35}
    ]

    data = []
    
    # Define a date range for the sales (e.g., last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2 * 365)

    for _ in range(num_records):
        # 1. Customer Demographics
        customer_name = fake.name()
        email = f"{customer_name.replace(' ', '.').lower()}@{fake.free_email_domain()}"
        
        # Address details
        address = fake.street_address()
        zip_code = fake.postcode()
        city = fake.city()
        state = fake.state_abbr()
        
        # 2. Device Specifications
        device = random.choice(device_catalog)
        storage = random.choice(storage_options)
        color = random.choice(color_options)
        os_version = random.choice(device["os_versions"])
        
        # Calculate total price based on base price and storage size
        total_price = round(device["base_price"] * storage["price_multiplier"], 2)
        
        # Simulating a Canvas Hash (Device Fingerprint) using MD5 for uniqueness
        # Usually represents a unique browser/hardware render combination
        raw_hash_string = f"{customer_name}{device['model']}{fake.date_time_this_year()}"
        canvas_hash = hashlib.md5(raw_hash_string.encode()).hexdigest()

        # 3. Transaction Details
        sale_date = fake.date_between(start_date=start_date, end_date=end_date)
        transaction_id = fake.unique.bothify(text='TXN-########-????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        # Payment Logic: Did the user give a down payment?
        has_down_payment = fake.boolean(chance_of_getting_true=45) # 45% of sales have a down payment
        
        if has_down_payment:
            # Down payment is usually between 20% and 50% of the total price
            down_payment_pct = random.uniform(0.20, 0.50)
            down_payment_value = round(total_price * down_payment_pct, 2)
        else:
            down_payment_value = 0.0
            
        # Add payment method for extra depth
        payment_method = np.random.choice(
            ["Credit Card (Installments)", "Pix", "Boleto", "Debit Card"], 
            p=[0.60, 0.25, 0.10, 0.05]
        )

        # Append row to data list
        data.append({
            "Transaction_ID": transaction_id,
            "Customer_Name": customer_name,
            "Email": email,
            "Address": address,
            "Zip_Code": zip_code,
            "City": city,
            "State": state,
            "Sale_Date": sale_date,
            "Manufacturer": device["make"],
            "Model": device["model"],
            "Storage_Capacity": storage["capacity"],
            "Color": color,
            "Camera_Resolution": device["camera"],
            "OS_Type": device["os_type"],
            "OS_Version": os_version,
            "Canvas_Hash": canvas_hash,
            "Total_Price_BRL": total_price,
            "Has_Down_Payment": has_down_payment,
            "Down_Payment_BRL": down_payment_value,
            "Payment_Method": payment_method
        })

    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Sort chronologically by sale date to simulate real database inserts
    df = df.sort_values(by="Sale_Date").reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Generate 1000 rows of cellphone sales data (easily adjustable)
    print("Generating cellphone sales database...")
    cellphone_df = generate_cellphone_sales_data(num_records=1000)
    
    # Display the first 5 rows to verify structure and consistency
    print("\nSample Data:")
    print(cellphone_df[['Customer_Name', 'Manufacturer', 'Model', 'OS_Type', 'Has_Down_Payment', 'Down_Payment_BRL']].head())
    
    # Export to CSV for Data Science use
    output_filename = "mock_cellphone_sales_db.csv"
    cellphone_df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nDatabase successfully generated and saved as '{output_filename}'.")
    print(f"Total Rows: {len(cellphone_df)} | Total Columns: {len(cellphone_df.columns)}")
