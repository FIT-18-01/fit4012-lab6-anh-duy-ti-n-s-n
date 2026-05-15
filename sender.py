import os
import socket
from pathlib import Path

from aes_socket_utils import build_data_packet, build_key_packet, encrypt_aes_cbc

SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
DATA_PORT = int(os.getenv("DATA_PORT", "6000"))
KEY_PORT = int(os.getenv("KEY_PORT", "6001"))
AES_KEY_SIZE = int(os.getenv("AES_KEY_SIZE", "16"))
MESSAGE_ENV = os.getenv("MESSAGE")
INPUT_FILE = os.getenv("INPUT_FILE", "")
LOG_FILE = os.getenv("SENDER_LOG_FILE", "")
TIMEOUT = float(os.getenv("SOCKET_TIMEOUT", "10"))


def get_plaintext() -> bytes:
    """Read plaintext from INPUT_FILE, MESSAGE, or keyboard input."""
    if INPUT_FILE:
        return Path(INPUT_FILE).read_bytes()
    if MESSAGE_ENV is not None:
        return MESSAGE_ENV.encode("utf-8")
    return input("Nhập bản tin: ").encode("utf-8")


def send_packet(host: str, port: int, packet: bytes, retries: int = 3) -> None:
    """Open one TCP connection and send all bytes with retry logic."""
    import time
    for attempt in range(retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(TIMEOUT)
                sock.connect((host, port))
                sock.sendall(packet)
            print(f"[+] Đã gửi packet tới {host}:{port}", flush=True)
            return  # Success
        except (ConnectionRefusedError, socket.timeout) as e:
            if attempt < retries - 1:
                print(f"[!] Kết nối thất bại tới {host}:{port}, thử lại... (lần {attempt + 1}/{retries})", flush=True)
                time.sleep(1)
            else:
                print(f"[-] Kết nối thất bại sau {retries} lần tới {host}:{port}: {e}", flush=True)
                raise


def main() -> None:
    try:
        plaintext = get_plaintext()
        key, iv, ciphertext = encrypt_aes_cbc(plaintext, key_size=AES_KEY_SIZE)

        key_packet = build_key_packet(key, iv)
        data_packet = build_data_packet(ciphertext)

        send_packet(SERVER_IP, KEY_PORT, key_packet)
        
        # Add delay to ensure receiver is ready to listen on DATA_PORT
        import time
        time.sleep(0.5)
        
        send_packet(SERVER_IP, DATA_PORT, data_packet)

        lines = [
            "[+] Đã tạo AES key và IV.",
            "[+] Đã gửi key/IV qua kênh khóa.",
            "[+] Đã gửi ciphertext qua kênh dữ liệu.",
            f"Server: {SERVER_IP}",
            f"Key port: {KEY_PORT}",
            f"Data port: {DATA_PORT}",
            f"AES key size: {len(key)} bytes",
            f"Key: {key.hex()}",
            f"IV: {iv.hex()}",
            f"Plaintext length: {len(plaintext)} bytes",
            f"Ciphertext length: {len(ciphertext)} bytes",
            f"Ciphertext: {ciphertext.hex()}",
        ]

        for line in lines:
            print(line, flush=True)

        if LOG_FILE:
            Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
            Path(LOG_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")
    except Exception as e:
        import sys
        print(f"[-] Error: {e}", file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()