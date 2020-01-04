from chess import Chessboard, Player
from console import print_board, LETTERS
import pieces
import re
from random import choice


class HumanPlayer(Player):
    def play_turn(self):
        move = input('{} player enter move:\n'.format(current_player)).lower()
        return move


class RandomPlayer(Player):
    def play_turn(self):
        possible_moves = []
        for piece in self.pieces:
            for move in piece.legal_moves:
                possible_moves.append((piece.position, move))

        selected_piece, target = choice(possible_moves)
        move = '{}{} to {}{}'.format(LETTERS[selected_piece[0]], selected_piece[1] + 1, LETTERS[target[0]], target[1] + 1)

        return move


chessboard = Chessboard()
white = HumanPlayer('White', 1)
black = RandomPlayer('Black', -1)


def set_up_pieces(board, player):
    row = player.direction // 2
    for n in range(len(board)):
        pieces.Pawn(board, player, n, row + player.direction)

    pieces.Rook(board, player, 0, row)
    pieces.Rook(board, player, 7, row)
    pieces.Knight(board, player, 1, row)
    pieces.Knight(board, player, 6, row)
    pieces.Bishop(board, player, 2, row)
    pieces.Bishop(board, player, 5, row)
    pieces.Queen(board, player, 3, row)
    pieces.King(board, player, 4, row)


def draw():
    print_board(chessboard, scale='positions')
    print('Score: {}-{}'.format(white.score, black.score))


set_up_pieces(chessboard, white)
set_up_pieces(chessboard, black)

current_player = white

move = ''
while move != 'exit':
    draw()
    move = current_player.play_turn()
    if 'to' in move:
        instructions = [i.strip() for i in move.lower().split('to')]
        if re.search('^[a-z][1-9]$', instructions[0]) and re.search('^[a-z][1-9]$', instructions[1]):
            piece = chessboard.get(LETTERS.lower().index(instructions[0][0]), int(instructions[0][1]) - 1)
            target = (LETTERS.lower().index(instructions[1][0]), int(instructions[1][1]) - 1)

            if piece and piece.player == current_player:
                if piece.move(*target):
                    current_player = black if current_player is white else white
                    if not [piece for piece in current_player.pieces if piece.legal_moves]:
                        draw()
                        print("Check mate, {} wins.".format(black if current_player is white else white))
                        move = 'exit'
