import time
import FullMenu
import game
from assign_points import assign_points

player1 = FullMenu.player1_username
player2 = FullMenu.player2_username

def start_game():
    global player1, player2
    import game

    game = game.Game(1, player1, player2)

    exit_code = ""
    while True:
        if exit_code in ["T", "Q"]:
            break
        exit_code = game.play()
    # while exit_code not in ["T", "Q"]:
    #     exit_code = game.play()
    return

start_time = time.time()

start_game()

end_time = time.time()
elapsed_time = end_time - start_time

if game.winner == player1:
    assign_points(player1, player2, elapsed_time)
else:
    assign_points(player2, player1, elapsed_time)
exit()