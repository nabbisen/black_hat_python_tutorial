import sys, threading, subprocess
import paramiko

def ssh_command(host, port, user, passwd, command):
    client = paramiko.SSHClient()
    ## public key authentication 
    #client.load_host_keys('/home/user/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=passwd, allow_agent=False)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return

def main():
    if len(sys.argv[1:]) != 5:
        print("[!!] Invalid arguments: host, port, username, password, command text are required.")
        sys.exit(0)
    
    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    command = sys.argv[5]

    ssh_command(host, port, user, passwd, command)

main()
