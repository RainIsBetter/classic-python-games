import random

board = [' '] * 9

wins = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

print("Welcome to Tic-Tac-Toe!")
print("1. Single player (against the computer)")
print("2. Two players")

while True:
    mode = input("Choose 1 or 2: ")
    if mode in ('1', '2'):
        break
    print("Invalid choice.")


def show_board():
    for i in range(0, 9, 3):
        print(' | '.join(
            board[j] if board[j] != ' ' else str(j + 1)
            for j in range(i, i + 3)
        ))
        if i < 6:
            print('--+---+--')


def has_won(player):
    return any(
        all(board[i] == player for i in line)
        for line in wins
    )


def computer_move():
    available = [i for i in range(9) if board[i] == ' ']

    # Try to win or block the player from winning
    for symbol in ('O', 'X'):
        for i in available:
            board[i] = symbol
            winning = has_won(symbol)
            board[i] = ' '

            if winning:
                return i

    # Otherwise, choose a random available space
    return random.choice(available)


player = 'X'

for turn in range(9):
    show_board()

    if mode == '1' and player == 'O':
        move = computer_move()
        print(f"Computer chooses {move + 1}.")

    else:
        while True:
            try:
                move = int(input(f"{player}, choose 1-9: ")) - 1

                if 0 <= move < 9 and board[move] == ' ':
                    break

            except ValueError:
                pass

            print("Invalid move.")

    board[move] = player

    # Check if someone won
    if has_won(player):
        if mode == '1':
            if player == 'X':
                print("You win!")
            else:
                print("Computer wins!")
        else:
            print(f"{player} wins!")

        break

    # Switch players
    player = 'O' if player == 'X' else 'X'

else:
    print("Draw!")

show_board()