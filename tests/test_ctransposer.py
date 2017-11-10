import unittest

import chord
import ctransposer

TEST_DATA = {6: [['Am', 11], ['C', 25], ['G', 35], ['Am(*)', 44]],
             15: [['F', 8], ['C', 18],  ['F', 29], ['C', 50], ['C/B', 55], ['F', 63]],
             17: [['C', 19], ['Am(*)', 29]], 19: [['F', 8], ['C', 19], ['F', 30], ['C', 53], ['C/B', 58], ['F', 65]],
             21: [['C', 15], ['G', 26]],
             24: [['Am', 18], ['C', 34], ['G', 51], ['F', 62], ['Am', 71], ['C', 75], ['G', 78]],
             27: [['F', 8], ['C', 20], ['F', 26], ['C', 53], ['F', 61]],
             29: [['C', 19], ['Am(*)', 26]], 31: [['F', 15], ['C', 28], ['Am', 40], ['G', 50], ['F', 58]],
             33: [['Am', 15], ['C', 28], ['G', 43]]}


class TestGetTotalDifficulty(unittest.TestCase):

    def setUp(self):
        self.test_data = {}
        for line_no, chord_list in TEST_DATA.items():
            new_chord_list = []
            for chord_text, col in chord_list:
                new_chord_list.append([chord.Chord(chord_text), col])
            self.test_data[line_no] = new_chord_list

    def test_easy_song(self):
        result = ctransposer.get_total_difficulty(chords_dict=self.test_data)
        self.assertEqual(result, 15)

    def test_easy_song_plus_two(self):
        ctransposer.transpose_song_dict(self.test_data, 2)
        result = ctransposer.get_total_difficulty(chords_dict=self.test_data)
        self.assertEqual(result, 31)

    def test_easy_song_plus_three(self):
        ctransposer.transpose_song_dict(self.test_data, 3)
        result = ctransposer.get_total_difficulty(chords_dict=self.test_data)
        self.assertEqual(result, 170)
