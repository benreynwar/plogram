from stenoprog import keys, state
from stenoprog.keys import UPP, MID, NON, LOW

def sort_longest_first(ll):
    with_lengths = [(len(l), l) for l in ll]
    with_lengths.sort(reverse=True)
    without = [wl[1] for wl in with_lengths]
    return without

# Second key is closest to the modifier.
bases = (
    ('', (NON, NON)),
    ('T', (NON, UPP)),
    ('TH', (NON, LOW)),
    ('W', (UPP, NON)),
    ('G', (LOW, NON)),
    ('N', (UPP, UPP)),
    ('F', (LOW, LOW)),
    ('L', (NON, MID)),
    ('R', (MID, NON)),
    ('P', (UPP, LOW)),
    ('C', (LOW, UPP)),
    ('V', (MID, MID)),
    ('H', (UPP, MID)),
    ('M', (MID, UPP)),
    ('D', (MID, LOW)),
    ('B', (LOW, MID)),
)

keys_to_base = {}
for base, positions in bases:
    ks = []
    for position in positions:
        ks += keys.position_to_keys(position)
    keys_to_base[tuple(ks)] = base

base_to_keys = dict([(v, k) for k, v in keys_to_base.items()])

vowels = (
    ('', (NON, NON)),   
    ('A', (LOW, NON)),
    ('O', (UPP, NON)),
    ('E', (NON, UPP)),
    ('U', (NON, LOW)),
    ('I', (NON, MID)),
    ('IO', (MID, NON)),
    ('EA', (LOW, UPP)),
    ('OU', (UPP, LOW)),
    ('IE', (UPP, UPP)),
    ('-E', (LOW, LOW)),
    ('A-E', (LOW, MID)),
    ('O-E', (UPP, MID)),
    ('U-E', (MID, LOW)),
    ('I-E', (MID, MID)),
    ('E-E', (MID, UPP)),
)

vowels_list = [v[0] for v in vowels if v[0]]

keys_to_vowel = {}
for vowel, positions in vowels:
    ks = []
    if positions is not None:
        for position in positions:
            ks += keys.position_to_keys(position)
        keys_to_vowel[tuple(ks)] = vowel

vowel_to_keys = dict([(v, k) for k, v in keys_to_vowel.items()])


# Order is None, Lower, Middle, Upper
ortho_starts = {
    '':  ('',   'S',  "'",  'Y'),    
    'T': ('T',  'IT', 'AT', 'ST'), 
    'TH':('TH', 'IS', 'J',  'Z'),
    'W': ('W',  'I',  'A',  'U'),

    'G': ('G',  'WH', 'AG', 'GR'),  
    'N': ('N',  'IN', 'UN', 'AR'),
    'F': ('F',  'SH', 'CH', 'FR'), 
    'L': ('L',  'UL', 'AL', 'TR'), 

    'R': ('R',  'UR', 'STR', 'OR'), 
    'P': ('P',  'SP', 'PL', 'PR'), 
    'C': ('C',  'IC', 'CL', 'CR'),
    'V': ('V',  'XXX','ACT','ACC'), 

    'H': ('H',  'K','PH', 'EXP'),
    'M': ('M',  'COMP','AM','COMM'),
    'D': ('D',  'ID', 'REC','DR'),
    'B': ('B',  'QU', 'Q',  'BR'), 
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
    '': ('/E',  'S/ES', 'SE/YS', 'Y/YING'), 
    'T': ('T/TE',  'TS/TES',  'TION/TIONS', 'ST/STS'),
    'TH': ('TH/THER', 'XXX/NCE',  'TER/TED', 'TY/TING'),  
    'W': ('ND/W',  'NDS/I', 'X/A', 'RT/O'), 
    'G': ('G/GE',  'NG/NGE',  'CTION/CTED',  'GHT/RN'),
    'N': ('N/NE',  'NS/NES',  'NT/NTS', 'NY/NING'),
    'F': ('F/FE',  'SH/SES', 'CH/SED', 'FF/FFE'),
    'L': ('L/LE',  'LS/LES', 'LD/AL', 'LY/NI'), 

    'R': ('R/RE',  'RS/RES', 'RD/RED', 'RY/RING'),
    'P': ('P/PE',  'LL/LI', 'IN/LO', 'LLY/LLING'),
    'C': ('C/CE',  'CT/CES', 'NAL/NO', 'XXX/RK'),
    'V': ('V/VE',  'TIVE/VES',  'VER/VED', 'CTIVE/VING'),
    'H': ('H/SS',  'K/KE', 'LF/WN', 'SSION/SION'),
    'M': ('M/ME',  'MS/MES', 'CK/MO', 'RM/MENT'),
    'D': ('D/DE',  'DS/DES',  'DER/DU', 'NTLY/NDING'),
    'B': ('B/BE',  'BLE/BLI', 'BILITY/NED', 'XXX/NA'),
}
 

