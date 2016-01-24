import re

from stenoprog.ortho_keys import starts_list, vowels_list, ends_list

def make_patterns(starts_list,  vowels_list, ends_list, finals_list=[]):

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
    ends_list = list(set(ends_list))
    finals_list = list(set(finals_list))
    combined_vowels.sort(key=len, reverse=True)
    starts_list.sort(key=len, reverse=True)
    ends_list.sort(key=len, reverse=True)
    finals_list.sort(key=len, reverse=True)
    start_regex = '|'.join(starts_list)
    vowel_regex = '|'.join(combined_vowels)
    end_regex = '|'.join(ends_list)
    final_regex = '|'.join(finals_list)
    start_vowel_rem_regex = '^(?P<start>{})?(?P<vowel>{})?(?P<remainder>.*?)$'.format(
        start_regex, vowel_regex)
    start_vowel_rem_pattern = re.compile(start_vowel_rem_regex)
    end_rem_regex = '^(?P<end>{})?(?P<remainder>.*?)$'.format(end_regex)
    end_rem_pattern = re.compile(end_rem_regex)
    final_rem_regex = '^(?P<end>{})?(?P<remainder>.*?)$'.format(final_regex)
    final_rem_pattern = re.compile(final_rem_regex)
    return {
        'start_vowel': start_vowel_rem_pattern,
        'end': end_rem_pattern,
        'final': final_rem_pattern,
        'vowel_with_e': vowel_with_e,
    }

default_patterns = make_patterns(starts_list, vowels_list, ends_list)

def match_text(text, patterns=default_patterns):
    old_remainder = None
    remainder = text
    chords = []
    while (old_remainder != remainder) and remainder:
        old_remainder = remainder
        start, vowel, end, vowelend, final, remainder = match_chord(remainder, patterns)
        chords.append({'start': start, 'vowel': vowel, 'end': end, 'vowelend': vowelend, 'final': final})
    result = None
    if remainder == '':
        result = chords
    return result
        
def match_chord(text, patterns=default_patterns):
    start, vowel, remainder = match_start_and_vowel(text, patterns['start_vowel'])
    vowelend = None
    end = None
    final = None
    if remainder:
        end, remainder = match_end(remainder, patterns['end'])
        if remainder and remainder[0] == 'E':
            if vowel in patterns['vowel_with_e']:
                vowelend = 'E'
                remainder = remainder[1:]
            elif start and start[-1] in patterns['vowel_with_e']:
                vowelend = 'E'
                vowel = start[-1]
                start = start[:-1]
                remainder = remainder[1:]
        if remainder:
            final, remainder = match_end(remainder, patterns['final'])
        if vowel is None and vowelend == 'E':
            import pdb
            pdb.set_trace()
    return start, vowel, end, vowelend, final, remainder

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

def match_end(text, pattern=default_patterns['end']):
    match = pattern.match(text)
    end = None
    if match:
        gd = match.groupdict()
        end = gd['end']
        remainder = gd['remainder']
    else:
        remainder = text
    return end, remainder

