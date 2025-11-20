import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

class EconometricModel:
    def __init__(self, data):
        self.data = data
        self.elasticities = {}
        
    def feature_engineering(self):
        """Prepares log-log terms for elasticity estimation."""
        self.data['log_qty'] = np.log1p(self.data['quantity_sold'])
        self.data['log_price'] = np.log1p(self.data['price'])
        self.data['log_comp_price'] = np.log1p(self.data['competitor_price'])
        
    def fit_own_elasticity(self):
        """
        Fits a Log-Log model:
        ln(Q) = β0 + β1*ln(P) + β2*ln(P_comp) + error
        β1 is Own Price Elasticity.
        β2 is Cross Price Elasticity (vs Competitor).
        """
        results = []
        unique_skus = self.data['sku_id'].unique()
        
        for sku in unique_skus:
            sku_data = self.data[self.data['sku_id'] == sku]
            
            # Model Specification
            model = smf.ols(
                formula="log_qty ~ log_price + log_comp_price", 
                data=sku_data
            ).fit()
            
            self.elasticities[sku] = {
                'own_elasticity': model.params['log_price'],
                'cross_elasticity_competitor': model.params['log_comp_price'],
                'r_squared': model.rsquared,
                'intercept': model.params['Intercept']
            }
            
        return pd.DataFrame(self.elasticities).T

    def fit_mixed_effects(self):
        """
        Advanced: Uses Mixed Effects model to share information across Categories.
        Useful when individual SKU data is sparse.
        """
        print("Running Mixed Effects Model (Hierarchical Bayesian-like approach)...")
        md = smf.mixedlm(
            "log_qty ~ log_price + log_comp_price", 
            self.data, 
            groups=self.data["category"]
        )
        mdf = md.fit()
        return mdf.summary()