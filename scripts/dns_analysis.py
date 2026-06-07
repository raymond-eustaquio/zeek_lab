import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import json

# ---------------------------------------------------------
# Resolve directories from environment (clean + Docker‑friendly)
# ---------------------------------------------------------
LOG_ROOT = os.getenv("LOG_ROOT", "/zeek_lab/logs")
GENERATED_DIR = os.getenv("GENERATED_DIR", "/zeek_lab/data/generated")

os.makedirs(GENERATED_DIR, exist_ok=True)

# ---------------------------------------------------------
# Load Zeek DNS log safely (auto-detect headers, skip metadata)
# ---------------------------------------------------------
def load_dns_log(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"DNS log not found: {path}")

    fields = None
    with open(path, "r") as f:
        for line in f:
            if line.startswith("#fields"):
                fields = line.strip().split()[1:]
                break

    if fields is None:
        raise ValueError("No '#fields' header found. This is not a valid Zeek log.")

    df = pd.read_csv(
        path,
        sep="\t",
        comment="#",
        header=None,
        names=fields,
        engine="python",
        on_bad_lines="skip"
    )

    if "ts" not in df.columns:
        raise ValueError("Zeek DNS log missing 'ts' column. File may be truncated or corrupted.")

    df["ts"] = pd.to_datetime(df["ts"], unit="s", errors="coerce")
    df = df.dropna(subset=["ts"])

    return df

# ---------------------------------------------------------
# Plot top DNS queries (saved into data/generated/)
# ---------------------------------------------------------
def plot_top_domains(df, basename):
    if "query" not in df.columns:
        print("No 'query' field found — cannot plot top domains.")
        return

    top = df["query"].value_counts().head(10)

    output_path = os.path.join(GENERATED_DIR, f"{basename}_top_domains.png")

    plt.figure(figsize=(10, 6))
    top.plot(kind="bar", color="steelblue")
    plt.title("Top DNS Queries")
    plt.xlabel("Domain")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)

    print(f"Saved chart to {output_path}")

# ---------------------------------------------------------
# Save summary JSON (saved into data/generated/)
# ---------------------------------------------------------
def save_summary_json(df, basename):
    summary = {
        "total_rows": len(df),
        "top_queries": df["query"].value_counts().head(10).to_dict()
        if "query" in df.columns else {}
    }

    output_path = os.path.join(GENERATED_DIR, f"{basename}_summary.json")

    with open(output_path, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"Saved summary JSON to {output_path}")

# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 dns_analysis.py <dns.log>")
        sys.exit(1)

    dnslog = sys.argv[1]
    basename = os.path.splitext(os.path.basename(dnslog))[0]

    df = load_dns_log(dnslog)

    print("Loaded DNS log with columns:")
    print(df.columns.tolist())
    print(f"Total rows: {len(df)}")

    if "query" in df.columns:
        print("\nTop DNS queries:")
        print(df["query"].value_counts().head(10))
    else:
        print("No 'query' field found in DNS log.")

    plot_top_domains(df, basename)
    save_summary_json(df, basename)

# ---------------------------------------------------------
# Run script
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
