import unittest

from database.db_connect import session, Game
from game_eff import current_eff, is_hard_var


class TestEff(unittest.TestCase):
    def test_current_eff(self):
        game_id = 869787
        game = session.query(Game).filter(Game.game_id == game_id).first()
        actual = current_eff(game)
        expected = round(25 / 18, 2)
        self.assertEqual(expected, actual)

    def test_is_hard_var(self):
        self.assertEqual(True, is_hard_var('Cow & Pig (6 Suits)', 6, 2))
        self.assertEqual(True, is_hard_var('Cow & Pig (6 Suits)', 6, 3))
        self.assertEqual(True, is_hard_var('Up or Down & Prism (5 Suits)', 5, 5))
        self.assertEqual(True, is_hard_var('Up or Down & Prism (5 Suits)', 5, 6))

        self.assertEqual(False, is_hard_var('Brown (6 Suits)', 6, 3))
        self.assertEqual(False, is_hard_var('Brown (6 Suits)', 6, 5))

        self.assertEqual(False, is_hard_var('Black & Prism (6 Suits)', 6, 3))
        self.assertEqual(True, is_hard_var('Black & Prism (6 Suits)', 6, 5))

        self.assertEqual(False, is_hard_var('Dark Pink & Dark Prism (6 Suits)', 6, 2))
        self.assertEqual(True, is_hard_var('Dark Pink & Dark Prism (6 Suits)', 6, 3))
        self.assertEqual(True, is_hard_var('Dark Pink & Dark Prism (6 Suits)', 6, 5))
        self.assertEqual(True, is_hard_var('Dark Pink & Dark Prism (6 Suits)', 6, 6))
        self.assertEqual(True, is_hard_var('Gray & Gray Pink (6 Suits)', 6, 6))
        self.assertEqual(True, is_hard_var('Gray Pink & Gray (6 Suits)', 6, 6))
        self.assertEqual(True, is_hard_var('Dark Null & Cocoa Rainbow (6 Suits)', 6, 6))

        self.assertEqual(True, is_hard_var('Clue Starved & Brown (6 Suits)', 6, 6))
        self.assertEqual(True, is_hard_var('Throw It in a Hole & Muddy Rainbow (6 Suits)', 6, 6))

        self.assertEqual(False, is_hard_var('Critical Fours (6 Suits)', 6, 3))
        self.assertEqual(True, is_hard_var('Critical Fours (6 Suits)', 6, 5))

        self.assertEqual(False, is_hard_var('No Variant', 5, 2))
        self.assertEqual(False, is_hard_var('Rainbow-Ones & Gray Pink (5 Suits)', 5, 2))
        self.assertEqual(True, is_hard_var('Rainbow-Ones & Gray Pink (5 Suits)', 5, 5))

        self.assertEqual(False, is_hard_var('4 Suits', 4, 2))
        self.assertEqual(True, is_hard_var('4 Suits', 4, 5))
        self.assertEqual(False, is_hard_var('Brown & Dark Prism (4 Suits)', 4, 2))
        self.assertEqual(True, is_hard_var('Brown & Dark Prism (4 Suits)', 4, 5))


if __name__ == '__main__':
    unittest.main()
