import pandas as pd
import numpy as np
import os

# Ensure the directory exists
os.makedirs("data/raw", exist_ok=True)

def generate_enterprise_data():
    print("⏳ Generating synthetic data for 50 SKUs...")
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    n_days = len(dates)
    
    # Categories and base ranges
    categories = ['Coffee', 'Cereal', 'Dairy', 'Snacks', 'Beverages']
    
    all_data = []
    
    # Generate 50 Unique SKUs
    for i in range(1, 51):
        sku_id = 100 + i
        cat = np.random.choice(categories)
        base_price = np.random.uniform(5, 25)
        cost = base_price * np.random.uniform(0.4, 0.7) # Margin 30-60%
        product_name = f"{cat}_Product_{i}"
        
        # 1. Seasonality
        t = np.arange(n_days)
        seasonality = 10 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 2, n_days)
        
        # 2. Prices
        price = base_price * np.random.uniform(0.9, 1.1, n_days)
        comp_price = base_price * np.random.uniform(0.85, 1.15, n_days)
        
        # 3. Elasticity Logic
        own_elast = np.random.uniform(-2.5, -0.5) # Random elasticity per product
        cross_elast = np.random.uniform(0.1, 0.6)
        
        # Demand Eq
        log_demand = (
            4.0 
            + (own_elast * np.log(price)) 
            + (cross_elast * np.log(comp_price)) 
            + (0.01 * seasonality) 
            + np.random.normal(0, 0.1, n_days)
        )
        quantity = np.exp(log_demand).astype(int)
        
        df = pd.DataFrame({
            'date': dates,
            'sku_id': sku_id,
            'product_name': product_name,
            'category': cat,
            'price': price.round(2),
            'cost': round(cost, 2),
            'competitor_price': comp_price.round(2),
            'quantity_sold': quantity
        })
        all_data.append(df)
        
    final_df = pd.concat(all_data)
    final_df.to_csv('data/raw/retail_transactions.csv', index=False)
    print(f"✅ Generated {len(final_df)} rows for 50 SKUs!")

if __name__ == "__main__":
    generate_enterprise_data()