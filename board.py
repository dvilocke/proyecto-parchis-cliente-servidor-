class Board:
    drawing_board = [
        ['#', ' ', ' ', '*', '?', '*', ' ', ' ', '#'],
        ['#', ' ', ' ', '1', ' ', '?', ' ', ' ', '#'],
        ['#', '#', '#', '*', ' ', '*', '#', '#', '#'],
        ['*', '?', '*', '*', ' ', '*', '*', '4', '*'],
        ['?', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '?'],
        ['*', '2', '*', '*', ' ', '*', '*', '?', '*'],
        ['#', ' ', ' ', '*', ' ', '*', ' ', ' ', '#'],
        ['#', ' ', ' ', '?', ' ', '3', ' ', ' ', '#'],
        ['#', '#', '#', '*', '?', '*', '#', '#', '#'],
    ]

    jail = []

    logs = []

    INSURANCE_POLICIES = [31, 1, 5, 7, 9, 13, 15, 17, 21, 23, 25, 29]

    INSURANCE_COORDINATE = [(0, 4), (4, 0), (8, 4), (4, 8), (1, 3), (3, 1), (5, 1), (7, 3), (7, 5), (5, 7), (3, 7),
                            (1, 5)]

    GENERAL_COORDINATES = {
        'red': [
            {
                'exit': 1,
                'full_turn': 31,
                'figure': '1'
            }
        ],
        'yellow': [
            {
                'exit': 9,
                'full_turn': 7,
                'figure': '2'
            }
        ],
        'blue': [
            {
                'exit': 17,
                'full_turn': 15,
                'figure': '3'
            }
        ],
        'green': [
            {
                'exit': 25,
                'full_turn': 23,
                'figure': '4'
            }
        ]
    }

    list_with_chordates = {
        0: (0, 3),
        1: (1, 3),
        2: (2, 3),
        3: (3, 3),
        4: (3, 2),
        5: (3, 1),
        6: (3, 0),
        7: (4, 0),
        8: (5, 0),
        9: (5, 1),
        10: (5, 2),
        11: (5, 3),
        12: (6, 3),
        13: (7, 3),
        14: (8, 3),
        15: (8, 4),
        16: (8, 5),
        17: (7, 5),
        18: (6, 5),
        19: (5, 5),
        20: (5, 6),
        21: (5, 7),
        22: (5, 8),
        23: (4, 8),
        24: (3, 8),
        25: (3, 7),
        26: (3, 6),
        27: (3, 5),
        28: (2, 5),
        29: (1, 5),
        30: (0, 5),
        31: (0, 4),
    }

    def __init__(self):
        self.a_player_is_eliminated = False

    def get_figure(self, color):
        # this function returns the figure corresponding to each player
        return self.GENERAL_COORDINATES[color][0]['figure']

    def get_start_criteria(self, color):
        # this function allows me to know the starting index of each player according to their color
        return self.GENERAL_COORDINATES[color][0]['exit']

    def __get_color(self, figure):
        for key, value in self.GENERAL_COORDINATES.items():
            for dictionary in value:
                if dictionary['figure'] == figure:
                    return key

    def __eat(self, figure, color, where_to_put_it):
        # function to eat other chips
        offset_coordinate = self.list_with_chordates[where_to_put_it]
        x, y = offset_coordinate
        if self.drawing_board[x][y] != '*' and self.drawing_board[x][y] != figure and self.drawing_board[x][y] != '?':
            if not (x, y) in self.INSURANCE_COORDINATE:
                # a chip is there
                figure_to_remove = self.drawing_board[x][y]
                color_to_remove = self.__get_color(figure_to_remove)

                self.__add_log(msg=f"the {color} kill color:{color_to_remove}, figure:{figure_to_remove}")

                self.jail.append(color_to_remove)

                self.__add_log(msg=f"the color {color_to_remove} was sent to jail")

                self.__delete_current_position(coordinate=(x, y))

            else:
                self.__add_log(msg=f"the {color} don't kill anyone")
        else:
            self.__add_log(msg=f"the {color} don't kill anyone")

    def __delete_current_position(self, coordinate):
        # function to delete the current position, that is, where the figure is located I put another character
        if coordinate in self.INSURANCE_COORDINATE:
            self.drawing_board[coordinate[0]][coordinate[1]] = '?'
        else:
            self.drawing_board[coordinate[0]][coordinate[1]] = '*'

    def __move_player(self, color, where_to_put_it):
        offset_coordinate = self.list_with_chordates[where_to_put_it]
        x, y = offset_coordinate
        self.drawing_board[x][y] = self.get_figure(color)
        self.__add_log(msg=f"the {color} moved to the coordinate:{offset_coordinate}")

        # get how long it takes to reach your goal

        self.__add_log(
            msg=f"the {color}, ({self.__goal(color, where_to_put_it)}) squares are missing to reach the finish line")

    def __goal(self, color, where_to_put_it):
        # get how long it takes to reach your goal
        counter_1 = where_to_put_it
        counter_2 = 0
        while counter_1 != self.GENERAL_COORDINATES[color][0]['full_turn']:
            counter_1 += 1
            if counter_1 > 31:
                counter_1 = 0
            counter_2 += 1

        return counter_2

    def __search_chip(self, figure):
        # function to find the tile on the board
        for x, row in enumerate(self.drawing_board):
            for y, column in enumerate(row):
                if figure == column:
                    return x, y

    # the logs allow me to know how the table is acting

    def delete_log(self):
        self.logs = []

    def __add_log(self, msg):
        self.logs.append(msg)

    def update_table(self, color, where_to_put_it):
        # steps to follow
        # function 1
        coordinate_now = self.__search_chip(self.get_figure(color))
        if coordinate_now:
            self.__add_log(msg=f"the {color} is not in jail")
            self.__add_log(msg=f"the {color} is located at the board coordinates:{coordinate_now}")

            # function 2
            self.__delete_current_position(coordinate_now)

            self.__add_log(msg=f"the {color} removed from current position")

            # function 3
            self.__eat(self.get_figure(color), color, where_to_put_it)

            # function 4
            self.__move_player(color, where_to_put_it)

        else:
            # there is no such figure on the board, it means he is in jail

            # se debe revisar esto por que eliminacion esta teniendo problemas
            pass

# UI.print_table(Board().drawing_board)
