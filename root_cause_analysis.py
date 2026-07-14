import sqlite3
import pandas as pd

conn = sqlite3.connect('marketing_analysis.db')
df = pd.read_csv('marketing_events.csv')
df.to_sql('events', conn, if_exists='replace', index=False)

# SQL Query using Window Functions to calculate week-over-week changes
root_cause_query = """
WITH weekly_metrics AS (
    SELECT 
        -- Extract the week number from the timestamp
        strftime('%W', timestamp) as calendar_week,
        COUNT(DISTINCT CASE WHEN funnel_stage = 'signup' THEN user_id END) as signups,
        COUNT(DISTINCT CASE WHEN funnel_stage = 'booking' THEN user_id END) as bookings
    FROM events
    GROUP BY 1
),
conversion_rates AS (
    SELECT 
        calendar_week,
        signups,
        bookings,
        ROUND((CAST(bookings AS REAL) / signups) * 100, 2) as signup_to_booking_pct
    FROM weekly_metrics
)
SELECT 
    calendar_week,
    signups,
    signup_to_booking_pct,
    -- LAG fetches the conversion rate from the previous row (previous week)
    LAG(signup_to_booking_pct, 1) OVER (ORDER BY calendar_week) as prev_week_pct,
    -- Calculate the absolute drop/gain week-over-week
    ROUND(signup_to_booking_pct - LAG(signup_to_booking_pct, 1) OVER (ORDER BY calendar_week), 2) as wow_change
FROM conversion_rates;
"""

analysis_results = pd.read_sql_query(root_cause_query, conn)
print("\n--- WEEK-OVER-WEEK FUNNEL DIAGNOSTICS ---")
print(analysis_results.to_markdown(index=False))

conn.close()