#!/usr/bin/env python3
"""
DeepSeek WebAssembly Proof of Work (PoW) Solver Replica
Author: Nizar Akkioui
Description: Reconstructed Python implementation of the client-side 
             anti-bot challenge (wasm_solve) found in the DeepSeek Chat WASM binary.
"""

import hashlib
import time

def solve_deepseek_pow(challenge: str, salt: str, difficulty: int) -> tuple:
    """
    Emulates the 'wasm_solve' function exported by the DeepSeek WASM module.
    
    Parameters:
    - challenge (str): The unique challenge token issued by the server.
    - salt (str): The dynamic salt value.
    - difficulty (int): The number of leading zeros required in the hex hash.
    
    Returns:
    - tuple: (nonce, resulting_hash, execution_time)
    """
    # Standard format verified from network payloads: salt + "_" + challenge
    prefix = f"{salt}_{challenge}"
    target_prefix = "0" * difficulty
    nonce = 0
    
    start_time = time.time()
    
    print(f"[*] Starting PoW solver...")
    print(f"[*] Prefix: {prefix}")
    print(f"[*] Target: Hash must start with '{target_prefix}' (Difficulty: {difficulty})")
    print("-" * 50)

    while True:
        # Reconstruct the string payload exactly like the WASM dynamic buffer
        payload = f"{prefix}{nonce}"
        
        # DeepSeek uses SHA-3 (Keccak-f [1600] constants mapped in memory)
        hasher = hashlib.sha3_256(payload.encode('utf-8'))
        current_hash = hasher.hexdigest()
        
        # Check if the hash meets the difficulty condition
        if current_hash.startswith(target_prefix):
            end_time = time.time()
            duration = end_time - start_time
            return nonce, current_hash, duration
            
        nonce += 1

# Local Testing Execution Loop
if __name__ == "__main__":
    # Example test vectors (similar to live session logs)
    SAMPLE_CHALLENGE = "4a8b2c9d1e3f5g7h"
    SAMPLE_SALT = "deepseek_anti_ddos"
    SAMPLE_DIFFICULTY = 4  # Typical threshold for standard browser verification
    
    nonce, final_hash, duration = solve_deepseek_pow(
        challenge=SAMPLE_CHALLENGE, 
        salt=SAMPLE_SALT, 
        difficulty=SAMPLE_DIFFICULTY
    )
    
    print("[+] Challenge Successfully Solved!")
    print(f"[+] Found Valid Nonce : {nonce}")
    print(f"[+] Resulting SHA3 Hash: {final_hash}")
    print(f"[+] Time Elapsed       : {duration:.4f} seconds")
