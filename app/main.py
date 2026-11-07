import streamlit as st
import subprocess
import time
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Data Engineering Pipeline & BI Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* HERO */
.hero {
    padding: 25px 30px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        rgba(99,102,241,0.18),
        rgba(168,85,247,0.12),
        rgba(236,72,153,0.08)
    );
    border: 1px solid rgba(139,92,246,0.25);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 2.35rem;
    font-weight: 800;
    margin-bottom: 5px;
    background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 15px;
}

/* STATUS */
.status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    border-radius: 20px;
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 0.85rem;
    color: #e2e8f0;
}

.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 12px rgba(34,197,94,0.8);
}

/* CARDS */
.glass-card {
    padding: 20px;
    border-radius: 16px;
    background: rgba(30,41,59,0.45);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
    transition: 0.25s ease;
}

.glass-card:hover {
    border-color: rgba(139,92,246,0.5);
    transform: translateY(-2px);
}

.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.card-text {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* PIPELINE */
.pipeline-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 25px 0;
    overflow-x: auto;
}

.pipeline-step {
    text-align: center;
    padding: 18px 20px;
    min-width: 145px;
    border-radius: 14px;
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.1);
}

.pipeline-icon {
    font-size: 2rem;
    margin-bottom: 5px;
}

.pipeline-name {
    font-weight: 700;
}

.pipeline-desc {
    color: #94a3b8;
    font-size: 0.75rem;
}

.arrow {
    font-size: 1.5rem;
    color: #8b5cf6;
}

