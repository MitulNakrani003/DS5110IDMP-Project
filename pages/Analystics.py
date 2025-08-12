import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="Boston Subway Analytics", layout="wide")

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
    <h1 style="margin: 0; font-size: 2.5em;">📊 Boston Subway Network Analytics</h1>
</div>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    stations_df = pd.read_csv("stations.csv")
    locations_df = pd.read_csv("locations.csv")
    connections_df = pd.read_csv("connections.csv")
    connections_df["Color"] = connections_df["Color"].str.lower()
    return stations_df, locations_df, connections_df

stations_df, locations_df, connections_df = load_data()

# Color mapping
color_map = {
    'red': '#e74c3c', 'blue': '#3498db', 'green': '#2ecc71',
    'orange': '#e67e22', 'yellow': '#f1c40f', 'purple': '#9b59b6'
}

# Network Analysis
st.header("Network Structure Analysis")

# Create network graph
G = nx.DiGraph()
for _, row in connections_df.iterrows():
    G.add_edge(row["From"], row["To"], weight=row["Minutes"], color=row["Color"])

# Calculate network metrics
total_stations = len(G.nodes())
total_connections = len(G.edges())
avg_degree = sum(dict(G.degree()).values()) / len(G.nodes())
density = nx.density(G)

# Network overview metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Stations", total_stations)
with col2:
    st.metric("Total Connections", total_connections)
with col3:
    st.metric("Average Connections per Station", f"{avg_degree:.1f}")


st.subheader("Line Performance Analysis")

# Line statistics
line_stats = connections_df.groupby("Color").agg({
    "Minutes": ["count", "mean", "min", "max", "sum"],
    "From": "nunique",
    "To": "nunique"
}).round(2)

line_stats.columns = ["Connections", "Avg_Time", "Min_Time", "Max_Time", "Total_Time", "Unique_From", "Unique_To"]
line_stats["Stations"] = line_stats[["Unique_From", "Unique_To"]].max(axis=1)
line_stats["Efficiency"] = line_stats["Total_Time"] / line_stats["Connections"]

# Line comparison chart
fig_line_comparison = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Stations per Line", "Average Travel Time", "Total Connections", "Network Efficiency"),
    specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
)

# Stations per line
fig_line_comparison.add_trace(
    go.Bar(x=line_stats.index, y=line_stats["Stations"], 
           name="Stations", marker_color=[color_map.get(c, '#95a5a6') for c in line_stats.index]),
    row=1, col=1
)

# Average travel time
fig_line_comparison.add_trace(
    go.Bar(x=line_stats.index, y=line_stats["Avg_Time"], 
           name="Avg Time", marker_color=[color_map.get(c, '#95a5a6') for c in line_stats.index]),
    row=1, col=2
)

# Total connections
fig_line_comparison.add_trace(
    go.Bar(x=line_stats.index, y=line_stats["Connections"], 
           name="Connections", marker_color=[color_map.get(c, '#95a5a6') for c in line_stats.index]),
    row=2, col=1
)

# Efficiency (lower is better)
fig_line_comparison.add_trace(
    go.Bar(x=line_stats.index, y=line_stats["Efficiency"], 
           name="Efficiency", marker_color=[color_map.get(c, '#95a5a6') for c in line_stats.index]),
    row=2, col=2
)

fig_line_comparison.update_layout(height=600, showlegend=False, title_text="Line Performance Metrics")
st.plotly_chart(fig_line_comparison, use_container_width=True)

# Station Connectivity Analysis
st.subheader("Station Connectivity Analysis")

# Calculate degree centrality for each station
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)

# Create centrality dataframe
centrality_df = pd.DataFrame({
    "Station": list(G.nodes()),
    "Degree_Centrality": [degree_centrality[node] for node in G.nodes()],
    "Betweenness_Centrality": [betweenness_centrality[node] for node in G.nodes()],
    "Closeness_Centrality": [closeness_centrality[node] for node in G.nodes()],
    "Total_Connections": [G.degree(node) for node in G.nodes()]
})

