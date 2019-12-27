import unittest
from chess import Chessboard, Player
from pieces import Pawn, King, Queen, Knight, Rook, Bishop
from sys import argv
if '-v' in argv:
    from console import print_board


class PieceTestCase(unittest.TestCase):
    '''
    Test case to set up board and players and add utility functions.
    '''
    def setUp(self):
        self.chessboard = Chessboard()
        self.player1 = Player('White', 1)
        self.player2 = Player('Black', -1)

    def tearDown(self):
        if '-v' in argv:
            print_board(self.chessboard)

    def create_enemy(self, x, y):
        '''
        Utility function to create a Pawn to attack.
        '''
        return Pawn(self.chessboard, self.player2, x, y)

    def create_pawn(self, x, y):
        '''
        Utility function to create an allied Pawn to block moves.
        '''
        return Pawn(self.chessboard, self.player1, x, y)

    def assertItemsIn(self, first, second):
        '''
        Test that the items of first are in iterable second.
        '''
        for item in first:
            self.assertIn(item, second)

    def assertItemsNotIn(self, first, second):
        '''
        Test that the items of first are not in iterable second.
        '''
        for item in first:
            self.assertNotIn(item, second)


class PawnTestCase(PieceTestCase):
    def test_possible_moves(self):
        '''
        Test the Pawn can move forwards one or two.
        '''
        pawn = self.create_pawn(4, 4)

        self.assertCountEqual(pawn.legal_moves,
                              [(4, 5), (4, 6)])

    def test_cant_move_forward_two_after_moving(self):
        pawn = self.create_pawn(4, 4)
        pawn.move(4, 5)

        self.assertNotIn((4, 7), pawn.legal_moves)
        self.assertIn((4, 6), pawn.legal_moves)

    def test_cant_move_forward_if_blocked(self):
        pawn = self.create_pawn(4, 4)
        self.create_enemy(4, 5)

        self.assertNotIn((4, 5), pawn.legal_moves)
        self.assertNotIn((4, 6), pawn.legal_moves)

    def test_moves_forward(self):
        pawn = self.create_pawn(4, 4)
        pawn.move(4, 5)

        self.assertEqual(pawn.position, (4, 5))
        self.assertIs(self.chessboard[4][5], pawn)

    def test_moves_forward_two_first_move(self):
        pawn = self.create_pawn(4, 4)
        pawn.move(4, 6)

        self.assertEqual(pawn.position, (4, 6))
        self.assertIs(self.chessboard[4][6], pawn)
        self.assertIsNone(self.chessboard[4][4])

    def test_possible_attacks(self):
        '''
        Test the Pawn can attack diagonally.
        '''
        pawn = self.create_pawn(4, 4)

        self.create_enemy(3, 5)
        self.create_enemy(5, 5)

        self.assertItemsIn([(3, 5), (5, 5)], pawn.legal_moves)

    def test_cant_attack_own_pieces(self):
        pawn = self.create_pawn(4, 4)

        self.create_pawn(3, 5)
        self.create_pawn(5, 5)

        self.assertItemsNotIn([(3, 5), (5, 5)], pawn.legal_moves)

    def test_attacks_diagonally(self):
        pawn = self.create_pawn(4, 4)

        self.create_enemy(3, 5)
        self.create_enemy(4, 6)

        pawn.move(3, 5)
        self.assertEqual(pawn.position, (3, 5))
        self.assertIs(self.chessboard[3][5], pawn)
        self.assertIsNone(self.chessboard[4][4])

        self.assertEqual(self.player1.score, 1)

        pawn.move(4, 6)
        self.assertEqual(pawn.position, (4, 6))
        self.assertIs(self.chessboard[4][6], pawn)
        self.assertIsNone(self.chessboard[3][5])

        self.assertEqual(self.player1.score, 2)

    def test_cant_move_off_edge_of_board(self):
        pawn = self.create_pawn(4, 7)

        self.assertEqual([], pawn.legal_moves)

    def test_taking_pawn_awards_one_point(self):
        self.create_pawn(4, 4)
        enemy = self.create_enemy(5, 5)

        enemy.move(4, 4)

        self.assertEqual(self.player2.score, 1)


