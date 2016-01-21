from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW, M, C 
from stenoprog.emacs_keys import from_emacs_command

edit_map = {
    # Deletes
    ((NON, NON), (UPP, NON, UPP, NON)): (True, '{#BackSpace}'),
    # Delete from this point to end of line (to kill-ring)
    ((NON, LOW), (LOW, NON, UPP, NON)): (False, C('k')),
    # Delete this line
    ((NON, NON), (MID, NON, UPP, NON)): (True, from_emacs_command('kill-whole-line')),
    # Paste from kill-ring
    ((NON, NON), (NON, NON, UPP, NON)): (False, C('y')),
    # Delete previous word
    ((NON, UPP), (UPP, NON, UPP, NON)): (True, M('Backspace')),
    # Moves
    ((NON, NON), (UPP, NON, NON, NON)): (True, '{#Left}'),
    ((NON, NON), (LOW, NON, NON, NON)): (True, '{#Right}'),
    ((NON, NON), (NON, UPP, NON, NON)): (True, '{#Up}'),
    ((NON, NON), (NON, LOW, NON, NON)): (True, '{#Down}'),
    # Move word 
    ((NON, UPP), (UPP, NON, NON, NON)): (True, M('b')),
    ((NON, UPP), (LOW, NON, NON, NON)): (True, M('f')),
    # Move page
    ((NON, UPP), (NON, UPP, NON, NON)): (True, from_emacs_command('scroll-down-command')),
    ((NON, UPP), (NON, LOW, NON, NON)): (True, from_emacs_command('scroll-up-command')),
    # All Way Moves
    ((NON, LOW), (UPP, NON, NON, NON)): (False, C('a')),
    ((NON, LOW), (LOW, NON, NON, NON)): (False, C('e')),
    ((NON, LOW), (NON, UPP, NON, NON)): (False, M('Shift_L(comma)')),
    ((NON, LOW), (NON, LOW, NON, NON)): (False, M('Shift_L(period)')),
    # Find Forward
    ((NON, NON), (UPP, NON, LOW, NON)): (False, C('s')),
    # Find Backwards
    ((NON, NON), (LOW, NON, LOW, NON)): (False, C('r')),
    # Alt-tab
    ((NON, UPP), (NON, NON, NON, NON)): (False, '{#Alt_L(Tab)}'),
    # Search and replace
    ((NON, NON), (UPP, NON, LOW, LOW)): (False, M('Shift_L(percent)')),
    
 }

def translate_edit_keys(ks):
    ps = keys.keys_to_positions(ks)
    k = (tuple(ps[0:2]), tuple(reversed(ps[5: 9])))
    can_repeat_and_edit = edit_map.get(k)
    if can_repeat_and_edit is not None:
        can_repeat, edit = can_repeat_and_edit
    else:
        can_repeat = None
        edit = None
    repeat = keys.keys_to_number(ks[8: 10] + ks[18: 20])
    if repeat == 1:
        repeat = 16 
    if edit and (repeat > 1) and can_repeat:
        edit = '{#Control_L(u)' + str(repeat) + '}' + edit 
    return edit

