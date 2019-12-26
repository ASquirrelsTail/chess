class Chessboard:
    def __init__(self):
        self._board = [[None] * 8 for n in range(8)]

    def __str__(self):
        return '{}x{} Chessboard'.format(len(self._board), len(self._board[0]))

    def __getitem__(self, key):
        return self._board[key]

    def get(self, x, y):
        try:
            return self._board[x][y]
        except IndexError:
            return False

    def set(self, x, y, value):
        self._board[x][y] = value

    def blank(self, x, y):
        self._board[x][y] = None


class Player:
    players = []

    def __init__(self, name, direction):
        self.name = name
        self.pieces = []
        self.direction = direction
        self.score = 0

    def __str__(self):
        return self.name

    def end_turn(self):
        pass


class Piece:
    '''
    Class to represent chess piece.
    '''
    value = 0
    name = 'Piece'
    symbol = '  '

    def __init__(self, board, player, x, y):
        self.board = board
        self._x, self._y = (x, y)
        self.player = player
        player.pieces.append(self)
        board.set(x, y, self)
        self.has_moved = False

    def __str__(self):
        return '{} {} @ {}, {}'.format(self.player, self.name, *self.position)

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(self.name, self.board, self.player, *self.position)

    @property
    def legal_moves(self):

        legal_moves = []

        return legal_moves

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def position(self):
        return (self._x, self._y)

    def move(self, x, y):
        if (x, y) in self.legal_moves:
            self.board.blank(*self.position)

            if self.board.get(x, y):
                self.player.score += self.board[x][y].value

            self._x, self._y = (x, y)
            self.board.set(x, y, self)
            self.player.end_turn()
