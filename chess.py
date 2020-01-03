class Chessboard:
    def __init__(self):
        self._board = [[None] * 8 for n in range(8)]

    def __str__(self):
        return '{}x{} Chessboard'.format(len(self._board), len(self._board[0]))

    def __getitem__(self, key):
        return self._board[key]

    def __len__(self):
        return len(self._board)

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
        self.king = False
        self.players.append(self)

    def __str__(self):
        return self.name

    def end_turn(self):
        pass

    @property
    def opponents(self):
        return [player for player in self.players if player is not self]


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
        self._x = (len(self.board) + x) % len(self.board)
        self._y = (len(self.board[0]) + y) % len(self.board[0])
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
        return {position for position in self.threatens
                if self.board.get(*position) is None or
                self.board.get(*position).player is not self.player}

    @property
    def threatens(self):
        threatens = set()

        for position in self.moves:
            target = self.positionRelative(position)
            target_piece = self.board.get(*target)
            if target_piece is not False:
                threatens.add(target)

        for direction in self.move_directions:
            target = self.positionRelative(direction)
            target_piece = self.board.get(*target)
            while target_piece is None:
                threatens.add(target)
                target = self.advancePosition(target, direction)
                target_piece = self.board.get(*target)
            else:
                if target_piece:
                    threatens.add(target)

        return threatens

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

    def advancePosition(self, old_pos, direction):
        '''
        Advances the target from its old position in the given direction,
        relative to the player's facing.
        '''
        x, y = old_pos
        ad_x, ad_y = direction
        return (x + ad_x, y + ad_y * self.player.direction)

    def move(self, x, y):
        if (x, y) in self.legal_moves:
            self.board.blank(*self.position)

            if self.board.get(x, y):
                self.player.score += self.board[x][y].value
                self.board[x][y].kill()

            self._x, self._y = (x, y)
            self.board.set(x, y, self)
            self.has_moved = True
            return True
        else:
            return False

    def kill(self):
        self.player.pieces.remove(self)
