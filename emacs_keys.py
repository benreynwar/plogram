from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

def from_emacs_command(command):
    return keys.M('x') + ' {PLOVER:PAUSE} ' + command + ' {#Return}'

emacs_map = {
    # Save buffer
    ((NON, NON, NON), (NON, NON, NON, NON, NON)): '{#Control_L(x) Control_L(s)}',
    # Close buffer
    # For some reason we can't pass 'k' as a control key.  Weird.
    ((NON, NON, NON), (NON, LOW, NON, NON, NON)): '{#Control_L(x)}k{^}{#Return}', 
    # Find file
    ((NON, NON, NON), (NON, UPP, NON, NON, NON)): '{#Control_L(x) Control_L(f)}',
    # Escape out of input
    ((NON, NON, NON), (NON, MID, NON, NON, NON)): '{#Control_L(g)}',
    # Switch to buffer
    ((NON, NON, NON), (NON, NON, LOW, NON, NON)): '{#Control_L(x) b Return}',
    # Save with a new name.
    ((NON, NON, NON), (NON, NON, UPP, NON, NON)): '{#Control_L(x) Control_L(w)}',
    # Previous word to upper case
    # NOT IMPLEMENTED
 }

keys_to_emacs = dict([(keys.positions_to_keys(positions[0]) + 
                       keys.positions_to_keys(positions[1], reversed=True) , emacs)
                     for positions, emacs in emacs_map.items()])

def translate_emacs_keys(ks):
    emacs = keys_to_emacs.get(ks[0: 4] + ks[8: 20], None)
    return emacs

