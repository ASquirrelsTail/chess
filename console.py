from colorama import init, Fore, Back, Style

init()

LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def print_board(board, scale=False):
    '''
    Prints the board to the terminal.
    '''
    result = '\n'
    for ri, row in enumerate(board):
        if scale:
            result += Back.BLACK + Fore.WHITE
            if scale == 'positions':
                result += LETTERS.upper()[ri] + ' '
            else:
                result += str(ri) + ' '
        for pi, position in enumerate(row):
            result += Back.BLUE if (pi + ri) % 2 else Back.RED
            if position:
                result += getattr(Fore, position.player.name.upper(), Fore.WHITE) + position.symbol + ' '
            else:
                result += '  '
        result += Back.BLACK + '\n'
    result += Back.BLACK + Fore.WHITE + '  ' + ' '.join([str(i + (1 if scale == 'positions' else 0)) for i in range(len(board))])
    print(result + Style.RESET_ALL)


if __name__ == '__main__':
    print_board([[None] * 8] * 8)
