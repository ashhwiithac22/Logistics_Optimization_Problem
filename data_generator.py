import pandas as pd
import random
import numpy as np

def generate_sample_data(num_rows=500, filename=None):
    """
    Generates a sample logistics dataset with float distances.
    """
    random.seed(42)
    np.random.seed(42)
    
    products = ['tooth paste', 'tooth brush', 'curtains', 'rice', 'vegetables', 'mobile phone', 'dresses']
    priorities = ['High', 'Medium', 'Low']
    
    data = {
        'Location_ID': [f'L{i}' for i in range(1, num_rows + 1)],
        'Product_Name': np.random.choice(products, num_rows),
        # Distance must be realistic float values between 1 and 50 km
        'Distance': [round(random.uniform(1.0, 50.0), 2) for _ in range(num_rows)],
        'Priority': np.random.choice(priorities, num_rows)
    }
    
    df = pd.DataFrame(data)
    if filename:
        df.to_csv(filename, index=False)
    return df
