#!/bin/bash

# Variables
NUM_RUNS=50
NUM_STRINGS=200
TOTAL_CHI_SQUARED=0

# Loop to run the Python program 50 times
for ((i=1; i<=NUM_RUNS; i++))
do
    echo "Run $i of $NUM_RUNS"
    
    # Run the Python program and capture the chi-squared value
    OUTPUT=$(python3 program.py -n $NUM_STRINGS 2>&1 | grep "Chi-squared value")
    
    # Extract the chi-squared value from the output
    CHI_SQUARED=$(echo $OUTPUT | awk '{print $3}')
    
    # Add the chi-squared value to the total
    TOTAL_CHI_SQUARED=$(echo "$TOTAL_CHI_SQUARED + $CHI_SQUARED" | bc)
done

# Calculate the average chi-squared value
AVERAGE_CHI_SQUARED=$(echo "scale=2; $TOTAL_CHI_SQUARED / $NUM_RUNS" | bc)

# Print the average chi-squared value
echo "Average chi-squared value over $NUM_RUNS runs: $AVERAGE_CHI_SQUARED"

