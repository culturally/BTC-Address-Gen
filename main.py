import random
import hashlib
import base58
import multiprocessing
import json
import os
from datetime import datetime
from ecdsa import SECP256k1, SigningKey
from colorama import Fore, Style, init

init(autoreset=True)
def get_search_patterns():
    print(Fore.WHITE + "powered by" + Fore.YELLOW + " yin.sh")
    print()
    print(Fore.WHITE + "Enter custom Bitcoin address patterns (separate with commas if multiple).")
    print()
    print(Fore.YELLOW + "Example patterns:" + Fore.WHITE + " 1Example, bc1Example")
    print()

    validated_patterns = []
    while not validated_patterns:
        user_input = input(Fore.YELLOW + "target" + Fore.WHITE + "> ").split(',')
        validated_patterns = []
        invalid_patterns = []

        for pattern in user_input:
            pattern = pattern.strip()

            if pattern.startswith("1") or pattern.startswith("bc1"):
                if len(pattern) > 6: 
                    print(Fore.RED + f"Warning: Pattern '{pattern}' is long and may take significantly longer to find.")
                validated_patterns.append(pattern)
            else:
                invalid_patterns.append(pattern)

        if invalid_patterns:
            print()
            print()
            print(Fore.RED + "Invalid patterns detected:")
            for invalid in invalid_patterns:
                print(Fore.RED + f"  '{invalid}': Patterns must start with '1' or 'bc1'.")
                print()
            print(Fore.YELLOW + "Please enter valid patterns again (e.g., '1Example' or 'bc1Example').")
            validated_patterns = []  

  
    case_sensitive = input(Fore.YELLOW + "Should the search be case-sensitive? (y/n): ").lower() == 'y'
    return validated_patterns, case_sensitive


def generate_private_key():
    return ''.join(random.choice('0123456789abcdef') for _ in range(64))

def private_key_to_wif(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    extended_key = b'\x80' + private_key_bytes
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    final_key = extended_key + checksum
    return base58.b58encode(final_key).decode('utf-8')


def private_key_to_public_key(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    verifying_key = signing_key.verifying_key
    public_key_bytes = b'\x04' + verifying_key.to_string()
    return public_key_bytes


def hash_public_key(public_key):
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    return ripemd160.digest()

def create_address(private_key_hex):
    public_key = private_key_to_public_key(private_key_hex)
    hashed_pub_key = hash_public_key(public_key)
    versioned_key = b'\x00' + hashed_pub_key
    checksum = hashlib.sha256(hashlib.sha256(versioned_key).digest()).digest()[:4]
    full_payload = versioned_key + checksum
    return base58.b58encode(full_payload).decode('utf-8')


def check_patterns(address, patterns, case_sensitive):
    for pattern in patterns:
        if case_sensitive and address.startswith(pattern):
            return pattern
        elif not case_sensitive and address.lower().startswith(pattern.lower()):
            return pattern
    return None


def save_address_details(private_key, address, pattern):
    wif = private_key_to_wif(private_key)
    public_key = private_key_to_public_key(private_key).hex()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    key_data = {
        "address": address,
        "private_key": private_key,
        "wif": wif,
        "pubkey": public_key,
        "pattern": pattern,
        "timestamp": timestamp
    }

    if os.path.exists("address.json"):
        with open("address.json", "r") as key_file:
            data = json.load(key_file)
    else:
        data = []

    data.append(key_data)
    with open("address.json", "w") as key_file:
        json.dump(data, key_file, indent=4)

    print(Fore.GREEN + f"Saved address: {address}, pattern: {pattern}, private key: {private_key}")


def find_matching_address_worker(worker_id, patterns, case_sensitive):
    print(Fore.YELLOW + f"Worker {worker_id} started searching.")

    while True:
        private_key = generate_private_key()
        address = create_address(private_key)

        pattern = check_patterns(address, patterns, case_sensitive)
        if pattern:
            print(Fore.GREEN + f"Worker {worker_id} found a match: {address} (Pattern: {pattern})")
            save_address_details(private_key, address, pattern)

def find_matching_address_parallel(num_workers=6, patterns=None, case_sensitive=True):
    pool = multiprocessing.Pool(processes=num_workers)
    worker_args = [(worker_id, patterns, case_sensitive) for worker_id in range(num_workers)]
    pool.starmap(find_matching_address_worker, worker_args)
    pool.close()
    pool.join()

if __name__ == "__main__":
    os.system('cls||clear')
    logo = """
    ⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣷⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
 ⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀
⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⠟⠿⠿⡿⠀⢰⣿⠁⢈⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣤⣄⠀⠀⠀⠈⠉⠀⠸⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⢠⣶⣶⣤⡀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⡆
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠼⣿⣿⡿⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢀⣀⣀⠀⠀⠀⠀⢴⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠁⠀⠀⣼⣿⣿⣿⣦⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⡿
⠸⣿⣿⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠛⠛⠿⠟⠋⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⠇
⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⣤⡄⠀⣀⣀⣀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⡟⠀
⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣄⣰⣿⠁⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢿⣿⣿⣿⣿⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
"""
    print(Fore.YELLOW + logo)
    
    patterns, case_sensitive = get_search_patterns()
    if not patterns:
        print(Fore.RED + "No valid patterns provided. Exiting.")
    else:
        try:
            print()
            num_workers = int(input(Fore.YELLOW + "Enter the number of workers (10 recommended): "))
            os.system('cls||clear')
            if num_workers <= 0:
                print(Fore.YELLOW + "Invalid number. Using the recommended 10 workers.")
                num_workers = 10
                os.system('cls||clear')
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Using the recommended 10 workers.")
            os.system('cls||clear')
            num_workers = 10
        find_matching_address_parallel(num_workers=num_workers, patterns=patterns, case_sensitive=case_sensitive)
