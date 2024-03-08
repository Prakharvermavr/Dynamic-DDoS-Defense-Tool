import socket
import threading

HOST = '0.0.0.0'
TCP_PORT = 8888
UDP_PORT = 8889
MAX_CONNECTIONS = 100
MAX_REQUESTS_PER_CONNECTION = 100
MAX_REQUESTS_PER_IP = 10

request_count = {}

def handle_tcp_client(client_socket, client_address):
    global request_count
    client_ip = client_address[0]
    if client_ip in request_count and request_count[client_ip] >= MAX_REQUESTS_PER_IP:
        print(f"Blocked {client_ip} - Exceeded request limit")
        client_socket.close()
        return

    if client_ip in request_count:
        request_count[client_ip] += 1
    else:
        request_count[client_ip] = 1
    for _ in range(MAX_REQUESTS_PER_CONNECTION):
        request = client_socket.recv(1024)
        if not request:
            break
    client_socket.close()
def handle_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((HOST, UDP_PORT))
    print(f"UDP server listening on {HOST}:{UDP_PORT}")
    while True:
        data, address = udp_socket.recvfrom(1024)
def start_tcp_server():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((HOST, TCP_PORT))
    tcp_socket.listen(MAX_CONNECTIONS)
    print(f"TCP server listening on {HOST}:{TCP_PORT}")
    while True:
        client_socket, client_address = tcp_socket.accept()
        print(f"Accepted TCP connection from {client_address[0]}:{client_address[1]}")
        client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, client_address))
        client_thread.start()
tcp_thread = threading.Thread(target=start_tcp_server)
tcp_thread.start()
handle_udp()
