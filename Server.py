import socket
import threading
import sys
import random

topics_in_computer_science = [
    "Algorithms",
    "Data Structures",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Robotics",
    "Expert Systems",
    "Knowledge Representation and Reasoning",
    "Search Algorithms",
    "Sorting Algorithms",
    "Graph Theory",
    "Cryptography",
    "Blockchain Technology",
    "Cybersecurity",
    "Network Protocols",
    "Operating Systems",
    "Distributed Systems",
    "Cloud Computing",
    "Virtualization",
    "Parallel Computing",
    "Compilers",
    "Interpreters",
    "Programming Languages",
    "Software Engineering",
    "Agile Development",
    "DevOps",
    "Continuous Integration and Continuous Deployment (CI/CD)",
    "Version Control Systems (e.g., Git)",
    "Web Development",
    "Frontend Development",
    "Backend Development",
    "Full-Stack Development",
    "Mobile Development",
    "Game Development",
    "Computer Graphics",
    "Human-Computer Interaction (HCI)",
    "User Interface Design",
    "User Experience (UX) Design",
    "Responsive Web Design",
    "Accessibility in Computing",
    "Big Data",
    "Data Mining",
    "Data Warehousing",
    "Database Management Systems (DBMS)",
    "SQL and NoSQL Databases",
    "Relational Database Design",
    "Entity-Relationship Modeling",
    "Distributed Databases",
    "Data Analytics",
    "Business Intelligence",
    "Data Visualization",
    "Statistical Analysis",
    "Cloud Databases",
    "Edge Computing",
    "Internet of Things (IoT)",
    "Embedded Systems",
    "Microcontrollers",
    "Real-Time Systems",
    "Quantum Computing",
    "Quantum Algorithms",
    "Quantum Cryptography",
    "Quantum Machine Learning",
    "Quantum Information Theory",
    "Computational Biology",
    "Bioinformatics",
    "Computational Chemistry",
    "Computational Physics",
    "Computational Neuroscience",
    "Computational Social Science",
    "Computational Linguistics",
    "Evolutionary Computing",
    "Genetic Algorithms",
    "Neural Networks",
    "Fuzzy Logic",
    "Evolutionary Algorithms",
    "Swarm Intelligence",
    "Game Theory",
    "Computational Complexity Theory",
    "P vs NP Problem",
    "NP-Completeness",
    "Computational Geometry",
    "Finite Element Analysis",
    "Numerical Analysis",
    "Symbolic Computation",
    "Computer Algebra Systems",
    "High-Performance Computing",
    "Grid Computing",
    "Quantum Computing",
    "Green Computing",
    "Internet Technologies",
    "Web Security",
    "Web Services",
    "RESTful APIs",
    "GraphQL",
    "Microservices",
    "Scalability",
    "Fault Tolerance",
    "Performance Optimization"
]

topic = random.choice(topics_in_computer_science)

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
                
                if peers.get(username) != None:
                    conn.sendall(b'Username already registered')
                else:
                    addr = [ip, port]
                    peers[username] = addr
                    print(username)
                    print(peers)
                    conn.sendall(b'Registered succesfully')
                
            elif data == 'LIST':
                users = list(peers.keys())
                conn.sendall(str(users).encode())
                print('test')
            elif data == 'TOPIC':
                conn.send(f"{topic}".encode())
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