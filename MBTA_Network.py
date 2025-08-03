import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Subway Network", layout="wide", page_icon="🚇")

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🚇 Subway Map")
st.sidebar.markdown("Interactive visualization of Boston subway network.")
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], horizontal=True)

# ---------- HEADER ----------
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1 {text-align: center; color: #2c3e50;}
    .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🗺️ Boston Subway Network</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Hover to reveal station names, use mouse to zoom/pan</p>", unsafe_allow_html=True)

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
    'yellow': '#f1c40f',
    'purple': '#9b59b6'
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
    template="plotly_white" if theme == "Light" else "plotly_dark",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------- DISPLAY FIGURE ----------
st.plotly_chart(fig, use_container_width=True)


