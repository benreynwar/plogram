from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

edit_map = {
    # Deletes
    ((NON, NON, NON), (NON, UPP, NON, UPP, NON)): '{#BackSpace}',
    # Moves
    ((NON, NON, NON), (NON, UPP, NON, NON, NON)): '{#Left}',
    ((NON, NON, NON), (NON, LOW, NON, NON, NON)): '{#Right}',
    ((NON, NON, NON), (NON, NON, UPP, NON, NON)): '{#Up}',
    ((NON, NON, NON), (NON, NON, LOW, NON, NON)): '{#Down}',
    # All Way Moves
    ((NON, LOW, NON), (NON, UPP, NON, NON, NON)): '{#Control_L(a)}',
    ((NON, LOW, NON), (NON, LOW, NON, NON, NON)): '{#Control_L(e)}',
    ((NON, LOW, NON), (NON, NON, UPP, NON, NON)): '{#Alt_L(Shift_L(comma))}',
    ((NON, LOW, NON), (NON, NON, LOW, NON, NON)): '{#Alt_L(Shift_L(period))}',
    # Find Forward
    ((NON, NON, NON), (NON, UPP, NON, LOW, NON)): '{#Control_L(s)}',
    # Find Backwards
    ((NON, NON, NON), (NON, LOW, NON, LOW, NON)): '{#Control_L(r)}',
 }

keys_to_edit = dict([(keys.positions_to_keys(positions[0]) + 
                      keys.positions_to_keys(positions[1], reversed=True) , edit)
                     for positions, edit in edit_map.items()])


def translate_edit_keys(ks):
    edit = keys_to_edit.get(ks[0: 4] + ks[8: 20], None)
    print(edit)
    return edit

