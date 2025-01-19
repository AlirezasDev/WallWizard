import json

def load_accounts():  # loading json file content which has users data
    with open('account.json', 'r') as data:
        return json.load(data)

def save_accounts(accounts): #save the changes made to users data on the jason file
    with open('account.json', 'w') as data:
        json.dump(accounts, data, indent=4)

def assign_points(winner, loser, spent_time):
    users = load_accounts()
    for user in users:
        if user['username'] == winner:
            user['points'] += 5
            user['wins'] += 1
        elif user['username'] == loser:
            user['points'] -= 5
            user['losses'] += 1
    
    for user in users:
        if user['username'] == winner:
            time = int(spent_time)
            time += user['play_time'][0]*3600
            time += user['play_time'][1]*60
            time += user['play_time'][2]
            hours, remain = divmod(int(time), 3600)
            minutes, seconds = divmod(remain, 60)
            elapsed_time = [hours, minutes, seconds]
            new_playtime = [elapsed_time[i] for i in range(3)]
            user['play_time'] = new_playtime
        elif user['username'] == loser:
            time = int(spent_time)
            time += user['play_time'][0]*3600
            time += user['play_time'][1]*60
            time += user['play_time'][2]
            hours, remain = divmod(int(time), 3600)
            minutes, seconds = divmod(remain, 60)
            elapsed_time = [hours, minutes, seconds]
            new_playtime = [elapsed_time[i] for i in range(3)]
            user['play_time'] = new_playtime
            
    return save_accounts(users)

