import json
import os

data_path = os.path.expanduser('~/KaliGhost/gui/frontend/dashboard_data.json')
with open(data_path, 'r') as f:
    data = json.load(f)

print(json.dumps(data))