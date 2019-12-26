import unittest
from chess import Chessboard, Player
from pieces import Pawn, King


class PieceTestCase(unittest.TestCase):
    '''
    Test case to set up board and players and add utility functions.
    '''
    def setUp(self):
        self.chessboard = Chessboard()
        self.player1 = Player('White', 1)
        self.player2 = Player('Black', -1)

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
        # This test needs ammending if it becomes illegal or Kings to move in to check.
        king = self.create_king(4, 4)

        for position in [(3, 5), (4, 5), (5, 5),
                         (3, 4), (5, 4),
                         (3, 3), (4, 3), (5, 3)]:
            self.create_enemy(*position)

        self.assertCountEqual(king.legal_moves,
                              [(3, 5), (4, 5), (5, 5),
                               (3, 4), (5, 4),
                               (3, 3), (4, 3), (5, 3)])


if __name__ == '__main__':
    unittest.main()
