#!/bin/bash
# This script watch for change in d2 file and generates the svg from it.
# usage: ./watch.sh arch

# Clean up d2 on exit
cleanup() {
    echo "Shutting down..."
    pkill -f "d2 --watch $file"
}
trap cleanup EXIT

file="$1"
d2 --watch "$file.d2" "${file%}.svg" -p 4002

wait
read -p "Press Enter to exit..."