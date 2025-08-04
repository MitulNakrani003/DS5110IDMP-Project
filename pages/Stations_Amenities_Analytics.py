import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    stations_df = pd.read_csv("stations.csv")
    connections_df = pd.read_csv("connections.csv")
    amenities_df = pd.read_csv("stations_amenities.csv")
    return stations_df, connections_df, amenities_df

stations_df, connections_df, amenities_df = load_data()

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
    <h1 style="margin: 0; font-size: 2.5em;">🚇 Station Amenities Analytics</h1>
</div>
""", unsafe_allow_html=True)

# Merge data for comprehensive analysis
def merge_station_data():
    # Get all unique stations and their lines
    station_lines = pd.concat([
        connections_df[['From', 'Color']].rename(columns={'From': 'Station'}),
        connections_df[['To', 'Color']].rename(columns={'To': 'Station'})
    ]).drop_duplicates()
    
    # Group by station to get all lines and count
    grouped = station_lines.groupby('Station').agg({
        'Color': lambda x: list(set(x))
    }).reset_index()
    grouped['Line_Count'] = grouped['Color'].apply(len)
    grouped.columns = ['Station', 'Lines', 'Line_Count']
    grouped['Lines_Str'] = grouped['Lines'].apply(lambda x: ', '.join([line.title() for line in x]))
    
    # Merge with amenities
    merged_df = grouped.merge(amenities_df, on='Station', how='left')
    
    return merged_df

merged_data = merge_station_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Line filter
all_lines = sorted(list(set([line for lines in merged_data['Lines'] for line in lines])))
selected_lines = st.sidebar.multiselect(
    "Subway Lines",
    options=all_lines,
    default=all_lines,
    help="Filter stations by subway lines"
)

# Amenity filters
amenity_options = ['Parking', 'Ramp', 'Lift', 'Underground']
selected_amenities = st.sidebar.multiselect(
    "Required Amenities",
    options=amenity_options,
    default=[],
    help="Filter stations that must have these amenities"
)

# Line count filter
min_lines = int(merged_data['Line_Count'].min())
max_lines = int(merged_data['Line_Count'].max())
line_count_range = st.sidebar.slider(
    "Number of Lines",
    min_value=0,
    max_value=max_lines,
    value=(0, max_lines),
    help="Filter by number of lines serving each station"
)

# Apply filters
filtered_data = merged_data.copy()

if selected_lines:
    filtered_data = filtered_data[filtered_data['Lines'].apply(lambda x: any(line in selected_lines for line in x))]

if selected_amenities:
    for amenity in selected_amenities:
        filtered_data = filtered_data[filtered_data[amenity] == 'Yes']

filtered_data = filtered_data[
    (filtered_data['Line_Count'] >= line_count_range[0]) &
    (filtered_data['Line_Count'] <= line_count_range[1])
]

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Stations", len(filtered_data))
    st.metric("Multi-line Stations", len(filtered_data[filtered_data['Line_Count'] > 1]))

with col2:
    st.metric("Parking Available", len(filtered_data[filtered_data['Parking'] == 'Yes']))
    st.metric("Ramp Access", len(filtered_data[filtered_data['Ramp'] == 'Yes']))

with col3:
    st.metric("Lift Access", len(filtered_data[filtered_data['Lift'] == 'Yes']))
    st.metric("Underground", len(filtered_data[filtered_data['Underground'] == 'Yes']))

with col4:
    st.metric("Avg Lines/Station", f"{filtered_data['Line_Count'].mean():.1f}")
    st.metric("Max Lines/Station", filtered_data['Line_Count'].max())

# Analytics tabs
tab1, tab2, tab3 = st.tabs(["📊 Line Analysis", "♿ Accessibility", "🅿️ Parking Analysis"])

with tab1:
    st.subheader("Line Distribution & Connectivity")
    
    # Line distribution chart
    line_counts = filtered_data['Line_Count'].value_counts().sort_index()
    fig_line_dist = px.bar(
        x=line_counts.index,
        y=line_counts.values,
        title="Distribution of Stations by Number of Lines",
        labels={'x': 'Number of Lines', 'y': 'Number of Stations'}
    )
    st.plotly_chart(fig_line_dist, use_container_width=True)
    
    # Top connected stations
    top_stations = filtered_data.nlargest(10, 'Line_Count')[['Station', 'Line_Count', 'Lines_Str']]
    st.subheader("Top 10 Most Connected Stations")
    st.dataframe(top_stations, use_container_width=True)

with tab2:
    st.subheader("Accessibility Analysis")
    
    # Accessibility metrics
    accessibility_data = []
    for amenity in ['Ramp', 'Lift']:
        count = len(filtered_data[filtered_data[amenity] == 'Yes'])
        total = len(filtered_data)
        percentage = (count / total) * 100 if total > 0 else 0
        accessibility_data.append({
            'Amenity': amenity,
            'Count': count,
            'Percentage': percentage
        })
    
    acc_df = pd.DataFrame(accessibility_data)
    
    # Accessibility chart
    fig_acc = px.bar(
        acc_df,
        x='Amenity',
        y='Percentage',
        title="Accessibility Coverage by Amenity",
        text='Count',
        color='Amenity',
        color_discrete_map={'Ramp': '#2ecc71', 'Lift': '#3498db'}
    )
    fig_acc.update_traces(textposition='outside')
    st.plotly_chart(fig_acc, use_container_width=True)
    
    # Fully accessible stations
    full_access = filtered_data[
        (filtered_data['Ramp'] == 'Yes') & 
        (filtered_data['Lift'] == 'Yes')
    ]
    st.subheader("♿ Fully Accessible Stations")
    if len(full_access) > 0:
        st.dataframe(full_access[['Station', 'Lines_Str', 'Line_Count']], use_container_width=True)
    else:
        st.info("No stations found with full accessibility features")

with tab3:
    st.subheader("Parking Analysis")
    
    # Parking statistics
    parking_stations = filtered_data[filtered_data['Parking'] == 'Yes']
    parking_percentage = (len(parking_stations) / len(filtered_data)) * 100 if len(filtered_data) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stations with Parking", len(parking_stations))
    with col2:
        st.metric("Parking Coverage", f"{parking_percentage:.1f}%")
    with col3:
        st.metric("Avg Lines (Parking)", f"{parking_stations['Line_Count'].mean():.1f}")
    
    # Parking by line analysis
    if len(parking_stations) > 0:
        parking_by_line = []
        for _, row in parking_stations.iterrows():
            for line in row['Lines']:
                parking_by_line.append(line.title())
        
        parking_line_counts = pd.Series(parking_by_line).value_counts()
        fig_parking = px.bar(
            x=parking_line_counts.index,
            y=parking_line_counts.values,
            title="Parking Availability by Line",
            labels={'x': 'Line', 'y': 'Stations with Parking'}
        )
        st.plotly_chart(fig_parking, use_container_width=True)

# Main station table
st.header("Station Information")

# Create a clean display table
display_columns = ['Station', 'Lines_Str', 'Line_Count', 'Parking', 'Ramp', 'Lift', 'Underground']
display_data = filtered_data[display_columns].copy()

# Rename columns for better display
display_data.columns = ['Station', 'Lines', 'Line Count', 'Parking', 'Ramp', 'Lift', 'Underground']

# Add amenity icons
def add_amenity_icons(row):
    icons = []
    if row['Parking'] == 'Yes':
        icons.append("🅿️")
    if row['Ramp'] == 'Yes':
        icons.append("♿")
    if row['Lift'] == 'Yes':
        icons.append("🛗")
    if row['Underground'] == 'Yes':
        icons.append("🚇")
    return ' '.join(icons) if icons else "—"

display_data['Amenities'] = display_data.apply(add_amenity_icons, axis=1)

# Show the table
st.dataframe(display_data, use_container_width=True)

# Summary insights
st.header("Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Lines:** {len(selected_lines)} selected")
    st.write(f"**Amenities:** {len(selected_amenities)} selected")
    st.write(f"**Line Count Range:** {line_count_range[0]}-{line_count_range[1]}")
    st.write(f"**Stations Shown:** {len(filtered_data)}")

# Footer
st.markdown("---")