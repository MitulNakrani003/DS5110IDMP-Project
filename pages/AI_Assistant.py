import streamlit as st
import pandas as pd
import sqlite3
import openai
import json
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
import threading

st.set_page_config(page_title="AI Assistant", layout="wide")

# Page header
st.title("🤖 AI Assistant for Subway Data Analysis")
st.markdown("Ask questions about the Boston subway network and get instant SQL-powered insights!")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = None

# Sidebar for API configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to enable AI-powered queries",
        value=st.session_state.api_key
    )
    
    if api_key:
        st.session_state.api_key = api_key
        # Initialize OpenAI client with new API format
        openai_client = openai.OpenAI(api_key=api_key)
        st.success("✅ API Key configured!")
    else:
        st.warning("⚠️ Please enter your OpenAI API key to use the AI assistant")
        openai_client = None
    
    st.markdown("---")
    
    # Data schema information
    st.header("📊 Data Schema")
    st.markdown("""
    **Tables Available:**
    
    **connections.csv:**
    - From (text): Departure station
    - To (text): Arrival station  
    - Color (text): Line color (red, blue, green, orange)
    - Minutes (float): Travel time in minutes
    
    **stations.csv:**
    - Station Name (text): Name of the station
    
    **locations.csv:**
    - Station Name (text): Name of the station
    - x (float): X coordinate
    - y (float): Y coordinate
    """)

# Load data
@st.cache_data
def load_data():
    connections_df = pd.read_csv("connections.csv")
    stations_df = pd.read_csv("stations.csv")
    locations_df = pd.read_csv("locations.csv")
    return connections_df, stations_df, locations_df

connections_df, stations_df, locations_df = load_data()

# Create database connection in a thread-safe way
def get_database_connection():
    if st.session_state.db_conn is None:
        # Create new connection in the current thread
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        
        # Create tables
        connections_df.to_sql('connections', conn, index=False, if_exists='replace')
        stations_df.to_sql('stations', conn, index=False, if_exists='replace')
        locations_df.to_sql('locations', conn, index=False, if_exists='replace')
        
        st.session_state.db_conn = conn
    
    return st.session_state.db_conn

# Schema information for GPT with proper SQLite syntax
SCHEMA_INFO = """
Database Schema for Boston Subway Network (SQLite):

Table: connections
- "From" (TEXT): Departure station name (use quotes as it's a reserved word)
- "To" (TEXT): Arrival station name (use quotes as it's a reserved word)
- Color (TEXT): Line color (red, blue, green, orange)
- Minutes (REAL): Travel time in minutes

Table: stations  
- "Station Name" (TEXT): Name of the station (use quotes for space in column name)

Table: locations
- "Station Name" (TEXT): Name of the station (use quotes for space in column name)
- x (REAL): X coordinate for mapping
- y (REAL): Y coordinate for mapping

IMPORTANT SQLite RULES:
1. Use double quotes around column names that are reserved words: "From", "To"
2. Use double quotes around column names with spaces: "Station Name"
3. Use single quotes for string literals: 'red', 'blue', etc.
4. SQLite is case-insensitive for keywords but case-sensitive for identifiers
5. Use proper JOIN syntax when combining tables
6. Use COUNT(), AVG(), SUM(), MIN(), MAX() for aggregations

Sample data insights:
- The network has multiple lines (red, blue, green, orange)
- Travel times range from 1 to 9 minutes between stations
- Some stations serve multiple lines
- Geographic coordinates are available for mapping

Example queries:
- SELECT COUNT(DISTINCT "From") FROM connections WHERE Color = 'red';
- SELECT Color, AVG(Minutes) FROM connections GROUP BY Color;
- SELECT "Station Name" FROM stations WHERE "Station Name" LIKE '%Square%';
"""

# Function to generate SQL query using ChatGPT
def generate_sql_query(user_question, openai_client):
    try:
        prompt = f"""
You are a SQLite expert analyzing a Boston subway network database. 

{SCHEMA_INFO}

User Question: {user_question}

Generate a SQLite query that answers this question. The query must:
1. Use valid SQLite syntax
2. Use double quotes around reserved words: "From", "To", "Station Name"
3. Use single quotes for string literals: 'red', 'blue', etc.
4. Return meaningful results
5. Use appropriate JOINs if needed
6. Include proper aggregation if required
7. Be efficient and readable

Return ONLY the SQL query, no explanations or markdown formatting.
"""

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a SQLite expert. Always use double quotes for reserved words and column names with spaces. Return only valid SQLite queries, no explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Clean up the response (remove markdown if present)
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        
        return sql_query.strip()
    
    except Exception as e:
        st.error(f"Error generating SQL query: {str(e)}")
        return None

