import sys
import os
import json
from socket import socket
from socket import AF_INET, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread, Lock
from p2p_functionality import download, send_file, load_config

lock = Lock()
commands = {
    "download": lambda x, y: download(x, y),
    "help": lambda x, y: print("Available commands: download, help, exit")
}

class ClientMechs:
    def __init__(self, target_addr: tuple[str, int]):
        self.target_addr = target_addr
        self.sock = socket(AF_INET, SOCK_STREAM)
    
    def handleConnection(self):
        while True:
            command = input("Enter Command: ")
            if command.lower() == "exit":
                break

            self.sock.sendall(command.encode())
            filename = self.sock.recv(1024).decode()
            commands[command](self.sock, filename)
    
    def run(self):
        self.sock.connect(self.target_addr)

class ServerMechs:
    def __init__(self, bind_addr: tuple[str, int]):
        self.bind_addr = bind_addr
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(self.bind_addr)
        self.sock.listen(5)
    
    def handleClient(self, client_sock: socket):
        while True:
            command = client_sock.recv(1024).decode()
            if not command:
                break

            if command in commands:
                client_sock.sendall(b"ready")
                filename = client_sock.recv(1024).decode()
                send_file(client_sock, filename)
            else:
                client_sock.sendall(b"invalid command")
    
    def run(self):
        print(f"Server listening on {self.bind_addr}")
        while True:
            client_sock, addr = self.sock.accept()
            print(f"Connection from {addr}")
            client_thread = Thread(target=self.handleClient, args=(client_sock,))
            client_thread.start()
    
if __name__ == "__main__":
    load_config("config.json")
