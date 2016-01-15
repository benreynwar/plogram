import re

from stenoprog import visualize

UPP = 'UPPER'
LOW = 'LOWER'
MID = 'MIDDLE'
NON = 'NEITHER'

def sort_longest_first(ll):
    with_lengths = [(len(l), l) for l in ll]
    with_lengths.sort(reverse=True)
    without = [wl[1] for wl in with_lengths]
    return without

def position_to_keys(position):
    if position == LOW:
        keys = (True, False)
    elif position == UPP:
        keys = (False, True)
    elif position == MID:
        keys = (True, True)
    elif position == NON:
        keys = (False, False)
    else:
        raise ValueError('Unknown position {}'.format(position))
    return keys

def positions_to_keys(positions, reversed=False):
    keys = []
    for position in positions:
        if reversed:
            keys[0:0] = position_to_keys(position)
        else:
            keys += position_to_keys(position)
    return tuple(keys)

# Second key is closest to the modifier.
bases = (
    ('L', (MID, MID)),
    ('TH', (NON, UPP)),
    ('N', (LOW, UPP)),
    ('T', (NON, LOW)),
    ('D', (LOW, NON)),
    ('W', (UPP, LOW)),
    ('B', (MID, NON)),
    ('F', (MID, UPP)),
    ('H', (MID, LOW)),
    ('G', (LOW, LOW)),
    ('C', (NON, MID)),
    ('P', (UPP, UPP)),
    ('',  (NON, NON)),
    ('R', (UPP, NON)),
    ('K', (LOW, MID)),
    ('M', (UPP, MID)),
)

keys_to_base = {}
for base, positions in bases:
    keys = []
    for position in positions:
        keys += position_to_keys(position)
    keys_to_base[tuple(keys)] = base

base_to_keys = dict([(v, k) for k, v in keys_to_base.items()])

vowels = (
    ('', (NON, NON)),   
    ('A', (LOW, NON)),
    ('O', (UPP, NON)),
    ('E', (NON, UPP)),
    ('U', (NON, LOW)),
    ('I', (NON, MID)),
    ('OU', (UPP, LOW)),
    ('IO', (UPP, MID)),
    ('EA', (LOW, UPP)),
    ('IE', (MID, MID)),
    ('EE', (MID, UPP)),
    ('AI', (LOW, MID)),
    ('OO', (MID, LOW)),
    ('OA', (MID, NON)), # uncommon ei and eu more common
    ('AU', (LOW, LOW)), # uncommon
    ('OE', (UPP, UPP)), # uncommon
)

vowels_list = sort_longest_first([v[0] for v in vowels if v[0]])

keys_to_vowel = {}
for vowel, positions in vowels:
    keys = []
    for position in positions:
        keys += position_to_keys(position)
    keys_to_vowel[tuple(keys)] = vowel

vowel_to_keys = dict([(v, k) for k, v in keys_to_vowel.items()])

keys_to_final = {
    (False, False): '',
    (True, False): 'E',
    (False, True): 'S',
    (True, True): 'ES',
}

final_to_keys = dict([(v, k) for k, v in keys_to_final.items()])

finals_list = sort_longest_first([f for f in keys_to_final.values() if f])

# Order is None, Lower, Middle, Upper
ortho_starts = {
    'L': ('L',  'SL',   None, None),    # 12 10   8   12       2
    'TH': ('TH', 'V',  'Z',   'THR'), # 1  7    13  10
    'N': ('N',  'SN',  'SPL', 'SPR'),  #13       1
    'T': ('T',  'ST',  'STR', 'TR'),   # 2       3   8
    'D': ('D',  'WH',  None,  'DR'),   # 9       4    7(nd)
    'W': ('W',  'SW',  None,  'WR'),   # 3       14
    'B': ('B',  'Y',   'BL',  'BR'),   # 6           9
    'F': ('F',  'PH',  'FL',  'FR'),   # 8       5
    'H': ('H',  None,  'Q',   'SHR'),  # 5
    'G': ('NG',  'G',  'GL',  'GR'),   # 14      6(ng)
    'C': ('C',  'SC',  'CL',  'CR'),  # 4
    'P': ('P',  'SP',  'PL',  'PR'),   # 11
    '': ('',  'S', 'SQU', 'SCR'),       # 4
    'K': ('K',  'SK',  'QU',  'KN'),
    'R': ('R',  'CH',  'SCH', 'SH'),
    'M': ('M',  'SM',  'X',  'J'),
}

starts_list = []
for ss in ortho_starts.values():
    starts_list += [s for s in ss if s]
starts_list = sort_longest_first(starts_list)

add_keys = {0: (False, False),
            1: (True, False),
            2: (True, True),
            3: (False, True),}

start_to_keys = {}
for base in [b[0] for b in bases]:
    base_keys = base_to_keys[base]
    for index, start in enumerate(ortho_starts[base]):
        combined_keys = add_keys[index] + base_keys
        start_to_keys[start] = combined_keys
        

