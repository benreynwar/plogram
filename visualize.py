

def visualize_keys(keys):
    template = '''
|B|D|F|H|:|R|P|N|L|
|A|C|E|G|:|Q|O|M|K|
         :
     |IJ|:|TS|
'''
    ordA = 65
    ss = template
    assert(len(keys) == 20)
    for index, key in enumerate(keys):
        v = 'X' if key else ' '
        ss = ss.replace(chr(ordA + index), v)
    return ss

if __name__ == '__main__':
    print(visualize_keys([True, True, True] + [False] * 16 + [True]))
