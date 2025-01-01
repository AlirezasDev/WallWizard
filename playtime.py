import time
import json

def load_accounts():  # loading json file content which has users data
    with open('account.json', 'r') as data:
        return json.load(data)

def save_accounts(accounts): #save the changes made to users data on the jason file
    with open('account.json', 'w') as data:
        json.dump(accounts, data, indent=4)

def playtime(spent_time, player1, player2):
    users = load_accounts()
    hours, remain = divmod(int(spent_time), 3600)
    minutes, seconds = divmod(remain, 60)
    elapsed_time = [hours,minutes,seconds]
    for user in users:
        if user['username'] == player1:
            new_playtime = [user['play_time'][i]+elapsed_time[i] for i in range(3)]
            user['play_time'] = new_playtime
        elif user['username'] == player2:
            new_playtime = [user['play_time'][i]+elapsed_time[i] for i in range(3)]
            user['play_time'] = new_playtime
    return save_accounts(users)

playtime(1000, 'Ehsan', 'Ehsan2')