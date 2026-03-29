import pandas as pd
import time

def validate_data(df):
    """
    Ensures the uploaded CSV meets ALL project requirements and constraints.
    Returns (is_valid, validation_report_dict, robust_df).
    """
    report = {
        "status": "Pass",
        "errors": [],
        "warnings": []
    }
    required_cols = {'Location_ID', 'Product_Name', 'Distance', 'Priority'}
    
    # 1. Check Missing Columns
    if not required_cols.issubset(df.columns):
        report["status"] = "Fail"
        report["errors"].append(f"Missing required columns. Expected: {required_cols}")
        return False, report, df

    # 2. Check Missing Values (NaN)
    missing_counts = df[list(required_cols)].isna().sum()
    if missing_counts.sum() > 0:
        report["status"] = "Fail"
        report["errors"].append(f"Missing values detected: {missing_counts[missing_counts > 0].to_dict()}")
        return False, report, df
        
    # 3. Check Duplicate Location_ID
    if df['Location_ID'].duplicated().any():
        num_dups = df['Location_ID'].duplicated().sum()
        report["status"] = "Fail"
        report["errors"].append(f"Found {num_dups} duplicate 'Location_ID' entries.")
        return False, report, df
    
    # 4. Check Distance constraint (Numeric, > 0)
    # Attempt to convert Distance to numeric, pushing non-numeric to NaN
    df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
    if df['Distance'].isna().any():
         report["status"] = "Fail"
         report["errors"].append("Column 'Distance' contains non-numeric strings.")
         return False, report, df
         
    if (df['Distance'] <= 0).any():
        num_invalid = (df['Distance'] <= 0).sum()
        report["status"] = "Fail"
        report["errors"].append(f"Found {num_invalid} rows with Distance <= 0. Distance must be > 0.")
        return False, report, df
        
    # 5. Check Priorities
    allowed_priorities = {'High', 'Medium', 'Low'}
    invalid_priorities = set(df['Priority'].unique()) - allowed_priorities
    if invalid_priorities:
        report["status"] = "Fail"
        report["errors"].append(f"Invalid priorities detected: {invalid_priorities}. Allowed: {allowed_priorities}")
        return False, report, df
        
    # 6. Success Metrics
    report["warnings"].append(f"Validated successfully: {len(df)} rows.")

    return True, report, df

def assign_deliveries(df, num_agents=3, use_weighted=False):
    """
    Core logistics logic implementing the dynamic greedy load-balancing algorithm.
    Returns: (processed_df, agent_workloads, sort_time, assign_time, cumulative_history)
    """
    df = df.copy()
    
    # 1. SORTING PHASE
    start_sort = time.perf_counter()
    
    priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
    df['Priority_Weight'] = df['Priority'].map(priority_map)
    df['Weighted_Workload'] = df['Distance'] * df['Priority_Weight']
    
    # Sort primarily by Priority (Descending) and Distance (Ascending)
    df = df.sort_values(by=['Priority_Weight', 'Distance'], ascending=[False, True])
    # Resetting the index is important so that the sequential assignment maps easily to lists
    df = df.reset_index(drop=True)
    sort_time = time.perf_counter() - start_sort
    
    # 2. ASSIGNMENT PHASE (Greedy Load Balancing)
    start_assign = time.perf_counter()
    
    agents = [f'Agent {i+1}' for i in range(num_agents)]
    
    metric_col = 'Weighted_Workload' if use_weighted else 'Distance'
    metric_idx = df.columns.get_loc(metric_col) + 1 # +1 for itertuples
    
    agent_workload = {agent: 0.0 for agent in agents}
    assigned_agents = []
    
    # Initialize a cumulative history structure for charting
    # list of dicts: [{'Agent 1': load, 'Agent 2': load, ...}]
    cumulative_history = []
    
    for row in df.itertuples(name=None):
        # Find the agent with the minimum active workload
        best_agent = min(agent_workload, key=agent_workload.get)
        assigned_agents.append(best_agent)
        
        # Increase their workload tracking by the float distance/load
        agent_workload[best_agent] += float(row[metric_idx])
        
        # Take a snapshot of workloads for this time step
        snapshot = {agent: round(agent_workload[agent], 2) for agent in agents}
        snapshot['Delivery_Index'] = row[0] # capture execution step
        cumulative_history.append(snapshot)
        
    df['Assigned_Agent'] = assigned_agents
    assign_time = time.perf_counter() - start_assign
    
    # Round final workloads for clean display
    agent_workload = {k: round(v, 2) for k, v in agent_workload.items()}
    
    # Ensure Distance column displays beautifully 
    df['Distance_km'] = df['Distance'].apply(lambda x: f"{x:.2f} km")
    
    # Reorganize final output columns explicitly
    cols = ['Location_ID', 'Product_Name', 'Distance_km', 'Priority', 'Assigned_Agent']
    # keep raw Distance and Priority weight for analytics
    final_df = df[cols + ['Distance', 'Priority_Weight', 'Weighted_Workload']].copy()

    return final_df, agent_workload, sort_time, assign_time, pd.DataFrame(cumulative_history)

def generate_summary(df, agent_workload):
    """Calculates comprehensive summary statistics metrics for the assigned dataframe."""
    total_deliveries = len(df)
    
    priority_counts = df['Priority'].value_counts().to_dict()
    num_high = priority_counts.get('High', 0)
    num_med = priority_counts.get('Medium', 0)
    num_low = priority_counts.get('Low', 0)
    
    avg_dist = round(df['Distance'].mean(), 2)
    max_dist = round(df['Distance'].max(), 2)
    min_dist = round(df['Distance'].min(), 2)
    
    highest_agent = max(agent_workload, key=agent_workload.get)
    lowest_agent = min(agent_workload, key=agent_workload.get)
    diff = round(agent_workload[highest_agent] - agent_workload[lowest_agent], 2)
    
    return {
        'total_deliveries': total_deliveries,
        'num_high': num_high,
        'num_medium': num_med,
        'num_low': num_low,
        'avg_distance': avg_dist,
        'max_distance': max_dist,
        'min_distance': min_dist,
        'workload_diff': diff,
        'highest_agent': highest_agent,
        'lowest_agent': lowest_agent,
    }
