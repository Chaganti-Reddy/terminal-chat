import socket
import ssl
import threading

HOST = '0.0.0.0'
PORT = 7777
CERT_FILE = 'certs/cert.pem'
KEY_FILE = 'certs/key.pem'
SHARED_KEY = 'letmein1337'
clients = []

def approve_client(ip, name, key):
    print(f"\n[REQUEST] Connection from {ip}")
    print(f"  Name: {name}")
    print(f"  Key: {key}")
    if key != SHARED_KEY:
        print("  [DENIED] Invalid shared key.")
        return False
    choice = input("  Accept? (y/n): ").strip().lower()
    return choice == 'y'

def handle_client(conn, addr, name):
    print(f"[CONNECTED] {name} ({addr}) joined the chat.")
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[{name}] {msg}")
            for c, _ in clients:
                if c != conn:
                    c.send(f"{name}: {msg}".encode())
    except:
        pass
    finally:
        print(f"[DISCONNECTED] {name} ({addr})")
        clients.remove((conn, name))
        conn.close()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"[SERVER] Listening securely on {HOST}:{PORT}")

while True:
    raw_sock, addr = server_socket.accept()
    conn = context.wrap_socket(raw_sock, server_side=True)
    try:
        name = conn.recv(1024).decode().strip()
        key = conn.recv(1024).decode().strip()
        if approve_client(addr[0], name, key):
            clients.append((conn, name))
            threading.Thread(target=handle_client, args=(conn, addr[0], name), daemon=True).start()
            conn.send("[ACCESS GRANTED] Welcome to the chat!".encode())
        else:
            conn.send("[ACCESS DENIED]".encode())
            conn.close()
    except Exception as e:
        print(f"[ERROR] Connection error from {addr[0]}: {e}")
        conn.close()
