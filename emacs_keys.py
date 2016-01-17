from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

emacs_map = {
    # Save buffer
    ((NON, NON, NON), (NON, NON, NON, NON, NON)): '{#Alt_L(x)} s a v e - b u f f e r',
    ((NON, NON, NON), (NON, LOW, NON, NON, NON)): '{#Alt_L(x)} close-buffer',
    ((NON, NON, NON), (NON, UPP, NON, NON, NON)): '{#Alt_L(x)} find-file',
    ((NON, NON, NON), (NON, NON, LOW, NON, NON)): '{#Alt_L(x)} switch-to-buffer',
 }

keys_to_emacs = dict([(keys.positions_to_keys(positions[0]) + 
                       keys.positions_to_keys(positions[1], reversed=True) , emacs)
                     for positions, emacs in emacs_map.items()])

def translate_emacs_keys(ks):
    emacs = keys_to_emacs.get(ks[0: 4] + ks[8: 20], None)
    print(emacs)
    return emacs

