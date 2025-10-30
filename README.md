# Tick-tack toe

---

Created by [Brouse_13](https://github.com/Brouse13)

## 📖 Project Description

---

Tick-tack toe is a project designed to test publish-subscribe (pub/sub) communication using a message broker that manages all exchanges between clients.
Each client can publish messages on a topic and subscribe to receive updates — simulating a real-time multiplayer communication system (like in a Tic-Tac-Toe game).

## 📌 How to Run the Project

---
The project works with **uv** as python environment, the first step is to install all the dependencies, to do it you'll have to run
the following command:
````shell
  uv init
  uv sync
````

Then, you will need to start the broker to make the communication possible between both clients
````shell
  uv run main.py --env env/broker.env
````

And finally each client that wants to use on the communication
````shell
  uv run main.py --env env/cli1.env
  uv run main.py --env env/cli2.env
````

## 📝 Versions
### 1.0.0
- First release version