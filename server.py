from safenet.encryption import Addr
from safenet.network import Server
import pyperclip

addr = Addr(
    ip="0.0.0.0",
    port=5125
)

connection_address = addr.ip2addr()

if connection_address is not False:
    print("Server stared\n")
    print("Connection addr: \n"+connection_address)
    print("\nAddress copied to clipboard")

    pyperclip.copy(connection_address)

    srv = Server(addr)
    srv.start()