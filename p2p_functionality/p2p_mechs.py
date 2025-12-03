import sys
import os
import json

from socket import socket
from socket import AF_INET, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread, Lock

from p2p_dataclasses import server_info 
from p2p_funcs import send_file, log_data, recv_file

from __commands__ import server_commands

lock = Lock()

class ClientMechs:
    def __init__(self, target_addr: tuple[str, int]):
        self.target_addr = target_addr
        self.sock = socket(AF_INET, SOCK_STREAM)
    
    def handleConnection(self):
        while True:
            command = input("> ")

            if command.lower() == "exit":
                break

            if command.split()[1] == "download":
                recv_file(self.sock, command.split()[2])
        
        return None

    def __call__(self, *args, **kwargs):
        self.sock.connect(self.target_addr)
        self.handleConnection()
        self.sock.close()

class ServerMechs:
    def __init__(self):
        self.files_directory = server_info.files_directory
        self.bind_addr = server_info.host, server_info.port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(self.bind_addr)
        self.sock.setsockopt(os.SOL_SOCKET, os.SO_REUSEADDR, 1)
        self.sock.listen(server_info.max_clients)
    
    def get_files(self):
        try:
            files = os.listdir(self.files_directory)
            return files
        
        except FileNotFoundError:
            print(f"[!] Files directory '{self.files_directory}' not found.")
            return []

    def handleClient(self, client_sock: socket):
        while True:
            command = client_sock.recv(1024).decode()
            if not command:
                break

            if command in server_commands:
                if command.split[0] == "download":
                    server_commands[command](client_sock, command.split()[1])
                else:
                    server_commands[command](client_sock, None)
                
            else:
                client_sock.sendall(b"invalid command")
        
        return None
    
    def run(self):
        while True:
            client_sock, addr = self.sock.accept()
            print(f"Connection from {addr}")
            client_thread = Thread(target=self.handleClient, args=(client_sock,))
            client_thread.start()
    
if __name__ == "__main__":
    print("This module is not meant to be run directly.")
