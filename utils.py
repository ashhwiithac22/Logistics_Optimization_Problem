import pandas as pd
import time

def validate_data(df):
    """
    Ensures the uploaded CSV meets project requirements.
    Returns (is_valid, error_message).
    """
    required_cols = {'Location_ID', 'Product_Name', 'Distance', 'Priority'}
    if not required_cols.issubset(df.columns):
        return False, f"Missing required columns. Expected: {required_cols}"
    
    # Check if Distance is numeric
    if not pd.api.types.is_numeric_dtype(df['Distance']):
        return False, "Column 'Distance' must be numeric."
        
    # Check Priorities
    allowed_priorities = {'High', 'Medium', 'Low'}
    if not set(df['Priority'].unique()).issubset(allowed_priorities):
        return False, f"Column 'Priority' contains invalid values. Allowed: {allowed_priorities}"
        
    return True, "Data is valid."

def assign_deliveries(df, use_weighted=False):
    """
    Core logistics logic implementing the greedy load-balancing algorithm.
    Returns: (processed_df, agent_workloads, sort_time, assign_time)
    """
    df = df.copy()
    
    # 1. SORTING PHASE
    start_sort = time.perf_counter()
    
    priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
    df['Priority_Weight'] = df['Priority'].map(priority_map)
    df['Weighted_Workload'] = df['Distance'] * df['Priority_Weight']
    
    # Sort primarily by Priority (Descending) and Distance (Ascending)
    df = df.sort_values(by=['Priority_Weight', 'Distance'], ascending=[False, True])
    sort_time = time.perf_counter() - start_sort
    
    # 2. ASSIGNMENT PHASE (Greedy Load Balancing)
    start_assign = time.perf_counter()
    
    agents = ['Agent A', 'Agent B', 'Agent C']
    
    metric_col = 'Weighted_Workload' if use_weighted else 'Distance'
    metric_idx = df.columns.get_loc(metric_col) + 1 # +1 for itertuples
    
    agent_workload = {agent: 0.0 for agent in agents}
    assigned_agents = []
    
    for row in df.itertuples(name=None):
        # Find the agent with the minimum active workload
        best_agent = min(agent_workload, key=agent_workload.get)
        assigned_agents.append(best_agent)
        
        # Increase their workload tracking by the float distance/load
        agent_workload[best_agent] += float(row[metric_idx])
        
    df['Assigned_Agent'] = assigned_agents
    assign_time = time.perf_counter() - start_assign
    
    # Round final workloads for clean display
    agent_workload = {k: round(v, 2) for k, v in agent_workload.items()}
    
    # Optional formatting to ensure display everywhere as "12.45 km"
    df['Distance_km'] = df['Distance'].apply(lambda x: f"{x:.2f} km")

    return df, agent_workload, sort_time, assign_time
    
def get_insights(agent_workload, use_weighted=False):
    """Calculates distribution insights from agent workloads."""
    highest_agent = max(agent_workload, key=agent_workload.get)
    lowest_agent = min(agent_workload, key=agent_workload.get)
    diff = round(agent_workload[highest_agent] - agent_workload[lowest_agent], 2)
    
    # Threshold based evaluation - 50 km for normal, 150 points for weighted
    threshold = 150.0 if use_weighted else 50.0  
    is_balanced = diff < threshold
    
    return {
        'highest_agent': highest_agent,
        'lowest_agent': lowest_agent,
        'highest_load': agent_workload[highest_agent],
        'lowest_load': agent_workload[lowest_agent],
        'difference': diff,
        'is_balanced': is_balanced
    }
