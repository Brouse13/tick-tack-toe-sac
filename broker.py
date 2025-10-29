from socket import socket, AF_INET, SOCK_DGRAM
from typing import Callable


# ---------------- CLIENT ----------------
class Client:
    def __init__(self, name: str, broker_ip: str, broker_port: int, listen_port: int):
        self.name = name
        self.broker_addr = (broker_ip, broker_port)
        self.listen_addr = ('', listen_port)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(self.listen_addr)

    def subscribe(self, topic: str):
        msg = f"SUBSCRIBE {self.name} {topic} {self.listen_addr[1]}"
        self.sock.sendto(msg.encode(), self.broker_addr)

    def publish(self, topic: str, message: str):
        msg = f"PUBLISH {topic} {message}"
        self.sock.sendto(msg.encode(), self.broker_addr)

    def listen(self, callback: Callable[[str], None]):
        print(f"[{self.name}] Listening for messages on UDP port {self.listen_addr[1]}...")
        while True:
            data, _ = self.sock.recvfrom(4096)
            callback(data.decode())
            print(f"[{self.name}] Received:", data.decode())


# ---------------- BROKER ----------------
class Broker:
    def __init__(self, host: str = '0.0.0.0', port: int = 9999):
        self.addr = (host, port)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.topics: dict[str, list[tuple[str, int]]] = {}  # topic -> [(ip, port)]

    def start(self):
        self.sock.bind(self.addr)
        print(f"[BROKER] Listening on {self.addr}")

        while True:
            data, client_addr = self.sock.recvfrom(1024)
            msg = data.decode().split(' ', 3)
            cmd = msg[0].upper()

            if cmd == "SUBSCRIBE":
                _, name, topic, port = msg
                self.topics.setdefault(topic, []).append((client_addr[0], int(port)))
                print(f"[BROKER] {name} subscribed to {topic}")

            elif cmd == "PUBLISH":
                _, topic, message = data.decode().split(' ', 2)
                self.publish(topic, message)

    def publish(self, topic: str, message: str):
        if topic not in self.topics:
            print(f"[BROKER] No subscribers for topic '{topic}'")
            return

        print(f"[BROKER] Publishing '{message}' to topic '{topic}'")
        for (ip, port) in self.topics[topic]:
            self.sock.sendto(f"{topic} {message}".encode(), (ip, port))