import time
import struct
import argparse
import random
import string
import collections

def generate_entropy(iterations=100):
    entropy = bytearray()
    for _ in range(iterations):
        start = time.perf_counter_ns()
        # Perform a small, randomized operation
        result = sum(i * i for i in range(10))  # Much smaller range
        end = time.perf_counter_ns()
        # Append the timing difference to the entropy pool
        entropy.extend(struct.pack('<Q', end - start))
    # Process entropy to remove trailing zeroes and ensure uniformity
    processed_entropy = bytearray()
    for byte in entropy:
        if byte != 0:  # Skip trailing zeroes
            processed_entropy.append(byte)
    # If the processed entropy is shorter than 16 bytes, pad it with non-zero values
    while len(processed_entropy) < 16:
        processed_entropy.append(1)  # Pad with 1 (non-zero)
    # Truncate to 16 bytes
    return bytes(processed_entropy[:16])

def generate_random_string():
    # Generate a random string of 16 numeric characters
    return ''.join(random.choices(string.digits, k=16))

def generate_strings(num_strings):
    strings = []
    for _ in range(num_strings):
        seed = generate_entropy()
        random.seed(seed)
        random_string = generate_random_string()
        strings.append(random_string)
    return strings

def monte_carlo_test(strings):
    # Convert numeric strings to points in [0,1) x [0,1)
    points = []
    for s in strings:
        # Convert first 8 digits to x, next 8 to y
        x = int(s[:8]) / 10**8
        y = int(s[8:16]) / 10**8
        points.append((x, y))
    
    # Count points inside unit circle
    inside = sum(1 for x, y in points if x*x + y*y <= 1)
    total = len(points)
    
    # Estimate π
    pi_estimate = 4 * inside / total
    
    # Calculate error from actual π
    error = abs(pi_estimate - 3.141592653589793)
    
    return pi_estimate, error

def main():
    parser = argparse.ArgumentParser(description="Test randomness using Monte Carlo π estimation.")
    args = parser.parse_args()
    
    total_runs = 50
    attempts_per_run = 50
    total_error = 0
    
    for run in range(total_runs):
        strings = generate_strings(attempts_per_run)
        _, error = monte_carlo_test(strings)
        total_error += error
    
    average_error = total_error / total_runs
    print(f"Average error across {total_runs} runs: {average_error}")

if __name__ == "__main__":
    main()