class KingTestCase(PieceTestCase):
    def create_king(self, x, y):
        return King(self.chessboard, self.player1, x, y)

    def test_possible_moves(self):
        king = self.create_king(4, 4)

        self.assertCountEqual(king.legal_moves,
                              [(3, 5), (4, 5), (5, 5),
                               (3, 4), (5, 4),
                               (3, 3), (4, 3), (5, 3)])

    def test_cant_move_if_blocked(self):
        king = self.create_king(4, 4)

        for position in [(3, 5), (4, 5), (5, 5),
                         (3, 4), (5, 4),
                         (3, 3), (4, 3), (5, 3)]:
            self.create_pawn(*position)

        self.assertEqual(king.legal_moves, [])

    def test_cant_move_off_edge_of_board(self):
        king = self.create_king(0, 7)

        self.assertCountEqual(king.legal_moves,
                              [(1, 7), (0, 6), (1, 6)])

    def test_can_attack_in_all_directions(self):
        # This test needs ammending if it becomes illegal for Kings to move in to check.
        king = self.create_king(4, 4)

        for position in [(3, 5), (4, 5), (5, 5),
                         (3, 4), (5, 4),
                         (3, 3), (4, 3), (5, 3)]:
            self.create_enemy(*position)

        self.assertCountEqual(king.legal_moves,
                              [(3, 5), (4, 5), (5, 5),
                               (3, 4), (5, 4),
                               (3, 3), (4, 3), (5, 3)])


class KnightTestCase(PieceTestCase):
    def create_knight(self, x, y):
        return Knight(self.chessboard, self.player1, x, y)

    def test_possible_moves(self):
        knight = self.create_knight(4, 4)

        self.assertCountEqual(knight.legal_moves,
                              [(3, 6), (5, 6),
                               (6, 5), (6, 3),
                               (2, 5), (2, 3),
                               (3, 2), (5, 2)])

    def test_cant_move_if_blocked(self):
        knight = self.create_knight(4, 4)

        for position in [(3, 6), (5, 6),
                         (6, 5), (6, 3),
                         (2, 5), (2, 3),
                         (3, 2), (5, 2)]:
            self.create_pawn(*position)

        self.assertEqual(knight.legal_moves, [])

    def test_cant_move_off_board(self):
        knight = self.create_knight(1, 6)

        self.assertCountEqual(knight.legal_moves,
                              [(3, 7), (3, 5),
                               (2, 4), (0, 4)])

    def test_can_attack_in_L_shape(self):
        knight = self.create_knight(4, 4)

        for position in [(3, 6), (5, 6),
                         (6, 5), (6, 3),
                         (2, 5), (2, 3),
                         (3, 2), (5, 2)]:
            self.create_enemy(*position)

        self.assertCountEqual(knight.legal_moves,
                              [(3, 6), (5, 6),
                               (6, 5), (6, 3),
                               (2, 5), (2, 3),
                               (3, 2), (5, 2)])

    def test_taking_knight_awards_three_points(self):
        self.create_knight(4, 4)
        enemy = self.create_enemy(5, 5)

        enemy.move(4, 4)

        self.assertEqual(self.player2.score, 3)


class RookTestCase(PieceTestCase):
    # Castle
    def create_rook(self, x, y):
        return Rook(self.chessboard, self.player1, x, y)

    def test_can_move_to_any_position_in_cardinal_directions(self):
        '''
        The rook should be able to move to any position in the
        directions up, down, left, right, within the bounds of the board.
        '''
        rook = self.create_rook(4, 4)

        self.assertCountEqual(rook.legal_moves,
                              [(4, 5), (4, 6), (4, 7),
                               (5, 4), (6, 4), (7, 4),
                               (4, 3), (4, 2), (4, 1), (4, 0),
                               (3, 4), (2, 4), (1, 4), (0, 4)])

    def test_can_only_move_until_blocked(self):
        '''
        The rook shouldn't be able to move into or past allied pieces.
        '''
        rook = self.create_rook(4, 4)

        for position in [(4, 6), (6, 4), (4, 2), (2, 4)]:
            self.create_pawn(*position)

        self.assertCountEqual(rook.legal_moves,
                              [(4, 5), (5, 4), (4, 3), (3, 4)])

    def test_cant_move_if_blocked(self):
        rook = self.create_rook(0, 0)

        for position in [(1, 0), (0, 1)]:
            self.create_pawn(*position)

        self.assertEqual(rook.legal_moves, [])

    def test_can_attack_in_cardinal_directions(self):
        rook = self.create_rook(4, 4)

        for position in [(4, 6), (6, 4), (4, 2), (2, 4)]:
            self.create_enemy(*position)

        self.assertCountEqual(rook.legal_moves,
                              [(4, 5), (4, 6),
                               (5, 4), (6, 4),
                               (4, 3), (4, 2),
                               (3, 4), (2, 4)])

    def test_cant_attack_if_blocked(self):
        rook = self.create_rook(0, 0)

        self.create_pawn(0, 2)
        self.create_pawn(1, 0)
        self.create_enemy(0, 3)

        self.assertEqual(rook.legal_moves, [(0, 1)])

    def test_taking_rook_awards_five_points(self):
        self.create_rook(4, 4)
        enemy = self.create_enemy(5, 5)

        enemy.move(4, 4)

        self.assertEqual(self.player2.score, 5)


