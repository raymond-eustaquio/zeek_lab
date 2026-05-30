#!/bin/bash

# Batch Zeek PCAP Processor
# Processes every .pcap in the current directory

shopt -s nullglob

for pcap in *.pcap; do
    base="${pcap%.pcap}"
    outdir="logs_${base}"

    echo "Processing $pcap → $outdir"

    mkdir -p "$outdir"

    zeek -C -r "$pcap" Log::default_logdir="$outdir"
done

echo "All PCAPs processed."
