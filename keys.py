UPP = 'UPPER'
LOW = 'LOWER'
MID = 'MIDDLE'
NON = 'NEITHER'

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

