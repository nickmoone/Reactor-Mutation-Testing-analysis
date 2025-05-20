#! /bin/bash

# Check if number of arguments is correct.
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path to file containing list of projects> <path to folder to store projects>"
    exit 1
fi

cd $2

while read line; do
    repo="https://$line.git"
    git clone $repo
done < $1
