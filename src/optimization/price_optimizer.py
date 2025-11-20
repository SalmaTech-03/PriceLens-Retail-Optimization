import numpy as np
from scipy.optimize import minimize

def profit_function(price, intercept, elasticity, cost):
    """
    Profit = (Price - Cost) * Demand
    Demand = exp(Intercept + Elasticity * ln(Price))  <-- Derived from Log-Log
    """
    # Prevent negative prices
    if price <= 0: return -1e9
    
    # Estimate Demand
    est_log_q = intercept + elasticity * np.log(price)
    est_q = np.exp(est_log_q)
    
    margin = price - cost
    profit = margin * est_q
    return -profit # We negate profit because scipy minimizes functions

def optimize_price(sku_id, current_price, cost, elasticity, intercept):
    """
    Finds the price that maximizes profit.
    """
    # Bounds: Don't let price go below cost or more than 3x cost (realistic guardrails)
    bounds = [(cost * 1.05, cost * 3.0)]
    
    result = minimize(
        profit_function,
        x0=np.array([current_price]), # Starting point
        args=(intercept, elasticity, cost),
        bounds=bounds,
        method='L-BFGS-B'
    )
    
    return result.x[0], -result.fun # Optimal Price, Max Profit