#! /bin/bash

# Check if number of arguments is correct.
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path to projects folder> <path to folder with log files>"
    exit 1
fi

# Loop over each sub folder in projects folder.
for dir in $1/*; do
    echo $dir
    # Check if folder is a git repository.
    if [ -d "$dir/.git" ]; then
        cd $dir
        mvn test-compile org.pitest:pitest-maven:mutationCoverage > $2/$(basename $dir).log
        cd ..
    fi
done
