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

        legal_moves += self.castles

        # Remove legal moves that put the king in check.

        return legal_moves

    @property
    def castles(self):
        if self.has_moved:
            return []

        castle_moves = []

        castle_positions = {self.positionRelative(position) for position in CARDINAL_DIRECTIONS}
        for rook in filter(lambda piece: piece.name == 'Rook' and not piece.has_moved, self.player.pieces):
            intersection = set(rook.legal_moves).intersection(castle_positions)
            if intersection:
                castle_target = intersection.pop()
                if self.board.get(*castle_target) is None:
                    c_x, c_y = castle_target
                    castle_moves.append(self.positionRelative(((c_x - self.x) * 2, (c_y - self.y) * 2)))

        return castle_moves

    def move(self, x, y):
        if (x, y) in self.castles:
            rook = next(piece for piece in self.player.pieces
                        if piece.name == 'Rook' and not piece.has_moved and (x, y) in piece.legal_moves)
            rook.move(*next(castle_position for castle_position in rook.legal_moves if castle_position in [self.positionRelative(position) for position in CARDINAL_DIRECTIONS]))

            self.board.blank(*self.position)
            self._x, self._y = (x, y)
            self.board.set(x, y, self)
            self.has_moved = True
            return True
        else:
            return super().move(x, y)


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
