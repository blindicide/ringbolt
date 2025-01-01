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
    # Generate a random string of 16 alphanumeric characters
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def generate_strings(num_strings):
    strings = []
    for _ in range(num_strings):
        seed = generate_entropy()
        random.seed(seed)
        random_string = generate_random_string()
        strings.append(random_string)
    return strings

def chi_squared_test(strings):
    # Flatten the list of strings into a single list of characters
    chars = [char for s in strings for char in s]
    
    # Count the frequency of each character
    observed_freq = collections.Counter(chars)
    
    # Expected frequency is uniform (each character should appear equally)
    total_chars = len(chars)
    expected_freq = total_chars / len(string.ascii_letters + string.digits)
    
    # Calculate the chi-squared statistic
    chi_squared = 0
    for char in string.ascii_letters + string.digits:
        observed = observed_freq.get(char, 0)
        chi_squared += (observed - expected_freq) ** 2 / expected_freq
    
    # Degrees of freedom is the number of categories minus 1
    degrees_of_freedom = len(string.ascii_letters + string.digits) - 1
    
    # You can compare the chi-squared value to a critical value or use a p-value
    # For simplicity, we'll just return the chi-squared value and degrees of freedom
    return chi_squared, degrees_of_freedom

def main():
    parser = argparse.ArgumentParser(description="Generate random alphanumeric strings and test their randomness.")
    parser.add_argument('-n', '--num_strings', type=int, required=True, help="Number of strings to generate")
    args = parser.parse_args()
    
    strings = generate_strings(args.num_strings)
    for s in strings:
        print(s)
    
    chi_squared, dof = chi_squared_test(strings)
    print(f"Chi-squared value: {chi_squared}")
    print(f"Degrees of freedom: {dof}")

if __name__ == "__main__":
    main()

