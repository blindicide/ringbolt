from flask import Flask, jsonify, request
import time
import struct
import random
import string

app = Flask(__name__)

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
        processed_entropy.append(random.randint(1,9))  # Pad with 1 (non-zero)
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

@app.route('/api/generate', methods=['GET'])
def api_generate():
    num_strings = 1  # Default to generating 1 string unless specified
    # For flexibility, you can also accept a query parameter for the number of strings
    if request.args.get('num'):
        num_strings = int(request.args.get('num'))
    strings = generate_strings(num_strings)
    return jsonify({"random_strings": strings})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

