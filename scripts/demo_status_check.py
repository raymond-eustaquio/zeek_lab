#!/usr/bin/env python3
import os
import subprocess

print("\n=== DEMO STATUS CHECK ===\n")

# ---------------------------------------------------------
# Resolve directories (Docker + host friendly)
# ---------------------------------------------------------
LAB_DIR = os.getenv("LAB_DIR", "/zeek_lab")
LOG_ROOT = os.getenv("LOG_ROOT", os.path.join(LAB_DIR, "logs"))
GENERATED_DIR = os.getenv("GENERATED_DIR", os.path.join(LAB_DIR, "data/generated"))
PCAP_DIR = os.getenv("PCAP_DIR", os.path.join(LAB_DIR, "pcaps"))
SCRIPTS_DIR = os.path.join(LAB_DIR, "scripts")
NOTEBOOKS_DIR = os.path.join(LAB_DIR, "notebooks")

# ---------------------------------------------------------
# 1. Splunk status (demo-safe)
# ---------------------------------------------------------
print("Checking Splunk status...")
print("Demo mode: Splunk status check skipped.\n")

# ---------------------------------------------------------
# 2. Check Jupyter Lab status
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 3. Check important project directories + files
# ---------------------------------------------------------
print("\nChecking project directories and files...\n")

checks = {
    "Lab root": LAB_DIR,
    "Scripts directory": SCRIPTS_DIR,
    "Notebooks directory": NOTEBOOKS_DIR,
    "PCAP directory": PCAP_DIR,
    "Logs root": LOG_ROOT,
    "Generated data directory": GENERATED_DIR,
}

for name, path in checks.items():
    exists = os.path.isdir(path)
    print(f"{name}: {'OK' if exists else 'MISSING'} ({path})")

# ---------------------------------------------------------
# 4. Check for at least one PCAP
# ---------------------------------------------------------
print("\nChecking for PCAP files...")
pcaps = [f for f in os.listdir(PCAP_DIR)] if os.path.isdir(PCAP_DIR) else []
if any(f.endswith(".pcap") for f in pcaps):
    print("PCAPs found.")
else:
    print("No PCAPs found in pcaps/ — demo may not run.")

# ---------------------------------------------------------
# 5. Check for logs
# ---------------------------------------------------------
print("\nChecking for Zeek logs...")
if os.path.isdir(LOG_ROOT) and any(os.listdir(LOG_ROOT)):
    print("Logs found in logs/.")
else:
    print("No logs found — run process_pcaps.sh first.")

# ---------------------------------------------------------
# 6. Check for generated JSON/PNG
# ---------------------------------------------------------
print("\nChecking generated data...")
if os.path.isdir(GENERATED_DIR) and any(os.listdir(GENERATED_DIR)):
    print("Generated data found in data/generated/.")
else:
    print("No generated data yet — run dns_to_json.py or dns_analysis.py.")

print("\nDemo environment check complete.\n")
