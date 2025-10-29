import os
import threading

from broker import Client, Broker

BROKER_IP = os.getenv("BROKER_IP", "127.0.0.1")
BROKER_PORT = os.getenv("BROKER_PORT", "8080")

LISTEN_PORT = os.getenv("LISTEN_PORT", "8081")
PLAYER = os.getenv("PLAYER", "X")

SERVER_TYPE = os.getenv("SERVER_TYPE", "game")

if __name__ == "__main__":
    if SERVER_TYPE == "game":
        from game import TicTacToe

        client = Client(PLAYER, BROKER_IP, int(BROKER_PORT), int(LISTEN_PORT))
        game = TicTacToe(PLAYER, client)

        threading.Thread(target=client.listen, args={game.on_receive, }, daemon=True).start()

        game.main()
    else:
        broker = Broker(BROKER_IP, int(BROKER_PORT))

        threading.Thread(target=broker.start).start()


