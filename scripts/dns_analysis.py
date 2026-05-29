import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# ---------------------------------------------------------
# Load Zeek DNS log safely (auto-detect headers, skip metadata)
# ---------------------------------------------------------
def load_dns_log(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"DNS log not found: {path}")

    # Extract Zeek header from "#fields" line
    fields = None
    with open(path, "r") as f:
        for line in f:
            if line.startswith("#fields"):
                fields = line.strip().split()[1:]
                break

    if fields is None:
        raise ValueError("No '#fields' header found. This is not a valid Zeek log.")

    # Load data (skip Zeek metadata lines)
    df = pd.read_csv(
        path,
        sep="\t",
        comment="#",
        header=None,
        names=fields,
        engine="python",
        on_bad_lines="skip"
    )

    # Validate timestamp column
    if "ts" not in df.columns:
        raise ValueError("Zeek DNS log missing 'ts' column. File may be truncated or corrupted.")

    # Convert timestamp
    df["ts"] = pd.to_datetime(df["ts"], unit="s", errors="coerce")
    df = df.dropna(subset=["ts"])

    return df


# ---------------------------------------------------------
# Plot top DNS queries (best for demo)
# ---------------------------------------------------------
def plot_top_domains(df, output="dns_top_domains.png"):
    if "query" not in df.columns:
        print("No 'query' field found — cannot plot top domains.")
        return

    top = df["query"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    top.plot(kind="bar", color="steelblue")
    plt.title("Top DNS Queries")
    plt.xlabel("Domain")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output)
    print(f"Saved chart to {output}")


# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 dns_analysis.py <dns.log>")
        sys.exit(1)

    dnslog = sys.argv[1]

    # Load Zeek DNS log
    df = load_dns_log(dnslog)

    print("Loaded DNS log with columns:")
    print(df.columns.tolist())
    print(f"Total rows: {len(df)}")

    # Print top DNS queries
    if "query" in df.columns:
        print("\nTop DNS queries:")
        print(df["query"].value_counts().head(10))
    else:
        print("No 'query' field found in DNS log.")

    # Generate bar chart for demo
    plot_top_domains(df)


# ---------------------------------------------------------
# Run script
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
