from socket import socket
import json

def download(conn: socket, filename: str, recv_buffer=2000):
    with open(filename, "wb") as f:
        while True:
            data = conn.recv(recv_buffer)
            if not data:
                break
            f.write(data)
    
    print(f"Downloaded file: {filename}")

def send_file(conn: socket, filename: str):
    with open(filename, "rb") as f:
        data = f.read()
        while True:
            if not data:
                break

            conn.sendall(data)
    
    return None

def load_config(filename: str):
    with open(filename, "r") as f:
        data = json.load(f)
    
    return data
