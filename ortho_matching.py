
start_regex = '|'.join(starts_list)
vowel_regex = '|'.join(vowels_list)
end_regex = '|'.join(ends_list)
final_regex = '|'.join(finals_list)

meta_chord_regex = '(?P<start{{num}}>{})(?P<vowel{{num}}>{})(?P<end{{num}}>{})(?P<final{{num}}>{})'.format(start_regex, vowel_regex, end_regex, final_regex)
start_vowel_regex = '(?P<start{{num}}>{})(?P<vowel{{num}}>{})'.format(start_regex, vowel_regex)
start_vowel_end_regex = '(?P<start{{num}}>{})(?P<vowel{{num}}>{})(?P<end{{num}}>{})'.format(start_regex, vowel_regex, end_regex)

start_vowel_rem_regex = '^(?P<start>{})?(?P<vowel>{})?(?P<remainder>.*?)$'.format(
    start_regex, vowel_regex)
start_vowel_rem_pattern = re.compile(start_vowel_rem_regex)
end_rem_regex = '^(?P<end>{})?(?P<remainder>.*?)$'.format(end_regex)
end_rem_pattern = re.compile(end_rem_regex)
final_rem_regex = '^(?P<final>{})?(?P<remainder>.*?)$'.format(final_regex)
final_rem_pattern = re.compile(final_rem_regex)

def match_text(text):
    old_remainder = None
    remainder = text
    chords = []
    while (old_remainder != remainder) and remainder:
        old_remainder = remainder
        start, vowel, end, final, remainder = match_chord(remainder)
        chords.append({'start': start, 'vowel': vowel, 'end': end, 'final': final})
    result = None
    if remainder == '':
        result = chords
    return result
        
def match_chord(text):
    start, vowel, remainder = match_start_and_vowel(text)
    if remainder:
        end, remainder = match_end(remainder)
    else:
        end = None
    if remainder:
        final, remainder = match_final(remainder)
    else:
        final = None
    return start, vowel, end, final, remainder

def match_start_and_vowel(text):
    match = start_vowel_rem_pattern.match(text)
    start = None
    vowel = None
    if match:
        gd = match.groupdict()
        start = gd['start']
        vowel = gd['vowel']
        remainder = gd['remainder']
    else:
        remainder = text
    return start, vowel, remainder

def match_end(text):
    match = end_rem_pattern.match(text)
    end = None
    if match:
        gd = match.groupdict()
        end = gd['end']
        remainder = gd['remainder']
    else:
        remainder = text
    return end, remainder

def match_final(text):
    match = final_rem_pattern.match(text)
    final = None
    if match:
        gd = match.groupdict()
        final = gd['final']
        remainder = gd['remainder']
    else:
        remainder = text
    return final, remainder

chord_regex = '^' + meta_chord_regex.format(num='') + '$'
def make_chord_regex(i):
    regex = meta_chord_regex.format(num=str(i))
    return regex

def make_multi_chord_regex(n_chords):
    regex = '^'
    for i in range(0, n_chords):
        regex += make_chord_regex(i)
    regex += '$'
    return regex

multi_chord_patterns = {}
def get_multi_chord_pattern(n_chords):
    if not n_chords in multi_chord_patterns:
        multi_chord_patterns[n_chords] = re.compile(make_multi_chord_regex(n_chords))
    return multi_chord_patterns[n_chords]

def get_n_chords(word):
    word = word.upper()
    for n_chords in range(1, 11):
        regex = make_multi_chord_regex(n_chords)
        pattern = get_multi_chord_pattern(n_chords)
        if re.match(pattern, word):
            return n_chords
    return None
    
    
#def translate_text(text):
#    '''
#    Assume that is can be encoded in a single chord.
#    '''
 
if __name__ == '__main__':
    while True:
        text = raw_input('Enter text:')
        chords = match_text(text)
        if chords is None:
            print('Cannot encode word')
        else:
            for chord in chords:
                keys = chord_to_keys(chord['start'], chord['vowel'], chord['end'], chord['final'])
                vchord = visualize.visualize_keys(keys)
                print(vchord)
