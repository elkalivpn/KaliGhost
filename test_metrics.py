import json
import sys
import os

# Change to the correct directory
os.chdir('/Users/mrhardcore/KaliGhost')

try:
    # Read the dashboard data file
    with open('gui/frontend/dashboard_data.json', 'r') as f:
        data = json.load(f)

    # Extract metrics
    cpu_percent = data['cpu']['percent']
    memory_percent = data['memory']['percent']
    disk_percent = data['disk']['percent']

    # Print metrics
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_percent}%")
    print(f"Disk Usage: {disk_percent}%")

    # Check for alerts based on thresholds
    alert_threshold_cpu = 80
    alert_threshold_memory = 85
    alert_threshold_disk = 90

    alerts = []

    if cpu_percent > alert_threshold_cpu:
        alerts.append(f"High CPU usage: {cpu_percent}%")

    if memory_percent > alert_threshold_memory:
        alerts.append(f"High Memory usage: {memory_percent}%")

    if disk_percent > alert_threshold_disk:
        alerts.append(f"High Disk usage: {disk_percent}%")

    if alerts:
        print("\nALERTS:")
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("\nAll system metrics are within normal thresholds.")
        
except FileNotFoundError:
    print("Error: dashboard_data.json file not found")
    sys.exit(1)
except Exception as e:
    print(f"Error reading metrics: {str(e)}")
    sys.exit(1)