from colorama import init, Fore, Back, Style

init()


def print_board(board):
    '''
    Prints the board to the terminal.
    '''
    result = '\n'
    for ri, row in enumerate(board):
        for pi, position in enumerate(row):
            result += Back.BLUE if (pi + ri) % 2 else Back.RED
            if position:
                result += getattr(Fore, position.player.name.upper(), Fore.WHITE) + position.symbol + ' '
            else:
                result += '  '
        result += Back.BLACK + '\n'

    print(result + Style.RESET_ALL)


if __name__ == '__main__':
    print_board([[None] * 8] * 8)
