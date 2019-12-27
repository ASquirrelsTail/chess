class Chessboard:
    def __init__(self):
        self._board = [[None] * 8 for n in range(8)]

    def __str__(self):
        return '{}x{} Chessboard'.format(len(self._board), len(self._board[0]))

    def __getitem__(self, key):
        return self._board[key]

    def get(self, x, y):
        if x >= 0 and y >= 0:
            try:
                return self._board[x][y]
            except IndexError:
                return False
        else:
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
    moves = []
    move_directions = []

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
        '''
        Returns a list of tuples for legal moves.
        '''
        def advancePosition(old_pos, direction):
            # Advances the target from its old position in the given direction.
            x, y = old_pos
            ad_x, ad_y = direction
            return (x + ad_x, y + ad_y * self.player.direction)

        legal_moves = []

        for position in self.moves:
            target = self.positionRelative(position)
            target_piece = self.board.get(*target)
            if target_piece is None \
                    or (target_piece and target_piece.player is not self.player):
                legal_moves.append(target)

        for direction in self.move_directions:
            target = self.positionRelative(direction)
            target_piece = self.board.get(*target)
            while target_piece is None:
                legal_moves.append(target)
                target = advancePosition(target, direction)
                target_piece = self.board.get(*target)
            else:
                if target_piece and target_piece.player is not self.player:
                    legal_moves.append(target)

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

    def positionRelative(self, pos):
        # Sets the target relative to the piece's current position.
        x, y = pos
        return (self.x + x, self.y + y * self.player.direction)

    def move(self, x, y):
        if (x, y) in self.legal_moves:
            self.board.blank(*self.position)

            if self.board.get(x, y):
                self.player.score += self.board[x][y].value

            self._x, self._y = (x, y)
            self.board.set(x, y, self)
            self.has_moved = True
            self.player.end_turn()
