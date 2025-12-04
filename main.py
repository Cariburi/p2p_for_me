# Start server and client from here
# Update main function for starting server and client
# For now, just a placeholder
# Dont forget nessessary imports
from p2p_functionality import ServerMechs, ClientMechs
from threading import Thread, Event

def main():
    try:
        print("<- CTRL+C to exit ->")
        print("<- Leave blank to just start server only mode ->")
        print("<- Put 'C' a the end for client only mode ->")
        print("<- Put host ip and port to start both server and client mode ->")
        print("-" * 50)
        server = ServerMechs()
        server_thread = Thread(target=server.run)
        input_data = input("Enter target host ip and port(seperate by space): ").upper()
        parts = input_data.split()

        if "C" in parts:

            parts.remove("C")
            if len(parts) != 2:
                print("[!] For client only mode, please provide both host ip and port and the c.")
                return None
            
            target_ip, target_port = parts
            client = ClientMechs((target_ip, int(target_port)))
            client()
            return None
        
        if len(input_data.split()) == 0:
            print("[*] No input detected from (user->YOU)")
            print("[*] Just starting server...")
            server_thread.start()
            server_thread.join()
            return None
        
        elif len(input_data.split()) == 2:
            target_ip, target_port = input_data.split()
            client = ClientMechs((target_ip, int(target_port)))
            server_thread.start()
            client()
            server.signal.set()
            server_thread.join()
            return None
        else:
            print("[!] Too little or too many values inputed from (user->YOU)")
            return None
    
    except ValueError as e:
        print(f"[!] {e}")
        print("\n[!] Exiting program...")
    
    except KeyboardInterrupt:
        print("\n[!] Exiting program...")
    
    return None

if __name__ == "__main__":
    main()