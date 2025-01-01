import hashlib
import time
import struct

def generate_entropy(iterations=1000):
    entropy = bytearray()
    for _ in range(iterations):
        start = time.perf_counter_ns()
        # Perform a computationally expensive operation
        result = sum(i * i for i in range(1000))
        end = time.perf_counter_ns()
        # Append the timing difference to the entropy pool
        entropy.extend(struct.pack('<Q', end - start))
    # Hash the entropy to ensure uniform distribution
    return hashlib.sha256(entropy).digest()[:16]

def generate_and_discard_seeds(num_seeds=100):
    start_time = time.time()
    for _ in range(num_seeds):
        seed = generate_entropy()
    end_time = time.time()
    total_time = end_time - start_time
    return total_time

# Generate and discard 1000 seeds, then calculate total time
total_time = generate_and_discard_seeds()
print(f"Total time to generate and discard 1000 seeds: {total_time:.4f} seconds")

