#! /bin/bash

# Check if number of arguments is correct.
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path to python scripts folder> <path to results folder>"
    exit 1
fi

# Loop over each sub folder in projects folder.
for dir in $2/*; do
    echo $dir
    python3 $1/methods.py $dir $dir/methods.csv
done

python3 $1/combine_methods.py $2 $2/../methods.csv
