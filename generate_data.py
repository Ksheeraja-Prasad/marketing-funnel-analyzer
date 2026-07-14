import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# This "seed" ensures that the random data generated is the same every time you run it
np.random.seed(42)

# We want to generate 10,000 mock user interactions
n_rows = 10000

# 1. Create a list of mock User IDs (ranging from USER_1000 to USER_3500)
user_ids = [f"USER_{1000 + i}" for i in np.random.randint(1, 2500, n_rows)]

# 2. Assign marketing channels using realistic probabilities
# (e.g., Google Ads brings in 40% of traffic, Email Referral brings in 10%)
channels = np.random.choice(
    ['Google Ads', 'Meta Ads', 'Organic Search', 'Email Referral'], 
    n_rows, 
    p=[0.4, 0.3, 0.2, 0.1]
)

# 3. Assign funnel stages
# To make it realistic, we expect more "clicks" and "visits" than actual "bookings"
stages = np.random.choice(
    ['click', 'visit', 'signup', 'booking'], 
    n_rows, 
    p=[0.5, 0.3, 0.15, 0.05]
)

# 4. Generate timestamps spanning a 90-day period in early 2026
start_date = datetime(2026, 1, 1)
date_list = [
    start_date + timedelta(
        days=int(np.random.randint(0, 90)), 
        hours=int(np.random.randint(0, 24)),
        minutes=int(np.random.randint(0, 60))
    ) 
    for _ in range(n_rows)
]

# 5. Combine everything into a structured table (Pandas DataFrame)
df = pd.DataFrame({
    'user_id': user_ids,
    'timestamp': date_list,
    'channel': channels,
    'funnel_stage': stages
})

# Sort chronologically so the event sequence makes sense
df = df.sort_values('timestamp').reset_index(drop=True)

# Save the generated table as a CSV file
df.to_csv('marketing_events.csv', index=False)
print("Success! Created 'marketing_events.csv' with 10,000 rows.")