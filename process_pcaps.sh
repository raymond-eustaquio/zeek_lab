#!/bin/bash

# Batch Zeek PCAP Processor
# Processes every .pcap inside $PCAP_DIR and writes logs to $LOG_ROOT

set -e
shopt -s nullglob

# Directories (override via environment variables if needed)
PCAP_DIR="${PCAP_DIR:-$(pwd)/pcaps}"
LOG_ROOT="${LOG_ROOT:-$(pwd)/logs}"

mkdir -p "$LOG_ROOT"

echo "Using PCAP_DIR: $PCAP_DIR"
echo "Using LOG_ROOT: $LOG_ROOT"
echo

for pcap in "$PCAP_DIR"/*.pcap; do
    base="$(basename "$pcap" .pcap)"
    outdir="$LOG_ROOT/logs_${base}"

    echo "Processing $pcap → $outdir"
    mkdir -p "$outdir"

    zeek -C -r "$pcap" Log::default_logdir="$outdir"
done

echo
echo "All PCAPs processed."
