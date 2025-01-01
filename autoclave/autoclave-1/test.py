import struct
import time
import random
import string

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
        processed_entropy.append(1)
    return bytes(processed_entropy[:16])


def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def generate_strings(num_strings):
    strings = []
    for _ in range(num_strings):
        seed = generate_entropy()
        random.seed(seed)
        random_string = generate_random_string() + generate_random_string()
        strings.append(random_string)
    return strings


if __name__ == "__main__":
    num_strings = 1
    key_string = generate_random_string() + generate_random_string()
    key = key_string.encode()
    nonce = generate_random_string().encode()[:12]
    counter = 0

    for _ in range(num_strings):
        key_stream = chacha_block(key, counter, nonce)
        random_numbers = [x for x in key_stream]

        print(''.join([str(x) for x in random_numbers]))

        counter += 1
