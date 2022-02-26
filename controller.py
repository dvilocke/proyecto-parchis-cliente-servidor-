import zmq

from board import *
from ui import *


class Controller:
    PLAYER_LIMIT = 2
    ALLOWED_COLORS = ('red', 'yellow', 'blue', 'green')

    color_user = []
    context = zmq.Context()
    finish_game = False

    def __init__(self):
        self.players = [self.context.socket(zmq.REQ) for _ in range(self.PLAYER_LIMIT)]
        self.board = Board()

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
                    'response': True,
                    'start_number': self.board.get_start_criteria(url['color']),
                    'figure': self.board.get_figure(url['color'])
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
                print(f"\nplayer's turn:{self.color_user[color]}")
                socket_user.send_json(UI.json_prototype(self.color_user[color], self.finish_game, True))
                player_response = socket_user.recv_json()
                print(f"{self.color_user[color]} had a result of {player_response['total']} on his dice\n")

                self.board.delete_log()
                self.board.update_table(player_response['color'], player_response['where_to_put_it'])

                # print log messages
                for msg in self.board.logs:
                    print(msg, end='\n')
                    time.sleep(2)

                UI.print_table(self.board.drawing_board)

                # send all players on board
                for socket in self.players:
                    socket.send_json(UI.json_prototype(' ', False, False, board=self.board.drawing_board))
                    print(socket.recv_string(), end='\n')


if __name__ == '__main__':
    Controller().hear_players()
