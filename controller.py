import zmq

class Controller:
    PLAYER_LIMIT = 1
    context = zmq.Context()

    def __init__(self):
        self.players = [self.context.socket(zmq.REQ) for _ in range(self.PLAYER_LIMIT)]

    def hear_players(self):
        socket = self.context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        for socket_user in self.players:
            url = socket.recv_json()
            print(url)
            socket_user.connect(f"tcp://localhost:{url['url']}")
            socket.send_json({
                'response': True
            })

        self.play()

    def play(self):
        for socket_user in self.players:
            socket_user.send_json({
                'response' : True
            })
            m = socket_user.recv_json()
            print(m['response'])



if __name__ == '__main__':
    Controller().hear_players()