'''
Get the word frequencies from the ANC file.
'''
import os


_stored_anc_freqs = None

def retrieve_anc_freqs():
    freqs = {}
    fn = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ANC-written-count.txt')
    with open(fn, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        if 'Total' in line:
            continue
        bits = line.split()
        word =  bits[0]
        counts = int(bits[3])
        if word not in freqs:
            freqs[word] = counts
    freq_first = [(f, w) for w, f in freqs.items()]
    freq_first.sort(reverse=True)
    return freq_first
    
def get_anc_freqs():
    global _stored_anc_freqs
    if _stored_anc_freqs is None:
        _stored_anc_freqs = retrieve_anc_freqs()
    return _stored_anc_freqs
