import zmq

from ui import *


class Controller:
    PLAYER_LIMIT = 2
    ALLOWED_COLORS = ('red', 'yellow', 'blue', 'green')

    color_user = []
    context = zmq.Context()
    finish_game = False

    def __init__(self):
        self.players = [self.context.socket(zmq.REQ) for _ in range(self.PLAYER_LIMIT)]

    def check_color(self, color) -> bool:
        return color in self.ALLOWED_COLORS and color not in self.color_user

    def hear_players(self):
        counter = 0
        socket = self.context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        while counter != self.PLAYER_LIMIT:
            url = socket.recv_json()
            if self.check_color(url['color']):
                self.players[counter].connect(f"tcp://localhost:{url['url']}")
                self.color_user.append(url['color'])
                socket.send_json({
                    'response': True
                })
                counter += 1
            else:
                socket.send_json({
                    'response': False
                })

        self.play()

    def play(self):
        while not self.finish_game:
            for color, socket_user in enumerate(self.players):
                print(f"player's turn:{self.color_user[color]}")
                socket_user.send_json(UI.json_prototype(self.color_user[color], self.finish_game, True))
                player_response = socket_user.recv_json()


if __name__ == '__main__':
    Controller().hear_players()
