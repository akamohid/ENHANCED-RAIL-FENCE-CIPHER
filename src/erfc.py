import hashlib
import random
import string
import sys
import regex

EMOJI_LIST = [
    '😀', '😁', '😂', '😃', '😄', '😅', '😆', '😇', '😉', '😊',
    '😏', '😐', '😒', '😔', '😕', '😖', '😛', '😜', '😝', '😞',
    '😟', '😠', '💣', '😢', '😭', '😮', '😯', '🥎', '😳', '😴',
    '😵', '😷', '🙈', '🙉', '🙊', '🙋', '🙌', '🙏', '👐', '👑',
    '👒', '👓', '👔', '👕', '👖', '🥇', '🧑', '👜', '👞', '👟',
    '👻', '☠', '🤖', '👽', '🐬', '👦', '🐱', '🐶', '🐭', '🐹',
    '🐰', '🐻'
]

if len(EMOJI_LIST) != 62:
    print(f"Error: EMOJI_LIST contains {len(EMOJI_LIST)} emojis. Exactly 62 unique emojis are required.")
    sys.exit(1)

def generate_substitution_mapping(key):
    chars = list(string.ascii_letters + string.digits)
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    seed = int(key_hash, 16)
    random.seed(seed)
    shuffled_emojis = EMOJI_LIST.copy()
    random.shuffle(shuffled_emojis)
    subs = {}
    rev_subs = {}
    for i, ch in enumerate(chars):
        e = shuffled_emojis[i]
        subs[ch] = e
        rev_subs[e] = ch
    print(f"[Debug] Generated one-to-one substitution mapping for {len(chars)} characters.")
    return subs, rev_subs

def generate_salt_and_encrypted_length(plaintext_length, key, length=12):
    if plaintext_length > 9999:
        raise ValueError("Plaintext too large to encode length in 4 digits.")
    length_str = f"{plaintext_length:04d}"
    encrypted_length = encrypt_length(length_str, key)
    salt_body = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    final_salt = encrypted_length + salt_body
    print(f"[Step 5] Generated Salt: {final_salt}")
    return final_salt

def parse_salt_and_decrypt_length(final_salt, key):
    length_encrypted_hex = final_salt[:8]
    decrypted_length_str = decrypt_length(length_encrypted_hex, key)
    plaintext_length = int(decrypted_length_str)
    print(f"[Step 1] Extracted Plaintext Length: {plaintext_length}")
    print(f"[Step 1] Extracted Salt: {final_salt}")
    return plaintext_length

def encrypt_length(length_str, key):
    key_hash = hashlib.sha256(key.encode()).digest()
    encrypted_bytes = bytes([ord(c) ^ key_hash[i % len(key_hash)] for i, c in enumerate(length_str)])
    encrypted_hex = encrypted_bytes.hex()
    return encrypted_hex

def decrypt_length(encrypted_length_hex, key):
    encrypted_bytes = bytes.fromhex(encrypted_length_hex)
    key_hash = hashlib.sha256(key.encode()).digest()
    decrypted_chars = [chr(b ^ key_hash[i % len(key_hash)]) for i, b in enumerate(encrypted_bytes)]
    decrypted_length_str = ''.join(decrypted_chars)
    return decrypted_length_str

def hash_message(key, salt, plaintext):
    combined = key + salt + plaintext
    return hashlib.sha256(combined.encode()).hexdigest()

def ascii_sum_key(key):
    return sum(ord(c) for c in key)

