#!/usr/bin/env python3
import pandas as pd
import sys
import os
import json

# ---------------------------------------------------------
# Resolve directories from environment (clean + Docker‑friendly)
# ---------------------------------------------------------
from pathlib import Path

# Determine project root dynamically (zeek_lab/)
LAB_ROOT = Path(__file__).resolve().parent.parent

# Output directory for generated JSON
GENERATED_DIR = LAB_ROOT / "data" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Zeek log safely (auto-detect headers, skip metadata)
# ---------------------------------------------------------
def load_zeek_log(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Log not found: {path}")

    fields = None
    with open(path, "r") as f:
        for line in f:
            if line.startswith("#fields"):
                fields = line.strip().split()[1:]
                break

    if fields is None:
        raise ValueError("No '#fields' header found — not a valid Zeek log.")

    df = pd.read_csv(
        path,
        sep="\t",
        comment="#",
        header=None,
        names=fields,
        engine="python",
        on_bad_lines="skip"
    )

    return df

# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 dns_to_json.py <dns.log>")
        sys.exit(1)

    log_path = sys.argv[1]

    # Derive output filename automatically
    base = os.path.splitext(os.path.basename(log_path))[0]
    out_path = os.path.join(GENERATED_DIR, f"{base}.json")

    df = load_zeek_log(log_path)

    # Write JSON‑lines (best for Splunk, jq, pandas)
    df.to_json(out_path, orient="records", lines=True)

    print(f"Saved JSON to {out_path}")

# ---------------------------------------------------------
# Run script
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
