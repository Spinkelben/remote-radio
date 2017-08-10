import socket, os, threading

def echo_data(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
    conn.close()


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
  os.remove('/tmp/chatter-sock')
except OSError:
  pass
s.bind('/tmp/chatter-sock')
s.listen(5)
while True:
  conn, addr = s.accept()
  print("Accepted Conenction from {}", addr)
  t = threading.Thread(target=echo_data, kwargs={"conn": conn, "addr": addr})
  t.start()
