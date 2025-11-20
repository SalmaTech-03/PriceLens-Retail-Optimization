import pandas as pd
import numpy as np
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import your custom modules
# (Make sure you created these files in src/econometrics/ and src/optimization/ first!)
from src.econometrics.elasticity_model import EconometricModel
from src.optimization.price_optimizer import optimize_price

def run():
    # 1. Load Data
    input_path = 'data/raw/retail_transactions.csv'
    if not os.path.exists(input_path):
        print(" Data file not found. Please run 'generate_data.py' first.")
        return

    print(f"🔄 Loading Data from {input_path}...")
    df = pd.read_csv(input_path)

    # 2. Train Models (Elasticity & Cross-Elasticity)
    print(" Training Econometric Models (Log-Log Regression)...")
    modeler = EconometricModel(df)
    modeler.feature_engineering()
    output_processed = 'data/processed/modeling_data.csv'
    os.makedirs('data/processed', exist_ok=True)
    modeler.data.to_csv(output_processed, index=False)
    print(f"   -> Processed data saved to {output_processed}")
    elasticity_df = modeler.fit_own_elasticity()
    
    print(f"   -> Model trained for {len(elasticity_df)} SKUs.")
    print(elasticity_df[['own_elasticity', 'cross_elasticity_competitor']].head())

    # 3. Optimization Loop
    print("\n Running Price Optimization Engine...")
    results = []

    # Get latest costs/prices for the simulation
    latest_state = df.sort_values('date').groupby('sku_id').last()
    
    for sku in elasticity_df.index:
        # Extract parameters for this SKU
        params = elasticity_df.loc[sku]
        cost = latest_state.loc[sku, 'cost']
        curr_price = latest_state.loc[sku, 'price']
        product_name = latest_state.loc[sku, 'product_name']
        category = latest_state.loc[sku, 'category']

        # Run the Optimizer (SciPy)
        opt_price, opt_profit = optimize_price(
            sku_id=sku,
            current_price=curr_price,
            cost=cost,
            elasticity=params['own_elasticity'],
            intercept=params['intercept']
        )
        
        # Calculate Baseline (Current) Logic for comparison
        # Demand = exp(intercept + elasticity * ln(price))
        curr_demand = np.exp(params['intercept'] + params['own_elasticity'] * np.log(curr_price))
        curr_profit = (curr_price - cost) * curr_demand
        
        # Store Results
        results.append({
            'SKU_ID': sku,
            'Product': product_name,
            'Category': category,
            'Current_Price': round(curr_price, 2),
            'Optimal_Price': round(opt_price, 2),
            'Price_Change_Pct': round(((opt_price - curr_price) / curr_price) * 100, 1),
            'Elasticity': round(params['own_elasticity'], 2),
            'Current_Profit': round(curr_profit, 2),
            'Optimized_Profit': round(opt_profit, 2),
            'Profit_Uplift_Dol': round(opt_profit - curr_profit, 2)
        })

    # 4. Export for Power BI / Reports
    final_report = pd.DataFrame(results)
    output_path = 'reports/powerbi_export.csv'
    
    # Create reports folder if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    final_report.to_csv(output_path, index=False)
    
    print("\n Optimization Complete!")
    print(f" Report saved to: {output_path}")
    print("-" * 30)
    print(final_report[['Product', 'Current_Price', 'Optimal_Price', 'Profit_Uplift_Dol']].to_string())

if __name__ == "__main__":
    run()