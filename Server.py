import socket
import sys
import threading


IP = '127.0.0.1'  
PORT = 12000  

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f'Server ready and listening on {ip}:{port}')


if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        IP = sys.argv[1] 

    start_server(IP, PORT)