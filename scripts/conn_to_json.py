import pandas as pd
import sys
from pathlib import Path
from io import StringIO

def load_conn_log(path: Path) -> pd.DataFrame:
    """
    Load a Zeek conn.log file while preserving the #fields header.
    Zeek metadata lines (#separator, #types, etc.) are skipped.
    """
    with open(path, "r") as f:
        lines = f.readlines()

    # Extract the Zeek #fields header
    header = None
    for line in lines:
        if line.startswith("#fields"):
            header = line.strip().split()[1:]
            break

    if header is None:
        raise ValueError("No #fields header found in conn.log")

    # Keep only data rows (skip metadata)
    data_rows = [l for l in lines if not l.startswith("#")]

    # Parse using the extracted header
    df = pd.read_csv(
        StringIO("".join(data_rows)),
        sep="\t",
        names=header,
        engine="python"   # python engine required for StringIO
    )

    return df


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 conn_to_json.py <path/to/conn.log>")
        sys.exit(1)

    log_path = Path(sys.argv[1]).resolve()
    out_path = Path("data/generated/conn.json")

    df = load_conn_log(log_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(out_path, orient="records", lines=True)

    print(f"[SUCCESS] Wrote {out_path}")


if __name__ == "__main__":
    main()