first_ends_list = []
second_ends_list = []
for ss in ortho_ends.values():
    for end in ss:
        if end is None:
            continue
        pieces = end.split('/')
        if len(pieces) == 1:
            first = pieces[0]
            second = pieces[0] + 'E'
        elif len(pieces) == 2:
            first = pieces[0]
            second = pieces[1]
        else:
            raise Exception('Unknown end format.')
        first_ends_list.append(first)
        second_ends_list.append(second)
        

ends_list = []
for ss in ortho_ends.values():
    ends_list += [s for s in ss if s]

end_to_keys = {}
for base in [b[0] for b in bases]:
    base_keys = base_to_keys[base]
    for index, end in enumerate(ortho_ends[base]):
        combined_keys = add_keys[index] + base_keys
        split_end = end.split('/')
        for e in split_end:
            end_to_keys[e] = combined_keys
        end_to_keys[combined_keys] = combined_keys

def keys_to_index(ks):
    return {
        (False, False): 0,
        (True, False): 1,
        (True, True): 2,
        (False, True): 3,
    }[ks]

def chord_to_keys(start, vowel, end):
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
    ks = start_keys + [False, False] + vowel_keys[:2] + end_keys + [False, False] + vowel_keys[2:]
    return ks

def translate_ortho_keys(ks):
    # Get start
    start_base_keys = ks[2: 6]
    start_base = keys_to_base[start_base_keys]
    start_mod_keys = ks[0: 2]
    start_mod_index = keys_to_index(tuple(start_mod_keys))
    start = ortho_starts[start_base][start_mod_index]
    # Get end
    end_base_keys = ks[12: 16]
    end_base = keys_to_base[end_base_keys]
    end_mod_keys = ks[10: 12]
    end_mod_index = keys_to_index(tuple(end_mod_keys))
    end = ortho_ends[end_base][end_mod_index]
    # Get vowel
    vowel_keys = ks[8: 10] + ks[18:20]
    vowel = keys_to_vowel[vowel_keys]
    # Combine vowel and end
    if vowel[-2:] == '-E':
        second_end = True
        vowel = vowel[:-2]
    else:
        second_end = False
    split_end = end.split('/')
    if len(split_end) == 1:
        if second_end:
            end = end + 'E'
    elif len(split_end) == 2:
        if second_end:
            end = split_end[1]
        else:
            end = split_end[0]
    else:
        raise Exception('Unknown end format')
    # Upper case
    uppercase_key = ks[6]
    # All upper case
    alluppercase_key = ks[7]
    # Ending
    ending_type = state.state['ending']
    if ks[16: 18] == (True, False):
        # Add space to the end
        ending = ''
    elif ks[16: 18] == (False, True):
        ending = '.' if ending_type == state.TEXT_ENDINGS else '{^}{#Alt_L(slash)}'
    elif ks[16: 18] == (True, True):
        ending = ',' if ending_type == state.TEXT_ENDINGS else '_{^}'
    else:
        ending = '{^}'
    # Combine
    if None in (start, vowel, end):
        combined = None
    else:
        combined = start + vowel + end
        combined = combined.lower()
    if combined and uppercase_key:
        if alluppercase_key:
            combined = combined.upper()
        else:
            combined = combined[0].upper() + combined[1:]
    if ending and (combined is not None):
        combined += ending
    return combined
