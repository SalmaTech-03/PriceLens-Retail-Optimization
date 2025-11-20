import pandas as pd
import statsmodels.formula.api as smf

class CrossElasticityMatrix:
    def __init__(self, df):
        self.df = df

    def calculate_matrix(self, category):
        """
        Calculates a Cross-Elasticity Matrix for all products in a category.
        Output: A dataframe where Row = Target Product, Col = Driver Price
        """
        cat_data = self.df[self.df['category'] == category].copy()
        products = cat_data['product_name'].unique()
        
        matrix = pd.DataFrame(index=products, columns=products)
        
        # Pivot data to have prices of all products day-by-day
        price_pivot = cat_data.pivot(index='date', columns='product_name', values='price')
        qty_pivot = cat_data.pivot(index='date', columns='product_name', values='quantity_sold')
        
        for target in products:
            for driver in products:
                if target == driver:
                    # Own Elasticity (Simple log-log)
                    continue 
                
                # Merge specific columns
                temp_df = pd.DataFrame({
                    'log_qty_target': pd.np.log1p(qty_pivot[target]),
                    'log_price_driver': pd.np.log1p(price_pivot[driver])
                }).dropna()
                
                # Fit Model
                try:
                    model = smf.ols("log_qty_target ~ log_price_driver", data=temp_df).fit()
                    coeff = model.params['log_price_driver']
                    matrix.loc[target, driver] = coeff
                except:
                    matrix.loc[target, driver] = 0.0
                    
        return matrix