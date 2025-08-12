import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Subway Network", layout="wide", page_icon="🚇")

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
    <h1 style="margin: 0; font-size: 2.5em;">🗺️ Boston Subway Network</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.9;">Hover to reveal station names, use mouse to zoom/pan</p>
</div>
""", unsafe_allow_html=True)


# ---------- LOAD DATA ----------
stations_df = pd.read_csv("stations.csv")
locations_df = pd.read_csv("locations.csv")
connections_df = pd.read_csv("connections.csv")

locations_df_unique = locations_df.drop_duplicates(subset='Station Name', keep='first')
location_map = locations_df_unique.set_index('Station Name')[['x', 'y']].to_dict('index')

# ---------- SCALE COORDINATES ----------
scale = 10
for station in location_map:
    location_map[station]['x'] *= scale
    location_map[station]['y'] *= scale

# ---------- COLOR MAPPING ----------
color_map = {
    'red': '#e74c3c',
    'blue': '#3498db',
    'green': '#2ecc71',
    'orange': '#e67e22',
}

# ---------- BUILD FIGURE ----------
fig = go.Figure()

# Draw colored edges per line
for color in set(connections_df['Color']):
    color_edges_x, color_edges_y = [], []
    for _, row in connections_df[connections_df['Color'] == color].iterrows():
        if row['From'] in location_map and row['To'] in location_map:
            x0, y0 = location_map[row['From']]['x'], location_map[row['From']]['y']
            x1, y1 = location_map[row['To']]['x'], location_map[row['To']]['y']
            color_edges_x += [x0, x1, None]
            color_edges_y += [y0, y1, None]
    fig.add_trace(go.Scatter(
        x=color_edges_x, y=color_edges_y,
        mode='lines',
        line=dict(color=color_map.get(color, '#95a5a6'), width=4),
        name=color.title() + " Line",
        hoverinfo='none'
    ))

# Draw stations
node_x = [v['x'] for v in location_map.values()]
node_y = [v['y'] for v in location_map.values()]
node_labels = list(location_map.keys())

fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    marker=dict(size=18, color='#2c3e50', line=dict(width=2, color='white')),
    text=node_labels,
    hoverinfo='text',
    name='Stations'
))

# ---------- STYLING ----------
fig.update_layout(
    title="Subway Network Map",
    showlegend=True,
    hovermode='closest',
    margin=dict(l=20, r=20, t=40, b=20),
    height=900,
    template="plotly_white",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------- DISPLAY FIGURE ----------
st.plotly_chart(fig, use_container_width=True)