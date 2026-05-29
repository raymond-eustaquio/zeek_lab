#!/usr/bin/env python3
import os
import shutil

LAB_DIR = os.path.expanduser("~/zeek_lab")
LOG_DIR = os.path.join(LAB_DIR, "logs_college_dns_noise")
SCRIPT_DIR = os.path.join(LAB_DIR, "scripts")

def main():
    print("=== Resetting Zeek DNS Demo Lab ===")

    # Safety check
    if not os.path.isdir(LAB_DIR):
        print(f"Error: Lab directory not found at {LAB_DIR}")
        return

    # Remove PNG files
    print("Removing PNG files...")
    for f in os.listdir(SCRIPT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(SCRIPT_DIR, f))

    # Remove logs directory
    print("Removing logs directory...")
    if os.path.isdir(LOG_DIR):
        shutil.rmtree(LOG_DIR)

    print("Reset complete. Run process_pcaps.sh next.")

if __name__ == "__main__":
    main()
