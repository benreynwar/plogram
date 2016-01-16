from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

edit_map = {
    ((NON, NON, NON), (NON, UPP, NON, NON, NON)): '{#BackSpace}',
 }

keys_to_edit = dict([(keys.positions_to_keys(positions[0]) + 
                      keys.positions_to_keys(positions[1], reversed=True) , edit)
                     for positions, edit in edit_map.items()])

def translate_edit_key(ks):
    print('translate_edit_key')
    edit = keys_to_edit.get(ks[0: 4] + ks[8: 20], None)
    print(edit)
    return edit

