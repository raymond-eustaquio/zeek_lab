#!/usr/bin/env python3
import pandas as pd
import json
from pathlib import Path
from io import StringIO

# -----------------------------
# Correct Zeek conn.log loader
# -----------------------------
def load_conn_log(path):
    with open(path, "r") as f:
        lines = f.readlines()

    # Extract Zeek #fields header
    header_line = None
    for line in lines:
        if line.startswith("#fields"):
            header_line = line.strip().split()[1:]
            break

    if header_line is None:
        raise ValueError("No #fields header found in conn.log")

    # Keep only data rows
    data = [l for l in lines if not l.startswith("#")]

    # Parse with correct header
    df = pd.read_csv(
        StringIO("".join(data)),
        sep="\t",
        names=header_line,
        engine="python"
    )

    return df


# -----------------------------
# Analysis functions
# -----------------------------
def save_json(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def analyze_tcp(df):
    required = ["id.orig_h", "id.resp_h", "id.resp_p"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        print(f"[WARN] Missing required TCP fields: {missing}")
        print("[WARN] Skipping full TCP analysis.")
        return {}

    # Filter TCP rows
    tcp = df[df["proto"] == "tcp"].copy()

    if tcp.empty:
        print("[WARN] No TCP rows found.")
        return {}

    # -----------------------------
    # Clean numeric fields
    # -----------------------------
    numeric_cols = [
        "id.resp_p", "id.orig_p",
        "orig_bytes", "resp_bytes",
        "duration", "missed_bytes",
        "orig_pkts", "resp_pkts"
    ]

    for col in numeric_cols:
        if col in tcp.columns:
            tcp[col] = pd.to_numeric(tcp[col], errors="coerce").fillna(0)

    results = {}

    # Top talkers
    results["top_talkers"] = (
        tcp["id.orig_h"].value_counts().head(20).to_dict()
    )

    # Top destinations
    results["top_destinations"] = (
        tcp["id.resp_h"].value_counts().head(20).to_dict()
    )

    # Port distribution
    results["port_distribution"] = (
        tcp["id.resp_p"].value_counts().head(20).to_dict()
    )

    # Connection states
    results["conn_states"] = (
        tcp["conn_state"].value_counts().to_dict()
    )

    # Elephant flows (large byte count)
    if "orig_bytes" in tcp.columns and "resp_bytes" in tcp.columns:
        tcp["total_bytes"] = tcp["orig_bytes"] + tcp["resp_bytes"]
        results["elephant_flows"] = (
            tcp.sort_values("total_bytes", ascending=False)
            .head(20)[["id.orig_h", "id.resp_h", "id.resp_p", "total_bytes"]]
            .to_dict(orient="records")
        )

    # Long-lived flows
    if "duration" in tcp.columns:
        results["long_lived"] = (
            tcp.sort_values("duration", ascending=False)
            .head(20)[["id.orig_h", "id.resp_h", "id.resp_p", "duration"]]
            .to_dict(orient="records")
        )

    return results


# -----------------------------
# Main
# -----------------------------
def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 conn_analysis.py <conn.log>")
        sys.exit(1)

    conn_path = Path(sys.argv[1]).resolve()
    print(f"[INFO] Loading conn.log from: {conn_path}")

    df = load_conn_log(conn_path)

    # Convert Zeek "-" placeholders to numeric zero
    df = df.replace("-", 0)

    results = analyze_tcp(df)

    outdir = Path("data/analysis")
    outdir.mkdir(parents=True, exist_ok=True)

    save_json(results, outdir / "conn_analysis.json")

    print("[INFO] Analysis complete.")
    print(f"[INFO] Wrote: {outdir}/conn_analysis.json")


if __name__ == "__main__":
    main()