class BishopTestCase(PieceTestCase):
    def create_bishop(self, x, y):
        return Bishop(self.chessboard, self.player1, x, y)

    def test_can_move_to_any_diagonal_position(self):
        bishop = self.create_bishop(4, 4)

        self.assertCountEqual(bishop.legal_moves,
                              [(5, 5), (6, 6), (7, 7),
                               (3, 3), (2, 2), (1, 1), (0, 0),
                               (5, 3), (6, 2), (7, 1),
                               (3, 5), (2, 6), (1, 7)])

    def test_can_only_move_until_blocked(self):
        bishop = self.create_bishop(4, 4)

        for position in [(6, 6), (2, 2), (6, 2), (2, 6)]:
            self.create_pawn(*position)

        self.assertCountEqual(bishop.legal_moves,
                              [(5, 5), (3, 3), (5, 3), (3, 5)])

    def test_can_attack_in_diagonals(self):
        bishop = self.create_bishop(4, 4)

        for position in [(6, 6), (2, 2), (6, 2), (2, 6), (1, 7)]:
            self.create_enemy(*position)

        self.assertCountEqual(bishop.legal_moves,
                              [(5, 5), (6, 6),
                               (3, 3), (2, 2),
                               (5, 3), (6, 2),
                               (3, 5), (2, 6)])

    def test_cant_attack_if_blocked(self):
        bishop = self.create_bishop(0, 0)

        self.create_pawn(2, 2)
        self.create_enemy(3, 3)

        self.assertEqual(bishop.legal_moves, [(1, 1)])

    def test_taking_bishop_awards_three_points(self):
        self.create_bishop(4, 4)
        enemy = self.create_enemy(5, 5)

        enemy.move(4, 4)

        self.assertEqual(self.player2.score, 3)


class QueenTestCase(PieceTestCase):
    def create_queen(self, x, y):
        return Queen(self.chessboard, self.player1, x, y)

    def test_can_move_to_any_diagonal_or_cardinal_position(self):
        queen = self.create_queen(4, 4)

        self.assertCountEqual(queen.legal_moves,
                              [(5, 5), (6, 6), (7, 7),
                               (3, 3), (2, 2), (1, 1), (0, 0),
                               (5, 3), (6, 2), (7, 1),
                               (3, 5), (2, 6), (1, 7),
                               (4, 5), (4, 6), (4, 7),
                               (5, 4), (6, 4), (7, 4),
                               (4, 3), (4, 2), (4, 1), (4, 0),
                               (3, 4), (2, 4), (1, 4), (0, 4)])

    def test_can_only_move_until_blocked(self):
        queen = self.create_queen(4, 4)

        for position in [(6, 6), (2, 2), (6, 2), (2, 6),
                         (4, 6), (6, 4), (4, 2), (2, 4)]:
            self.create_pawn(*position)

        self.assertCountEqual(queen.legal_moves,
                              [(5, 5), (3, 3), (5, 3), (3, 5),
                               (4, 5), (5, 4), (4, 3), (3, 4)])

    def test_can_attack_in_diagonals_and_cardinals(self):
        queen = self.create_queen(4, 4)

        for position in [(6, 6), (2, 2), (6, 2), (2, 6), (1, 7),
                         (4, 6), (6, 4), (4, 2), (2, 4)]:
            self.create_enemy(*position)

        self.assertCountEqual(queen.legal_moves,
                              [(5, 5), (6, 6),
                               (3, 3), (2, 2),
                               (5, 3), (6, 2),
                               (3, 5), (2, 6),
                               (4, 5), (4, 6),
                               (5, 4), (6, 4),
                               (4, 3), (4, 2),
                               (3, 4), (2, 4)])

    def test_cant_attack_if_blocked(self):
        queen = self.create_queen(0, 0)

        self.create_pawn(2, 2)
        self.create_enemy(3, 3)
        self.create_pawn(0, 2)
        self.create_enemy(0, 3)
        self.create_pawn(2, 0)
        self.create_enemy(3, 0)

        self.assertCountEqual(queen.legal_moves,
                              [(1, 1), (0, 1), (1, 0)])

    def test_taking_queen_awards_nine_points(self):
        self.create_queen(4, 4)
        enemy = self.create_enemy(5, 5)

        enemy.move(4, 4)

        self.assertEqual(self.player2.score, 9)


if __name__ == '__main__':
    unittest.main()
