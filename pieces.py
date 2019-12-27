from chess import Piece
from sys import maxsize

CARDINAL_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIAGONAL_DIRECTIONS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
ALL_DIRECTIONS = CARDINAL_DIRECTIONS + DIAGONAL_DIRECTIONS


class Pawn(Piece):
    '''
    A Pawn can move forward one space, and attack diagonally in the forward direction.
    On its fist move it may move two spaces.
    '''
    name = 'Pawn'
    value = 1
    symbol = '♟'

    @property
    def legal_moves(self):
        legal_moves = []

        # Move forward one space, or two if not yet moved.
        forward_one = self.positionRelative((0, 1))
        if self.board.get(*forward_one) is None:
            legal_moves.append(forward_one)
            forward_two = self.positionRelative((0, 2))
            if not self.has_moved and self.board.get(*forward_two) is None:
                legal_moves.append(forward_two)

        # Attack only in diagonals.
        for position in [self.positionRelative((-1, 1)), self.positionRelative((1, 1))]:
            piece = self.board.get(*position)
            if piece and piece.player is not self.player:
                legal_moves.append(position)

        return legal_moves


class King(Piece):
    name = 'King'
    value = maxsize - 39
    symbol = '♚'
    moves = ALL_DIRECTIONS

    @property
    def legal_moves(self):
        legal_moves = super().legal_moves
        # Remove legal moves that put the king in check.

        return legal_moves


class Knight(Piece):
    name = 'Knight'
    value = 3
    symbol = '♞'
    moves = [(1, 2), (-1, 2), (2, 1), (2, -1), (-2, 1), (-2, -1), (-1, -2), (1, -2)]


class Rook(Piece):
    name = 'Rook'  # Castle
    value = 5
    symbol = '♜'
    move_directions = CARDINAL_DIRECTIONS


class Bishop(Piece):
    name = 'Bishop'
    value = 3
    symbol = '♝'
    move_directions = DIAGONAL_DIRECTIONS


class Queen(Piece):
    name = 'Queen'
    value = 9
    symbol = '♛'
    move_directions = ALL_DIRECTIONS
