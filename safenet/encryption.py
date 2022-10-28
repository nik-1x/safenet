from base64 import b64encode as b64e
from base64 import b64decode as b64d
from hashlib import md5
from socket import inet_aton
from socket import error as socket_error
import json

class Addr(object):

    __slots__ = ('ip', 'port', 'addr', 'mappings')

    def __init__(self, ip:str="", port:int=-1, addr:str="", mappings_file:str="mappings.data"):
        self.ip, self.port, self.addr = ip, port, addr
        try:
            with open(mappings_file, 'rb') as file:
                self.mappings = json.loads(b64d(file.read()).decode('utf-8'))
                file.close()
        except:
            print("Mappings are incorrect.")

    def addr2ip(self):
        if self.addr != "" and self.port != -1 and self.addr is not None and self.port is not None:
            def search(val):
                for s in self.mappings:
                    if self.mappings[s] == val:
                        return s
            return (".".join(list(map(str, [search(ip_elem) for ip_elem in b64d(self.addr.encode('utf-8')).decode('utf-8').split(":")]))), self.port)  # type: ignore
        else:
            return False
        
    def ip2addr(self):
        if self.ip != "" and self.port != -1 and self.ipCheckValid():
            return b64e(str(":".join([self.mappings[ip_elem] for ip_elem in self.ip.split(".")])).encode('utf-8')).decode('utf-8')+":"+str(self.port)
        else:
            return False
        
    def ipCheckValid(self) -> bool:
        try:
            inet_aton(self.ip)
            return True
        except socket_error:
            return False