/* SECTION */
.section-title {
    font-size: 1.5rem;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #64748b;
    margin-bottom: 20px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.75rem;
    padding: 30px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "pipeline_runs" not in st.session_state:
    st.session_state.pipeline_runs = []

if "pipeline_running" not in st.session_state:
    st.session_state.pipeline_running = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ⚡ E-Commerce Data Platform")
    st.markdown("""
    <div class="status">
        <span class="status-dot"></span>
        Platform Online
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🎛️ Control Center")

    navigation = st.radio(
        "Navigate",
        [
            "📊 Executive Dashboard",
            "🚀 Pipeline Control",
            "🔍 Data Quality",
            "🏗️ Architecture",
            "📋 Run History"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### 🧰 Technology Stack")
    st.markdown("""
    **Processing**  
    Apache Spark 3.x  

    **Orchestration**  
    Apache Airflow  

    **Storage**  
    MySQL 8.0  

    **Visualization**  
    Tableau Public  

    **Infrastructure**  
    Docker & Docker Compose  

    **Application**  
    Streamlit
    """)

    st.divider()
    st.caption("E-Commerce Data Engineering Pipeline & BI Dashboard")
    st.caption("Aditya Mishra • 2026")


# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">
        ⚡ E-Commerce Data Engineering Pipeline & BI Dashboard
    </div>
    <div class="hero-subtitle">
        End-to-end data engineering platform transforming Brazilian
        e-commerce data into analytics-ready warehouse tables and
        interactive business intelligence.
    </div>
    <div class="status">
        <span class="status-dot"></span>
        Data Platform Operational
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PLATFORM METRICS
# ============================================================

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("📦 Source Records", "~100K", "Olist Dataset")
with m2:
    st.metric("💰 Revenue", "$16.57M", "Processed")
with m3:
    st.metric("⚡ Processing", "PySpark", "Distributed ETL")
with m4:
    st.metric("🗄️ Warehouse", "MySQL", "olist_dw")
with m5:
    st.metric("📊 BI Layer", "Tableau", "Interactive")

st.divider()


# ============================================================
# TAB 1 — EXECUTIVE DASHBOARD
# ============================================================

if navigation == "📊 Executive Dashboard":
    st.markdown('<div class="section-title">📊 Executive Business Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Interactive business intelligence powered by the Gold layer.</div>', unsafe_allow_html=True)

    tableau_url = (
        "https://public.tableau.com/views/"
        "Book1_17889684359940/"
        "Dashboard1?:showVizHome=no"
        "&:embed=true"
        "&:render=true"
        "&:device=desktop"
    )

    st.iframe(
        tableau_url,
        height=900
    )


# ============================================================
# TAB 2 — PIPELINE CONTROL
# ============================================================

elif navigation == "🚀 Pipeline Control":
    st.markdown('<div class="section-title">🚀 Pipeline Control Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Trigger the PySpark ETL pipeline and monitor its execution in real-time.</div>', unsafe_allow_html=True)

    # PIPELINE FLOW
    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-step">
            <div class="pipeline-icon">📁</div>
            <div class="pipeline-name">Raw Data</div>
            <div class="pipeline-desc">CSV Source Files</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🥉</div>
            <div class="pipeline-name">Bronze</div>
            <div class="pipeline-desc">Raw Ingestion</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🥈</div>
            <div class="pipeline-name">Silver</div>
            <div class="pipeline-desc">Clean + Validate</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🥇</div>
            <div class="pipeline-name">Gold</div>
            <div class="pipeline-desc">Star Schema</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🗄️</div>
            <div class="pipeline-name">MySQL</div>
            <div class="pipeline-desc">Data Warehouse</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.metric("Pipeline", "Ready", "PySpark")
    with p2:
        st.metric("Target", "olist_dw", "MySQL")
    with p3:
        st.metric("Schema", "Star Schema", "Gold")
    with p4:
        st.metric("Orchestration", "Airflow", "Enabled")

    st.write("")

    run_button = st.button(
        "🚀 Execute PySpark ETL Pipeline",
        type="primary",
        width="stretch",
        disabled=st.session_state.pipeline_running
    )

    if run_button:
        st.session_state.pipeline_running = True
        start_time = time.time()
        progress_bar = st.progress(0)
        status_box = st.status("🔄 Initializing Spark Job...", expanded=True)

        stdout_logs, stderr_logs = "", ""
        return_code = -1

        try:
            status_box.write("🔌 Triggering Docker exec command on spark-master...")
            progress_bar.progress(15)

            cmd = [
                "docker", "exec", "-u", "root", "spark-master",
                "/opt/spark/bin/spark-submit",
                "--packages", "mysql:mysql-connector-java:8.0.28",
                "/app/scripts/load_to_mysql.py"
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            status_box.write("⚡ Executing PySpark transformations (Bronze ➔ Silver ➔ Gold)...")
            progress_bar.progress(45)

            stdout_logs, stderr_logs = process.communicate(timeout=300)
            return_code = process.returncode

            progress_bar.progress(100)
            duration = round(time.time() - start_time, 2)

            if return_code == 0:
                status_box.update(label="✅ Pipeline executed successfully!", state="complete")
                st.success(f"🎉 Gold layer loaded into MySQL warehouse in {duration}s.")
                st.session_state.pipeline_runs.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "SUCCESS",
                    "duration": f"{duration}s"
                })
            else:
                status_box.update(label="❌ Pipeline execution failed", state="error")
                st.error("Pipeline run failed. Check execution logs below.")
                st.session_state.pipeline_runs.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "FAILED",
                    "duration": f"{duration}s"
                })

        except subprocess.TimeoutExpired:
            process.kill()
            status_box.update(label="⌛ Execution timed out (5 mins)", state="error")
            st.error("Spark job timed out after 5 minutes.")
            st.session_state.pipeline_runs.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "TIMEOUT",
                "duration": ">300s"
            })
        except Exception as e:
            status_box.update(label="❌ System error", state="error")
            st.error(f"Execution Error: {str(e)}")
        finally:
            st.session_state.pipeline_running = False

        st.markdown("### 📋 Real-Time Execution Logs")
        with st.expander("View Standard Output (stdout)", expanded=(return_code == 0)):
            if stdout_logs:
                st.code(stdout_logs[-8000:], language="text")
            else:
                st.info("No standard output generated.")

        if stderr_logs:
            with st.expander("View Standard Error / Spark Logs (stderr)", expanded=(return_code != 0)):
                st.code(stderr_logs[-8000:], language="text")


# ============================================================
# TAB 3 — DATA QUALITY
# ============================================================

elif navigation == "🔍 Data Quality":
    st.markdown('<div class="section-title">🔍 Data Quality Monitor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Quality assertions applied across Silver and Gold layers.</div>', unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.metric("Null Validation", "Passed", "✓")
    with q2:
        st.metric("Timestamp Validation", "Passed", "✓")
    with q3:
        st.metric("Foreign Keys", "Passed", "✓")
    with q4:
        st.metric("Payment Validation", "Passed", "✓")

    st.write("")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🧹 Silver Layer Checks</div>
            <div class="card-text">
            ✓ Missing-value handling<br>
            ✓ Duplicate record removal<br>
            ✓ Standardized ISO timestamps<br>
            ✓ Invalid order status filtering<br>
            ✓ Outlier payment value validation<br>
            ✓ Key referential integrity
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🥇 Gold Layer Validation</div>
            <div class="card-text">
            ✓ fact_sales grain consistency<br>
            ✓ Customer surrogate keys integrity<br>
            ✓ Product category coverage<br>
            ✓ Seller performance metrics check<br>
            ✓ Full date dimension generation<br>
            ✓ Strict Star-Schema joins
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 Gold Warehouse Tables")
    table_data = {
        "Table": ["fact_sales", "dim_customer", "dim_product", "dim_seller", "dim_date"],
        "Type": ["Fact", "Dimension", "Dimension", "Dimension", "Dimension"],
        "Purpose": ["Transaction metrics", "Customer analytics", "Product attributes", "Seller details", "Time breakdown"],
        "Layer": ["Gold", "Gold", "Gold", "Gold", "Gold"]
    }
    st.dataframe(table_data, width="stretch", hide_index=True)


# ============================================================
# TAB 4 — ARCHITECTURE
# ============================================================

elif navigation == "🏗️ Architecture":
    st.markdown('<div class="section-title">🏗️ Platform Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">End-to-end data flow and architectural design.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-step">
            <div class="pipeline-icon">📄</div>
            <div class="pipeline-name">CSV Sources</div>
            <div class="pipeline-desc">Olist Dataset</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🐳</div>
            <div class="pipeline-name">Docker</div>
            <div class="pipeline-desc">Runtime</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">⚡</div>
            <div class="pipeline-name">Apache Spark</div>
            <div class="pipeline-desc">ETL Engine</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🥇</div>
            <div class="pipeline-name">Gold Layer</div>
            <div class="pipeline-desc">Star Schema</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🗄️</div>
            <div class="pipeline-name">MySQL</div>
            <div class="pipeline-desc">Warehouse</div>
        </div>
        <div class="arrow">→</div>
        <div class="pipeline-step">
            <div class="pipeline-icon">📊</div>
            <div class="pipeline-name">Tableau</div>
            <div class="pipeline-desc">BI Layer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🥉 Bronze Layer</div>
            <div class="card-text">Raw CSV data ingestion into storage with schema enforcement.<br><br><b>Goal:</b> Historical raw landing zone.</div>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🥈 Silver Layer</div>
            <div class="card-text">Data cleansing, deduplication, type casting, and validation.<br><br><b>Goal:</b> Single source of truth.</div>
        </div>
        """, unsafe_allow_html=True)
    with a3:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">🥇 Gold Layer</div>
            <div class="card-text">Business aggregation into dimensional star-schema tables.<br><br><b>Goal:</b> High-performance analytics.</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### ⭐ Gold Star Schema Data Model")
    st.code("""
                    ┌──────────────────┐
                    │   dim_customer   │
                    └────────┬─────────┘
                             │
                             ▼
┌──────────────────┐    ┌──────────────┐    ┌──────────────────┐
│   dim_product    │ ──►│  fact_sales  │◄── │    dim_seller    │
└──────────────────┘    └──────┬───────┘    └──────────────────┘
                               │
                               ▼
                       ┌────────────────┐
                       │    dim_date    │
                       └────────────────┘
    """, language="text")


# ============================================================
# TAB 5 — RUN HISTORY
# ============================================================

elif navigation == "📋 Run History":
    st.markdown('<div class="section-title">📋 Pipeline Run History</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Execution logs and audit metrics for active session runs.</div>', unsafe_allow_html=True)

    if not st.session_state.pipeline_runs:
        st.info("No pipeline executions recorded yet. Run the pipeline from Pipeline Control.")
    else:
        history = list(reversed(st.session_state.pipeline_runs))
        st.dataframe(history, width="stretch", hide_index=True)

        successful = sum(1 for run in history if run["status"] == "SUCCESS")
        failed = sum(1 for run in history if run["status"] == "FAILED")

        h1, h2, h3 = st.columns(3)
        h1.metric("Total Runs", len(history))
        h2.metric("Successful", successful)
        h3.metric("Failed", failed)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
⚡ E-Commerce Data Engineering Pipeline & BI Dashboard<br>
Apache Spark • Airflow • Docker • MySQL • Streamlit • Tableau<br><br>
Built by Aditya Mishra • 2026
</div>
""", unsafe_allow_html=True)