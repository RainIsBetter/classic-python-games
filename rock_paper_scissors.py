import random
choices=('rock','paper','scissors'); beats={'rock':'scissors','paper':'rock','scissors':'paper'}
while True:
    user=input('Rock, paper, scissors, or quit: ').strip().lower()
    if user=='quit': break
    if user not in choices: print('Invalid choice.'); continue
    cpu=random.choice(choices); print('Computer:',cpu)
    print('Tie!' if user==cpu else 'You win!' if beats[user]==cpu else 'Computer wins!')
