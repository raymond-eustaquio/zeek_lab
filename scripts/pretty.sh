#!/usr/bin/env bash

LOGFILE="$1"

if [[ -z "$LOGFILE" ]]; then
    echo "Usage: $0 <zeek_log>"
    exit 1
fi

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

# Process log with zeek-cut (preserves tabs)
zeek-cut -d -U < "$LOGFILE" | grep -v "^#" | while IFS=$'\t' read -r -a ROW; do
    for ((i=0; i<${#COLS[@]}; i++)); do
        printf "%-30s" "${ROW[i]}"
    done
    printf "\n"
done
