import os
import random
import time


class UI:

    @staticmethod
    def print_table(table):
        print('\n')
        for row in table:
            for column in row:
                print(column, end=' ')
            print('\n')

    @staticmethod
    def json_prototype(color: str, finish_game=False, your_turn=False, dice_result=0, dice_1=0, dice_2=0, total=0,
                       where_to_put_it=0, board=''):
        json = {
            'color': color,
            'finish_game': finish_game,
            'your_turn': your_turn,
            'dice_result': dice_result,
            'dice_1': dice_1,
            'dice_2': dice_2,
            'total': total,
            'where_to_put_it': where_to_put_it,
            'board': board
        }
        return json

    @staticmethod
    def throw_dice():
        dice_1 = 0
        dice_2 = 0
        while True:
            UI.clear_console()
            option = int(input('press (1) to roll the dice:'))
            if option == 1:
                dice_1 = random.randint(1, 6)
                dice_2 = random.randint(1, 6)
                total = dice_1 + dice_2
                print(f"dice 1 = ({dice_1}), dice 2 = ({dice_2}), total = {total}")
                time.sleep(6)
                return dice_1, dice_2, total

    @staticmethod
    def roll_only_one_dice():
        dice_1 = 0
        while True:
            # UI.clear_console()
            option = int(input('press (1) to roll a die:'))
            if option == 1:
                dice_1 = random.randint(1, 6)
                total = dice_1
                print(f"dice 1 = ({dice_1}), total = {total}")
                time.sleep(6)
                return dice_1, total

    @staticmethod
    def clear_console():
        command = 'clear'
        # If Machine is running on Windows, use cls
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)
