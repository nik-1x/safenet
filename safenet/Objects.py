import json
from .Encryption import Encryption

class Message:
    __slots__ = ('encryption', 'session_id', 'sender', 'message', 'date')

    def __init__(self, encryption, session_id, sender, message, date):
        self.encryption: Encryption = encryption
        self.sender = sender
        self.message = message
        self.date = date
        self.session_id = session_id

    def get(self):        
        if self.sender is not None and self.message is not None and self.date is not None:
            return str(json.dumps({
                "session_id": self.session_id,
                "sender": str(self.sender),
                "message": self.encryption.encrypt(self.message).decode('utf-8'),
                "date": self.date
            })).encode('utf-8')
        else:
            return False