import json
import os

data = {
    "timestamp": 1779318640.311286,
    "cpu": {
        "percent": 0
    },
    "memory": {
        "percent": 98.02
    },
    "disk": {
        "percent": 62
    }
}

os.makedirs(os.path.dirname("/Users/mrhardcore/KaliGhost/gui/frontend/dashboard_data.json"), exist_ok=True)
with open("/Users/mrhardcore/KaliGhost/gui/frontend/dashboard_data.json", "w") as f:
    json.dump(data, f)

print("Dashboard data updated successfully")