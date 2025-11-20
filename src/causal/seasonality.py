import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def decompose_demand(df, sku_id, period=7):
    """
    Performs seasonal decomposition on demand data for a specific SKU.
    Useful for visualizing underlying trends vs seasonal spikes.
    """
    sku_data = df[df['sku_id'] == sku_id].sort_values('date').copy()
    sku_data['date'] = pd.to_datetime(sku_data['date'])
    sku_data.set_index('date', inplace=True)
    
    # Simple additive decomposition
    decomposition = sm.tsa.seasonal_decompose(sku_data['quantity_sold'], model='additive', period=period)
    
    fig = decomposition.plot()
    fig.set_size_inches(10, 8)
    plt.title(f"Seasonal Decomposition for SKU {sku_id}")
    plt.show()
    
    return decomposition.trend, decomposition.seasonal, decomposition.resid