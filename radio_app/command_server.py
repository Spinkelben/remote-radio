import socket
import os
import threading
import logging


class CommandServer():
    def __init__(self, address, action, num_connections=5):
        """ action must be a callable which takes a message and returns a response
        """
        self.address = address
        self.num_connections = num_connections
        self.action = action
        self.daemon = None

    def __enter__(self):
        logging.info("Creating server on socket adress {}".format(self.address))
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.socket.bind(self.address)
        except OSError:
            logging.warn("File already in use, deleting")
            os.remove(self.address)
            self.socket.bind(self.address)
        self.socket.listen(self.num_connections)
        self.daemon = threading.Thread(target=self._loop, daemon=True)
        self.daemon.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info("Closing command server...")
        self.socket.close()
        os.remove(self.address)
        logging.info("Command server closed")

    def _recieve_message(self, conn, addr):
        logging.debug("Recieving command")
        message = []
        # Recieve all data
        while True:
            data = conn.recv(4096)
            if not data: break
            message.append(data)

        message = b''.join(message)
        logging.debug("Command Recieved")
        response = self.action(message)
        if response:
            conn.send(response)
        conn.close()

    def _loop(self):
        while True:
            logging.info("Waiting for conenctions")
            conn, addr = self.socket.accept()
            logging.info("Accepted connection")
            t = threading.Thread(target=self._recieve_message, kwargs={"conn": conn, "addr": addr})
            t.start()
