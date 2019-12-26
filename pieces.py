from chess import Piece


class Pawn(Piece):
    '''
    A Pawn can move forward one space, and attack diagonally in the forward direction.
    On its fist move it may move two spaces.
    '''
    name = 'Pawn'
    value = 1
    symbol = '♟ '
    moves = [(0, 1)]
    attacks = [(1, 1), (-1, 1)]

    @property
    def legal_moves(self):
        # Add the ability to move forward two spaces for first move.
        legal_moves = super().legal_moves

        if self.board.get(self.x, self.y + 2 * self.player.direction) is None \
                and self.board.get(self.x, self.y + self.player.direction) is None \
                and not self.has_moved:
            legal_moves.append((self.x, self.y + 2 * self.player.direction))

        return legal_moves
