from dataclasses import dataclass

from .p2p_funcs import load_config
from threading import Event

json_file = "p2p_functionality/json_files/config.json"

@dataclass
class ServerInfo:

    """
        Dataclass to hold server configuration information;
        Essentially a structured way to store server settings;
        Example:
        server_info = ServerInfo(\n
            host="127.0.0.1", // Host ip address\n
            port=4000, // Port number\n
            max_clients=5, // Max number of clients\n
            files_directory="files/" // Directory to store files
        )

        But all of the info is in a loaded file(config.json);
    """

    host: str
    port: int
    max_clients: int
    files_directory: str
    log_file: str
    thread_signal: Event

data = load_config(json_file)
thread_signal = Event()
server_info = ServerInfo(
    host=data["host_ip"],
    port=data["host_port"],
    max_clients=data["max_clients"],
    files_directory=data["files_directory"],
    log_file=data["log_file"],
    thread_signal=thread_signal
)

if __name__ == "__main__":
    print("SERVER FILE TEST")
    print("SERVER HOST: ", server_info.host)
    print("SERVER PORT: ", server_info.port)
    print("SERVER'S MAX CLIENTS: ", server_info.max_clients)
    print("SERVER'S FILES DIRECTORY: ", server_info.files_directory)
    print("-" * 50)
    print("This module is not meant to be run directly.")
