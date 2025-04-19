import socket, ssl
import threading

HOST = 'IP' 
PORT = 7777

name = input("Enter your name: ")
key = input("Enter shared key: ")

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname=HOST)
conn.connect((HOST, PORT))

conn.send(name.encode())
conn.send(key.encode())

response = conn.recv(1024).decode()
if "DENIED" in response:
    print("[ACCESS DENIED] Server rejected your request.")
    conn.close()
    exit()

print("[ACCESS GRANTED] Connected to chat.")

def receive():
    while True:
        try:
            msg = conn.recv(1024).decode()
            if msg:
                print(msg)
        except:
            break

threading.Thread(target=receive, daemon=True).start()

try:
    while True:
        msg = input()
        if msg.strip():
            conn.send(msg.encode())
except KeyboardInterrupt:
    print("\n[EXITING] Chat closed.")
    conn.close()
