from socket import socket
from datetime import datetime
import os
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

    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("")

    with open(log_file, "a") as f:
        time = get_time()
        f.write(f"[{time}] {message}\n")
    
    return None

def get_files():

    """
        Get list of files in the server's file directory;
    """

    try:
        files_directory = load_config("p2p_functionality/json_files/config.json")["files_directory"]
        files_in_dir = os.listdir(files_directory)
        if "README.TXT" in files_in_dir:
            files_in_dir.remove("README.TXT")
        
        file_list = '\n'.join(files_in_dir)
        return file_list
    
    except FileNotFoundError:
        print(f"[!] Files directory '{files_directory}' not found.")
        return []

if __name__ == "__main__":
    print("This module is not meant to be run directly.")
