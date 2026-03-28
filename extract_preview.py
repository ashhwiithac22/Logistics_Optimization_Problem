import pandas as pd
df = pd.read_csv('output_delivery_plan.csv')
print(df.head(5).to_markdown(index=False))
