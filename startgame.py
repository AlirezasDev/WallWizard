import FullMenu
from game import Game

player1_username = ""
player2_username = ""

def start_game():
    global player1_username, player2_username

    if not player1_username or not player2_username:
        print("Both players must be logged in before starting the game.")
        return

    game = Game(1, player1_username, player2_username)

    exit_code = ""
    while exit_code not in ["T", "Q"]:
        exit_code = game.play()

# Example Usage
if __name__ == "__main__":
    player1_username = "player1"
    player2_username = "player2"

    start_game()