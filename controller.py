import zmq
from ui import *

class Controller:
    PLAYER_LIMIT = 2
    usernames = []
    context = zmq.Context()
    finish_game = False

    def __init__(self):
        self.players = [self.context.socket(zmq.REQ) for _ in range(self.PLAYER_LIMIT)]

    def hear_players(self):
        socket = self.context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        for socket_user in self.players:
            url = socket.recv_json()
            socket_user.connect(f"tcp://localhost:{url['url']}")
            self.usernames.append(url['name'])
            socket.send_json({
                'response': f"welcome to the game:{url['name']}"
            })

        self.play()

    def play(self):
        while not self.finish_game:
            for id_name, socket_user in enumerate(self.players):
                print(f"player's turn:{self.usernames[id_name]}")
                socket_user.send_json(UI.json_prototype(self.usernames[id_name], self.finish_game, True))
                player_response = socket_user.recv_json()


if __name__ == '__main__':
    Controller().hear_players()