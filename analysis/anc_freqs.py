'''
Get the word frequencies from the ANC file.
'''

def get_anc_freqs():
    freqs = {}
    with open('ANC-written-count.txt', 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        if 'Total' in line:
            continue
        bits = line.split()
        word =  bits[0]
        counts = int(bits[3])
        if word not in freqs:
            freqs[word] = counts
    return freqs

