#!/bin/bash

for filename in $(find first/ -name '*.json'); do
	echo $filename
	stem=$(echo $filename | cut -f 1 -d '.')
	echo $stem
	python3 by_nl2code/data_processing/filter_docs.py $filename  $stem-filter.out
done

