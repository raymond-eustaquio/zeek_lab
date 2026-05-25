#!/bin/bash

dir=$1

if [ -z "$dir" ]; then
    echo "Usage: ./pretty_all.sh <log_directory>"
    exit 1
fi

for log in $dir/*.log; do
    echo "==================== $log ===================="
    ( sed -n 's/^#fields //p' "$log" ; zeek-cut < "$log" ) | column -t -s $'\t'
    echo
done