ortho_ends = {
    'L': ('L',  'LK',  'LL',  'LT'),  
    'TH': ('TH', 'V',  'Z',   'RTH'),
    'N': ('N',  'NK',  'WN',  'RN'), 
    'T': ('T',  'NT',  'CT',  'RT'), 
    'D': ('D',  'ND',  'LD',  'RD'), 
    'W': ('W',  'WN',  'RL',  'XT'), 
    'B': ('B',  'Y',   'BL',  'RB'), 
    'F': ('F',  'PH',  'LF',  'FT'), 
    'H': ('H',  'SH',  'GH',  'GHT'),
    'G': ('NG',  'G',  'GN',  'RG'), 
    'C': ('C',  'NC',  'CH',  'RCH'),
    'P': ('P',  'MP',  'LP',  'RP'), 
    '': ('',  'S',  'SL', 'SS'    ),
    'R': ('R', 'ST', 'TT', 'RST'), #NST 
    'K': ('K',  'SK',  'CK',  'RK'), 
    'M': ('M',  'SM',   'X',   'J'),
}

ends_list = []
for ss in ortho_ends.values():
    ends_list += [s for s in ss if s]
ends_list = sort_longest_first(ends_list)

end_to_keys = {}
for base in [b[0] for b in bases]:
    base_keys = base_to_keys[base]
    for index, end in enumerate(ortho_ends[base]):
        combined_keys = add_keys[index] + base_keys
        end_to_keys[end] = combined_keys

def keys_to_index(keys):
    return {
        (False, False): 0,
        (True, False): 1,
        (True, True): 2,
        (False, True): 3,
    }[keys]

def chord_to_keys(start, vowel, end, final):
    if start:
        start_keys = list(start_to_keys[start])
    else:
        start_keys = [None] * 6
    if vowel:
        vowel_keys = list(vowel_to_keys[vowel])
    else:
        vowel_keys = [None] * 4
    if end:
        end_keys = list(end_to_keys[end])
    else:
        end_keys = [None] * 6
    if final:
        final_keys = list(final_to_keys[final])
    else:
        final_keys = [None] * 2
    keys = start_keys + [False, False] + vowel_keys[:2] + end_keys + final_keys + vowel_keys[2:]
    return keys

def translate_key(keys):
    trans = None
    if not keys[7]:
        trans = translate_normal_key(keys)
    elif keys[4:7] == (False, False, False):
        trans = translate_symbol_key(keys)
    elif keys[4:7] == (False, True, False):
        trans = translate_edit_key(keys)
    else:
        print('not translation')
    return trans

symbol_map = {
    (LOW, NON, NON, NON): '{#Return}',
    (UPP, NON, NON, NON): '{#space}',
    (UPP, NON, UPP, NON): '{#period}',
    (UPP, NON, LOW, NON): '{#comma}',
    (LOW, NON, UPP, NON): '{:}',
    (LOW, NON, LOW, NON): '{;}',
    (UPP, UPP, NON, NON): '(',
    (UPP, LOW, NON, NON): ')',
    (LOW, UPP, NON, NON): '[',
    (LOW, LOW, NON, NON): ']',
    (MID, UPP, NON, NON): '{',
    (MID, LOW, NON, NON): '}',
    (UPP, UPP, UPP, NON): "'",
    (LOW, UPP, UPP, NON): '"',
    (LOW, LOW, LOW, NON): '_',
    (MID, MID, NON, NON): '=',
    (MID, MID, MID, NON): '==',
    (NON, UPP, UPP, NON): '+',
    (NON, LOW, LOW, NON): '-',
}

keys_to_symbol = dict([(positions_to_keys(positions, reversed=True), symbol)
                       for positions, symbol in symbol_map.items()])

def translate_symbol_key(keys):
    symbol = keys_to_symbol.get(keys[10:18], None)
    return symbol

edit_map = {
    ((NON, NON, NON), (NON, UPP, NON, NON, NON)): '{#BackSpace}',
 }

keys_to_edit = dict([(positions_to_keys(positions[0]) + 
                      positions_to_keys(positions[1], reversed=True) , edit)
                     for positions, edit in edit_map.items()])

def translate_edit_key(keys):
    print('translate_edit_key')
    edit = keys_to_edit.get(keys[0: 4] + keys[8: 20], None)
    print(edit)
    return edit

def translate_normal_key(keys):
    # Get start
    start_base_keys = keys[2: 6]
    start_base = keys_to_base[start_base_keys]
    start_mod_keys = keys[0: 2]
    start_mod_index = keys_to_index(tuple(start_mod_keys))
    start = ortho_starts[start_base][start_mod_index]
    # Get end
    end_base_keys = keys[12: 16]
    end_base = keys_to_base[end_base_keys]
    end_mod_keys = keys[10: 12]
    end_mod_index = keys_to_index(tuple(end_mod_keys))
    end = ortho_ends[end_base][end_mod_index]
    # Get vowel
    vowel_keys = keys[8: 10] + keys[18:20]
    vowel = keys_to_vowel[vowel_keys]
    # Upper case
    uppercase_key = keys[6]
    # Space
    space_key = keys[16]
    if space_key:
        space = ' '
    else:
        space = ''
    # Combine
    if None in (start, vowel, end, space):
        combined = None
    else:
        combined = start + vowel + end + space
    combined = combined.lower()
    if combined and uppercase_key:
        combined = combined[0].upper() + combined[1:]
    return combined


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
