from dataclasses import dataclass

from p2p_funcs import load_config

json_file = "json_files/config.json"

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

data = load_config(json_file)
server_info = ServerInfo(
    host=data["host_ip"],
    port=data["host_port"],
    max_clients=data["max_clients"],
    files_directory=data["files_directory"]
)

if __name__ == "__main__":
    print("SERVER HOST: ", server_info.host)
    print("SERVER PORT: ", server_info.port)
    print("SERVER'S MAX CLIENTS: ", server_info.max_clients)
