import requests
import json
import random
import time
import sys
from datetime import datetime

TOKEN_FILE = "token.json"
SWAP_API_URL = "https://api3.blockpad.fun/api/swap/execute"

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}", flush=True)
    sys.stdout.flush()

def load_token():
    """Memuat token dari file token.json."""
    log("Memuat token dari file token.json...")
    try:
        with open(TOKEN_FILE, "r") as file:
            data = json.load(file)
            token = data.get("Authorization")
            if token:
                log("Token berhasil dimuat.", "SUCCESS")
                return token
            log("Token tidak ditemukan dalam file!", "ERROR")
            return None
    except (FileNotFoundError, json.JSONDecodeError):
        log("File token.json tidak ditemukan atau format tidak valid!", "ERROR")
        return None

def swap_token(token, from_token, to_token, amount):
    """Melakukan swap token dengan percobaan berulang jika gagal."""
    while True:
        log(f"Mengirim permintaan swap: {amount} {from_token} -> {to_token}...")
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {"fromToken": from_token, "toToken": to_token, "amount": amount}
        
        response = requests.post(SWAP_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            log(f"Swap berhasil: {amount} {from_token} -> {to_token}", "SUCCESS")
            log(f"Response: {response.json()}")
            break  # Keluar dari loop jika berhasil
        else:
            status_code = response.status_code
            if status_code in [500, 502, 504]:
                log(f"[ERROR] Status kode {status_code}: Terjadi kesalahan pada server.", "ERROR")
            else:
                log(f"[ERROR] Swap gagal! Status Code: {status_code}. Response: {response.text.strip()}", "ERROR")
            log("Mengulangi swap dalam 5 detik...")
            time.sleep(5)

if __name__ == "__main__":
    log("Memulai skrip USDT to BPAD...")
    token = load_token()
    
    if not token:
        log("Token tidak ditemukan! Harap isi file token.json terlebih dahulu.", "ERROR")
        sys.exit()
    
    while True:
        amount = random.randint(1, 5)
        swap_token(token, "USDT", "BPAD", amount)
        
        delay = random.randint(7, 15)
        log(f"Menunggu {delay} detik sebelum swap berikutnya...")
        time.sleep(delay)
