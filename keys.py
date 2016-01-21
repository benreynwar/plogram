UPP = 'UPPER'
LOW = 'LOWER'
MID = 'MIDDLE'
NON = 'NEITHER'

def M(c):
    return '{#Alt_L(' + c + ')}'

def C(c):
    return '{#Control_L(' + c + ')}'

def keys_to_number(keys):
    assert(len(keys) == 4)
    m = 1
    t = 0
    for key in keys:
        if key:
            t += m
        m *= 2
    return t

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

def keys_to_positions(keys):
    assert(len(keys) % 2 == 0)
    positions = []
    for index in range(0, len(keys), 2):
        keyA = keys[index]
        keyB = keys[index+1]
        positions.append({
            (True, True): MID,
            (True, False): LOW,
            (False, True): UPP,
            (False, False): NON,
        }[(keyA, keyB)])
    return positions
