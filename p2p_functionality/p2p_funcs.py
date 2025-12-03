from socket import socket
from datetime import datetime
import json

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def download(conn: socket, filename: str, recv_buffer=2000):

    """
        Download a file over a socket connection;
    """

    with open(filename, "wb") as f:
        while True:
            data = conn.recv(recv_buffer)
            if not data:
                break
            f.write(data)
    
    print(f"Downloaded file: {filename}")

def recv_file(conn: socket, filename: str, recv_buffer=2000):
    
    """
        Receive a file over a socket connection;
    """

    with open(filename, "wb") as f:
        while True:
            data = conn.recv(recv_buffer)
            if not data:
                break
            f.write(data)
    
    print(f"Received file: {filename}")

def send_file(conn: socket, filename: str, send_buffer=2000):

    """
        Send a file over a socket connection;
    """

    try:
        with open(filename, "rb") as f:
            while True:
                data = f.read(send_buffer)
                if not data:
                    break
                conn.sendall(data)
        
        print(f"Sent file: {filename}")
    
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        conn.sendall(b"")  # Send empty bytes to indicate file not found
    
    return None

def print_files(file_list: list[str]):

    """
        Print available files to the console;
    """

    print("Available files:")

    for file in file_list:
        if file == "README.txt":
            continue

        print(f"- {file}")

def load_config(filename: str):

    """
        Load data from json files;
    """

    with open(filename, "r") as f:
        data = json.load(f)
    
    return data

def log_data(log_file: str, message):

    """
        Log data to a specified log file with a timestamp;
    """

    with open(log_file, "a") as f:
        time = get_time()
        f.write(f"[{time}] {message}\n")
    
    return None

if __name__ == "__main__":
    print("This module is not meant to be run directly.")
