import socket



while True:
    data = input()
    if data == '':
        break
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/tmp/chatter-sock')
    s.send(str.encode(data))
    data = s.recv(1024)
    print('Received ' + data.decode())
    s.close()
