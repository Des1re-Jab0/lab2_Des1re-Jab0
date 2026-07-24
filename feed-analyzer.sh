#!/bin/bash
# feed-analyzer.sh

INPUT="twitter_dataset.csv"

if [ ! -f "$INPUT" ]; then
    echo "Error: $INPUT not found in current directory."
    exit 1
fi

awk '
{
    line = line (line ? " " : "") $0
    n = gsub(/"/, "\"", line)
    if (n % 2 == 0) {
        print line
        line = ""
    }
}
' "$INPUT" \
  | tail -n +2 \
  | cut -d',' -f2 \
  | sort \
  | uniq -c \
  | sort -nr \
  | head -5

