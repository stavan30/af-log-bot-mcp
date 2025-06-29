import pandas as pd
from datetime import datetime, timedelta
from datetime import timezone
import os

# Path to the live CSV log file
LOG_FILE = "data/artifactory_logs_live.csv"

def search_logs(username=None, resp_code=None, keyword=None, last_n_minutes=10):
    if not os.path.exists(LOG_FILE):
        return []

    try:
        df = pd.read_csv(LOG_FILE)

        # Ensure timestamp column is datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Filter: only recent logs
        time_cutoff = datetime.now(timezone.utc) - timedelta(minutes=last_n_minutes)
        df = df[df["timestamp"] >= time_cutoff]

        # Optional filters
        if username:
            df = df[df["username"].str.lower() == username.lower()]
        if resp_code:
            if isinstance(resp_code, list):
                df = df[df["resp_code"].isin(resp_code)]
            else:
                df = df[df["resp_code"] == resp_code]            
        if keyword:
            keyword = keyword.lower()
            df = df[df.apply(lambda row: keyword in str(row.to_string()).lower(), axis=1)]

        # Convert to dict for return
        return df.to_dict(orient="records")

    except Exception as e:
        return [{"error": str(e)}]
