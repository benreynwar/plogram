from plogram import keys
from plogram.keys import NON, UPP, LOW

TEXT_ENDINGS = 'TEXT_ENDINGS'
CODE_ENDINGS = 'CODE_ENDINGS'

state = {
    'ending': TEXT_ENDINGS,
    }

def set_ending_to_text():
    state['ending'] = TEXT_ENDINGS

def set_ending_to_code():
    state['ending'] = CODE_ENDINGS

state_pos_map = {
    (NON, NON, NON, NON, UPP, NON): set_ending_to_text,
    (NON, NON, NON, NON, LOW, NON): set_ending_to_code,
}
    
def translate_state_keys(ks):
    assert(ks[0: 8] == (False, True, False, False, False, False, False, True))
    ps = keys.keys_to_positions(ks[8: 20])
    state_func = state_pos_map.get(tuple(ps), None)
    if state_func is not None:
        state_func()
