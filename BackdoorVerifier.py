import socket

host = 'your_server_ip' # replace with your server IP
port = your_port_number # replace with the port you have set for the reverse shell

def check_reverse_shell(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        print("Reverse shell is working!")
        s.close()
    except:
        print("Reverse shell is not working.")

check_reverse_shell(host, port)
