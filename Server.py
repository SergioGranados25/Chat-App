import socket
import threading
import sys

def handle_peer(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data.startswith('REGISTER'):
                print(peers)
                print(data)
                _, username, ip, port = data.split()
                addr = [ip, port]
                peers[username] = addr
                print(username)
                print(peers)
                
            elif data == 'LIST':
                users = list(peers.keys())
                conn.sendall(str(users).encode())
                print('test')
            elif data.startswith('GET'):
                _, username = data.split()
                peer_info = peers.get(username, None)
                if peer_info:
                    conn.sendall(f"{peer_info[0]}:{peer_info[1]}".encode())
                else:
                    conn.sendall(b'Not found')
            elif data.startswith('EXIT'):
                _, username = data.split()
                print(data)
                print(username)
                peers.pop(username)
                print(peers)
        except:
            break
    conn.close()

def server():
    host = '10.54.36.155'
    port = 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_peer, args=(conn, addr)).start()
        #print(peers)


peers = {}
server_thread = threading.Thread(target=server)
server_thread.start()
