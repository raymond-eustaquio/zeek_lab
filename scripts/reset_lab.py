#!/usr/bin/env python3
import os
import shutil

# Resolve directories from environment (Docker + host friendly)
LAB_DIR = os.getenv("LAB_DIR", "/home/raymo/zeek_lab")
LOG_ROOT = os.getenv("LOG_ROOT", os.path.join(LAB_DIR, "logs"))
GENERATED_DIR = os.getenv("GENERATED_DIR", os.path.join(LAB_DIR, "data/generated"))
IMAGES_DIR = os.path.join(LAB_DIR, "images")

def safe_rmtree(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Removed: {path}")
    else:
        print(f"Skipped (not found): {path}")

def safe_remove_pngs(path):
    if not os.path.isdir(path):
        print(f"Skipped PNG cleanup (directory not found): {path}")
        return

    removed = 0
    for f in os.listdir(path):
        if f.endswith(".png"):
            os.remove(os.path.join(path, f))
            removed += 1

    print(f"Removed {removed} PNG files from {path}")

def main():
    print("=== Resetting Zeek Lab Environment ===")

    print(f"LAB_DIR:        {LAB_DIR}")
    print(f"LOG_ROOT:       {LOG_ROOT}")
    print(f"GENERATED_DIR:  {GENERATED_DIR}")
    print(f"IMAGES_DIR:     {IMAGES_DIR}")
    print()

    # 1. Remove all logs
    print("Cleaning logs...")
    safe_rmtree(LOG_ROOT)
    os.makedirs(LOG_ROOT, exist_ok=True)

    # 2. Remove generated JSON + PNGs
    print("Cleaning generated data...")
    safe_rmtree(GENERATED_DIR)
    os.makedirs(GENERATED_DIR, exist_ok=True)

    # 3. Remove PNGs from images/
    print("Cleaning PNGs in images/ ...")
    safe_remove_pngs(IMAGES_DIR)

    print("\nReset complete.")
    print("Next step: run process_pcaps.sh to regenerate logs.")

if __name__ == "__main__":
    main()
