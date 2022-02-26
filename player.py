import sys

import zmq

from ui import *

ALLOWED_COLORS = ['red', 'yellow', 'blue', 'green']


class Player:
    context = zmq.Context()

    def __init__(self, color: str, controller_url: str, url_where_listening_to_the_controller: str):
        self.color = color
        self.controller_url = controller_url
        self.url_where_listening_to_the_controller = url_where_listening_to_the_controller

    def enter_the_game(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect(self.controller_url)
        socket.send_json({
            'color': self.color,
            'url': self.url_where_listening_to_the_controller
        })
        controller_response = socket.recv_json()
        if controller_response['response']:
            self.play()
        else:
            print('color not allowed or was already chosen by another user')
            print('allowed colors -> (red, yellow, blue, green)')

    def play(self):
        socket_player = self.context.socket(zmq.REP)
        socket_player.bind(f"tcp://*:{self.url_where_listening_to_the_controller}")
        while True:
            UI.clear_console()
            print(f"\nWelcome to the game, player with color:{self.color}\n")
            print("\nanother player's turn, wait your turn\n")
            controller_response = socket_player.recv_json()
            if not controller_response['finish_game']:
                if controller_response['your_turn']:
                    total = UI.throw_dice()
                    socket_player.send_json(UI.json_prototype(self.color, False, total))
                else:
                    pass


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2] and sys.argv[3]:
        Player(sys.argv[1], sys.argv[2], sys.argv[3]).enter_the_game()
    else:
        print('arguments missing')
