import socket, os, threading
import message_pb2

class CommandServer():
    def __init__(self, address, num_connections=5):
        self.address = address
        self.num_connections = num_connections

    def __enter__(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.listen(self.num_connections)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.socket.close()
        os.remove(self.address)

    def accept(self):
        conn, addr = self.socket.accept()
