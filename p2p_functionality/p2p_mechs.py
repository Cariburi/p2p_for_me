# wrote'FUNCTION' and 'FUNCTION END' comments for readability and
# wrote 'CLASS' and 'CLASS END' comments for readability.

from socket import socket
from socket import SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread, Lock, Event

from .p2p_dataclasses import server_info 
from .p2p_funcs import log_data, recv_file

from .__commands__ import server_commands

lock = Lock()
# CLASS
class ClientMechs:
    # FUNCTION
    def __init__(self, target_addr: tuple[str, int]):
        self.target_addr = target_addr
        self.sock = socket(AF_INET, SOCK_STREAM)
    # FUNCTION END
    
    # FUNCTION
    def handleConnection(self):
        print("[?] Type quit to exit")
        while True:
            send_data = None
            command = input("> ")

            if len(command.split()) == 0:
                print("[!] Enter a command don't leave blank")
                continue

            if command.lower() == "quit":
                break

            try:
                if command.split()[0] == "download":
                    filename = command.split()[1]
                    send_data = command.encode()
                    self.sock.sendall(send_data.encode())
                    recv_file(self.sock, filename)
            
                send_data = self.sock.sendall(command.encode())
                response = self.sock.recv(2048)
                print(f"Response from server: \n-  {response.decode()}")
            except BrokenPipeError:
                print("[!] SERVER CRASHED, CLOSED or AN ERROR HAS OCCURED")
                break

            except ConnectionResetError:
                print("[!] SERVER CONNECTION RESET")
        
        return None
    # FUNCTION END

    # FUNCTION
    def __call__(self, *args, **kwargs):
        self.sock.connect(self.target_addr)
        self.handleConnection()
        self.sock.close()
        print("<<CTRL+C to close Server>>")
        return None
    # FUNCTION END
# CLASS END

# CLASS
class ServerMechs:
    # FUNCTION
    def __init__(self):
        self.conn_threads: list[Thread] = []
        self.clients: list[socket] = []
        self.signal = server_info.thread_signal
        self.files_directory = server_info.files_directory
        self.bind_addr = server_info.host, server_info.port
        self.log_file = server_info.log_file
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(self.bind_addr)
        self.sock.listen(server_info.max_clients)
    # FUNCTION END

    # FUNCTION
    def handleClient(self, client_sock: socket, addr):
        while not self.signal.is_set():
            try:
                command = client_sock.recv(1024).decode()
                if not command:
                    break

                if command == "quit":
                    break
            except Exception as e:
                break

            with lock:
                log_data(self.log_file, f"Received command: {command} <-from-> {addr[0]}:{addr[1]}")
            
            try:
                if command.split()[0] in server_commands:
                    parts = command.split()

                    if len(parts) > 2:
                        with lock:
                            log_data(self.log_file, f"To much data inputed from user -> {addr[0]}:{addr[1]}")
                        
                        client_sock.send("Sent an invalid amount of arguments for command")
                    
                    if "download" in parts:
                        server_commands[command](client_sock, parts[1])
                    else:
                        send_data = server_commands[parts[0]](client_sock, None)
                        client_sock.sendall(send_data.encode())
                else:
                    with lock:
                        log_data(self.log_file, f"Invalid command received: {command} <-from-> {addr[0]}:{addr[1]}")
                
                    client_sock.sendall(b"Invalid command")
            
            except ValueError:
                with lock:
                    log_data(self.log_file, f"To few arguments recieved from user -> {addr[0]}:{addr[1]}")
            
                client_sock.sendall("To few arguments given for command")
                continue

            except BrokenPipeError as e:
                with lock:
                    log_data(self.log_file, f"Client disconnected -> {addr[0]}:{addr[1]}")
                break

            except ConnectionResetError:
                with lock:
                    log_data(self.log_file, f"[!] Connection Error: {e} -> {addr[0]}:{addr[1]}")
                break

            except Exception as e:
                with lock:
                    log_data(self.log_file, f"[!] Client Error: {e} -> {addr[0]}:{addr[1]}")
                
                break
        try:
            client_sock.send("Closing connection.".encode())
        except:
            pass

        client_sock.close()
        
        return None
    # FUNCTION END
    
    # FUNCTION
    def run(self):
        log_data(self.log_file, f"Server started at {self.bind_addr[0]}:{self.bind_addr[1]}")
        
        try:
            while not self.signal.is_set():

                try:
                    client_sock, addr = self.sock.accept()
                except OSError:
                    break

                self.clients.append(client_sock)
                with lock:
                    log_data(self.log_file, f"Connection established with {addr[0]}:{addr[1]}")
            
                client_thread = Thread(target=self.handleClient, args=(client_sock, addr))
                client_thread.start()
                self.conn_threads.append(client_thread)

        except KeyboardInterrupt:
            with lock:
                log_data(self.log_file, "Server shutting down...")
                
            self.signal.set()
        
        except Exception as e:
            with lock:
                log_data(self.log_file, f"Server encountered an error: {e}")
            
            self.signal.set()

        finally:
            self.signal.set()
            self.sock.close()
            for t in self.conn_threads:
                if t.is_alive():
                    t.join()
                else:
                    continue
        
        log_data(self.log_file, f"<\\SERVER SHUT DOWN/>")
        return None
    # FUNCTION END
# CLASS END

if __name__ == "__main__":
    print("This module is not meant to be run directly.")