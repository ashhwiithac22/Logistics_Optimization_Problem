import pandas as pd
from data_generator import generate_sample_data
from utils import validate_data, assign_deliveries, get_insights

def main():
    print("=== Logistics Delivery Optimization CLI ===")
    
    print("1. Generating Dataset...")
    df = generate_sample_data(num_rows=500, filename="sample_input.csv")
    
    valid, msg = validate_data(df)
    if not valid:
        print(f"Validation Failed: {msg}")
        return
        
    print("2. Running Normal Greedy Optimization...")
    proc_df, workloads, sort_t, assign_t = assign_deliveries(df, use_weighted=False)
    
    print(f"Sorting Time: {sort_t:.4f}s | Assignment Time: {assign_t:.4f}s")
    for agent, load in workloads.items():
        print(f"{agent}: {load} km")
        
    stats = get_insights(workloads)
    print(f"Is Balanced: {'Yes' if stats['is_balanced'] else 'No'} (Difference: {stats['difference']} km)")
    
    proc_df.to_csv("output_delivery_plan.csv", index=False)
    print("Results saved to 'output_delivery_plan.csv'")

if __name__ == "__main__":
    main()
