import sys, socket, threading

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2
    for i in range(0, len(src), length):
        s = src[i:(i + length)]
        hexa = " ".join(map("{0:0>2X}".format, src))
        text = "".join([chr(x) if 0x20 <= x < 0x7F else "." for x in s])
        result.append("%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text) )
    return "\n".join(result)

def receive_from(connection):
    timeout_seconds = 3
    receive_size = 4096

    buffer = b""

    connection.settimeout(timeout_seconds)

    try:
        while True:
            data = connection.recv(receive_size)
            if not data:
                break
            buffer += data
    except:
        pass
    
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)

        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print("[<==] Sending {} bytes to localhost.".format(len(remote_buffer)))
            
            client_socket.send(remote_buffer)
        
    while True:
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received {} bytes from localhost.".format(len(local_buffer)))
            
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)

            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Received {} bytes from remote.".format(len(remote_buffer)))

            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len (remote_buffer):
            print("[*] No more data. Closing connections.")

            client_socket.close()
            remote_socket.close()

            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    thread_max_num = 5

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((local_host, local_port))
    except:
        print("""
[!!] Failed to listen on {}:{}
[!!] Check for other listening sockets or correct permissions.
        """.format(local_host, local_port))
        sys.exit(0)
    
    print("[*] Listening on {}:{}".format(local_host, local_port))

    server.listen(thread_max_num)
    
    while True:
        client_socket, addr = server.accept()
        
        print("[==>] Received incoming connection from {}:{}".format(addr[0], addr[1]))

        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("""
Usage: python ./bh_tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]
Example: python ./bh_tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True
        """)
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    receive_first = "True" in receive_first

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)    

main()
