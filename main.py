import os
import sys
from socket import inet_aton
from socket import error as socket_error
from threading import Thread
import random

def is_ip_valid(ip: str):
    try:
        inet_aton(ip)
        return True
    except socket_error:
        return False

try:
    os.system("clear")
    pyver = sys.version
    verdata = pyver.split(' ')[0].split(".")
    ver_main = int(verdata[0])
    ver_sub = int(verdata[1])
    current_path = "~"
    username = os.getlogin()

    server_thread = None
    server_thread_started = False
    server_host: str | None = None
    server_port: int | None = None

    client_mode = False
    client = None

    nickname = "Anonymous"
    session_id = random.randint(1000000000000000, 9999999999999999)


    if ver_main == 3 and ver_sub >= 10:
        while True:

            if client_mode == True:
                input_prefix = ""
            else:
                input_prefix = f"safe-net@{username} $ {current_path} "

            input_data = input(input_prefix)

            if client_mode == False:
                command = input_data.split(" ")
                arg = " ".join(command[1:])

                if command[0] == "exit":
                    os.system("clear")
                    break

                elif command[0] == "clear" or command[0] == "cls":
                    os.system("clear")

                elif command[0] == "pyver":
                    verdata = pyver.split(' ')[0].split(".")
                    ver_main = int(verdata[0])
                    ver_sub = int(verdata[1])
                    print(f"{ver_main}.{ver_sub}")

                elif command[0] == "server":
                    if len(command) >= 3:
                        host = command[1]
                        port = command[2]

                        if is_ip_valid(host) == True:
                            if port.isdigit() == True:

                                server_host = str(host)
                                server_port = int(port)

                                from safenet.Encryption import ServerConnectionAddr
                                addr = ServerConnectionAddr.encryption()
                                addr.host = str(server_host)
                                addr.port = int(str(server_port))
                                print(f"Server is initialized on {server_host}:{server_port}")
                                print(f"Server connection addr: {addr.get()}")

                                print("\nUse: 'server.start' to run it.")

                                from safenet.Network import Server, RequestsHandler
                                server = Server(host, int(port), RequestsHandler)
                                server_thread = Thread(target=server.start, daemon=True, name="ServerThread")
                                
                            else:
                                print("Port must be a number")
                    else:
                        print("Invalid arguments. Usage: server <host> <port>")

                elif command[0] == "server.start":
                    if server_thread != None:
                        server_thread_started = True
                        server_thread.start()
                        
                        from safenet.Encryption import ServerConnectionAddr
                        addr = ServerConnectionAddr.encryption()
                        addr.host = str(server_host)
                        addr.port = int(str(server_port))
                        print(f"Server is running on {server_host}:{server_port}")
                        print(f"Server connection addr: {addr.get()}")

                    else:
                        print("Server is not initialized. Usage: server <host> <port>")

                elif command[0] == "server.info":
                    if server_thread_started == True:
                        from safenet.Encryption import ServerConnectionAddr

                        addr = ServerConnectionAddr.encryption()
                        addr.host = str(server_host)
                        addr.port = int(str(server_port))

                        print(f"Server is running on {server_host}:{server_port}")
                        print(f"Server connection addr: {addr.get()}")
                    elif server_thread != None:
                        print(f"Server is initialized on {server_host}:{server_port} but not running")
                    else:
                        print("Server is not initialized. Usage: server <host> <port>")

                elif command[0] == "server.stop":
                    if server_thread != None and server_thread_started == True:
                        os.system("clear")
                        server_thread_started = False
                        break
                    else:
                        print("Server is not initialized. Usage: server <host> <port>")

                elif command[0] == "nick":
                    if len(command) >= 2:
                        nickname = arg
                        print(f"Nickname is set to '{nickname}'")
                    else:
                        print("Invalid arguments. Usage: nick <nickname>")

                elif command[0] == "client":
                    if len(command) >= 3:
                        addr = str(command[1]).encode('utf-8')
                        password = command[2]

                        client_mode = True

                        from safenet.Network import Client
                        client = Client(addr, password, session_id)
                        client.start_listener()
                        
                        print(f"Trying to run client: {addr}")

                    else:
                        print("Invalid arguments. Usage: client <host> <port>")

                else:
                    print("Unknown command")
            else:
                if input_data.startswith("!nick"):
                    nickname = input_data.split(" ", 1)[1]
                    print(f"Nickname is set to '{nickname}'")
                else:
                    if client is not None:
                        client.send_message(session_id, nickname, input_data)

    else:
        print("Python version is not supported, required version is 3.10 or later")
except KeyboardInterrupt:
    os.system("clear")
    sys.exit()

# 192.168.1.108 515