import random
import time

def generate_seed():
    # Generate a 16-byte seed using Python's random module
    return bytes(random.getrandbits(8) for _ in range(16))

def generate_and_discard_seeds(num_seeds=1000):
    start_time = time.time()
    for _ in range(num_seeds):
        seed = generate_seed()
    end_time = time.time()
    total_time = end_time - start_time
    return total_time

# Generate and discard 1000 seeds, then calculate total time
total_time = generate_and_discard_seeds()
print(f"Total time to generate and discard 1000 seeds using Python's PRNG: {total_time:.4f} seconds")

