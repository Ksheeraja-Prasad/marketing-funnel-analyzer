import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Marketing Analytics Portfolio", layout="wide")

st.title("📊 Marketing Funnel & Root Cause Performance Tracker")
st.markdown("""
Welcome to my live data analytics portfolio. This application processes **10,000 synthetic marketing event logs** using a SQL database layer inside Python to analyze channel conversion performance and diagnose metric drop-offs.
""")

# Load data into SQLite
@st.cache_resource
def load_data():
    df = pd.read_csv('marketing_events.csv')
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    df.to_sql('events', conn, if_exists='replace', index=False)
    return conn

conn = load_data()

# Sidebar filter
st.sidebar.header("Filter Options")
selected_channel = st.sidebar.selectbox("Select Marketing Channel", ['All', 'Google Ads', 'Meta Ads', 'Organic Search', 'Email Referral'])

# Build dynamic query based on filter
where_clause = "" if selected_channel == 'All' else f"WHERE channel = '{selected_channel}'"

query = f"""
SELECT 
    funnel_stage,
    COUNT(DISTINCT user_id) as unique_users
FROM events
{where_clause}
GROUP BY funnel_stage
ORDER BY 
    CASE funnel_stage 
        WHEN 'click' THEN 1 
        WHEN 'visit' THEN 2 
        WHEN 'signup' THEN 3 
        WHEN 'booking' THEN 4 
    END;
"""

funnel_df = pd.read_sql_query(query, conn)

# Visualizing Key Metrics
st.subheader(f"Funnel Overview: {selected_channel}")
cols = st.columns(4)
stages = ['click', 'visit', 'signup', 'booking']

for idx, stage in enumerate(stages):
    val = funnel_df[funnel_df['funnel_stage'] == stage]['unique_users'].values
    count = val[0] if len(val) > 0 else 0
    cols[idx].metric(label=f"Total {stage.title()}s", value=f"{count:,}")

# Chart section
st.write("---")
st.subheader("Funnel Drop-off Visualization")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(funnel_df['funnel_stage'], funnel_df['unique_users'], color='#2b5c8f')
ax.set_ylabel("Unique Users")
ax.set_xlabel("Funnel Stage")
st.pyplot(fig)

# Show the underlying raw SQL code block so recruiters see your capability
st.write("---")
st.subheader("The SQL Logic Behind This View")
st.code(query, language='sql')