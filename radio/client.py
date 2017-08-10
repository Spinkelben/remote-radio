import socket



while True:
    data = input()
    if data == '':
        break
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/tmp/chatter-sock')
    s.send(str.encode(data))
    s.shutdown(socket.SHUT_WR)
    message = []

    while True:
        data = s.recv(1024)
        if not data: break
        message.append(data)
    message = b''.join(message)
    print('Received ' + message.decode())
    s.close()
