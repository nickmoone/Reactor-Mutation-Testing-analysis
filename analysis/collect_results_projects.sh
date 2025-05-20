#! /bin/bash

# Check if number of arguments is correct.
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <path to python scripts folder> <path to projects folder> <path to results folder>"
    exit 1
fi

# Loop over each sub folder in projects folder.
for dir in $2/*; do
    echo $dir
    # Check if folder is a git repository.
    if [ -d "$dir/.git" ]; then
        python3 $1/collect.py $dir $3/results
    fi
done
