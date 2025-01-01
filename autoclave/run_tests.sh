#!/bin/bash

# Measure time for 100 entropy runs
echo "Running 100 entropy tests..."
start_time=$(date +%s.%N)
for i in {1..100}
do
    python3 finish.py --entropy > /dev/null
done
end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "Entropy tests completed in $elapsed_time seconds"

# Measure time for 100 PRNG runs
echo "Running 100 PRNG tests..."
start_time=$(date +%s.%N)
for i in {1..100}
do
    python3 finish.py --prng > /dev/null
done
end_time=$(date +%s.%N)
elapsed_time=$(echo "$end_time - $start_time" | bc)
echo "PRNG tests completed in $elapsed_time seconds"
