'''
A tutorial to teach the system.
'''
import random
import os
import json

# Test 1) Test of the basic ?? letters on left.
# Test 2) Test of the basic ?? letters followed by enter/space/underscore
# Test 3) Test vowels
# Test 4) Test letters on right.

# Test 5) Test of common words that just use those basic letters.
# - get words that would be typed without blends.
# - mix most common with word that uses a random letter.

# Test 6) Test first group of blends.
# Test 7) Test words using them. 

from plogram import ortho_keys, visualize, tutorial_mining, ortho_matching

VOWELS = 'AEIOU'

def get_left_single_letter_questions(data):
    left_single_letter_keys = [k.lower() for k in ortho_keys.starts_list
                               if len(k) == 1 and k not in VOWELS]
    possible_questions = [(data.get_score(start + '-'), start + '-', start) for start in
                          left_single_letter_keys]
    possible_questions.sort()
    return possible_questions

def get_words(data, width=10000, start_level=2, end_level=2):
    simple_words = tutorial_mining.get_words(start=0, start_level=start_level, end_level=end_level, width=width,
                                             start_limited=False, end_limited=False)
    possible_questions = [(data.get_score(word), word, word) for word in simple_words]
    possible_questions.sort()
    return possible_questions

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


def main():
    data = DataStorage()
    while True:
        possible_questions = get_words(data)
        data.save()
        p_random = 0.5
        if random.random() < p_random:
            random_int = random.randint(0, len(possible_questions)-1)
        else:
            random_int = 0
        score, question, answer = possible_questions[random_int]
        clear()
        attempt = input('Type {}: '.format(question))
        data.answer(question, attempt == answer)
        if attempt == answer:
            print('Correct!')
        else:
            print('Incorrect!')
            chords = None
            if question[-1] == '-':
                raise Exception('Unimplemented')
                #keys = ortho_keys.chord_to_keys(answer.upper(), None, None)
            elif question[0] == '-':
                raise Exception('Unimplemented')
                #keys = ortho_keys.chord_to_keys(None, None, answer.upper())                
            else:
                chords = ortho_matching.match_text(answer.upper())
            if not chords:
                raise Exception('Could not match text {}'.format(answer.upper()))
            for chord in chords:
                keys = ortho_keys.chord_to_keys(chord['start'], chord['vowel'], chord['end'])                
                vchord = visualize.visualize_keys(keys)
                print(vchord)
            while attempt != answer:
                attempt = input('Type {}: '.format(question))
                if attempt == answer:
                    print('Correct!')
                else:
                    print('Incorrect!')
    

if __name__ == '__main__':
    main()
