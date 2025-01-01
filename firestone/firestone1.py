import time
import struct

def generate_entropy(iterations=1000):
    entropy = 0
    for _ in range(iterations):
        start = time.perf_counter_ns()
        # Perform a computationally expensive operation
        result = sum(i * i for i in range(1000))
        end = time.perf_counter_ns()
        # XOR the timing difference into the entropy pool
        entropy ^= (end - start)
    # Convert the entropy to bytes
    return entropy.to_bytes(8, byteorder='little')

# Generate 16 bytes of entropy
seed = generate_entropy(iterations=2)  # Adjust iterations as needed
print(f"Generated seed: {seed.hex()}")

