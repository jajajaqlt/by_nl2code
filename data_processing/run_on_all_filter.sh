#!/bin/bash

for filename in DATA*; do
    echo $filename
    python3 count_progs.py
done