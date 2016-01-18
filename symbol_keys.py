from stenoprog import keys
from stenoprog.keys import UPP, MID, NON, LOW

symbol_map = {
    (LOW, NON, NON, NON): '{#Tab}',
    (UPP, NON, NON, NON): '{#Return}',
    (UPP, NON, UPP, NON): '{#period}',
    (UPP, NON, LOW, NON): '{#comma}',
    (LOW, NON, UPP, NON): '{:}',
    (LOW, NON, LOW, NON): '{;}',
    (MID, NON, NON, NON): '?{^}',
    (MID, NON, LOW, NON): '#{^}',
    (MID, NON, UPP, NON): '!{^}',
    (NON, UPP, NON, NON): '({^}',
    (NON, LOW, NON, NON): '){^}',
    (LOW, UPP, NON, NON): '[{^}',
    (LOW, LOW, NON, NON): ']{^}',
    (MID, UPP, NON, NON): '{{^}',
    (MID, LOW, NON, NON): '}{^}',
    (UPP, UPP, NON, NON): '<{^}',
    (UPP, LOW, NON, NON): '>{^}',
    (UPP, UPP, UPP, NON): "'",
    (LOW, UPP, UPP, NON): '"{^}',
    (LOW, LOW, LOW, NON): '_{^}',
    (MID, MID, NON, NON): '={^}',
    (MID, MID, MID, NON): '=={^}',
    (NON, UPP, UPP, NON): '+{^}',
    (NON, LOW, LOW, NON): '-{^}',
    (NON, MID, UPP, NON): '*{^}',
    
}

keys_to_symbol = dict([(keys.positions_to_keys(positions, reversed=True), symbol)
                       for positions, symbol in symbol_map.items()])

def translate_symbol_keys(ks):
    symbol = keys_to_symbol.get(ks[10:18], None)
    if symbol is not None:
        add_space = ks[19]
        if symbol[-3:] == '{^}' and add_space:
            symbol = symbol[:-3]
    return symbol

