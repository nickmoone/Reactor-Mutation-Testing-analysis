#! /bin/bash

# Check if number of arguments is correct.
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <path to add_pitest.py> <path to projects folder> <path to plugin-snippet.xml>"
    exit 1
fi

# Loop over each sub folder in projects folder.
for dir in $2/*; do
    echo $dir
    # Check if folder is a git repository.
    if [ -d "$dir/.git" ]; then
        python3 $1 $dir $3
    fi
done
