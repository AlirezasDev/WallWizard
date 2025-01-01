import keyboard
import json
from printy import printy

def leaderboard():
    with open('account.json', 'r') as data:
        users = json.load(data)

    sorted_users = sorted(users, key=lambda x: x["points"], reverse=True)

    printy(" ====================TOP 3 PLAYERS======================== ", "BHw")
    printy("   {:<23}{:<20}{:<12} ".format("username", "points", "play time"), "BH")

    printy("    {:<24}{:<22}{:<8} ".format(sorted_users[0]['username'], sorted_users[0]['points'],
                                         sorted_users[0]['play_time']), "BHy")
    printy("    {:<24}{:<22}{:<8} ".format(sorted_users[1]['username'], sorted_users[1]['points'],
                                         sorted_users[1]['play_time']), "BHc")
    printy("    {:<24}{:<22}{:<8} ".format(sorted_users[2]['username'], sorted_users[2]['points'],
                                         sorted_users[2]['play_time']), "BHm")
    while True:
        if keyboard.is_pressed('q'):
            exit()

leaderboard()
