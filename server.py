import socket
import threading
from typing import Callable

class Server:
    def __init__(self, recv_port, send_port, host):
        self.recv_port = recv_port
        self.send_port = send_port
        self.host = host

        print(f"Host - {host} Send  {send_port} Recv {recv_port}")

    def listen(self, callback: Callable[[str], None]):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.recv_port))
            s.listen()
            print(f"[Server] Listening on port {self.recv_port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.__recieve, args=(conn, callback), daemon=True).start()

    def __recieve(self, conn, callback: Callable[[str], None]):
        with conn:
            while True:
                data = conn.recv(128)
                if not data: break
                print(f"[Server] Received: {data.decode()}")
                callback(data.decode())

    def send(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.send_port))
            s.sendall(data.encode())
            print(f"[Server] Send data {data} to {self.send_port}")
