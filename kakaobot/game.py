from random import randint

def rcpgame(player_choice):
    if player_choice == '가위':
        numbering = 0
    elif player_choice == '바위':
        numbering = 1
    elif player_choice == '보':
        numbering = 2
    computer_numbering = randint(0, 2)

    if numbering == computer_numbering:
        return 'draw'
    elif (numbering + 1) % 3 == computer_numbering:
        return 'lose'
    elif (computer_numbering + 1) % 3 == numbering:
        return 'win'