# 🌐 Pro Logistics Command Dashboard

**Developed as part of a recruitment task at Digitivity Solutions**

A modern, highly optimized enterprise delivery sorting system built using Streamlit and Plotly.

---

## 📌 Problem Statement Overview

Modern delivery systems handle hundreds of delivery locations with varying distances and priorities. Efficiently distributing these deliveries among multiple agents is critical to avoid workload imbalance, delays, and operational inefficiencies.

This project processes raw CSV input data and transforms it into a well-balanced delivery allocation using an optimized greedy algorithm.

---

## 🛠️ Advanced Greedy Routing Logic

The core engine uses an efficient and scalable greedy approach:

1. **Float-Based Targeting**
   All distances are handled as precise floating-point values (e.g., 15.42 km).

2. **Priority-Based Sorting**
   Deliveries are strictly sorted in this order:
   `High → Medium → Low`

3. **Distance Optimization**
   Within each priority group, deliveries are sorted from nearest to farthest.

4. **Greedy Assignment**
   Each delivery is assigned to the agent with the current minimum total workload (distance), ensuring balanced distribution.

5. **Dynamic Agent Handling**
   Supports flexible fleet sizes (e.g., 3 to 15 agents or more).

---

## 📊 Streamlit Platform Modules

The application uses a fully customized UI with injected CSS and a modern teal/blue gradient theme.

### Features:

* **Upload Dataset**

  * Accepts CSV input
  * Validates structure and required columns

* **Data Preview**

  * Displays raw dataset for verification

* **Data Validation**

  * Detects:

    * Missing values (NaN)
    * Duplicate Location IDs
    * Invalid priorities
    * Negative or zero distances

* **Run Optimization**

  * Applies greedy algorithm
  * Supports configurable number of agents
  * Optional priority-weighted logic

* **View Results**

  * Displays:

    * Location ID
    * Product Name
    * Distance (km)
    * Priority
    * Assigned Agent

* **Analytics Dashboard**

  * Bar Chart: Total distance per agent
  * Pie Chart: Priority distribution
  * Histogram: Distance distribution
  * Line Chart: Cumulative workload per agent

* **Download Output**

  * Export results as CSV

---

## 🎨 UI Highlights

* Custom gradient backgrounds
* Responsive metric cards
* Hover effects and modern layout
* Color-coded priorities:

  * High → Red
  * Medium → Orange
  * Low → Green

---

## 💻 Running the App

### Requirements

* Python 3.9+

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

---



## 📊 Key Metrics Generated

* Total Deliveries
* Priority-wise Counts (High / Medium / Low)
* Average Distance
* Maximum & Minimum Distance
* Total Distance per Agent
* Workload Difference Between Agents

---

## ⚙️ Code Structure

* `app.py` → Streamlit UI and workflow
* `utils.py` → Core logic:

  * `load_data()`
  * `validate_data()`
  * `optimize_deliveries()`
  * `generate_summary()`

---

## 🚀 Conclusion

This project demonstrates how a greedy algorithm, when combined with a well-designed UI and proper validation, can evolve into a powerful logistics decision-support dashboard.

It ensures:

* Balanced workload distribution
* Improved operational efficiency
* Clean and interactive visualization
* Scalable architecture for real-world use

---