def compute_matrix_dims(key, text_length, expansion_factor=5):
    a_sum = ascii_sum_key(key)
    target = expansion_factor * text_length
    R = (a_sum % 10) + 10
    C = max((target // R) + 1, (a_sum % 50) + 20)
    while R * C < target:
        C += 1
    print(f"[Step 2] Matrix Dimensions: {R} rows x {C} columns")
    return R, C

def create_big_matrix(plaintext_emojis, R, C, key):
    matrix = [['' for _ in range(C)] for _ in range(R)]
    total_cells = R * C
    seed = ascii_sum_key(key)
    random.seed(seed)
    all_positions = [(r, c) for r in range(R) for c in range(C)]
    random.shuffle(all_positions)
    real_count = len(plaintext_emojis)
    if real_count > total_cells:
        raise ValueError("Matrix too small to hold all plaintext emojis.")
    for i in range(real_count):
        r, c = all_positions[i]
        matrix[r][c] = plaintext_emojis[i]
    for i in range(real_count, total_cells):
        r, c = all_positions[i]
        matrix[r][c] = random.choice(EMOJI_LIST)
    print(f"[Step 3] Big Matrix Created.")
    return matrix

def serialize_matrix(matrix):
    result = ''.join(cell for row in matrix for cell in row)
    print(f"[Step 4] Serialized Cipher Body Length: {len(result)}")
    return result

def deserialize_matrix(cipher_body, R, C):
    graphemes = regex.findall(r'\X', cipher_body)
    if len(graphemes) != R * C:
        raise ValueError(f"Cipher body length does not match matrix dimensions. Expected {R*C}, got {len(graphemes)}.")
    matrix = []
    it = iter(graphemes)
    for _ in range(R):
        row = [next(it) for _ in range(C)]
        matrix.append(row)
    print(f"[Step 3] Deserialized Matrix.")
    return matrix

def extract_plaintext_emojis(matrix, real_count, key):
    R = len(matrix)
    C = len(matrix[0]) if R > 0 else 0
    total_cells = R * C
    seed = ascii_sum_key(key)
    random.seed(seed)
    all_positions = [(r, c) for r in range(R) for c in range(C)]
    random.shuffle(all_positions)
    if real_count > total_cells:
        raise ValueError("Matrix not large enough to contain all real emojis.")
    emojis = []
    for i in range(real_count):
        r, c = all_positions[i]
        emojis.append(matrix[r][c])
    result = ''.join(emojis)
    print(f"[Step 4] Extracted Real Emojis: {result}")
    return result

def substitute_text(text, substitution_mapping):
    result = ''.join(substitution_mapping[char] for char in text)
    print(f"[Step 1] Substituted Text: {result}")
    return result

def reverse_substitute_text(text, reverse_substitution_mapping):
    result = ''.join(reverse_substitution_mapping[char] for char in text)
    print(f"[Step 5] Recovered Plaintext: {result}")
    return result

def encrypt(plaintext, key):
    print("\n--- Encryption Process Started ---")
    if not plaintext.isalnum():
        print("Error: Plaintext contains non-alphanumeric characters. Only a-z, A-Z, 0-9 are allowed.")
        return None, None
    substitution_mapping, _ = generate_substitution_mapping(key)
    try:
        substituted_text = substitute_text(plaintext, substitution_mapping)
    except KeyError as e:
        print(f"Error: Character '{e.args[0]}' is not in substitution mapping.")
        return None, None
    R, C = compute_matrix_dims(key, len(substituted_text))
    big_matrix = create_big_matrix(substituted_text, R, C, key)
    cipher_body = serialize_matrix(big_matrix)
    final_salt = generate_salt_and_encrypted_length(len(plaintext), key, length=12)
    message_hash = hash_message(key, final_salt, plaintext)
    print(f"[Step 6] Generated SHA-256 Hash: {message_hash}")
    final_ciphertext = cipher_body + final_salt
    print(f"[Step 7] Final Ciphertext Length: {len(final_ciphertext)}")
    print("--- Encryption Process Completed ---\n")
    return final_ciphertext, message_hash

def decrypt(ciphertext, key, received_hash):
    print("\n--- Decryption Process Started ---")
    salt_length = 20
    if len(ciphertext) < salt_length:
        print("Error: Ciphertext too short to contain salt and encrypted length.")
        return None
    final_salt = ciphertext[-salt_length:]
    cipher_body = ciphertext[:-salt_length]
    try:
        plaintext_length = parse_salt_and_decrypt_length(final_salt, key)
    except Exception as e:
        print(f"Error during salt parsing/decryption: {e}")
        return None
    R, C = compute_matrix_dims(key, plaintext_length)
    try:
        matrix = deserialize_matrix(cipher_body, R, C)
    except ValueError as ve:
        print(f"Error during matrix deserialization: {ve}")
        return None
    try:
        real_emojis = extract_plaintext_emojis(matrix, plaintext_length, key)
    except ValueError as ve:
        print(f"Error during emoji extraction: {ve}")
        return None
    _, reverse_substitution_mapping = generate_substitution_mapping(key)
    try:
        plaintext = reverse_substitute_text(real_emojis, reverse_substitution_mapping)
    except KeyError as e:
        print(f"Error: Emoji '{e.args[0]}' not found in reverse substitution mapping.")
        return None
    regenerated_hash = hash_message(key, final_salt, plaintext)
    print(f"[Step 6] Regenerated SHA-256 Hash: {regenerated_hash}")
    print(f"[Step 6] Received SHA-256 Hash: {received_hash}")
    if regenerated_hash != received_hash:
        print("Error: Integrity check failed. The message may have been tampered with or the key is incorrect.")
        return None
    print("--- Decryption Process Completed ---\n")
    return plaintext

def main():
    while True:
        print("=== Enhanced Rail Fence Cipher (ERFC) ===")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")
        if choice == '1':
            plaintext = input("\n=== Encryption ===\nEnter the plaintext (a-z, A-Z, 0-9): ")
            key = input("Enter the secret key: ")
            ciphertext, full_hash = encrypt(plaintext, key)
            if ciphertext is None:
                continue
            print("\n--- Encryption Output ---")
            print(f"Ciphertext: {ciphertext}")
            print(f"SHA-256 Hash: {full_hash}")
            print(f"Ciphertext Length: {len(ciphertext)}")
            print("-------------------------\n")
        elif choice == '2':
            ciphertext = input("\n=== Decryption ===\nEnter the ciphertext: ")
            key = input("Enter the secret key: ")
            received_hash = input("Enter the SHA-256 hash: ")
            plain = decrypt(ciphertext, key, received_hash)
            if plain is None:
                continue
            print("\n--- Decryption Output ---")
            print(f"Plaintext: {plain}")
            print("-------------------------\n")
        elif choice == '3':
            print("Exiting ERFC. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
