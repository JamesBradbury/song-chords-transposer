"""
Module containing chord class and related constants.
"""
import logging

ST_IN_OCTAVE = 12

DEFAULT_CHORD_ROOTS = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
ILLEGAL_CHORD_NAMES = ['Chorus', 'Bridge', 'Capo']

SUBCHORD_SEPS = ['/']
DEFAULT_SUB_SEP = '/'

SCALE_MAP = {1: ('A',),
             2: ('A#', 'Bb'),
             3: ('B',),
             4: ('C',),
             5: ('C#', 'Db'),
             6: ('D',),
             7: ('D#', 'Eb'),
             8: ('E',),
             9: ('F',),
             10: ('F#', 'Gb'),
             11: ('G',),
             12: ('G#', 'Ab')}

CHORD_MAP = {'A': 1,
             'A#': 2,
             'Bb': 2,
             'Hb': 2,  # German notation
             'B': 3,
             'H': 3,   # German notation
             'C': 4,
             'C#': 5,
             'Db': 5,
             'D': 6,
             'D#': 7,
             'Eb': 7,
             'E': 8,
             'F': 9,
             'F#': 10,
             'Gb': 10,
             'G': 11,
             'G#': 12,
             'Ab': 12}

# Subjective assessment of how hard it is to play different chord shapes. 0=Easy, 5=Hard
# Usually barre chords are harder.
# Not all variations and chord shapes can listed, but it can fall back to the base if not found.
CHORD_DIFFICULTY = {'A': 1,
                    'Am': 0,
                    'A#': 5,
                    'Bb': 5,
                    'B': 5,
                    'Bm': 2,
                    'C': 0,
                    'C#': 5,
                    'Db': 5,
                    'D': 0,
                    'D#': 5,
                    'Eb': 5,
                    'E': 0,
                    'F': 1,
                    'F#': 5,
                    'Gb': 5,
                    'G': 0,
                    'G#': 5,
                    'Ab': 5}


