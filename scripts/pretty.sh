#!/usr/bin/env bash

set -e

# Allow override via environment variable
LOG_ROOT="${LOG_ROOT:-/zeek_lab/logs}"

LOGFILE="$1"

if [[ -z "$LOGFILE" ]]; then
    echo "Usage: $0 <zeek_log>"
    echo "Or set LOG_ROOT and run: LOG_ROOT=/zeek_lab/logs $0 logs_<pcap>/dns.log"
    exit 1
fi

# If user passed only a filename, prepend LOG_ROOT
if [[ ! -f "$LOGFILE" ]]; then
    if [[ -f "$LOG_ROOT/$LOGFILE" ]]; then
        LOGFILE="$LOG_ROOT/$LOGFILE"
    else
        echo "Error: Log file not found: $LOGFILE"
        exit 1
    fi
fi

echo "Pretty-printing: $LOGFILE"
echo

# Extract header fields
FIELDS=$(grep "^#fields" "$LOGFILE" | cut -f2-)
IFS=$'\t' read -r -a COLS <<< "$FIELDS"

# Print header row
for col in "${COLS[@]}"; do
    printf "%-30s" "$col"
done
printf "\n"

# Print separator
for col in "${COLS[@]}"; do
    printf "%-30s" "------------------------------"
done
printf "\n"

# Pretty-print rows using zeek-cut
zeek-cut -d -u < "$LOGFILE" | grep -v "^#" | while IFS=$'\t' read -r -a ROW; do
    for ((i=0; i<${#COLS[@]}; i++)); do
        printf "%-30s" "${ROW[i]}"
    done
    printf "\n"
done
