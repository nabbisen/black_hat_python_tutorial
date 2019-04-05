import sys, socket, getopt, threading, subprocess

# global vars
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0
thread_max_num = 5

def usage():
    usage = """
BHP Net Tool

Usage: python bh_netcat.py -t target_host -p port
-l --listen                       - listen on [host]:[port] for
                                    incoming connections
-e --execute=file_to_run          - execute the given file upon
                                    receiving a connection
-c --command                      - initialize a command shell
-u --upload=destination           - upon receiving connection upload a
                                    file and write to [destination]


Examples:
bh_netcat.py -t 192.168.0.1 -p 5555 -l -c
bh_netcat.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe
bh_netcat.py -t 192.168.0.1 -p 5555 -l e \"cat /etc/passwd\"
echo 'ABCDEFGHI' | ./bh_netcat.py -t 192.168.11.12 -p 135
    """
    print(usage)
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            try:
                buffer = bytes(buffer, encoding="utf-8")
            except:
                pass
            client.send(buffer)
        
        while True:
            recv_size = 4096
            recv_len = 1
            res = bytearray()
            while recv_len:
                data = client.recv(recv_size)
                recv_len = len(data)
                res += data

                if recv_len < recv_size:
                    break
            
            print(res.decode("utf-8"))

            buffer = input()
            buffer += "\n"

            client.send(bytes(buffer, encoding="utf-8"))

    except Exception as err:
        print("[*] Exception! [{}]".format(err))
        print("[*] Exiting.")

        client.close()

def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((target, port))
    server.listen(thread_max_num)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True
        )
    except:
        output = "Failed to execute command.\r\n"

    return output

def client_handler(client_socket):
    global upload, execute, command

    if len(upload_destination):
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)
            if len(data) == 0:
                break
            else:
                file_buffer += data
        
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send(
                b"Successfully saved file to {}\r\n".format(upload_destination)
            )
        except:
            client_socket.send(
                b"Failed to save file to {}\r\n".format(upload_destination)
            )

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        prompt = "<BHP:#> "
        client_socket.send(bytes(prompt, encoding="utf-8"))

        while True:
            command_buffer = ""
            while "\n" not in command_buffer:
                command_buffer += client_socket.recv(1024).decode("utf-8")
            res = run_command(command_buffer).decode("utf-8")
            
            res += prompt
            client_socket.send(bytes(res, encoding="utf-8"))

def main():
    global listen, port, execute, command, upload_destination, target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hle:t:p:cu:",
            ["help", "listen", "execute=", "target=", "port=", "command", "upload="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and 0 < port:
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()

main()
            