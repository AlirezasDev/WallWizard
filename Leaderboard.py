import keyboard
import json
from printy import printy

def load_accounts():  # loading json file content which has users data
    with open('account.json', 'r') as data:
        return json.load(data)

def leaderboard():
    users = load_accounts()
    sorted_users = sorted(users, key=lambda x: x["points"], reverse=True)

    printy("="*44+"TOP 3 PLAYERS"+"="*44, "BHw")
    printy(" {:30}{:<20}{:<15}{:<20}{:<15}".format("Username", "Points", "Wins", "Losses", "Play Time"), "BH")

    try:
        printy("  {:30}{:<+20}{:<15}{:<20}{:<14}".format(sorted_users[0]['username'], sorted_users[0]['points'],
                                             sorted_users[0]['wins'], sorted_users[0]['losses'],
                                                         f"{sorted_users[0]['play_time'][0]}h"
                                                         f"{sorted_users[0]['play_time'][1]}m"
                                                         f"{sorted_users[0]['play_time'][2]}s"), "BHy")
    except:
        pass
    try:
        printy("  {:30}{:<+20}{:<15}{:<20}{:<14}".format(sorted_users[1]['username'], sorted_users[1]['points'],
                                             sorted_users[1]['wins'], sorted_users[1]['losses'],
                                                         f"{sorted_users[1]['play_time'][0]}h"
                                                         f"{sorted_users[1]['play_time'][1]}m"
                                                         f"{sorted_users[1]['play_time'][2]}s"), "BHc")
    except:
        pass
    try:
        printy("  {:30}{:<+20}{:<15}{:<20}{:<14}".format(sorted_users[2]['username'], sorted_users[2]['points'],
                                             sorted_users[2]['wins'], sorted_users[2]['losses'],
                                                         f"{sorted_users[2]['play_time'][0]}h"
                                                         f"{sorted_users[2]['play_time'][1]}m"
                                                         f"{sorted_users[2]['play_time'][2]}s"), "BHm")
    except:
        pass

    while True:
        if keyboard.is_pressed('q'):
            exit()

leaderboard()