# Function to execute SQL query and return results
def execute_sql_query(sql_query):
    try:
        # Get database connection
        db_conn = get_database_connection()
        
        # Execute query
        result_df = pd.read_sql_query(sql_query, db_conn)
        return result_df, None
    except Exception as e:
        return None, str(e)

# Function to create visualization based on data
def create_visualization(df, question):
    try:
        # Determine the best visualization based on data structure and question
        if len(df) == 0:
            return None
            
        # If it's a time-based analysis
        if 'Minutes' in df.columns and len(df) > 1:
            if 'Color' in df.columns:
                # Time by line
                fig = px.box(df, x='Color', y='Minutes', title=f"Analysis: {question}")
                return fig
            else:
                # Time distribution
                fig = px.histogram(df, x='Minutes', title=f"Analysis: {question}")
                return fig
        
        # If it's a count analysis
        elif len(df.columns) == 2 and df.iloc[:, 1].dtype in ['int64', 'float64']:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=f"Analysis: {question}")
            return fig
        
        # If it's geographic data
        elif 'x' in df.columns and 'y' in df.columns:
            fig = px.scatter(df, x='x', y='y', title=f"Analysis: {question}")
            return fig
        
        # Default to table view
        return None
        
    except Exception as e:
        st.warning(f"Could not create visualization: {str(e)}")
        return None


# Example questions
st.markdown("**💡 Example Questions:**")
example_questions = [
    "Which line has the most stations?",
    "What is the average travel time for each line?",
    "Show me the top 5 stations with the most connections",
    "Which connection takes the longest time?",
    "How many stations are on the red line?",
    "What is the total travel time for all connections?",
    "Show me stations that serve multiple lines",
    "Which line has the fastest average travel time?"
]

# Display example questions as clickable buttons
cols = st.columns(2)
for i, question in enumerate(example_questions):
    with cols[i % 2]:
        if st.button(f"❓ {question}", key=f"example_{i}"):
            st.session_state.user_question = question

# User input
user_question = st.text_input(
    "Ask your question:",
    placeholder="e.g., Which line has the most stations?",
    key="user_question"
)

# Process the question
if user_question and st.button("🚀 Generate Analysis", type="primary"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar first!")
    else:
        with st.spinner("🤖 Generating SQL query..."):
            # Generate SQL query
            sql_query = generate_sql_query(user_question, openai_client)
            
            if sql_query:
                st.success("✅ SQL Query Generated!")
                
                # Display the generated SQL
                with st.expander("🔍 Generated SQL Query", expanded=True):
                    st.code(sql_query, language="sql")
                
                # Execute the query
                with st.spinner("📊 Executing query..."):
                    result_df, error = execute_sql_query(sql_query)
                
                if error:
                    st.error(f"❌ SQL Error: {error}")
                    st.info("💡 Tip: The AI might need to adjust the query. Try rephrasing your question.")
                elif result_df is not None:
                    st.success(f"✅ Query executed successfully! Found {len(result_df)} results.")
                    
                    # Display results
                    st.subheader("📋 Results")
                    
                    # Show data
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.dataframe(result_df, use_container_width=True)
                    
                    with col2:
                        st.markdown("**📊 Data Summary:**")
                        st.write(f"**Rows:** {len(result_df)}")
                        st.write(f"**Columns:** {len(result_df.columns)}")
                        if len(result_df) > 0:
                            st.write(f"**Memory Usage:** {result_df.memory_usage(deep=True).sum() / 1024:.2f} KB")
                    
                    # Create visualization
                    if len(result_df) > 0:
                        st.subheader("📈 Visualization")
                        fig = create_visualization(result_df, user_question)
                        
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("📊 Data displayed in table format above")
                    
                    # Add to chat history
                    chat_entry = {
                        "question": user_question,
                        "sql": sql_query,
                        "results": result_df,
                        "timestamp": pd.Timestamp.now()
                    }
                    st.session_state.chat_history.append(chat_entry)
                    
                else:
                    st.error("❌ Failed to execute query")

# Chat history
if st.session_state.chat_history:
    st.header("📚 Chat History")
    
    for i, entry in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"💬 {entry['question']} ({entry['timestamp'].strftime('%H:%M')})", expanded=False):
            st.markdown(f"**Question:** {entry['question']}")
            st.code(entry['sql'], language="sql")
            
            if len(entry['results']) > 0:
                st.dataframe(entry['results'], use_container_width=True)
                
                # Show summary stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Results", len(entry['results']))
                with col2:
                    st.metric("Columns", len(entry['results'].columns))

# Footer
st.markdown("---")

# Clear chat history button
if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun() 