#!/bin/bash
# organizer.sh - archives grades.csv with a timestamp and logs the action

if [ ! -f grades.csv ]; then
    echo "Error: grades.csv was not found in $(pwd)."
    exit 1
fi

if [ ! -d archive ]; then
    if ! mkdir archive; then
        echo "Error: could not create the archive directory."
        exit 1
    fi
    echo "Created the archive directory."
fi

timestamp=$(date +%Y%m%d-%H%M%S)
archived_name="grades_${timestamp}.csv"

if ! mv grades.csv "archive/$archived_name"; then
    echo "Error: could not move grades.csv into the archive directory."
    exit 1
fi
touch grades.csv

echo "$timestamp | original: grades.csv | archived: archive/$archived_name" >> organizer.log
echo "Archived grades.csv as archive/$archived_name and created a fresh grades.csv."
