import time
import struct

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

def generate_and_discard_seeds(num_seeds=1000):
    start_time = time.time()
    for _ in range(num_seeds):
        seed = generate_entropy()
    end_time = time.time()
    total_time = end_time - start_time
    return total_time

# Generate and discard 1000 seeds, then calculate total time
total_time = generate_and_discard_seeds()
print(f"Total time to generate and discard 1000 seeds (simpler entropy): {total_time:.4f} seconds")

