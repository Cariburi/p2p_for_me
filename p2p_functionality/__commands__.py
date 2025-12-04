# THis file is for making custom commands 
from .p2p_funcs import download, load_config, get_files

try:
    json_file = "p2p_functionality/json_files/commands_help.json"

    # Add custom commands here
    # Please update help in the file so that users know how to use them
    # json file: commands_help.json
    file_data = load_config(json_file)

    def help_command():
        help_msg: str = file_data["help"]
        return help_msg
    
    server_commands = {
        "download": lambda x, y: download(x, y),
        "help": lambda x, y: help_command(),
        "ls": lambda x, y: get_files()
    }

except FileNotFoundError:
    print("[!] JSON FILE FOR HELP COMMAND WAS NOT FOUND")

if __name__ == "__main__":
    print("This module is not meant to be run directly.")