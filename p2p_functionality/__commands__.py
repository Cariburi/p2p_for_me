# THis file is for making custom commands 
from p2p_funcs import download, load_config

try:
    json_file = "json_files/commands_help.json"

    # Add custom commands here
    # Please update help in the file so that users know how to use them
    # json file: commands_help.json
    file_data = load_config(json_file)

    def help_command(conn, y):
        help_msg: str = file_data["help"]
        conn.sendall(help_msg.encode())
    
    server_commands = {
        "download": lambda x, y: download(x, y),
        "help": lambda x, y: help_command(x, y)
    }

except FileNotFoundError:
    print("[!] JSON FILE FOR HELP COMMAND WAS NOT FOUND")

if __name__ == "__main__":
    print("This module is not meant to be run directly.")