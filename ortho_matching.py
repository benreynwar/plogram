import re

from plogram import ortho_keys, visualize
from plogram.ortho_keys import starts_list, vowels_list, first_ends_list, second_ends_list

def make_patterns(starts_list=starts_list,
                  vowels_list=vowels_list,
                  first_ends_list=first_ends_list,
                  second_ends_list=second_ends_list):

    vowel_without_e = []
    vowel_with_e = []
    for v in vowels_list:
        if v.endswith('-E'):
            vowel_with_e.append(v[:-2])
        else:
            vowel_without_e.append(v)
    combined_vowels = vowel_with_e + vowel_without_e
    combined_vowels = list(set(combined_vowels))
    starts_list = list(set(starts_list))
    first_ends_list = list(set(first_ends_list))
    second_ends_list = list(set(second_ends_list))
    combined_vowels.sort(key=len, reverse=True)
    starts_list.sort(key=len, reverse=True)
    first_ends_list.sort(key=len, reverse=True)
    second_ends_list.sort(key=len, reverse=True)
    start_regex = '|'.join(starts_list)
    vowel_regex = '|'.join(combined_vowels)
    first_end_regex = '|'.join(first_ends_list)
    second_end_regex = '|'.join(second_ends_list)
    start_vowel_rem_regex = '^(?P<start>{})?(?P<vowel>{})?(?P<remainder>.*?)$'.format(
        start_regex, vowel_regex)
    start_vowel_rem_pattern = re.compile(start_vowel_rem_regex)
    first_end_rem_regex = '^(?P<end>{})?(?P<remainder>.*?)$'.format(first_end_regex)
    first_end_rem_pattern = re.compile(first_end_rem_regex)
    second_end_rem_regex = '^(?P<end>{})?(?P<remainder>.*?)$'.format(second_end_regex)
    second_end_rem_pattern = re.compile(second_end_rem_regex)
    return {
        'starts_list': starts_list,
        'vowels_list': vowels_list,
        'start_vowel': start_vowel_rem_pattern,
        'first_end': first_end_rem_pattern,
        'second_end': second_end_rem_pattern,
        'vowel_with_e': vowel_with_e,
    }

default_patterns = make_patterns(starts_list, vowels_list, first_ends_list, second_ends_list)

def match_text(text, patterns=default_patterns):
    old_remainder = None
    remainder = text
    chords = []
    while (old_remainder != remainder) and remainder:
        old_remainder = remainder
        start, vowel, end, remainder = match_chord(remainder, patterns)
        chords.append({'start': start, 'vowel': vowel, 'end': end, })
    result = None
    if remainder == '':
        result = chords
    return result
        
def match_chord(text, patterns=default_patterns):
    start, vowel, remainder = match_start_and_vowel(text, patterns['start_vowel'])
    if not vowel and start in vowels_list:
        vowel = start
        start = None
    end = None
    if remainder:
        can_vowel_with_e = False
        if (vowel is None) and start and (start[-1] in patterns['vowel_with_e']) and (
                (start[:-1] in patterns['starts_list']) or (start[:-1] == '')):
            can_vowel_with_e = True
        elif vowel in patterns['vowel_with_e']:
            can_vowel_with_e = True
        if can_vowel_with_e:
            second_end, second_remainder = match_end(remainder, patterns['second_end'])
            first_end, first_remainder = match_end(remainder, patterns['first_end'])
            if ((second_end is None) or (second_end is None and first_end is None) or
                (first_end is not None and (len(first_end) > len(second_end)))):
                end = first_end
                remainder = first_remainder
            else:
                end = second_end
                remainder = second_remainder
                if vowel is None:
                    vowel = start[-1]
                    start = start[:-1]
                else:
                    vowel = vowel + '-E'
        else:
            end, remainder = match_end(remainder, patterns['first_end'])            
    return start, vowel, end, remainder

def match_start_and_vowel(text, pattern=default_patterns['start_vowel']):
    match = pattern.match(text)
    start = None
    vowel = None
    if match:
        gd = match.groupdict()
        start = gd['start']
        vowel = gd['vowel']
        remainder = gd['remainder']
    else:
        remainder = text
    return start, vowel, remainder

def match_end(text, pattern):
    match = pattern.match(text)
    end = None
    if match:
        gd = match.groupdict()
        end = gd['end']
        remainder = gd['remainder']
    else:
        remainder = text
    return end, remainder


if __name__ == '__main__':
    while True:
        text = raw_input('Enter text:')
        chords = match_text(text)
        if chords is None:
            print('Cannot encode word')
        else:
            for chord in chords:
                keys = ortho_keys.chord_to_keys(chord['start'], chord['vowel'], chord['end'])
                vchord = visualize.visualize_keys(keys)
                print(vchord)

