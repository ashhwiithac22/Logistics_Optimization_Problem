import streamlit as st
import pandas as pd
import io
import plotly.express as px
from data_generator import generate_sample_data
from utils import validate_data, assign_deliveries, get_insights

st.set_page_config(page_title="Pro Logistics Optimizer", page_icon="🚚", layout="wide")

# Initialize session state for data sharing between pages
for key in ['df', 'processed_df', 'agent_workloads', 'exec_stats']:
    if key not in st.session_state:
        st.session_state[key] = None
if 'use_weighted' not in st.session_state:
    st.session_state['use_weighted'] = False

# Sidebar Navigation
st.sidebar.title("🚚 Navigator")
menu = st.sidebar.radio(
    "Choose Action:",
    [
        "📂 Upload Data",
        "🧪 Generate Sample Data",
        "⚙️ Run Optimization",
        "📊 Analytics Dashboard",
        "🔄 Algorithm Comparison",
        "🔍 Data Insights",
        "📁 Download Results",
        "ℹ️ About / Documentation"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Pro Logistics Optimization Dashboard")

# 1. 📂 Upload Data
if menu == "📂 Upload Data":
    st.title("📂 Upload Logistics Data")
    st.markdown("Upload a CSV file with deliveries to optimize. Ensure it contains the required headers.")
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df
            
            # Data Validation
            is_valid, msg = validate_data(df)
            if is_valid:
                st.success(f"✅ {msg}")
                st.subheader("Dataset Preview")
                st.dataframe(df.head(20), use_container_width=True)
            else:
                st.error(f"❌ Validation Failed: {msg}")
                st.session_state['df'] = None # Invalidate strictly
                
        except Exception as e:
            st.error(f"Error reading file: {e}")
            
    elif st.session_state['df'] is not None:
        st.info("Currently loaded dataset preview:")
        st.dataframe(st.session_state['df'].head(10), use_container_width=True)

# 2. 🧪 Generate Sample Data
elif menu == "🧪 Generate Sample Data":
    st.title("🧪 Generate Sample Data")
    st.markdown("Instantly generate a highly realistic logistics dataset (500 rows) perfectly formatted for execution.")
    
    if st.button("Generate 500-Row Dataset", type="primary"):
        with st.spinner("Generating floating-point geo-data..."):
            df = generate_sample_data(num_rows=500)
            st.session_state['df'] = df
            
            # Auto-reset processing states
            st.session_state['processed_df'] = None
            st.session_state['agent_workloads'] = None
            
        st.success("✅ Dataset successfully built and loaded into memory!")
        st.dataframe(df.head(10), use_container_width=True)
        
    if st.session_state['df'] is not None:
        csv_buffer = io.StringIO()
        st.session_state['df'].to_csv(csv_buffer, index=False)
        st.download_button("⬇️ Download Sample Data to Local", data=csv_buffer.getvalue(), file_name="generated_sample.csv", mime="text/csv")

# 3. ⚙️ Run Optimization
elif menu == "⚙️ Run Optimization":
    st.title("⚙️ Run Optimization Algorithm")
    st.markdown("Apply the constraint-based greedy load-balancing algorithm to your loaded dataset.")
    
    if st.session_state['df'] is None:
        st.warning("⚠️ Please upload or generate data first.")
    else:
        st.session_state['use_weighted'] = st.toggle("Use Weighted Algorithm (Priority-Based)", value=st.session_state['use_weighted'])
        
        button_text = "Process Deliveries (Weighted)" if st.session_state['use_weighted'] else "Process Deliveries (Standard Dist)"
        
        if st.button(button_text, type="primary"):
            with st.spinner("Executing Greedy Router Algorithm..."):
                proc_df, workloads, sort_t, assign_t = assign_deliveries(st.session_state['df'], use_weighted=st.session_state['use_weighted'])
                
                st.session_state['processed_df'] = proc_df
                st.session_state['agent_workloads'] = workloads
                st.session_state['exec_stats'] = {'sort': sort_t, 'assign': assign_t}
                
            st.success(f"✅ Pipeline Processed in {sort_t + assign_t:.4f} aggregated seconds!")
            
        if st.session_state['processed_df'] is not None:
            st.subheader("📦 Assigned Deliveries Plan")
            st.dataframe(st.session_state['processed_df'][['Location_ID', 'Product_Name', 'Distance_km', 'Priority', 'Assigned_Agent']].head(100), use_container_width=True)
            
            st.subheader("🏃‍♂️ Real-Time Agent Target Workloads")
            cols = st.columns(3)
            metric_label = "Load (Points)" if st.session_state['use_weighted'] else "Total Distance (km)"
            for idx, (agent, load) in enumerate(st.session_state['agent_workloads'].items()):
                cols[idx].metric(label=f"{agent} {metric_label}", value=f"{load}")

# 4. 📊 Analytics Dashboard
elif menu == "📊 Analytics Dashboard":
    st.title("📊 Analytics Dashboard")
    if st.session_state['processed_df'] is None:
        st.warning("⚠️ Optimization sequence must be executed first.")
    else:
        metric_name = "Workload Points" if st.session_state['use_weighted'] else "Total Distance (km)"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Agent Operational Balance ({metric_name})**")
            agent_df = pd.DataFrame(list(st.session_state['agent_workloads'].items()), columns=['Agent', 'Load'])
            st.plotly_chart(px.bar(agent_df, x='Agent', y='Load', color='Agent', text_auto=True), use_container_width=True)
            
        with col2:
            st.markdown("**Urgency Target Distribution**")
            st.plotly_chart(px.pie(st.session_state['processed_df'], names='Priority', color='Priority', color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'}), use_container_width=True)

# 5. 🔄 Algorithm Comparison
elif menu == "🔄 Algorithm Comparison":
    st.title("🔄 Multi-Algorithmic Comparison")
    st.markdown("Stress test and benchmark Standard Greedy (Distance) versus Advanced Greedy (Priority-Weighted).")
    
    if st.session_state['df'] is None:
        st.warning("⚠️ Data source isolated. Load external data first.")
    else:
        if st.button("▶️ Run Complete Comparative Simulation", type="primary"):
            with st.spinner("Compiling dual-environment simulations in sandbox..."):
                df1, loads1, _, _ = assign_deliveries(st.session_state['df'], use_weighted=False)
                df2, loads2, _, _ = assign_deliveries(st.session_state['df'], use_weighted=True)
                
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Standard Focus (Distance Only)")
                st.write("*Ignores package urgency.*")
                for a, l in loads1.items():
                    st.info(f"**{a}:** {l:.2f} km")
            with col2:
                st.subheader("Weighted Focus (Priority Based)")
                st.write("*Penalizes high-urgency bottlenecks.*")
                for a, l in loads2.items():
                    st.info(f"**{a}:** {l:.2f} workload points")

# 6. 🔍 Data Insights
elif menu == "🔍 Data Insights":
    st.title("🔍 Operational Data Insights & Equity Matrix")
    if st.session_state['agent_workloads'] is None:
        st.warning("⚠️ Execute core optimizer first to generate heuristics.")
    else:
        stats = get_insights(st.session_state['agent_workloads'], st.session_state['use_weighted'])
        
        st.subheader("Agent Fairness Diagnostic")
        st.success(f"✅ **Max Efficiency Achieved:** {stats['lowest_agent']} handling {stats['lowest_load']}")
        st.error(f"🛑 **Critical Infrastructure Load:** {stats['highest_agent']} operating at {stats['highest_load']}")
        st.metric("Total Operational Variance Delta", f"{stats['difference']}")
        
        if stats['is_balanced']:
            st.success("Verdict: ✅ **Highly Balanced Route Generation (System Nominal)**")
        else:
            st.warning("Verdict: ⚠️ **Severe Imbalance Detected in Logistics Assignment!**")

        if st.session_state['exec_stats']:
            st.markdown("---")
            st.subheader("Time Complexity Profiler")
            st.code(f"Sorting Overhead     : {st.session_state['exec_stats']['sort']:.6f} milliseconds\nMemory Assingment    : {st.session_state['exec_stats']['assign']:.6f} milliseconds")

# 7. 📁 Download Results
elif menu == "📁 Download Results":
    st.title("📁 Export Verified Delivery Plan")
    if st.session_state['processed_df'] is None:
        st.warning("⚠️ Process memory empty. Run optimizations first.")
    else:
        st.markdown("✅ Final assignments securely written to deployment buffer.")
        csv_buffer = io.StringIO()
        st.session_state['processed_df'].to_csv(csv_buffer, index=False)
        st.download_button(
            "⬇️ Fetch Output Plan File (CSV)",
            data=csv_buffer.getvalue(),
            file_name="verified_delivery_plan.csv",
            mime="text/csv",
            type="primary"
        )

# 8. ℹ️ About / Documentation
elif menu == "ℹ️ About / Documentation":
    st.title("ℹ️ Theoretical Documentation")
    st.markdown("""
    ### System Architecture Overview
    This multi-module Streamlit dashboard solves complex N-tier logistics problems using constraint-based greedy traversal mechanics.
    
    ### Optimization Matrix Methodologies
    - **Algorithmic Engine:** Each instantiated delivery is dynamically routed to the courier framework possessing the currently minimized cumulative metric block.
    - **Variable Workload Definitions:** 
        - Default Euclidean: `Load = Pure Vector Distance`
        - Aggregated Contextual Weighted: `Load = Euclidean Distance × Priority Matrix Value`
        
    ### Structural Assumptions & Theoretical Limitations
    - **Operational Assumptions:** Courier velocities are normalized constants. Vector pathways translate one-to-one regarding temporal expenditure.
    - **Boundary Limitations:** Static distance constraints. Fails to contextualize dense geographic clusters or Traveling Salesperson routing optimization maps natively, functioning instead strictly on volume/demand equalization.
    """)
