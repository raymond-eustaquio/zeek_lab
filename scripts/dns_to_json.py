#!/usr/bin/env python3
import pandas as pd
import sys
import os

def load_zeek_log(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Log not found: {path}")

    # Extract Zeek header
    fields = None
    with open(path, "r") as f:
        for line in f:
            if line.startswith("#fields"):
                fields = line.strip().split()[1:]
                break

    if fields is None:
        raise ValueError("No '#fields' header found — not a valid Zeek log.")

    # Load TSV data, skipping metadata lines
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

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 dns_to_json.py <dns.log> <output.json>")
        sys.exit(1)

    log_path = sys.argv[1]
    out_path = sys.argv[2]

    df = load_zeek_log(log_path)

    # Write JSON‑lines (best for Splunk, jq, pandas)
    df.to_json(out_path, orient="records", lines=True)

    print(f"Saved JSON to {out_path}")

if __name__ == "__main__":
    main()
