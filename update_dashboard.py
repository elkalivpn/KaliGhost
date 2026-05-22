import json
import os

data = {
    "timestamp": 1779446473.821841,
    "cpu": {
        "percent": 0
    },
    "memory": {
        "percent": 97.99
    },
    "disk": {
        "percent": 52
    }
}

filepath = os.path.expanduser("~/KaliGhost/gui/frontend/dashboard_data.json")
os.makedirs(os.path.dirname(filepath), exist_ok=True)

with open(filepath, 'w') as f:
    json.dump(data, f)

print(f"Dashboard data updated at {filepath}")