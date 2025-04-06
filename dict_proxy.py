import socket
from typing import List

def is_response_complete(response):
    return (b"250" in response or b"220" in response or b"221" in response) and response[-2:] == b"\r\n"

def make_dict_request(commands: List[str], server: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))

    responses = []
    # Receive server header
    received = sock.recv(1024)
    while not is_response_complete(received):
        received += sock.recv(1024)
    responses.append(received.decode())

    # Send commands and receive output
    for command in commands:
        sock.sendall(command.encode() + b"\n")
        received = sock.recv(1024)
        while not is_response_complete(received):
            received += sock.recv(1024)
        responses.extend(received.decode().split("\n"))

    sock.sendall(b"QUIT\n")
    received = sock.recv(1024)
    while not is_response_complete(received):
        received += sock.recv(1024)
    responses.append(received.decode())
    sock.close()
    return responses
