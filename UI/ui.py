import streamlit as st
import requests
import json
from typing import Dict, Any

# Configure page
st.set_page_config(
    page_title="Boston MBTA System",
    page_icon="🚇",
    layout="wide"
)

# API base URL - adjust if your FastAPI runs on different host/port
API_BASE_URL = "http://localhost:8000"

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003DA5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        text-align: center;
        padding: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚇 Boston MBTA System</h1>', unsafe_allow_html=True)

# Helper functions
def make_api_request(endpoint: str, method: str = "GET", data: Dict[str, Any] = None):
    """Make API request to FastAPI backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Main content with tabs
tab1, tab2, tab3 = st.tabs(["🗺️ System Map", "🚉 Route Planning", "💬 AI Chat"])

# Tab 1: System Map
with tab1:
    st.header("MBTA System Map")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("View System Map")
        map_data = make_api_request("/api/system-map")
        
        if map_data:
            st.markdown(f"**Last Updated:** {map_data.get('last_updated', 'N/A')}")
            
            st.markdown("### Map Options:")
            st.markdown(f"📄 [Download PDF Map]({map_data.get('map_url', '#')})")
            st.markdown(f"🌐 [Interactive Web Map]({map_data.get('interactive_map', '#')})")
    
    with col2:
        st.subheader("Quick Facts")
        st.info("""
        **MBTA Subway Lines:**
        - 🔴 Red Line
        - 🟠 Orange Line  
        - 🔵 Blue Line
        - 🟢 Green Line
        
        **Operating Hours:**
        - Weekdays: 5:00 AM - 1:00 AM
        - Weekends: 6:00 AM - 1:00 AM
        """)

# Tab 2: Route Planning
with tab2:
    st.header("Route Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get stations list
        stations_data = make_api_request("/api/stations")
        stations = stations_data.get("stations", []) if stations_data else []
        
        origin = st.selectbox("Origin Station", stations, key="origin")
        destination = st.selectbox("Destination Station", stations, key="destination")
        fare_type = st.selectbox("Fare Type", ["regular", "reduced", "student"])
    
    with col2:
        st.subheader("Fare Information")
        st.markdown("""
        **Fare Types:**
        - **Regular**: $2.40
        - **Reduced**: $1.10 (Seniors, disabilities)
        - **Student**: $1.10 (With valid ID)
        """)
    
    if st.button("Plan Route", type="primary"):
        if origin and destination:
            if origin == destination:
                st.warning("Please select different origin and destination stations.")
            else:
                route_data = {
                    "origin": origin,
                    "destination": destination,
                    "fare_type": fare_type
                }
                
                result = make_api_request("/api/plan-route", method="POST", data=route_data)
                
                if result:
                    st.success("Route Found!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Estimated Time", result.get("estimated_time", "N/A"))
                    with col2:
                        st.metric("Fare", f"${result.get('fare', 0):.2f}")
                    with col3:
                        st.metric("Transfers", len(result.get("routes", [])) - 1)
                    
                    st.subheader("Route Details")
                    for i, route in enumerate(result.get("routes", [])):
                        st.markdown(f"**Step {i+1}:** Take {route.get('line', 'N/A')} towards {route.get('direction', 'N/A')}")
                        if route.get('stops'):
                            st.markdown(f"Stops: {' → '.join(route['stops'])}")

# Tab 3: AI Chat
with tab3:
    st.header("AI Assistant")
    st.markdown("Ask me anything about the MBTA system!")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about MBTA (e.g., 'What are the operating hours?')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        chat_data = {"prompt": prompt}
        response = make_api_request("/api/chat", method="POST", data=chat_data)
        
        if response:
            ai_response = response.get("response", "Sorry, I couldn't process your request.")
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.markdown(ai_response)

# Footer
st.markdown("""
<div class="footer">
    <p>Created by [Your Name] | 
    <a href="https://github.com/yourusername/mbta-system" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white" alt="GitHub">
    </a>
    </p>
</div>
""", unsafe_allow_html=True)

# Add some padding at the bottom to prevent content overlap with footer
st.markdown("<br><br>", unsafe_allow_html=True)