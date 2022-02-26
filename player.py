import sys

import zmq

from ui import *


class Player:
    context = zmq.Context()

    def __init__(self, color: str, controller_url: str, url_where_listening_to_the_controller: str):
        self.color = color
        self.controller_url = controller_url
        self.url_where_listening_to_the_controller = url_where_listening_to_the_controller

        # important variables
        self.start_number = any
        self.box_counter = any
        self.figure = any

        self.table = ''

    def move(self, total):
        for _ in range(total):
            self.box_counter += 1
            if self.box_counter > 31:
                self.box_counter = 0

    def enter_the_game(self):
        socket = self.context.socket(zmq.REQ)
        socket.connect(self.controller_url)
        socket.send_json({
            'color': self.color,
            'url': self.url_where_listening_to_the_controller
        })
        controller_response = socket.recv_json()
        if controller_response['response']:
            self.figure = controller_response['figure']
            self.start_number = controller_response['start_number']
            self.box_counter = self.start_number
            self.play()
        else:
            print('color not allowed or was already chosen by another user')
            print('allowed colors -> (red, yellow, blue, green)')

    def play(self):
        socket_player = self.context.socket(zmq.REP)
        socket_player.bind(f"tcp://*:{self.url_where_listening_to_the_controller}")
        while True:
            UI.clear_console()
            print(f"\nWelcome to the game, player with color:{self.color}, your figure is:{self.figure}\n")
            print("\nanother player's turn, wait your turn\n")

            if self.table:
                UI.print_table(self.table)

            controller_response = socket_player.recv_json()
            if not controller_response['finish_game']:
                if controller_response['your_turn']:
                    dice_1, total = UI.roll_only_one_dice()
                    self.move(total=total)

                    socket_player.send_json(
                        UI.json_prototype(color=self.color, dice_result=total, dice_1=dice_1, total=total,
                                          where_to_put_it=self.box_counter)
                    )

                    controller_response = socket_player.recv_json()
                    self.table = controller_response['board']
                    socket_player.send_string(f"{self.color} received the board")

                else:
                    self.table = (controller_response['board'])
                    socket_player.send_string(f"{self.color} received the board")


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2] and sys.argv[3]:
        Player(sys.argv[1].lower(), sys.argv[2], sys.argv[3]).enter_the_game()
    else:
        print('arguments missing')
