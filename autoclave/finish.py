import struct
import time
import random
import string
import argparse

def rotate_left(v, n):
    w = (v << n) | (v >> (32 - n))
    return w & 0xFFFFFFFF

def quarter_round(a, b, c, d):
    a = (a + b) & 0xFFFFFFFF
    d ^= a
    d = rotate_left(d, 16)
    c = (c + d) & 0xFFFFFFFF
    b ^= c
    b = rotate_left(b, 12)
    a = (a + b) & 0xFFFFFFFF
    d ^= a
    d = rotate_left(d, 8)
    c = (c + d) & 0xFFFFFFFF
    b ^= c
    b = rotate_left(b, 7)
    return a, b, c, d

def chacha_block(key, counter, nonce):
    state = [0] * 16
    state[0:4] = [0x61707865, 0x3120646e, 0x79622d32, 0x6b206574]  # "expand 32-byte k"
    state[4:12] = list(struct.unpack("<IIIIIIII", key))
    state[12] = counter
    state[13:16] = list(struct.unpack("<III", nonce))

    working_state = state[:]
    for _ in range(10):
        # Column rounds
        working_state[0], working_state[4], working_state[8], working_state[12] = quarter_round(working_state[0], working_state[4], working_state[8], working_state[12])
        working_state[1], working_state[5], working_state[9], working_state[13] = quarter_round(working_state[1], working_state[5], working_state[9], working_state[13])
        working_state[2], working_state[6], working_state[10], working_state[14] = quarter_round(working_state[2], working_state[6], working_state[10], working_state[14])
        working_state[3], working_state[7], working_state[11], working_state[15] = quarter_round(working_state[3], working_state[7], working_state[11], working_state[15])
        # Diagonal rounds
        working_state[0], working_state[5], working_state[10], working_state[15] = quarter_round(working_state[0], working_state[5], working_state[10], working_state[15])
        working_state[1], working_state[6], working_state[11], working_state[12] = quarter_round(working_state[1], working_state[6], working_state[11], working_state[12])
        working_state[2], working_state[7], working_state[8], working_state[13] = quarter_round(working_state[2], working_state[7], working_state[8], working_state[13])
        working_state[3], working_state[4], working_state[9], working_state[14] = quarter_round(working_state[3], working_state[4], working_state[9], working_state[14])

    for i in range(16):
        state[i] = (state[i] + working_state[i]) & 0xFFFFFFFF

    return struct.pack("<IIIIIIIIIIIIIIII", *state)

def generate_entropy(iterations=100):
    entropy = bytearray()
    for _ in range(iterations):
        start = time.perf_counter_ns()
        result = sum(i * i for i in range(10))
        end = time.perf_counter_ns()
        entropy.extend(struct.pack('<Q', end - start))
    processed_entropy = bytearray()
    for byte in entropy:
        if byte != 0:
            processed_entropy.append(byte)
    while len(processed_entropy) < 16:
        processed_entropy.append(random.randint(1,9)) # at least some randomness
    return bytes(processed_entropy[:16])

def generate_numbers(key, nonce, counter, count=1):
    result = ''
    for _ in range(count):
        key_stream = chacha_block(key, counter, nonce)
        # Convert each byte to its 3-digit representation and concatenate
        result += ''.join(f"{byte:03d}" for byte in key_stream)
        counter += 1
    return result

def main():
    parser = argparse.ArgumentParser(description="Generate random numbers using ChaCha20.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--custom", type=str, help="Custom seed string (16 symbols)")
    group.add_argument("--prng", action="store_true", help="Use PRNG seed (Python's random library). Not very secure.")
    group.add_argument("--entropy", action="store_true", help="Use entropy seed, internally generated using the STARSTONE algorithm. Slower than PRNG, but it's the best option if you don't have a random seed.")
    parser.add_argument("-n", type=int, default=1, help="Number of strings to generate")

    args = parser.parse_args()

    # Generate nonce from entropy
    nonce = generate_entropy()[:12]
    counter = 0

    # Generate key based on selected method
    if args.custom:
        if len(args.custom) != 16:
            raise ValueError("Custom string must be 16 symbols long")
        key = (args.custom + args.custom).encode()
    elif args.prng:
        random.seed(time.time())
        key = (''.join(random.choices(string.ascii_letters + string.digits, k=16)) +
              ''.join(random.choices(string.ascii_letters + string.digits, k=16))).encode()
    elif args.entropy:
        key = generate_entropy() + generate_entropy()

    # Generate and print numbers
    numbers = generate_numbers(key, nonce, counter, args.n)
    print(numbers)

if __name__ == "__main__":
    main()
