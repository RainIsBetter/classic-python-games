import random
word=random.choice(["pickle", "waffle", "goblin", "banana", "penguin",
    "noodle", "quicksand", "flabbergasted", "platypus",
    "shenanigans", "bumblebee", "kaleidoscope",
    "hippopotamus", "zucchini", "discombobulated"])
used=set(); lives=6
while lives and not set(word)<=used:
    print(' '.join(c if c in used else '_' for c in word),f' | Lives: {lives}')
    guess=input('Guess a letter: ').strip().lower()
    if len(guess)!=1 or not guess.isalpha() or guess in used: print('Choose a new letter.'); continue
    used.add(guess)
    if guess not in word: lives-=1
print('You win!' if set(word)<=used else 'You lose!','Word:',word)
