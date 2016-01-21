from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

primary_map = {
    (LOW, NON): '.', #TH
    (UPP, NON): '=', #T
    (NON, LOW): "'", #D
    (NON, UPP): '"', #R
    (LOW, UPP): '/', #W
    (UPP, LOW): '+', #N
    (UPP, UPP): '==', #P
    (LOW, LOW): '_', #G
    (MID, NON): '*', #C
    (MID, MID): '!=',  #L
    (NON, MID): '|', #B
    (LOW, MID): '#', #H
    (MID, UPP): '&', #M
    (MID, LOW): '\\ ', #K
    (UPP, MID): '-', #F
    (NON, NON): '',
}

secondary_map = {
    (LOW, NON): '', #TH
    (UPP, NON): '~', #T
    (NON, LOW): '$', #D
    (NON, UPP): '^', #R
    (LOW, UPP): '?', #W
    (UPP, LOW): '', #N
    (UPP, UPP): '%', #P
    (LOW, LOW): '', #G
    (MID, NON): '<=', #C
    (MID, MID): '!', #L
    (NON, MID): '`', #B
    (LOW, MID): '', #H
    (MID, UPP): '@', #M
    (MID, LOW): '>=', #K
    (UPP, MID): '', #F
    (NON, NON): '',
}

bracket_map = {
    (NON, NON): '(',
    (NON, LOW): ')',
    (NON, MID): '()',
    (LOW, NON): '[',
    (LOW, LOW): ']',
    (LOW, MID): '[]',
    (UPP, NON): '\{',
    (UPP, UPP): '\}',
    (UPP, MID): '\{\}',
    (MID, NON): '<',
    (MID, LOW): '>',
    (MID, MID): '<>',
    (NON, UPP): '',
    (LOW, UPP): '',
    (UPP, LOW): '',
    (NON, UPP): '',
}

choice_map = {
    NON: primary_map,
    UPP: bracket_map,
    LOW: secondary_map,
    MID: None,
}

first_modifier_map = {
    NON: '',
    UPP: ',',
    LOW: ';',
    MID: ':',
}

second_modifier_map = {
    NON: '{^}',
    UPP: '{^}{#Return}',
    LOW: '',
    MID: '{^}{#Return Tab}',
}


def translate_symbol_keys(ks):
    ps = keys.keys_to_positions(ks)

    null_positions = tuple(ps[0: 2])
    necessary_positions = tuple(ps[2: 4])
    choice_positions = ps[4]
    pinky_position = ps[5]
    main_positions = tuple(ps[6: 8])
    second_modifier_positions = ps[8]
    first_modifier_positions = ps[9]

    assert(necessary_positions == (NON, UPP))
    if null_positions == (NON, NON) and pinky_position == NON:
        main_map = choice_map[choice_positions]
        if main_map is None:
            main_symbol = ''
        else:
            main_symbol = main_map[tuple(reversed(main_positions))]
            print('main = {}'.format(main_symbol))
        first_modifier = first_modifier_map[first_modifier_positions]
        second_modifier = second_modifier_map[second_modifier_positions]
        combined = main_symbol + first_modifier + second_modifier
        if combined == '' :
            combined = '{#Tab}'
    else:
        combined = ''
    print('combined is {}'.format(combined))
    return combined

