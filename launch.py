# Copyright (c) 2013 Hesky Fisher, 2015 Ben Reynwar
# See LICENSE.txt for details.

import os
import traceback

from plover import main, app
import plover.gui.main
import plover.oslayer.processlock
from plover import translation
from plover.machine import keymap
from plover.oslayer.config import CONFIG_DIR, ASSETS_DIR
from plover.config import CONFIG_FILE, DEFAULT_DICTIONARIES, Config

from stenoprog import ortho_keys, symbol_keys, edit_keys, emacs_keys, state

keymap.Keymap.DEFAULT = [
    ["0A", ["a"]],
    ["0B", ["q"]],
    ["1A", ["s"]],
    ["1B", ["w"]],
    ["2A", ["d"]],
    ["2B", ["e"]],
    ["3A", ["f"]],
    ["3B", ["r"]],
    ["4A", ["c"]],
    ["4B", ["v"]],
    ["5A", [";"]],
    ["5B", ["p"]],
    ["6A", ["l"]],
    ["6B", ["o"]],
    ["7A", ["k"]],
    ["7B", ["i"]],
    ["8A", ["j"]],
    ["8B", ["u"]],
    ["9A", ["m"]],
    ["9B", ["n"]],
]

def steno_keys_to_key_list(steno_keys):
    keys = []
    for i in range(10):
        for j in ('A', 'B'):
            name = str(i) + j
            keys.append(name in steno_keys)
    return tuple(keys)

def translate_keys(keys):
    trans = None
    if (not keys[7]) or (keys[7] and keys[6]):
        trans = ortho_keys.translate_ortho_keys(keys)
    elif keys[0:7] == (False, False, False, False, False, False, False):
        trans = symbol_keys.translate_symbol_keys(keys)
    elif keys[4:7] == (False, True, False):
        trans = edit_keys.translate_edit_keys(keys)
    elif keys[4: 7] == (True, True, False):
        trans = emacs_keys.translate_emacs_keys(keys)
    elif keys[0: 7] == (False, True, False, False, False, False, False):
        trans = state.translate_state_keys(keys)
    else:
        print('not translation')
    return trans

def _lookup (strokes, dictionary, suffixes):
    if len(strokes) == 1:
        dict_key = steno_keys_to_key_list(strokes[0].steno_keys)
        trans = translate_keys(dict_key)
        if trans is None:
            result = None
        else:
            result = trans
    else:
        result = None
    return result

#Override the method from plover so we can handle undo
def _translate_stroke(stroke, state, dictionary, callback):
    """
    Process a stroke.

    See the class documentation for details of how Stroke objects
    are converted to Translation objects.

    Arguments:

    stroke -- The Stroke object to process.

    state -- The state object hold stroke and translation history.

    dictionary -- The steno dictionary.

    callback -- A function that takes the following arguments: A list of
    translations to undo, a list of new translations, and the translation that
    is the context for the new translations.

    """
    
    undo = []
    do = []
    if stroke.steno_keys == ['3B', '2B']:
        stroke.is_correction = True
    # TODO: Test the behavior of undoing until a translation is undoable.
    if stroke.is_correction:
        empty = True
        for t in reversed(state.translations):
            undo.append(t)
            if translation.has_undo(t):
                empty = False
                break
        undo.reverse()
        for t in undo:
            do.extend(t.replaced)
        if empty:
            # There is no more buffer to delete from -- remove undo and add a
            # stroke that removes last word on the user's OS
            undo = []
            do = [translation.Translation([stroke], translation._back_string())]
    else:
        # Figure out how much of the translation buffer can be involved in this
        # stroke and build the stroke list for translation.
        num_strokes = 1
        translation_count = 0
        for t in reversed(state.translations):
            num_strokes += len(t)
            if num_strokes > dictionary.longest_key:
                break
            translation_count += 1
        translation_index = len(state.translations) - translation_count
        translations = state.translations[translation_index:]

        mapping = _lookup([stroke], dictionary, [])

        t = translation._find_translation(translations, dictionary, stroke, mapping)
        if t is not None:
            do.append(t)
            undo.extend(t.replaced)
    del state.translations[len(state.translations) - len(undo):]
    callback(undo, do, state.last())
    state.translations.extend(do)


translation._lookup = _lookup
translation._translate_stroke = _translate_stroke

def new_main():
    """Launch plover."""
    try:
        # Ensure only one instance of Plover is running at a time.
        with plover.oslayer.processlock.PloverLock():
            main.init_config_dir()
            config = Config()
            config.target_file = CONFIG_FILE
            engine = app.StenoEngine()
            gui = plover.gui.main.PloverGUI(config, engine=engine)
            engine.formatter.set_space_placement('After Output')
            gui.MainLoop()
            with open(config.target_file, 'wb') as f:
                config.save(f)
    except plover.oslayer.processlock.LockNotAcquiredException:
        main.show_error('Error', 'Another instance of Plover is already running.')
    except:
        main.show_error('Unexpected error', traceback.format_exc())
    os._exit(1)

if __name__ == '__main__':
    new_main()
