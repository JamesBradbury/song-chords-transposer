'''
Transposes chords text files into other keys.
Can be helpful for acoustic players with a capo.
'''

'''
Todo:
1. Auto-tune for easy 12-string playing with open chords
2. Chord pro compatible mode.
3. Handle compound/sub-chords - DONE
4. Fix bug where line 21 of 74-75.txt is not included. - DONE

'''

import sys
import chord
# from string import letters, digits
from optparse import OptionParser
#from copy import deepcopy


def is_chord_line(line):
    '''
    Tests the first letter after each space to see if it is a valid chord
    start. Returns True if letters which could be chords significantly
    outnumber those which aren't.
    + Could have a regex solution?
    '''
    chordy = 0
    non_chordy = 0
    previous_char = ' '  # Causes check on first char.
    illegal_items = any(name in line for name in chord.ILLEGAL_CHORD_NAMES)
    
    for char in line:
        if previous_char == ' ' and char != ' ':
            if char.upper() in chord.DEFAULT_CHORD_ROOTS:
                chordy += 1
            # Count any other "ordinary" chars as non-chordy
            elif ord(char) >= 33 and ord(char) <= 126:
                non_chordy +=1         
        previous_char = char
    
    if line.strip(' ').startswith('C '):
        result = (chordy >= 1 + (non_chordy * 2)) and not illegal_items
        print "DEBUG: result: %s, ille_i: %s, ch: %s, n_ch: %s" % (result, illegal_items, chordy, non_chordy)
        
    return (chordy >= 1 + (non_chordy * 2)) and not illegal_items
  
def split_chord_line(c_line):
    '''
    Splits a chord line into chord object and the column in which it starts.
    Only works on lines containing chords.
    A column of -1 indicates an error.
    '''  
    chords = []
    chord_text = ''
    chord_text_col = -1
    for column, char in enumerate(c_line):
        if chord_text != '':
            # End of chord
            if char == ' ':
                chords.append([chord.Chord(chord_text),
                               chord_text_col])
                chord_text = ''
            else:
                chord_text += char
        # Only get chords with valid start.
        elif char in chord.DEFAULT_CHORD_ROOTS:
            chord_text_col = column
            chord_text = char    
                           
    # Append final chord, if any                
    if chord_text != '':
        chords.append([chord.Chord(chord_text), chord_text_col])

    return chords

def get_chords_from_song(song, shift=0):
    '''
    Extracts chords from a list of strings (eg: file) and stores them in a
    dictionary indexed by line number with values in the following form:
    [[chord_obj, column_chord_starts], [..], ...]
    Assumes that a line with chords contains *only* chords.
    '''
    indexed_chord_lines = {}
    found_some_chords = False
    for line_no, line_text in enumerate(song):
        if line_no == 21:
            print "DEBUG: line found!!", line_text           
        if is_chord_line(line_text):
            # TODO: check '    C    G' works here.
            found_some_chords = True
            indexed_chord_lines[line_no] = split_chord_line(line_text)
    if not found_some_chords:
        print "Could not find any chords in song!"
        
    return indexed_chord_lines

def transpose_song_dict(chords_dict, semitones):
    '''
    Transposes all chords in the dictionary structure by the specified number
    of semitones. chords_dict is modified in place.
    '''
    if semitones != 0:
        for line in chords_dict.iteritems():
            for chord_ref in line[1]:
                # Check the object type first
                if type(chord_ref[0]) == chord.Chord:
                    chord_ref[0].transpose(semitones)
                    
def transpose_song_lines(song, semitones, empty_list_on_error=True):
    '''
    Transposes all chords in the file by the number of semitones specified.
    If there are any errors, then, by default, an empty list is returned.
    '''
    # Make a copy of song list of strings.
    transposed_song = song[:]
    song_chords = get_chords_from_song(song)
    # Modify song chords in place
    transpose_song_dict(song_chords, semitones)
    # print song_chords[15]
    
    # Put new chords into song lines.
    for line_no in song_chords.keys():
        line_list = list(transposed_song[line_no])
        for chord_pair in song_chords[line_no]:
            chord_text = chord_pair[0].get_chord_text()
            for offset, char in enumerate(chord_text):
                line_list[chord_pair[1] + offset] = char
        transposed_song[line_no] = "".join(line_list)
            
    return transposed_song


def handle_options():
    """ Processes the command-line parameters returning resulting variables. """
    ops = OptionParser(usage="ctransposer.py [options]")
    ops.add_option("--file", "-f",
        action="store", dest="filename", default="",
        help="Text file containing *single* song." )
    ops.add_option("--semitones", "-s", action="store", 
        dest="semitones", default=0, type="int",
        help="Positive/negative semitones by which to transpose the song. " 
             "Defaults to '%default', unless --auto specified.")
    ops.add_option("--auto", "-a", action="store_true", dest="auto",
        default=False,
        help="Automatically find a key which is easy to play using open "
             "chords.")

    # Throw away any spare parameters.
    options, _ = ops.parse_args()
    
    if options.filename == '':
        print "No file specified - nothing to do!"
        sys.exit(1)
        
    return options.filename, options.semitones, options.auto

def main():
    '''
    Main entry point where it all kicks off.
    '''
    filename, semitones, auto = handle_options()
       
    with open(filename, mode='r') as song_file:
        song_lines = song_file.readlines()
        #song_chords = get_chords_from_song(song_lines)
        transposed_song = transpose_song_lines(song_lines, semitones)
        
        print "orig:", song_lines[21]
        print "tran:", transposed_song[21]
  
    if semitones == 0:
        file_suffix = ''
    elif semitones > 0:
        file_suffix = '+' + str(semitones)
    elif semitones < 0:
        file_suffix = str(semitones)

    new_filename = "%s[%+d].%s" \
            % (filename.split('.')[0], semitones, filename.split('.')[1]) 
        
    with open(new_filename, mode='w') as tran_file:
        tran_file.writelines(transposed_song)
        print "Wrote: %s line to file %s" % (len(transposed_song),
                                             filename + file_suffix)
  
    
#    print sorted(song_chords.iteritems())
        
    
if __name__ == '__main__':
    main()