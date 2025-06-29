import csv
import random
import time
from datetime import datetime, timezone
import os

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Log file path
log_file = "data/artifactory_logs_live.csv"

# Fieldnames for the CSV
fieldnames = [
    "timestamp", "username", "req_method", "resp_code", "artifact", "host",
    "client_ip", "user_agent", "repo", "action", "status", "latency_ms"
]

# Sample data to randomize entries
usernames = ["john.wick", "james.bond", "harry.potter", "tony.stark", "bruce.wayne"]
methods = ["GET", "POST", "PUT", "DELETE"]
resp_codes = [200, 201, 204, 301, 400, 401, 403, 404, 500, 502]
artifacts = [
    "ml/ocr-kamino-jobs/0.10.0-2862adb/manifest.json",
    "docker/hello-world/1.0.0/image.tar",
    "libs-release-local/com/example/lib/1.2.3/lib.jar",
    "helm/monitoring-stack/3.5.2/index.yaml"
]
hosts = ["af_1server.com", "af_2server.com", "af_backup.com"]
ips = ["192.168.1.34", "10.0.0.12", "172.16.5.4", "192.168.42.101"]
user_agents = ["curl/7.79.1", "jfrog-cli/2.34.1", "wget/1.21.1", "python-requests/2.25.1"]
repos = ["docker-local", "libs-release", "helm-prod", "ml-models"]
actions = ["pull", "push", "promote", "delete", "search"]
statuses = ["success", "failed", "unauthorized", "not_found"]

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

# Function to generate a random log entry
def generate_log_entry():
    timestamp = datetime.now(timezone.utc).isoformat()
    username = random.choice(usernames)
    req_method = random.choice(methods)
    resp_code = random.choice(resp_codes)
    artifact = random.choice(artifacts)
    host = random.choice(hosts)
    client_ip = random.choice(ips)
    user_agent = random.choice(user_agents)
    repo = random.choice(repos)
    action = random.choice(actions)
    status = "success" if resp_code < 400 else random.choice(["failed", "unauthorized", "not_found"])
    latency_ms = random.randint(10, 5000)

    return {
        "timestamp": timestamp,
        "username": username,
        "req_method": req_method,
        "resp_code": resp_code,
        "artifact": artifact,
        "host": host,
        "client_ip": client_ip,
        "user_agent": user_agent,
        "repo": repo,
        "action": action,
        "status": status,
        "latency_ms": latency_ms
    }

# Start appending log entries every 5 seconds
print("🔁 Log simulator started. Writing logs every 5 seconds...")
while True:
    with open(log_file, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(generate_log_entry())
    time.sleep(5)
