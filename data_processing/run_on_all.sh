#!/bin/bash

for filename in DATA*; do
    echo $filename
    stem=$(echo $filename | cut -f 1 -d '.')
    python3 filter_docs.py $filename $stem-filter.json
done
