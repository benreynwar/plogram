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
    ('OU', (UPP, LOW)),
    ('IO', (MID, NON)),
    ('EA', (LOW, UPP)),
    ('IE', (MID, MID)),
    ('EE', (MID, UPP)),
    ('AI', (LOW, MID)),
    ('OO', (MID, LOW)),
    #('OA', (MID, NON)), # uncommon ei and eu more common
    ('AU', (LOW, LOW)), # uncommon
    ('OE', (UPP, UPP)), # uncommon
)

vowels_list = sort_longest_first([v[0] for v in vowels if v[0]])

keys_to_vowel = {}
for vowel, positions in vowels:
    ks = []
    for position in positions:
        ks += keys.position_to_keys(position)
    keys_to_vowel[tuple(ks)] = vowel

vowel_to_keys = dict([(v, k) for k, v in keys_to_vowel.items()])

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
