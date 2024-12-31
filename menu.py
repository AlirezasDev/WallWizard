import keyboard
from printy import printy
import time
import os

def menu(options: list):

    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def fancy_menu(options, current_selection: int):
        clear_terminal()
        printy("-use the 'arrow keys' to navigate.", "g")
        printy("-use the 'space bar' to confirm your selection.", "g")
        printy("-use the 'q button' to quit the application.", "g")
        print("\n")

        for line in range(len(options)):
            if line == current_selection:
                printy("🔴   "+f"[mBI]{options[line]}@")
                print("\n")
            else:
                printy("    "+options[line], "B")
                print("\n")
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
