"""Tests for LyName and it's child classes."""
import unittest
from lyskel import lynames


class TestLyName(unittest.TestCase):

    def test_init(self):
        """Test normalization of name input."""
        test1 = lynames.LyName('TEST name ')
        self.assertEqual(
            test1.name,
            'test_name'
        )

        test2 = lynames.LyName('  another_test-name')
        self.assertEqual(
            test2.name,
            'another_test_name'
        )

    def test_movement(self):
        """Test movement method for num and word."""
        testlyname = lynames.LyName('global')
        self.assertEqual(
            testlyname.file_name(1),
            'global_1'
        )

        self.assertEqual(
            testlyname.file_name(2),
            'global_2'
        )

        self.assertEqual(
            testlyname.var_name(2),
            'global_second_mov'
        )

        self.assertEqual(
            testlyname.var_name(31),
            'global_thirty_first_mov'
        )

        # test exceptions
        self.assertRaisesRegex(
            TypeError,
            ".*'form'.*",
            testlyname._movement,
            1
        )

        self.assertRaisesRegex(
            TypeError,
            '.*integer',
            testlyname._movement,
            '10',
            form='word'
        )

        self.assertRaisesRegex(
            ValueError,
            ".*'form'.*'word'",
            testlyname._movement,
            10,
            form='fail'
        )


# class TestInstrument(unittest.TestCase):
#     """Test the Instrument Class."""
#     def test_name_num(self):
#         """Test the name_num method."""
#         test1 = lynames.Instrument('violin', 1)
#         self.assertEqual(
#             test1.name_num(form='num'),
#             'violin_1'
#         )
#
#         self.assertEqual(
#             test1.name_num(form='word'),
#             'violin_one'
#         )
