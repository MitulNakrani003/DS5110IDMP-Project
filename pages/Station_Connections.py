import streamlit as st
import pandas as pd

st.set_page_config(page_title="Connections by Line", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .filter-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stats-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .legend-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .conn-table table {
        border-collapse: separate; 
        border-spacing: 0 8px; 
        width: 100%;
        margin-top: 15px;
    }
    
    .conn-table th {
        text-align: left; 
        font-size: 14px; 
        color: #334155; 
        padding: 12px 15px;
        background: #f8fafc;
        border-bottom: 2px solid #e2e8f0;
        font-weight: 600;
    }
    
    .conn-table td {
        background: #ffffff; 
        padding: 15px; 
        font-size: 14px; 
        vertical-align: middle;
        border: 1px solid #e2e8f0;
    }
    
    .conn-table tr td:first-child {
        border-top-left-radius: 10px; 
        border-bottom-left-radius: 10px;
    }
    
    .conn-table tr td:last-child {
        border-top-right-radius: 10px; 
        border-bottom-right-radius: 10px;
    }
    
    .conn-table tbody tr:hover td {
        background: #f1f5f9;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .download-section {
        background: #f0f9ff;
        border: 1px solid #0ea5e9;
        border-radius: 10px;
        padding: 20px;
        margin-top: 25px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5em;">🚉 Station Connections Analytics</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.9;">Explore and filter train connections across different lines</p>
</div>
""", unsafe_allow_html=True)

# --- Load data ---
connections_df = pd.read_csv("connections.csv")

# Normalize/clean
connections_df["Color"] = connections_df["Color"].str.lower().str.strip()
if "Minutes" in connections_df.columns:
    connections_df["Minutes"] = pd.to_numeric(connections_df["Minutes"], errors="coerce")

# --- Color map ---
color_map = {
    "red": "#e74c3c",
    "blue": "#3498db",
    "green": "#2ecc71",
    "orange": "#e67e22",
}

# --- Filter Menu (Collapsible) ---
with st.expander("🔍 **Filter Options**", expanded=True):
    #st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    # Create three columns for filters
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("**Line Filter**")
        line_options = sorted(connections_df["Color"].dropna().unique().tolist())
        sel_lines = st.multiselect(
            "Select line(s)",
            options=line_options,
            default=line_options,
            format_func=lambda x: x.title(),
            help="Choose which metro lines to display"
        )
    
    with col2:
        st.markdown("**Time Filter**")
        if connections_df["Minutes"].notna().any():
            mn = float(connections_df["Minutes"].min())
            mx = float(connections_df["Minutes"].max())
            sel_min, sel_max = st.slider(
                "Journey time (minutes)", 
                min_value=mn, 
                max_value=mx, 
                value=(mn, mx),
                help="Filter connections by travel time"
            )
        else:
            sel_min, sel_max = None, None
    
    with col3:
        st.markdown("**Search Filter**")
        q = st.text_input(
            "Search stations", 
            "", 
            placeholder="Enter station name...",
            help="Search by departure or arrival station"
        ).strip().lower()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
df = connections_df.copy()
if sel_lines:
    df = df[df["Color"].isin(sel_lines)]

if sel_min is not None and sel_max is not None and "Minutes" in df.columns:
    df = df[df["Minutes"].between(sel_min, sel_max, inclusive="both")]

if q:
    df = df[
        df["From"].str.lower().str.contains(q, na=False) |
        df["To"].str.lower().str.contains(q, na=False)
    ]

# --- Statistics Cards ---
st.markdown("### Connection Statistics")
stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="margin: 0; color: #667eea;">{len(df):,}</h3>
        <p style="margin: 5px 0 0 0; color: #64748b;">Total Connections</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col2:
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="margin: 0; color: #667eea;">{len(df['Color'].unique()):,}</h3>
        <p style="margin: 5px 0 0 0; color: #64748b;">Active Lines</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col3:
    avg_time = df["Minutes"].mean() if "Minutes" in df.columns and df["Minutes"].notna().any() else 0
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="margin: 0; color: #667eea;">{avg_time:.1f}</h3>
        <p style="margin: 5px 0 0 0; color: #64748b;">Avg Time (min)</p>
    </div>
    """, unsafe_allow_html=True)

# --- Color chip function ---
def color_chip(line: str) -> str:
    bg = color_map.get(str(line).lower(), "#999")
    label = str(line).title()
    return (
        f"<span style='display:inline-block;background:{bg};color:white;"
        f"padding:4px 12px;border-radius:999px;font-weight:600;font-size:13px;"
        f"box-shadow:0 2px 4px rgba(0,0,0,0.15);'>{label}</span>"
    )

df_display = pd.DataFrame({
    "From": df["From"],
    "→": ["→"] * len(df),
    "To": df["To"],
    "Line": df["Color"].apply(color_chip),
    "Minutes": df["Minutes"] if "Minutes" in df.columns else None
})

# --- Results Section ---
st.markdown("### Connection Details")
st.caption(f"Showing {len(df_display):,} connections based on the selectedfilters")

# Render table as HTML
st.markdown(
    df_display.to_html(escape=False, index=False, classes="conn-table"),
    unsafe_allow_html=True
)

# --- Download Section ---
#st.markdown('<div class="download-section">', unsafe_allow_html=True)
st.markdown("**💾 Export Data**")
csv_bytes = df[["From", "To", "Color", "Minutes"]].to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download Filtered Connections (CSV)",
    data=csv_bytes,
    file_name="connections_filtered.csv",
    mime="text/csv",
    help="Download the filtered connections as a CSV file"
)
st.markdown('</div>', unsafe_allow_html=True)
