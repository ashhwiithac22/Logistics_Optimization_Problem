import streamlit as st
import pandas as pd
import io
import plotly.express as px
import time
from data_generator import generate_sample_data
from utils import validate_data, assign_deliveries, generate_summary

# 1. PAGE CONFIG & CUSTOM THEMING
st.set_page_config(page_title="Advanced Logistics Platform", page_icon="🚚", layout="wide")

# Inject Custom CSS for modern card-like styling of metrics and background
st.markdown("""
<style>
    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        border: 1px solid #d1d9e6;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        color: #2b2d42;
    }
    div[data-testid="metric-container"] label {
        color: #6c757d;
        font-weight: 600;
        font-size: 0.95rem;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0077b6;
        font-size: 1.8rem;
        font-weight: 700;
    }
    /* Headers & Text Formatting */
    h1 { color: #023e8a; }
    h2 { color: #0077b6; border-bottom: 2px solid #00b4d8; padding-bottom: 5px; }
    h3 { color: #0096c7; }
</style>
""", unsafe_allow_html=True)

# Application Global State Initialization
for key in ['df', 'processed_df', 'agent_workloads', 'cumulative_history', 'summary_stats', 'validation_report']:
    if key not in st.session_state:
        st.session_state[key] = None

# 2. SIDEBAR NAVIGATION
st.sidebar.markdown("## 🌐 Logistics Command")
st.sidebar.divider()
menu = st.sidebar.radio(
    "Modules:",
    [
        "📂 Upload Dataset",
        "👀 Data Preview",
        "🛡️ Data Validation",
        "⚙️ Run Optimization",
        "📑 View Results",
        "📊 Analytics Dashboard",
        "⬇️ Download Output"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 Tip: Use 'Data Preview' to inspect auto-generated or uploaded CSV structural integrity.")

# Global Color Palette Dictionary
PRIORITY_COLORS = {'High': '#e63946', 'Medium': '#f4a261', 'Low': '#2a9d8f'}

# --- UPLOAD DATASET ---
if menu == "📂 Upload Dataset":
    st.title("📂 System Initialization & Import")
    st.markdown("Load a CSV batch or generate an identical test schema to commence operational routing.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Import Custom Fleet Data")
        uploaded_file = st.file_uploader("Drop CSV Here", type=["csv"])
        if uploaded_file is not None:
            try:
                st.session_state['df'] = pd.read_csv(uploaded_file)
                st.session_state['processed_df'] = None # Clear old runs
                st.success("✅ File payload acquired successfully!")
            except Exception as e:
                st.error(f"Error accessing schema: {e}")
                
    with col2:
        st.subheader("Or Generate Synthetic Batch")
        st.markdown("Creates 500 rows with normalized float vectors and categorical urgencies.")
        if st.button("Generate Demo Batch", type="primary", use_container_width=True):
            st.session_state['df'] = generate_sample_data(num_rows=500)
            st.session_state['processed_df'] = None
            st.success("🤖 Synthetic data array injected into memory.")

# --- DATA PREVIEW ---
elif menu == "👀 Data Preview":
    st.title("👀 Operational Data Preview")
    if st.session_state['df'] is None:
        st.warning("⚠️ No data batch loaded in RAM.")
    else:
        st.markdown("Raw Dataset View:")
        
        # Advanced Filtering & Sorting Pre-computation
        search_query = st.text_input("🔍 Search Location ID:", "")
        priority_filter = st.multiselect("Filter by Target Urgency:", options=['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low'])
        
        preview_df = st.session_state['df'].copy()
        if search_query:
            preview_df = preview_df[preview_df['Location_ID'].astype(str).str.contains(search_query, case=False)]
        
        preview_df = preview_df[preview_df['Priority'].isin(priority_filter)]
        
        st.dataframe(preview_df, use_container_width=True, height=600)
        st.metric("Total Match Found:", len(preview_df))

# --- DATA VALIDATION ---
elif menu == "🛡️ Data Validation":
    st.title("🛡️ Pre-Flight Diagnostic Checks")
    st.markdown("Ensuring vector payload integrity before pushing to algorithm constraint matrices.")
    if st.session_state['df'] is None:
         st.warning("⚠️ Data block empty.")
    else:
        with st.spinner("Processing deep structural scan..."):
            time.sleep(0.5) # Slight delay for UI effect
            is_valid, report, robust_df = validate_data(st.session_state['df'].copy())
            st.session_state['validation_report'] = report
        
        if is_valid:
            st.success("✅ **OVERALL STATUS: GREEN.** Data satisfies all execution constraints.")
            st.balloons()
            for msg in report["warnings"]:
                st.info(msg)
        else:
            st.error("❌ **OVERALL STATUS: RED.** Structural violations detected!")
            for error in report["errors"]:
                st.error(f"- {error}")
            st.warning("Resolution required before `Run Optimization` is enabled.")

# --- RUN OPTIMIZATION ---
elif menu == "⚙️ Run Optimization":
    st.title("⚙️ Algorithmic Load Balancer")
    if st.session_state['df'] is None:
        st.warning("⚠️ Data module empty.")
    else:
        # Prevent if invalid
        valid_status = False
        if st.session_state['validation_report']:
            valid_status = st.session_state['validation_report']['status'] == "Pass"
        else:
            valid_status, r, _ = validate_data(st.session_state['df'].copy())
            st.session_state['validation_report'] = r
            
        if not valid_status:
            st.error("🛑 Hard Stop: Current dataset failed integrity checks. Go to Data Validation.")
        else:
            st.subheader("Configuration Matrix")
            col_a, col_b = st.columns(2)
            with col_a:
                num_agents = st.slider("Select Available Agents:", min_value=1, max_value=15, value=3)
            with col_b:
                 use_weighted = st.toggle("Apply Priority-Weighted Engine", value=False, help="Forces heavy loads towards Agent equilibrium.")
            
            if st.button("🚀 INITIATE GREEDY ASSIGNMENT SEQUENCE"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Building priority weights & sorting trees...")
                progress_bar.progress(30)
                time.sleep(0.5)
                
                status_text.text(f"Dispatching greedy sub-routines across {num_agents} worker nodes...")
                proc_df, loads, sort_t, assign_t, history = assign_deliveries(st.session_state['df'], num_agents=num_agents, use_weighted=use_weighted)
                st.session_state['processed_df'] = proc_df
                st.session_state['agent_workloads'] = loads
                st.session_state['cumulative_history'] = history
                st.session_state['summary_stats'] = generate_summary(proc_df, loads)
                progress_bar.progress(80)
                time.sleep(0.3)
                
                status_text.text("Finalizing memory caches...")
                progress_bar.progress(100)
                time.sleep(0.2)
                
                st.success(f"✅ Protocol complete in {sort_t + assign_t:.5f}s. Move to **View Results**.")

# --- VIEW RESULTS ---
elif menu == "📑 View Results":
    st.title("📑 Fleet Execution Output Table")
    if st.session_state['processed_df'] is None:
        st.warning("⚠️ Pending assignment algorithms. Execute Optimizer first.")
    else:
        st.markdown("Filter and inspect the finalized dispatch roster.")
        
        col1, col2 = st.columns(2)
        with col1:
             agent_filter = st.multiselect("Filter Assigned Agent:", options=list(st.session_state['agent_workloads'].keys()), default=list(st.session_state['agent_workloads'].keys()))
        with col2:
             route_search = st.text_input("🔍 Find Location ID (Post-Assign):")
             
        res_df = st.session_state['processed_df'].copy()
        
        # Mandatory formatting columns: Location ID | Product Name | Distance (km) | Priority | Assigned Agent 
        display_cols = ['Location_ID', 'Product_Name', 'Distance_km', 'Priority', 'Assigned_Agent']
        
        res_df = res_df[res_df['Assigned_Agent'].isin(agent_filter)]
        if route_search:
            res_df = res_df[res_df['Location_ID'].astype(str).str.contains(route_search, case=False)]
            
        st.dataframe(res_df[display_cols], use_container_width=True, height=500)

# --- ANALYTICS DASHBOARD ---
elif menu == "📊 Analytics Dashboard":
    st.title("📊 Enterprise Route Analytics")
    if st.session_state['summary_stats'] is None:
         st.warning("⚠️ No telemetry available. Execute routing logic first.")
    else:
        stats = st.session_state['summary_stats']
        
        st.subheader("Global KPI Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📦 Active Packages", stats['total_deliveries'])
        m2.metric("📏 Avg Dist. (km)", f"{stats['avg_distance']:.2f}")
        m3.metric("⚠️ Peak Max Dst.", f"{stats['max_distance']:.2f} km")
        m4.metric("📉 Minimum Dst.", f"{stats['min_distance']:.2f} km")
        
        st.divider()
        st.subheader("Agent Load Equilibrium")
        c1, c2, c3 = st.columns(3)
        c1.metric("🏆 Min Load Runner", stats['lowest_agent'])
        c2.metric("🥵 Max Stress Runner", stats['highest_agent'])
        c3.metric("⚖️ Variance (Delta)", f"{stats['workload_diff']} bounds")

        st.divider()
        st.subheader("Comprehensive Visualizations")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown('**1. Delivery Priority Density (Pie)**')
            # Use discrete color map to enforce Red, Orange, Green
            fig_pie = px.pie(st.session_state['processed_df'], names='Priority', color='Priority',
                             color_discrete_map=PRIORITY_COLORS, hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            st.markdown('**2. Workload Distributed Sums (Bar)**')
            agent_df = pd.DataFrame(list(st.session_state['agent_workloads'].items()), columns=['Agent', 'Total Load Limit'])
            fig_bar = px.bar(agent_df, x='Agent', y='Total Load Limit', color='Agent', text_auto=True)
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown('**3. Distance Vector Frequency (Histogram)**')
        fig_hist = px.histogram(st.session_state['processed_df'], x='Distance', nbins=20, 
                                color_discrete_sequence=['#0077b6'], title="Distribution of Raw Distance Vertices")
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown('**4. Algorithmic Matrix Processing Trace (Line)**')
        if st.session_state['cumulative_history'] is not None:
             history_df = st.session_state['cumulative_history']
             # Melt for easy plotly line chart (Delivery Index as X)
             metric_cols = [c for c in history_df.columns if c != 'Delivery_Index']
             melted_hist = history_df.melt(id_vars='Delivery_Index', value_vars=metric_cols, var_name='Agent', value_name='Cumulative Load')
             fig_line = px.line(melted_hist, x='Delivery_Index', y='Cumulative Load', color='Agent', title="Load Curve Velocity Through Greedy Loop")
             st.plotly_chart(fig_line, use_container_width=True)

# --- DOWNLOAD OUTPUT ---
elif menu == "⬇️ Download Output":
    st.title("⬇️ Document & Report Export")
    if st.session_state['processed_df'] is None:
        st.warning("⚠️ No finalized payload array built yet.")
    else:
        st.success("✅ Output verified securely in Memory Buffer.")
        
        # Provide clean structured payload
        display_cols = ['Location_ID', 'Product_Name', 'Distance_km', 'Priority', 'Assigned_Agent']
        clean_df = st.session_state['processed_df'][display_cols]
        
        csv_buffer = io.StringIO()
        clean_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Final CSV",
            data=csv_buffer.getvalue(),
            file_name="Optimum_Dispatch_Plan.csv",
            mime="text/csv",
            type="primary"
        )
        
        st.divider()
        st.subheader("Summary Report Snapshot")
        st.markdown(f"""
        - **Total Shipments Logged:** {len(clean_df)}
        - **System Assigned Fleet Members:** {len(st.session_state['agent_workloads'])}
        - **Priority Breakdown:** High ({st.session_state['summary_stats']['num_high']}), Medium ({st.session_state['summary_stats']['num_medium']}), Low ({st.session_state['summary_stats']['num_low']})
        """)
        
        for ag, ld in st.session_state['agent_workloads'].items():
            st.write(f"- **{ag} Assigned Quota:** {ld:.2f}")
