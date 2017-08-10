import socket
import os
import threading


class CommandServer():
    def __init__(self, address, action, num_connections=5):
        """ action must be a callable which takes a message and returns a response
        """
        self.address = address
        self.num_connections = num_connections
        self.action = action
        self.daemon = None
        self.action = action

    def __enter__(self):
        print("Creating server on socket adress {}".format(self.address))
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(self.num_connections)
        self.daemon = threading.Thread(target=self._loop, daemon=True)
        self.daemon.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing command server...")
        self.socket.close()
        os.remove(self.address)
        print("Command server closed")

    def _recieve_message(self, conn, addr):
        message = []
        # Recieve all data
        while True:
            data = conn.recv(4096)
            if not data: break
            message.append(data)

        message = b''.join(message)
        response = self.action(message)
        if response:
            conn.send(response)
        conn.close()

    def _loop(self):
        while True:
            print("Waiting for conenctions")
            conn, addr = self.socket.accept()
            print("Accepted connection")
            t = threading.Thread(target=self._recieve_message, kwargs={"conn": conn, "addr": addr})
            t.start()
