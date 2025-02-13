import requests
import json
import random
import time
import sys
from datetime import datetime

TOKEN_FILE = "token.json"
SWAP_API_URL = "https://api2.blockpad.fun/api/swap/execute"

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}", flush=True)
    sys.stdout.flush()

def load_token():
    log("Memuat token dari file token.json...")
    try:
        with open(TOKEN_FILE, "r") as file:
            data = json.load(file)
            token = data.get("Authorization")
            if token:
                log("Token berhasil dimuat.", "SUCCESS")
                return token
            else:
                log("[ERROR] Token tidak ditemukan dalam file!", "ERROR")
                return None
    except (FileNotFoundError, json.JSONDecodeError):
        log("[ERROR] File token.json tidak ditemukan atau format tidak valid!", "ERROR")
        return None

def swap_token(token, from_token, to_token, amount):
    while True:  # Loop terus menerus sampai swap berhasil
        log(f"Mengirim permintaan swap: {amount} {from_token} -> {to_token}...")
        headers = {"Authorization": token, "Content-Type": "application/json"}
        payload = {"fromToken": from_token, "toToken": to_token, "amount": amount}
        
        response = requests.post(SWAP_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            log(f"[SUCCESS] Swap berhasil: {amount} {from_token} -> {to_token}", "SUCCESS")
            log(f"[DETAILS] Response: {response.json()}")
            break  # Berhenti loop jika berhasil
        else:
            log(f"[ERROR] Swap gagal! Status Code: {response.status_code}, Response: {response.text}", "ERROR")
            log("Mengulangi swap dalam 5 detik...")
            time.sleep(5)  # Tunggu sebelum mencoba lagi

if __name__ == "__main__":
    log("Memulai skrip USDT to tICE...")
    token = load_token()
    if not token:
        log("[ERROR] Token tidak ditemukan! Harap isi file token.json terlebih dahulu.", "ERROR")
        exit()
    
    while True:
        amount = random.randint(1, 5)
        swap_token(token, "USDT", "tICE", amount)
        
        delay = random.randint(5, 15)
        log(f"Menunggu {delay} detik sebelum swap berikutnya...")
        time.sleep(delay)
