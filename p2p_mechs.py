from pprint import pprint
from socket import socket as s
from socket import AF_INET, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread, Lock
import json

lock = Lock()
# Add a download command
# LATEEERR add encoding as encryption

def load_config(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    
    return data

class ClientMechs:
    def __init__(self, target_addr: tuple[str, int]):
        self.target_addr = target_addr
        self.sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    def handleConnection(self):
        pass

    def run(self):
        self.sock.connect(self.target_addr)

if __name__ == "__main__":
    load_config("config.json")
