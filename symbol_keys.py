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

number_map = {
    (NON, NON): '',
    (LOW, NON): '1',
    (UPP, NON): '2',
    (MID, NON): '3',
    (NON, LOW): '4',
    (LOW, LOW): '5',
    (UPP, LOW): '6',
    (MID, LOW): '7',
    (NON, UPP): '8',
    (LOW, UPP): '9',
    (UPP, UPP): '0',
    (MID, UPP): '',
    (NON, MID): '.',
    (LOW, MID): ',',
    (UPP, MID): '$',
    (MID, MID): '-',
}

def translate_symbol_keys(ks):
    ps = keys.keys_to_positions(ks)
    null_position = ps[0]
    number_position = ps[1]
    necessary_positions = tuple(ps[2: 4])
    choice_positions = ps[4]
    pinky_position = ps[5]
    main_positions = tuple(ps[6: 8])
    second_modifier_positions = ps[8]
    first_modifier_positions = ps[9]

    assert(necessary_positions == (NON, UPP))
    if (null_position == NON) and (number_position == NON) and (pinky_position == NON):
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
    elif (null_position == NON) and (number_position == UPP) and (pinky_position == NON):
        first_positions = (ps[4], ps[9])
        second_positions = (ps[8], ps[7])
        third_positions = (ps[6], ps[5])
        combined = number_map[first_positions] + number_map[second_positions] + number_map[third_positions] + '{^}'
    else:
        combined = ''
    print('combined is {}'.format(combined))
    return combined

