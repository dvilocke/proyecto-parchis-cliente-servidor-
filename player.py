import zmq
import sys
from ui import *

class Player:
    context = zmq.Context()

    def __init__(self, name:str, controller_url:str, url_where_listening_to_the_controller:str):
        self.name = name
        self.controller_url = controller_url
        self.url_where_listening_to_the_controller = url_where_listening_to_the_controller

    def enter_the_game(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect(self.controller_url)
        socket.send_json({
            'name' : self.name,
            'url': self.url_where_listening_to_the_controller
        })
        controller_response = socket.recv_json()
        self.play(controller_response['response'])

    def play(self, msg):
        socket_player = self.context.socket(zmq.REP)
        socket_player.bind(f"tcp://*:{self.url_where_listening_to_the_controller}")
        while True:
            UI.clear_console()
            print(msg)
            print("\nanother player's turn, wait your turn\n")
            controller_response = socket_player.recv_json()
            if not controller_response['finish_game']:
                if controller_response['your_turn']:
                    total = UI.throw_dice()
                    socket_player.send_json(UI.json_prototype(self.name, False, total))
                else:
                    pass

if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2] and sys.argv[3]:
        Player(sys.argv[1], sys.argv[2], sys.argv[3]).enter_the_game()
    else:
        print('arguments missing')