# Top 10 most connected stations
top_stations = centrality_df.nlargest(10, "Total_Connections")

fig_top_stations = px.bar(
    top_stations, 
    x="Station", 
    y="Total_Connections",
    title="Top 10 Most Connected Stations",
    color="Total_Connections",
    color_continuous_scale="viridis"
)
fig_top_stations.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_top_stations, use_container_width=True)

# --- Travel Time Analysis ---
st.subheader("Travel Time Analysis")

# Travel time distribution
fig_time_dist = px.histogram(
    connections_df, 
    x="Minutes", 
    nbins=20,
    title="Distribution of Travel Times Between Stations",
    labels={"Minutes": "Travel Time (minutes)", "count": "Number of Connections"}
)
st.plotly_chart(fig_time_dist, use_container_width=True)

# Travel time by line
fig_time_by_line = px.histogram(
    connections_df, 
    x="Color", 
    y="Minutes",
    title="Travel Time Distribution by Line",
    color="Color",
    color_discrete_map=color_map
)
st.plotly_chart(fig_time_by_line, use_container_width=True)

# --- Network Efficiency Analysis ---
st.subheader("Network Efficiency Analysis")

# Calculate shortest paths
def calculate_network_efficiency():
    efficiency_data = []
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                try:
                    shortest_path = nx.shortest_path_length(G, source, target, weight="Minutes")
                    efficiency_data.append({
                        "Source": source,
                        "Target": target,
                        "Shortest_Path_Time": shortest_path
                    })
                except nx.NetworkXNoPath:
                    continue
    return pd.DataFrame(efficiency_data)

efficiency_df = calculate_network_efficiency()

# Average travel time to reach any station
avg_travel_times = efficiency_df.groupby("Source")["Shortest_Path_Time"].mean().sort_values()
fig_avg_travel = px.bar(
    x=avg_travel_times.index,
    y=avg_travel_times.values,
    title="Average Travel Time from Each Station to All Other Stations",
    labels={"x": "Station", "y": "Average Travel Time (minutes)"}
)
fig_avg_travel.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_avg_travel, use_container_width=True)

# --- Geographic Analysis ---
st.subheader("Geographic Network Analysis")

# Merge location data with centrality data
locations_analysis = locations_df.merge(centrality_df, left_on="Station Name", right_on="Station", how="left")

# Geographic distribution of connectivity
fig_geo_connectivity = px.scatter(
    locations_analysis,
    x="x",
    y="y",
    size="Total_Connections",
    color="Degree_Centrality",
    hover_name="Station Name",
    title="Geographic Distribution of Station Connectivity",
    color_continuous_scale="viridis",
    size_max=20
)
fig_geo_connectivity.update_layout(
    xaxis_title="X Coordinate",
    yaxis_title="Y Coordinate"
)
st.plotly_chart(fig_geo_connectivity, use_container_width=True)

# Key Insights
st.subheader("Key Insights")

most_efficient_line = line_stats["Efficiency"].idxmin()
busiest_station = centrality_df.loc[centrality_df["Total_Connections"].idxmax(), "Station"]
# Number of isolated components
longest_connection = connections_df.loc[connections_df["Minutes"].idxmax()]

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Most Efficient Liner:** {most_efficient_line.title()} (lowest average time per connection)")
    st.write(f"**Busiest Station:** {busiest_station} ({centrality_df['Total_Connections'].max()} connections)")
    st.write(f"**Longest Connection:** {longest_connection['From']} → {longest_connection['To']} ({longest_connection['Minutes']} min)")
   


# Data Summary Table 
st.subheader("Network Summary")
summary_data = {
    "Metric": ["Total Stations", "Total Connections", "Average Travel Time", "Most Connected Station"],
    "Value": [
        total_stations,
        total_connections,
        f"{connections_df['Minutes'].mean():.2f} minutes",
        busiest_station
    ]
}
summary_df = pd.DataFrame(summary_data)
st.table(summary_df)

# Footer
st.markdown("---")