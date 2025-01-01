import time
import struct
import argparse
import random
import string

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

def main():
    parser = argparse.ArgumentParser(description="Generate random alphanumeric strings.")
    parser.add_argument('-n', '--num_strings', type=int, required=True, help="Number of strings to generate")
    args = parser.parse_args()
    
    strings = generate_strings(args.num_strings)
    for s in strings:
        print(s)

if __name__ == "__main__":
    main()

