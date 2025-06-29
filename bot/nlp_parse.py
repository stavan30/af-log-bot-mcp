import re
from datetime import datetime

def extract_filters_from_query(query: str):
    query = query.lower()
    filters = {}

    # Username extraction (match patterns like john.wick, harry.potter)
    user_match = re.search(r"(john\.wick|james\.bond|harry\.potter|tony\.stark|bruce\.wayne)", query)
    if user_match:
        filters["username"] = user_match.group()

    # Response code (match 3-digit numbers starting with 4 or 5)
    resp_match = re.search(r"\b(4\d{2}|5\d{2})\b", query)
    if resp_match:
        filters["resp_code"] = int(resp_match.group())

    # Keyword: pick a known word like "manifest", "helm", "docker"
    for keyword in ["manifest", "docker", "helm", "image", "token", "artifact"]:
        if keyword in query:
            filters["keyword"] = keyword
            break

    # Time window (match patterns like 'last 10 minutes')
    time_match = re.search(r"last (\d{1,3}) minute", query)
    if time_match:
        filters["last_n_minutes"] = int(time_match.group(1))
    else:
        filters["last_n_minutes"] = 10  # default fallback

    return filters
