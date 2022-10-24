from base64 import b64encode as b64e
from base64 import b64decode as b64d
from dataclasses import dataclass
import hashlib
from cryptography.fernet import Fernet


class Encryption:
    """
    Key = b64(sha3_256(Password))
    """
    __slots__ = ('key')

    def __init__(self, key):
        self.key = b64e(
            hashlib.md5(
                hashlib.sha3_512(
                    key.encode('utf-8')
                ).hexdigest().encode('utf-8')
            ).hexdigest().encode('utf-8')
        )

    def encrypt(self, data):
        return Fernet(self.key).encrypt(data.encode('utf-8'))
    
    def decrypt(self, data):
        return Fernet(self.key).decrypt(data).decode('utf-8')
    

class ServerConnectionAddrEncryption:
    host: str = "0.0.0.0"
    port: int = 51251

    def get(self):
        return b64e((
            b64e((str(self.host)).encode('utf-8')).decode('utf-8') \
            + ":" \
            + b64e((str(self.port)).encode('utf-8')).decode('utf-8')
        ).encode('utf-8')).decode('utf-8')
    

class ServerConnectionAddrDecryption:
    addr: str

    def __init__(self, addr):
        self.addr = addr

    def get(self):
        decoded = b64d(self.addr).decode('utf-8').split(":")
        host = b64d(decoded[0].encode('utf-8')).decode('utf-8')
        port = int(b64d(decoded[1].encode('utf-8')).decode('utf-8'))
        return host, port

@dataclass
class ServerConnectionAddr:
    encryption = ServerConnectionAddrEncryption
    decryption = ServerConnectionAddrDecryption