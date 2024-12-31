import keyboard
from printy import printy
import time

def menu(options: list):

    def fancy_menu(options, current_selection: int):
        print("-use the 'arrow keys' to navigate.",
              "-use the 'space bar' to confirm your selection.",
              "-use the 'q button' to quit the application.", sep="\n")
        for line in range(len(options)):
            if line == current_selection:
                printy("➡ "+options[line], "mBI")
            else:
                printy(options[line], "B")
        print("\n")

    j = 0
    fancy_menu(options, j)
    while True:
        if keyboard.is_pressed('up'):
            j -= 1
            fancy_menu(options, j % len(options))
            time.sleep(0.2)
        elif keyboard.is_pressed('down'):
            j += 1
            fancy_menu(options, j % len(options))
            time.sleep(0.2)
        elif keyboard.is_pressed('space'):
            print(f"Option selected: {options[j % len(options)]}")
            break


menu(["new-game", "continue", "login", "signup"])
