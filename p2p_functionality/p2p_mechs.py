import sys
import os
import json
from socket import socket
from socket import AF_INET, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread, Lock
from p2p_functionality import download, send_file, load_config

lock = Lock()
commands = {
    "download": lambda x, y: download(x, y)
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

if __name__ == "__main__":
    load_config("config.json")
