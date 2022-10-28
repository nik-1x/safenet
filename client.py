from safenet.encryption import Addr
from safenet.network import Client
from safenet.object import User

addr = Addr(
    addr="Y2ZjZDIwODQ5NWQ1NjVlZjY2ZTdkZmY5Zjk4NzY0ZGE6Y2ZjZDIwODQ5NWQ1NjVlZjY2ZTdkZmY5Zjk4NzY0ZGE6Y2ZjZDIwODQ5NWQ1NjVlZjY2ZTdkZmY5Zjk4NzY0ZGE6Y2ZjZDIwODQ5NWQ1NjVlZjY2ZTdkZmY5Zjk4NzY0ZGE=",
    port=5125
)

client = Client(address=addr, user=User(username="Anon", password="fhaiuwhfiuafwhiaufhifwhi"))
client.listener()

while True:
    client.sendMessage(input(), client.addr)