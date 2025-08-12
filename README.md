# DS5110IDMP-Project
# SmartTransit: A Data-Driven System for Navigating and Analyzing Public Transport

**SmartTransit** is an interactive platform for analyzing and visualizing the Massachusetts Bay Transportation Authority (MBTA) subway network.  
It combines **open transit data**, **graph analytics**, and **AI-assisted querying** to deliver actionable insights for city planners, researchers, and commuters.

---

## Features
- **Data Integration** – Uses MBTA’s official [GTFS feed](https://www.mbta.com/developers/gtfs) and supplementary datasets from MassDOT Open Data.
- **Graph Analytics** – Computes network centrality, connection efficiency, and accessibility metrics using [NetworkX](https://networkx.org/).  
- **AI Query Assistant** – Natural language to SQL translation with the [OpenAI GPT-4 API](https://platform.openai.com/docs/) for intuitive data exploration.  
- **Interactive Dashboards** – Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/python/) for dynamic, real-time visualizations.  
- **Accessibility Insights** – Maps stations with elevators, ramps, and wheelchair access to inform infrastructure planning.

---

## Methodology
1. **Data Collection** – Pulls GTFS feeds and MassDOT datasets for stops, routes, travel times, and facilities.  
2. **Preprocessing** – Cleans and structures raw data into relational tables (stations, connections, amenities).  
3. **Storage** – In-memory SQLite database for fast queries and AI integration.  
4. **Analysis** – Uses Python (Pandas, NumPy, SciPy, NetworkX) for metrics computation.  
5. **Visualization** – Generates network graphs, heatmaps, line comparisons, and geospatial plots.  
6. **AI Interface** – Accepts plain-English queries and returns results with visualizations.

---

## System Architecture
<img width="2363" height="242" alt="flowchart_smarttransit" src="https://github.com/user-attachments/assets/4e60547e-c1aa-47ce-806d-c5ceb88ebfe1" />

---

## Tech Stack
| Component        | Technology |
|------------------|------------|
| **Frontend**     | Streamlit, HTML/CSS, Plotly |
| **Backend**      | Python (Pandas, NumPy, SciPy, NetworkX) |
| **Database**     | SQLite (in-memory) |
| **AI Integration** | OpenAI GPT-4 API |
| **Data Sources** | MBTA GTFS feed, MassDOT datasets |

---
## Usage
streamlit run MBTA_Network.py

---




