import socketserver
import socket
from .encryption import Addr
from .object import Message, User
from threading import Thread
import json

class Server(object):

    __slots__ = ('server')

    class Handler(socketserver.BaseRequestHandler):
        storage = []

        def handle(self):
            socket = self.request[1]            # socket
            client_addr = self.client_address   # client ip and port
            sent_data = self.request[0].strip() # data sent by client

            if client_addr not in self.storage:
                self.storage.append(client_addr)
            else:
                for socket_ in self.storage:
                    socket.sendto(sent_data, socket_)

    def __init__(self, address: Addr):
        addr = (address.ip, address.port)

        if addr is not False:
            self.server = socketserver.UDPServer(addr, self.Handler)
        else:
            raise Exception

    def start(self):
        thread = Thread(target=self.server.serve_forever(), daemon=True, name="ServerThread")
        thread.start()

class Client(object):

    __slots__ = ('user', 'addr', 'socket')

    def __init__(self, address: Addr, user: User):
        self.addr = address.addr2ip()
        self.user = user

        if self.addr is not False:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.sendto("PING".encode("utf-8"), self.addr)
        else:
            raise Exception
        

    def listener(self):
        def action(socket):
            while True:
                data, server = socket.recvfrom(4096)
                message = Message(user=self.user)
                message.import_data(json.loads(data.decode("utf-8")))

                if message.session_id != self.user.session_id:
                    format_message = self.user.chat_formatting
                    format_message = format_message.replace("%name", message.nickname)
                    format_message = format_message.replace("%msg", message.text)
                    print(format_message)

        listener_ = Thread(target=action, args=(self.socket, ), daemon=True, name="ListenerThread")
        listener_.start()
        
    def sendMessage(self, data: str, addr):
        message = json.dumps(Message(
                user=self.user,
                text=data,
                session_id=self.user.session_id,
                nickname=self.user.username
            ).export_data()).encode('utf-8')
        self.socket.sendto(message, addr)