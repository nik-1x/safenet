import hashlib
import json
import socket
import socketserver
import sys
from threading import Thread
from .Encryption import Encryption

class RequestsHandler(socketserver.BaseRequestHandler):

    storage = []

    def handle(self):
        socket = self.request[1]            # socket
        client_addr = self.client_address   # client ip and port
        sent_data = self.request[0].strip() # data sent by client

        if client_addr not in self.storage:
            self.storage.append(client_addr)
        else:
            for socket_ in self.storage:
                print('[SERVER]', sent_data)
                socket.sendto(sent_data, socket_)

class Server:

    __slots__ = ('server')
    
    def __init__(self, host, port, handler):
        self.server = socketserver.UDPServer((host, port), handler)

    def start(self):
        self.server.serve_forever()

class Client:

    __slots__ = ('enc', 'host', 'port', 'socket', 'session_id')

    def __init__(self, addr, password, session_id):
        from safenet.Encryption import ServerConnectionAddr

        self.session_id = session_id

        addr = ServerConnectionAddr.decryption(addr)

        self.host, self.port = addr.get()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.sendto("PING".encode("utf-8"), (self.host, self.port))

        from safenet.Encryption import Encryption
        self.enc = Encryption(password)

    def listener(self, socket, enc: Encryption):
        while True:
            data, server = self.socket.recvfrom(4096)
            value = json.loads(data.decode('utf-8'))
            if value["session_id"] != self.session_id:
                print(value["sender"] + ": "+ enc.decrypt(value["message"].encode('utf-8')))

    def start_listener(self):
        listener_ = Thread(target=self.listener, args=(self.socket, self.enc, ))
        listener_.start()

    def send_message(self, session_id, user, message):
        from .Objects import Message

        message = Message(
            encryption=self.enc,
            session_id=session_id,
            sender=user,
            message=message,
            date="test"
        ).get()

        if message is not False:    
            self.socket.sendto(message, (self.host, self.port))
        else:
            print("Message is not valid")
    