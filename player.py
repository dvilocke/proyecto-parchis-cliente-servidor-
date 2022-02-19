import zmq
import sys


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
        if controller_response['response']:
            self.play()

    def play(self):
        socket_player = self.context.socket(zmq.REP)
        socket_player.bind(f"tcp://*:{self.url_where_listening_to_the_controller}")
        controller_response = socket_player.recv_json()
        if controller_response['response']:
            print('funciona')
            socket_player.send_json({
                'response' : 'funciona'
            })


if __name__ == '__main__':
    Player('Miguel', sys.argv[1], sys.argv[2]).enter_the_game()