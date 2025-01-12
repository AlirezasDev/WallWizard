import os
import keyboard

def create_corridor_board():
    size = 9
    board = [[' ' for _ in range(size * 2 - 1)] for _ in range(size * 2 - 1)]

    for i in range(size * 2 - 1):
        for j in range(size * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                board[i][j] = '■'
            elif i % 2 == 1 and j % 2 == 0:
                board[i][j] = '─'
            elif i % 2 == 0 and j % 2 == 1:
                board[i][j] = '|'
            else:
                board[i][j] = ' '
    return board

def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        print(' '.join(row))
    print("\nPress 'esc' to exit.")

board = create_corridor_board()
i1, j1 = 0, 8
i2, j2 = 16, 8
turn = 1

while True:
    board[i1][j1] = '●'
    board[i2][j2] = '○'

    print_board(board)

    event = keyboard.read_event()
    if event.event_type == "down":
        if turn == 1:

            turn_not_chaing_eror=0
            board[i1][j1] = '■'
            if event.name == 'w' and i1 - 2 >= 0:
                i1 -= 2
                if i1==i2 and j1==j2:
                    if i1 - 2 >= 0:
                        i1-=2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 2
                


            elif event.name == 's' and i1 + 2 < len(board):
                i1 += 2
                if i1==i2 and j1==j2:
                    if i1 + 2 < len(board):
                        i1 += 2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 2


            elif event.name == 'a' and j1 - 2 >= 0:
                j1 -= 2
                if i1==i2 and j1==j2:
                    if j1 - 2 >= 0:
                        j1 -= 2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 2



            elif event.name == 'd' and j1 + 2 < len(board[0]):
                j1 += 2

                if i1==i2 and j1==j2:
                    if j1 + 2 < len(board[0]):
                        j1 +=2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 2
            else:
                print("Error: Invalid move! Try again.")



        elif turn == 2:

            board[i2][j2] = '■'

            if event.name == 'w' and i2 - 2 >= 0:
                i2 -= 2
                if i1==i2 and j1==j2:
                    if i2 - 2 >= 0:
                        i2 -=2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 1


            elif event.name == 's' and i2 + 2 < len(board):
                i2 += 2
                if i1==i2 and j1==j2:
                    if i2 + 2 < len(board):
                        i2 += 2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 1


            elif event.name == 'a' and j2 - 2 >= 0:
                j2 -= 2
                if i1==i2 and j1==j2:
                    if j2 - 2 >= 0:
                        j2 -=2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 1


            elif event.name == 'd' and j2 + 2 < len(board[0]):
                j2 += 2
                if i1==i2 and j1==j2:
                    if j2 + 2 < len(board[0]):
                        j2 += 2
                    else:
                        turn_not_chaing_eror=1
                        print("Error: Invalid move! Try again.")
                if turn_not_chaing_eror==0:
                    turn = 1
            
            else:
                print("Error: Invalid move! Try again.")

    if event.name == 'esc':
        break