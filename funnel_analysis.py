import sqlite3
import pandas as pd

# Step A: Connect to a temporary, virtual SQL database in memory
conn = sqlite3.connect('marketing_analysis.db')

# Step B: Load our CSV dataset into a SQL table named "events"
df = pd.read_csv('marketing_events.csv')
df.to_sql('events', conn, if_exists='replace', index=False)

# Step C: Write the SQL query to calculate funnel metrics
sql_query = """
WITH stage_counts AS (
    -- This CTE counts the unique users at each stage of the funnel, grouped by marketing channel
    SELECT 
        channel,
        COUNT(DISTINCT CASE WHEN funnel_stage = 'click' THEN user_id END) as total_clicks,
        COUNT(DISTINCT CASE WHEN funnel_stage = 'visit' THEN user_id END) as total_visits,
        COUNT(DISTINCT CASE WHEN funnel_stage = 'signup' THEN user_id END) as total_signups,
        COUNT(DISTINCT CASE WHEN funnel_stage = 'booking' THEN user_id END) as total_bookings
    FROM events
    GROUP BY channel
)
SELECT 
    channel,
    total_clicks,
    total_visits,
    -- Calculate click-to-visit conversion rate
    ROUND((CAST(total_visits AS REAL) / total_clicks) * 100, 2) as click_to_visit_pct,
    total_signups,
    -- Calculate visit-to-signup conversion rate
    ROUND((CAST(total_signups AS REAL) / total_visits) * 100, 2) as visit_to_signup_pct,
    total_bookings,
    -- Calculate signup-to-booking conversion rate
    ROUND((CAST(total_bookings AS REAL) / total_signups) * 100, 2) as signup_to_booking_pct
FROM stage_counts;
"""

# Step D: Run the SQL query and print the result as a clean text table
analysis_results = pd.read_sql_query(sql_query, conn)
print("\n--- MARKETING FUNNEL PERFORMANCE BY CHANNEL ---")
print(analysis_results.to_markdown(index=False))

# Step E: Close the database connection
conn.close()