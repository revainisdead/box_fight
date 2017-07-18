import contextlib
import socket
import thread


class Server:
    def __init__(self):
        pass


    @contextlib.contextmanager
    def sock(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 1500))
            s.listen(5)
            yield s


    def serve(self):
        with self.sock() as s:
            while True:
                # Accepts a new connection when it appears.
                # Run this in a new thread, socket.accept is blocking.
                conn, addr = s.accept()


class Client:
    def __init__(self):
        pass


    def setup(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


"""
Ex. 3 peers

Peer1: 192.168.0.1
Peer2: 192.168.0.2
Peer3: 192.168.0.3

Peer1: 192.168.0.1
    Server: connections from
        - 192.168.0.2
        - 192.168.0.3
    Client: connect to
        - 192.168.0.2
        - 192.168.0.3

Peer2: 192.168.0.2
    Server: connections from
        - 192.168.0.1
        - 192.168.0.3
    Client: connect to
        - 192.168.0.1
        - 192.168.0.3

Keep a list of client IPs.

But how to establish the first connection to another peer without the IP?
Have them enter it?
Scan the network for it?

"""
