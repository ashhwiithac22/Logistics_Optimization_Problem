import pandas as pd
import numpy as np
import random

def main():
    # 1. Generate Dataset
    random.seed(42)
    np.random.seed(42)

    products = ['tooth paste', 'tooth brush', 'curtains', 'rice', 'vegetables', 'mobile phone', 'dresses']
    priorities = ['High', 'Medium', 'Low']

    data = {
        'Location_ID': [f'L{i}' for i in range(1, 501)],
        'Product_Name': np.random.choice(products, 500),
        'Distance': np.random.randint(1, 51, 500),
        'Priority': np.random.choice(priorities, 500)
    }

    df = pd.DataFrame(data)
    df.to_csv('sample_input.csv', index=False)

    print("=== SAMPLE CSV PREVIEW ===")
    print(df.head(10).to_markdown(index=False))

    # 2. Logic
    priority_map = {'High': 1, 'Medium': 2, 'Low': 3}
    df['Priority_Rank'] = df['Priority'].map(priority_map)
    df = df.sort_values(by=['Priority_Rank', 'Distance']).drop(columns=['Priority_Rank'])

    agents = ['Agent A', 'Agent B', 'Agent C']
    agent_distances = {agent: 0 for agent in agents}
    assigned_agents = []

    for _, row in df.iterrows():
        best_agent = min(agent_distances, key=agent_distances.get)
        assigned_agents.append(best_agent)
        agent_distances[best_agent] += row['Distance']

    df['Assigned_Agent'] = assigned_agents
    df.to_csv('output_delivery_plan.csv', index=False)

    print("\n=== SAMPLE OUTPUT PREVIEW ===")
    print(df.head(10).to_markdown(index=False))

    print("\n=== TOTAL DISTANCE PER AGENT ===")
    for a, d in agent_distances.items():
        print(f"{a}: {d}")

if __name__ == "__main__":
    main()
