'''
A tutorial to teach the system.
'''
import random
import os
import json

from stenoprog import ortho_theory, visualize

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class DataStorage:

    fn = 'tutorial.json'

    def __init__(self):
        if os.path.exists(self.fn):
            with open(self.fn, 'r') as f:
                string_data = f.read()
            self.data = json.loads(string_data)
        else:
            self.data = {}
    
    def answer(self, question, correct):
        if question not in self.data:
            self.data[question] = []
        self.data[question].append(correct)

    def get_score(self, question):
        if question not in self.data:
            score = 2
        else:
            recents = self.data[question][-10:]
            corrects = sum([1 if c else 0 for c in recents])
            total = len(recents)
            if total < 3:
                total = total + 1
            score = float(corrects)/total
        return score
        
    def save(self):
        with open(self.fn, 'w') as f:
            f.write(json.dumps(self.data))

def get_questions(data):
    starts = []
    for base in ortho_theory.ortho_starts:
        starts += [s.lower() for s in ortho_theory.ortho_starts[base] if s is not None]
    ends = []
    for base in ortho_theory.ortho_ends:
        ends += [s.lower() for s in ortho_theory.ortho_ends[base] if s is not None]
    vowels = [s[0].lower() for s in ortho_theory.vowels if s[0]]
    possible_questions = []
    #possible_questions += [(data.get_score(start + '-'), start + '-', start) for start in starts]
    #possible_questions += [(data.get_score('-' + end), '-' + end, end) for end in ends]    
    possible_questions += [(data.get_score(vowel), vowel, vowel) for vowel in vowels]    
    possible_questions.sort()
    return possible_questions

def main():
    data = DataStorage()
    possible_questions = get_questions(data)
    print(possible_questions)
    import pdb
    pdb.set_trace()
    while True:
        possible_questions = get_questions(data)
        data.save()
        p_random = 0.5
        if random.random() < p_random:
            random_int = random.randint(0, len(possible_questions)-1)
        else:
            random_int = 0
        score, question, answer = possible_questions[random_int]
        clear()
        attempt = raw_input('Type {}: '.format(question))
        data.answer(question, attempt == answer)
        if attempt == answer:
            print('Correct!')
        else:
            print('Incorrect!')
            if question[-1] == '-':
                keys = ortho_theory.chord_to_keys(answer.upper(), None, None, None)
            elif question[0] == '-':
                keys = ortho_theory.chord_to_keys(None, None, answer.upper(), None)                
            else:
                keys = ortho_theory.chord_to_keys(None, answer.upper(), None, None)                
            vchord = visualize.visualize_keys(keys)
            print(vchord)
            while attempt != answer:
                attempt = raw_input('Type {}: '.format(question))
                if attempt == answer:
                    print('Correct!')
                else:
                    print('Incorrect!')
    

if __name__ == '__main__':
    main()
