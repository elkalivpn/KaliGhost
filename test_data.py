import json
import os

data = {
    "timestamp": 1779295891.155061,
    "cpu": {
        "percent": 0
    },
    "memory": {
        "percent": 98.09
    },
    "disk": {
        "percent": 63
    }
}

print(json.dumps(data))