import unittest

import chord


class TestChordValidity(unittest.TestCase):
    def setUp(self):
        self.data_and_expectations = [
            ('A', True),
            ('B', True),
            ('Bm', True),
            ('A#', True),
            ('A#m', True),
            ('Am#', False),
            ('H', True),    # German notation = B
            ('J', False),
        ]

    def test_valid_and_invalid_chords(self):
        for test_input, expectation in self.data_and_expectations:
            c = chord.Chord(test_input)
            self.assertEqual(c.is_valid(), expectation)


class TestChordNames(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_em_default_name(self):
        em = chord.Chord(8, 'm')
        self.assertEqual(em.get_chord_text(), 'Em')

    def test_get_em_sharp_name(self):
        em = chord.Chord(8, 'm')
        self.assertEqual(em.get_sharp_name(), 'Em')

    def test_get_em_flat_name(self):
        em = chord.Chord(8, 'm')
        self.assertEqual(em.get_flat_name(), 'Em')


class TestGetSuffixes(unittest.TestCase):
    def setUp(self):
        self.data_and_expectations = [
            ('Em7', 'm7'),
            ('A', ''),
            ('Bbm', 'm'),
            ('G/C', '/C')
        ]

    def test_transposing_chords(self):
        for chord_text, expectation in self.data_and_expectations:
            c = chord.Chord(chord_text)
            self.assertEqual(c.get_suffixes(), expectation)


class TestTransposeChords(unittest.TestCase):
    def setUp(self):
        self.data_and_expectations = [
            ('Em', -3, 'C#m'),
            ('Esus4', +1, 'Fsus4'),
            ('Bm7', 0, 'Bm7'),
            ('Ab', +1, 'A'),
            ('G', +5, 'C'),
            ('C', -5, 'G'),
            ('F#', -2, 'E'),
        ]

    def test_transposing_chords(self):
        for chord_text, semitones, expectation in self.data_and_expectations:
            c = chord.Chord(chord_text)
            c.transpose(semitones=semitones)
            self.assertEqual(c.get_chord_text(), expectation)


class TestGetDifficulty(unittest.TestCase):
    def setUp(self):
        self.simple_data_and_expectations = [
            ('E', 0),
            ('F', 1),
            ('B', 5),
            ('A', 1),
            ('G', 0),
            ('C', 0),
        ]
        self.sharps_flats_minors_data_and_expectations = [
            ('Em', 0),
            ('F#', 5),
            ('Bm', 2),
            ('Am', 0),
            ('Gb', 5),
            ('C#m', 5),
        ]
        self.suffixes_data_and_expectations = [
            ('Asus2', 1),
            ('Dsus4', 0),
            ('Cadd9', 0),
            ('E7', 0),
            ('Gbm', 5),
            ('C#m7', 5),
        ]

    def test_simple_chords(self):
        for chord_text, expected_difficulty in self.simple_data_and_expectations:
            c = chord.Chord(chord_text)
            result = c.get_difficulty()
            self.assertEqual(result, expected_difficulty)

    def test_sharps_flats_minors(self):
        for chord_text, expected_difficulty in self.sharps_flats_minors_data_and_expectations:
            c = chord.Chord(chord_text)
            result = c.get_difficulty()
            self.assertEqual(result, expected_difficulty)

    def test_suffixes(self):
        for chord_text, expected_difficulty in self.suffixes_data_and_expectations:
            c = chord.Chord(chord_text)
            result = c.get_difficulty()
            self.assertEqual(result, expected_difficulty)
