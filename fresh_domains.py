import requests
import csv
from datetime import datetime, timedelta

# intervalo de tempo (últimas 48h)
since = (datetime.utcnow() - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%S")

url = "https://crt.sh/?q=%25&output=json"

response = requests.get(url, timeout=30)
data = response.json()

domains = set()

for entry in data:
    name = entry.get("name_value", "")
    if "." in name and not "*" in name:
        domains.add(name.lower())

domains = list(domains)[:500]  # MVP: 500 domínios

# salva CSV
filename = "fresh_domains.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["domain"])
    for d in domains:
        writer.writerow([d])

print(f"Saved {len(domains)} domains to {filename}")
