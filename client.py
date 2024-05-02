import socket
import threading

def handle_incoming_messages(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f"{message}")
        except:
            break
    conn.close()

def start_peer_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Listening for messages on {host}:{port}")
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_incoming_messages, args=(conn, addr)).start()

import socket

def register_with_server(server_ip, server_port, username, my_ip, my_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    s.send(f"REGISTER {username} {my_ip} {my_port}".encode())
    
    # Receive response from the server
    response = s.recv(2048).decode()
    
    # Check if username is already registered
    if response == 'Username already registered':
        print('There is already a user registered with that username')
        s.close()
        return False
    
    # Process greeting if registration is successful
    
    s.close()
    return True


def request_peers(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    s.send(b"LIST")
    full_data = s.recv(4096).decode()
    full_data = full_data.split(',')
    print('Peers on network:')
    for i in range(len(full_data)):
        if i == 0 and len(full_data) != 1:
            user = full_data[i]
            print(f'{i}: {user[1:]}')
        elif i == len(full_data) - 1 and len(full_data) != 1:
            user = full_data[i]
            print(f'{i}: {user[:len(user) - 1]}')
        elif i == len(full_data) - 1 and len(full_data) == 1:
            user = full_data[i]
            print(f'{i}: {user[1:len(user) - 1]}')
        else:
            print(f'{i}: {full_data[i]}')
    s.close()

def request_topic(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    s.send(b"TOPIC")
    topic = s.recv(4096).decode()
    print(f"Welcome to CompsHI! Today's topic is: {topic}")
    s.close()

def request_peer_info(server_ip, server_port, username):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    s.send(f"GET {username}".encode())
    data = s.recv(1024).decode()
    s.close()
    return data

def send_message(ip, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.send(message.encode())
    s.close()

def servexit(server_ip, server_port, username):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    s.send(f"EXIT {username}".encode())
    print('Exited successfully!')
    s.close()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print("Error:", e)
        ip_address = None
    finally:
        s.close()
    return ip_address

def get_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
    except Exception as e:
        print("Error:", e)
        port = None
    finally:
        s.close()
    return port


def main_peer(host, ip, port, server_ip, server_port):
    username = input("Enter your username: ")
    threading.Thread(target=start_peer_server, args=(host, port)).start()
    while register_with_server(server_ip, server_port, username, ip, port) == False:
        username = input("Enter new username: ")
    request_topic(server_ip, server_port)
    
    users = {}

    while True:
        print("\nMenu:")
        print("1. List peers")
        print("2. Get peer info")
        print("3. Send message")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            request_peers(server_ip, server_port)
        elif choice == '2':
            peer_username = input("Enter peer username: ")
            users[peer_username] = request_peer_info(server_ip, server_port, peer_username)
            print(peer_username, users[peer_username])
        elif choice == '3':
            peer_username = input("Enter peer username for message: ")
            exists = users.get(peer_username)
            if exists != None:
                message = input('Enter message:')
                peer_info = users[peer_username]
                ip, port = peer_info.split(':')
                message = (f'\n<<{username}>> {message}')
                send_message(ip, port, message)
            else:
                print("Peer not found")
        elif choice == '4':
            print("Exiting...")
            servexit(server_ip, server_port, username)
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    host, port = get_ip_address(), get_unused_port()
    server_ip, server_port = '10.54.36.155', 12000
    main_peer(host, host, port, server_ip, server_port)