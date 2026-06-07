#!/bin/bash

# Pretty-print ALL Zeek logs in a directory
# Uses environment variables for clean Docker + host usage

set -e

# Allow override via environment variable
LOG_ROOT="${LOG_ROOT:-/zeek_lab/logs}"

DIR="${1:-$LOG_ROOT}"

if [ ! -d "$DIR" ]; then
    echo "Error: Directory not found: $DIR"
    echo "Usage: ./pretty_all.sh <log_directory>"
    exit 1
fi

shopt -s nullglob

for log in "$DIR"/*.log; do
    echo "==================== $log ===================="
    
    (
        # Print header from #fields
        sed -n 's/^#fields //p' "$log"

        # Print aligned rows
        zeek-cut < "$log"
    ) | column -t -s $'\t'

    echo
done

echo "Pretty-print complete."
