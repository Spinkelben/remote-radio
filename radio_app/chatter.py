import socket, os, threading
from command_server import CommandServer

def echo_data(message):
    return message

with CommandServer(address='/tmp/chatter-sock', action=echo_data):
    print("Press enter to close")
    input()
