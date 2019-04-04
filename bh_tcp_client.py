import socket

target_host = "127.0.0.1"
target_port = 9999
send_data = b"GET /?param=test HTTP/1.1\r\nHost: localhost\r\n\r\n"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))
client.send(send_data)
res = client.recv(4096)

print(res)
