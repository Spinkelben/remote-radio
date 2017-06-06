import socket, os

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
  os.remove('/tmp/chatter-sock')
except OSError:
  pass
s.bind('/tmp/chatter-sock')
s.listen(1)
conn, addr = s.accept()
while True:
  data = conn.recv(1024)
  if not data: break
  conn.send(data)
conn.close()

