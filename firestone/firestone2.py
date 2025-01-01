import time
import os
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
    # Add process ID and system time
    entropy.extend(struct.pack('<I', os.getpid()))
    entropy.extend(struct.pack('<Q', time.perf_counter_ns()))
    # Truncate or pad to 16 bytes
    return bytes(entropy[:16])

# Generate 16 bytes of entropy
seed = generate_entropy(iterations=2)  # Adjust iterations as needed
print(f"Generated seed: {seed.hex()}")

