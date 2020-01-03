from chess import Piece
from sys import maxsize

CARDINAL_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIAGONAL_DIRECTIONS = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
ALL_DIRECTIONS = CARDINAL_DIRECTIONS + DIAGONAL_DIRECTIONS


class DefensivePiece(Piece):
    @property
    def legal_moves(self):
        legal_moves = super().legal_moves

        # Constrain legal moves to any defensive moves required by a king in check
        if self.player.king and self.player.king.defensive_moves is not False:
            legal_moves.intersection_update(self.player.king.defensive_moves)

        return legal_moves


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
        legal_moves = set()

        # Move forward one space, or two if not yet moved.
        forward_one = self.positionRelative((0, 1))
        if self.board.get(*forward_one) is None:
            legal_moves.add(forward_one)
            forward_two = self.positionRelative((0, 2))
            if not self.has_moved and self.board.get(*forward_two) is None:
                legal_moves.add(forward_two)

        # Attack only in diagonals.
        for position in [self.positionRelative((-1, 1)), self.positionRelative((1, 1))]:
            piece = self.board.get(*position)
            if piece and piece.player is not self.player:
                legal_moves.add(position)

        # Constrain legal moves to any defensive moves required by a king in check
        if self.player.king and self.player.king.defensive_moves is not False:
            legal_moves.intersection_update(self.player.king.defensive_moves)

        return legal_moves

    @property
    def threatens(self):
        threatens = set()
        for position in [self.positionRelative((-1, 1)), self.positionRelative((1, 1))]:
            if self.board.get(*position) is not False:
                threatens.add(position)

        return threatens


class King(Piece):
    name = 'King'
    value = maxsize - 39
    symbol = '♚'
    moves = ALL_DIRECTIONS

    def __init__(self, *args):
        super().__init__(*args)
        self.player.king = self

    @property
    def legal_moves(self):
        legal_moves = super().legal_moves

        legal_moves.update(self.castles)

        # Remove legal moves that put the king in check.

        for opponent in self.player.opponents:
            for threats in [piece.threatens for piece in opponent.pieces]:
                legal_moves.difference_update(threats)

        return legal_moves

    @property
    def castles(self):
        '''
        Returns target positions for possible castle moves.
        '''
        if self.has_moved:
            return set()

        castle_moves = set()

        castle_positions = {self.positionRelative(position) for position in CARDINAL_DIRECTIONS}
        for rook in [piece for piece in self.player.pieces if piece.name == 'Rook' and not piece.has_moved]:
            intersection = rook.legal_moves.intersection(castle_positions)
            if intersection:
                castle_target = intersection.pop()
                if self.board.get(*castle_target) is None:
                    c_x, c_y = castle_target
                    castle_moves.add(self.positionRelative(((c_x - self.x) * 2, (c_y - self.y) * 2)))

        return castle_moves

    @property
    def threatened_by(self):
        threatened_by = []
        for opponent in self.player.opponents:
            for piece in opponent.pieces:
                if self.position in piece.threatens:
                    threatened_by.append(piece)
        return threatened_by

    @property
    def in_check(self):
        return bool(self.threatened_by)

    @property
    def defensive_moves(self):
        '''
        A set of moves that are permissible to defend a king in check.
        '''
        threats = self.threatened_by
        defensive_moves = False

        if len(threats) > 1:  # If there is more than one threat to the king no pieces except the king can move.
            return set()
        elif len(threats) == 1:
            attacker = threats[0]
            defensive_moves = set()
            defensive_moves.add(attacker.position)  # The attacker's position is a valid defensive move

            if attacker.move_directions:  # If the threat can be blocked
                direction = (attacker.x - self.player.king.x,
                             attacker.y - self.player.king.y)
                direction = (max(min(direction[0], 1), -1), max(min(direction[1], 1), -1) * self.player.direction)

                position = self.player.king.positionRelative(direction)
                while self.board.get(*position) is None:
                    defensive_moves.add(position)
                    position = self.player.king.advancePosition(position, direction)

        return defensive_moves

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


class Knight(DefensivePiece):
    name = 'Knight'
    value = 3
    symbol = '♞'
    moves = [(1, 2), (-1, 2), (2, 1), (2, -1), (-2, 1), (-2, -1), (-1, -2), (1, -2)]


class Rook(DefensivePiece):
    name = 'Rook'  # Castle
    value = 5
    symbol = '♜'
    move_directions = CARDINAL_DIRECTIONS


class Bishop(DefensivePiece):
    name = 'Bishop'
    value = 3
    symbol = '♝'
    move_directions = DIAGONAL_DIRECTIONS


class Queen(DefensivePiece):
    name = 'Queen'
    value = 9
    symbol = '♛'
    move_directions = ALL_DIRECTIONS
