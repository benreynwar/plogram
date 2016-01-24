from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

def sort_longest_first(ll):
    with_lengths = [(len(l), l) for l in ll]
    with_lengths.sort(reverse=True)
    without = [wl[1] for wl in with_lengths]
    return without

# Second key is closest to the modifier.
bases = (
    ('L', (MID, MID)),
    ('TH', (NON, UPP)),
    ('N', (LOW, UPP)),
    ('T', (NON, LOW)),
    ('D', (LOW, NON)),
    ('W', (UPP, LOW)),
    ('M', (MID, NON)),
    ('F', (MID, UPP)),
    ('H', (MID, LOW)),
    ('G', (LOW, LOW)),
    ('C', (NON, MID)),
    ('P', (UPP, UPP)),
    ('',  (NON, NON)),
    ('R', (UPP, NON)),
    ('V', (LOW, MID)),
    ('B', (UPP, MID)),
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
    ('AI', (LOW, LOW)),
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
    '': ('',  'S', 'Y', "'"),    
    'TH': ('TH', 'QU',  'AR',   'STR'),
    'T': ('T',  'ST',  'TR', 'IT'), 
    'R': ('R',  'OR',  'WH', 'SH'),

    'D': ('D',  'ID',  'K',  'AT'),  
    'C': ('C',  'IC',  'CR',  'CL'), 
    'F': ('F',  'I',  'FR',  'A'), 
    'P': ('P',  'SP',  'PR',  'PL'), 

    'G': ('G',  'AG',  'GR',  'Z'), 
    'W': ('W',  'IS',  'COMP', 'PH'), 
    'N': ('N',  'IN',  'U', 'IND'),
    'L': ('L',  'AL',  'UL', 'J'), 

    'M': ('M',  'AM',  'DR',  'COMM'),
    'V': ('V',  'EXP',  'Q',  'ACC'),
    'B': ('B',  'UN',   'BR',  'REC'), 
    'H': ('H',  'CH',  'UR',   'ACT'),
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
    '': ('',  'S', 'Y', "YS"),    
    'TH': ('TH', 'SS',  'THER',   'NO'),
    'T': ('T',  'ST',  'RT', 'TION'), 
    'R': ('R',  'RS',  'TED', 'SH'),

    'D': ('D',  'ND',  'K',  'LD'),  
    'C': ('C',  'NC',  'CT',  'CK'), 
    'F': ('F',  'TY',  'FF',  'X'), 
    'P': ('P',  'O',  'SED',  'TS'), 

    'G': ('G',  'NG',  'GHT',  'NDS'), 
    'W': ('W',  'TES',  'TER', 'CTION'), 
    'N': ('N',  'NS',  'NT', 'NTS'),
    'L': ('L',  'LY',  'LLY', 'LL'), 

    'M': ('M',  'LO',  'RD',  'MENT'),
    'V': ('V',  'VES',  'VER',  'DUC'),
    'B': ('B',  'TIONS',   'BILITY',  'BL'), 
    'H': ('H',  'CH',  'SE',   'NY'),
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
    # Upper case
    uppercase_key = ks[6]
    # Ending
    print(ks[16:18])
    if ks[16: 18] == (True, False):
        # Add space to the end
        ending = ''
    elif ks[16: 18] == (False, True):
        ending = '{^}{#Alt_L(slash)}'
    elif ks[16: 18] == (True, True):
        ending = '_{^}'
    else:
        ending = '{^}'
    # Combine
    if None in (start, vowel, end):
        combined = None
    else:
        combined = start + vowel + end
        combined = combined.lower()
    if combined and uppercase_key:
        combined = combined[0].upper() + combined[1:]
    if ending and combined:
        combined += ending
    return combined
