#!/usr/bin/env python3
import os
import subprocess

print("\n=== DEMO STATUS CHECK ===\n")

# 1. Splunk status (demo-safe)
print("Checking Splunk status...")
print("Demo mode: Splunk status check skipped.\n")

# 2. Check Jupyter Lab status
print("Checking Jupyter Lab status...")
try:
    result = subprocess.run(
        ["pgrep", "-fl", "jupyter-lab"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print("Jupyter Lab is running:")
        print(result.stdout)
    else:
        print("Jupyter Lab is NOT running.")
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
