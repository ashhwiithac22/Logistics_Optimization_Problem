# Logistics Delivery Optimization System

## 📌 Problem Explanation
The goal of this project is to optimize a logistics delivery system. We are given a list of 500 deliveries, each with a specific location, product type, distance from the warehouse, and urgency (`Priority`). The objective is to efficiently distribute these deliveries among three agents (Agent A, Agent B, Agent C), ensuring that the workload is fairly distributed while strictly prioritizing the most urgent deliveries.

## ⚙️ Algorithm Explanation (Weighted Greedy Method)
We solve this problem using an optimized greedy algorithm augmented with a priority weighting penalty.

1. **Calculating Weighted Workload**: 
   A simple distance metric fails to capture the true urgency of high-priority packages. Therefore, we map priorities mathematically: `High = 3, Medium = 2, Low = 1`.
   Then, we define the true workload requirement for each package as:
   `Weighted_Workload = Distance × Priority_Weight`
   
2. **Sorting**: We prioritize and group the deliveries. The dataset is sorted by:
   - **Priority_Weight** in descending order (High urgency first).
   - **Distance** in ascending order, so nearest locations for the same urgency class are handled efficiently.

3. **Load Balancing (Greedy Strategy)**: We process each delivery sequentially taking advantage of the fastest iteration methods (`itertuples`). The package is assigned to the agent who currently has the **minimum active Weighted Workload**.
    - This continually bridges the gap between agent metrics.
    - If enabled, the toggle allows rolling back to standard distance assignment.

## ⚖️ Why Weighting Improves Fairness
Assigning high-priority items generally takes more immediate focus and rush compared to non-urgent items. If two agents travel 50 km in total, but Agent A delivers exclusively "High" priority packages and Agent B delivers exclusively "Low" priority packages, Agent A is under significantly more operational stress.

By weighting the workload (`Distance × Priority_Weight`), the algorithm actively punishes assigning too many high-priority items to a single agent. The ultimate result is that each agent gets an incredibly fair mix of total distance AND priority urgencies.

## ⏱️ Time Complexity Analysis
* **Sorting Phase:** `O(n log n)`
  Sorting the pandas DataFrame by Priority Weight and Distance dictates our theoretical ceiling for arrangement.
* **Assignment Phase:** `O(n)`
  The greedy load assignment steps through the data exactly once. By avoiding `iterrows()` and utilizing `.itertuples()`, the constant factors of overhead are minimal.
* **Overall Time Complexity:** `O(n log n)` due to the sorting bound.

## 🚀 Conclusion
This optimization logic achieves incredible consistency across delivery metrics, ensuring logistics agencies can trust that routes are both mathematically balanced and operationally fair, reducing employee burnout and improving high-priority delivery success metrics.

## 💻 How to Run

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```
   *Features interactive charts, toggles, and analysis views!*

3. **Run the Standalone Script**:
   ```bash
   python main.py
   ```