class Chord(object):
    """
    Class representing musical chords which can be created from text or
    semitone index within an octave.
    """
    __chord_is_valid = False
    __sharp_name = ''
    __flat_name = ''
    __suffixes = ''
    __index = 0  # 0 is an invalid index
    __sub_chord = None

    def __init__(self, *args):
        if len(args) == 1 and type(args[0] == str):
            self._setup_with_text(args[0])
        elif len(args) == 2 and type(args[0] == int):
            self._setup_with_index(args[0], args[1])
        else:
            logging.warning("Invalid chord parameters: {}".format(args))

    def __str__(self):
        """Returns the string used when class instance is printed"""
        return "Chord object %s" % self.get_chord_text()

    def __repr__(self):
        """Returns the string used when class instance is output"""
        return "Chord object: %s" % self.get_chord_text()    

    def _process_suffixes(self, suffixes):
        """Finds any subchords in the suffixes, creating a subchord object,
           or, if none are found, stores suffixes.        
        """
        sub_chord_found = False
        for sep in SUBCHORD_SEPS:
            if sep in suffixes:
                sub_chord_found = True
                sub_chord_text = suffixes.split(sep)[1]
                self.__suffixes = suffixes.split(sep)[0]
                # print("DEBUG: sub-chord found: %s, suffixes: %s" % (sub_chord_text, self.__suffixes)
                self.__sub_chord = Chord(sub_chord_text) 
        
        if not sub_chord_found:        
            self.__suffixes = suffixes

    def _setup_with_index(self, index, suffixes):
        """
        Creates a chord with the specified index and the specified suffixes,
        which are not checked.
        """
        if index not in SCALE_MAP:
            logging.warning("Invalid index: {}".format(index))
        else:
            self.__index = index
            self.__sharp_name = SCALE_MAP[index][0]
            if len(SCALE_MAP[index]) > 1:
                self.__flat_name = SCALE_MAP[index][1]
            else:
                self.__flat_name = self.__sharp_name
            self._process_suffixes(suffixes)
            self.__chord_is_valid = True

    def _setup_with_text(self, chord_text):
        """
        Partially checks validity of chord_text and uses it to populate the
        class variables above.
        """
        self._populate_names_and_suffixes(chord_text.strip())
        if self.__sharp_name in CHORD_MAP:
            self.__index = CHORD_MAP[self.__sharp_name]
            self._setup_with_index(self.__index, self.__suffixes)
        elif self.__flat_name in CHORD_MAP:
            self.__index = CHORD_MAP[self.__flat_name]
            self._setup_with_index(self.__index, self.__suffixes)
        else:
            logging.warning("Invalid chord: '{}'".format(chord_text))

    def _populate_names_and_suffixes(self, chord_text):
        """
        Splits the chord_text into chord root (including any sharp or flat) and
        populates the class names for the sharp/flat names.
        Anything which follows is assumed to be a valid suffix and stored in
        suffixes.
        """
        # Check it starts with a valid letter
        valid_letters = set([a[0] for a in CHORD_MAP.keys()])
        if not chord_text[0].upper() in valid_letters:
            logging.warning("Invalid chord: '{}'".format(chord_text))
        else:
            # Start name with first letter of chord text in upper case.
            name = chord_text[0].upper()
            suffs = ''
            for char in chord_text[1:]:
                if char in ['#', 'b']:
                    name = chord_text[:2]
                else:
                    suffs = suffs + char
            self.__suffixes = suffs

            if '#' in name:
                self.__sharp_name = name

            elif 'b' in name:
                self.__flat_name = name
            else:
                self.__sharp_name = self.flat_name = name

    def is_valid(self):
        """Returns true if the chord appears to be valid."""
        return self.__chord_is_valid

    def get_chord_text(self):
        """
        Returns a string representing the chord, including all suffixes 
        and any sub-chord.
        This is the sharp name by default.
        """
        return self.__sharp_name + self.get_suffixes()

    def get_sharp_name(self):
        """Returns the chord's root sharp name, or an empty string."""
        return self.__sharp_name + self.get_suffixes()

    def get_flat_name(self):
        """Returns the chord's root flat name, or an empty string."""
        return self.__flat_name + self.get_suffixes()

    def get_suffixes(self):
        """Returns the chord's suffixes (and sub-chord), or an empty string."""
        if self.__sub_chord:
            real_sub_chord_text = DEFAULT_SUB_SEP + self.__sub_chord.get_chord_text()
        else:
            real_sub_chord_text = ''
            
        return self.__suffixes + real_sub_chord_text

    def transpose(self, semitones):
        """
        transposes the chord up or down the specified number of semitones.
        Alters all class variables to match.
        + Could also transpose additional notes, eg: C/G (G currently ignored as
          part of suffixes).
        """
        # Modal addition for transposes beyond single octave.
        # Offset of 1 prevents zero result.
        self._setup_with_index(((self.__index + semitones - 1) % ST_IN_OCTAVE) + 1,
                               self.__suffixes)
        if self.__sub_chord:
            self.__sub_chord.transpose(semitones)

    def get_difficulty(self):
        """
        Returns an int 1-5 representing how hard the chord is to play, especially on a 12-string with a large action.
        1 is easy, 5 is hard.
        :return: int 1-5
        """
        if self.get_chord_text() in CHORD_DIFFICULTY:
            return CHORD_DIFFICULTY[self.get_chord_text()]
        elif self.__sharp_name in CHORD_DIFFICULTY:
            return CHORD_DIFFICULTY[self.__sharp_name]
        elif self.__sharp_name[0] in CHORD_DIFFICULTY:
            return CHORD_DIFFICULTY[self.__sharp_name[0]]
        else:
            logging.ERROR("Could not match difficulty from chord text '{}', defaulting to 3"
                          .format(self.get_chord_text()))
            return 3


if __name__ == '__main__':
    logging.info("Chord class loaded as main")
