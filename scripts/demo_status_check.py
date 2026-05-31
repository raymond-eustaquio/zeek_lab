#!/usr/bin/env python3
import os
import subprocess

print("\n=== DEMO STATUS CHECK ===\n")

# 1. Check Splunk status
print("Checking Splunk status...")
try:
    result = subprocess.run(
        ["sudo", "/opt/splunk/bin/splunk", "status"],
        capture_output=True, text=True
    )
    print(result.stdout)
except Exception as e:
    print(f"Error checking Splunk: {e}")

# 2. Check Jupyter Notebook status
print("\nChecking Jupyter Notebook status...")
try:
    result = subprocess.run(
        ["pgrep", "-fl", "jupyter-notebook"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print("Jupyter Notebook is running:")
        print(result.stdout)
    else:
        print("Jupyter Notebook is NOT running.")
except Exception as e:
    print(f"Error checking Jupyter: {e}")

# 3. Check important project files
print("\nChecking project files...")

BASE = os.path.dirname(os.path.abspath(__file__))

paths = {
    "dns.json": os.path.join(BASE, "dns.json"),
    "dns_analysis_demo.ipynb": os.path.join(BASE, "dns_analysis_demo.ipynb"),
    "Zeek logs directory": os.path.join(BASE, "../logs_college_dns_noise"),
    "PCAP file": os.path.join(BASE, "../college_dns_noise.pcap"),
}

for name, path in paths.items():
    exists = os.path.exists(path)
    print(f"{name}: {'OK' if exists else 'MISSING'} ({path})")

print("\nDemo environment check complete.\n")
