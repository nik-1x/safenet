import hashlib, random

class User(object):

    __slots__ = ('username', 'session_id', 'chat_formatting', 'password')
    
    def __init__(self, username: str, password: str, chat_formatting: str="%name: %msg"):
        self.username = username
        self.session_id = hashlib.md5(
                str(
                    random.randint(
                        int("10"*100), 
                        int("99"*100)
                    )
                ).encode('utf-8')
            ).hexdigest()
        self.chat_formatting = chat_formatting
        self.password = password.encode('utf-8')


class Message(object):

    __slots__ = ('text', 'session_id', 'nickname')

    def __init__(self, 
        user: User,
        text: str = "",
        session_id: str = "",
        nickname: str = ""
        ):
        self.text = text
        self.session_id = session_id
        self.nickname = nickname

    def import_data(self, data: dict):
        if 'text' in data:
            self.text = data['text']
        else: return False

        if 'session_id' in data:
            self.session_id = data['session_id']
        else: return False

        if 'nickname' in data:
            self.nickname = data['nickname']
        else: return False

        return True

    def export_data(self):
        return {
            'text': str(self.text),
            'session_id': str(self.session_id),
            'nickname': str(self.nickname)
        }
    