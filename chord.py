"""
Module containing chord class and related constants.
"""

ST_IN_OCTAVE = 12

DEFAULT_CHORD_ROOTS = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#',
                       'E', 'F', 'F#', 'G', 'G#']

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

CHORD_MAP = {'A' : 1,
             'A#': 2,
             'Bb': 2,
             'Hb': 2,  # German notation
             'B' : 3,
             'H' : 3,  # German notation
             'C' : 4,
             'C#': 5,
             'Db': 5,
             'D' : 6,
             'D#': 7,
             'Eb': 7,
             'E' : 8,
             'F' : 9,
             'F#': 10,
             'Gb': 10,
             'G' : 11,
             'G#': 12,
             'Ab': 12}


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
        if len(args) == 1 and type(args[0] == int):
            self._setup_with_text(args[0])
        elif len(args) == 2 and type(args[0] == str):
            self._setup_with_index(args[0], args[1])
        else:
            print("Invalid chord parameters.")

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
                #print("DEBUG: sub-chord found: %s, suffixes: %s" % (sub_chord_text, self.__suffixes)
                self.__sub_chord = Chord(sub_chord_text) 
        
        if not sub_chord_found:        
            self.__suffixes = suffixes

    def _setup_with_index(self, index, suffixes):
        """
        Creates a chord with the specified index and the specified suffixes,
        which are not checked.
        """
        if not index in SCALE_MAP:
            print("Invalid index: %s" % index)
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
        if self.__sharp_name != '':
            self.__index = CHORD_MAP[self.__sharp_name]
            self._setup_with_index(self.__index, self.__suffixes)
        elif self.__flat_name != '':
            self.__index = CHORD_MAP[self.__flat_name]
            self._setup_with_index(self.__index, self.__suffixes)
        else:
            print("Invalid chord.")

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
            print("Invalid chord found: %s" % chord_text)
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
            # print("DEBUG: transposing sub-chord: %s" % self.__sub_chord.get_chord_text()
            self.__sub_chord.transpose(semitones)
            # print("DEBUG: transposed sub-chord: %s" % self.__sub_chord.get_chord_text()


def test_chord():
    """Set of simple tests for chord class."""
    a = Chord("A#  ")
    b = Chord("Bm")
    c = Chord("S/G")
    print("'S/G' is valid: ", c.is_valid())
    d = Chord("D#7Sus2")
    print("chord name: ", d.get_chord_text())
    em = Chord(8, 'm')
    print("---")
    print("Chord name: ", em.get_chord_text())
    print("sharp name: ", em.get_sharp_name())
    print("flat name: ", em.get_flat_name())
    em.transpose(-3)
    print("- transpose Em -3 -")
    print("Chord name: ", em.get_chord_text())
    print("sharp name: ", em.get_sharp_name())
    print("flat name: ", em.get_flat_name())
    b.transpose(-2)
    print("- transpose Bm -2 -")
    print("Chord name: ", b.get_chord_text())
    print("sharp name: ", b.get_sharp_name())
    print("flat name: ", b.get_flat_name())
    print("Suffixes: ", b.get_suffixes())

if __name__ == '__main__':
    print("Chord class loaded as main")
    test_chord()

# x-test
