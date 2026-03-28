import pandas as pd
df = pd.read_csv('output_delivery_plan.csv')
with open('preview_output.md', 'w') as f:
    f.write("=== PREVIEW ===\n")
    f.write(df.head(10).to_markdown(index=False))
    
    # Calculate workloads directly as well
    weight_map = {'High': 3, 'Medium': 2, 'Low': 1}
    df['Priority_Weight'] = df['Priority'].map(weight_map)
    df['Weighted_Workload'] = df['Distance'] * df['Priority_Weight']
    workloads = df.groupby('Assigned_Agent')['Weighted_Workload'].sum()
    
    f.write("\n\n=== WORKLOADS ===\n")
    for agent, load in workloads.items():
        f.write(f"{agent}: {load} points\n")
