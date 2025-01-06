from functools import reduce
import random
import csv

teams = ["ARS","AVL","BHA","BOU","BRE","BUR","CHE","CRY","EVE","FUL","LIV","LUT","MCI","MUN","NEW","NFO","SHU","TOT","WHU","WOL"]

def make_players(teams):
    num_players_per_team = 30

    players = []
    num_gkp, num_def, num_mid, num_fwd = 3,10,10,7
    positions = ["GKP"] * num_gkp + ["DEF"] * num_def + ["MID"] * num_mid + ["FWD"] * num_fwd

    for team in teams:
        player_in_position = 0
        for i in range(num_players_per_team):
            players.append(team + positions[i] + str(player_in_position + 1))
            if player_in_position == num_gkp - 1 and positions[i] == "GKP":
                player_in_position = 0
            elif player_in_position == num_def - 1 and positions[i] == "DEF":
                player_in_position = 0
            elif player_in_position == num_mid - 1 and positions[i] == "MID":
                player_in_position = 0
            elif player_in_position == num_fwd - 1 and positions[i] == "FWD":
                player_in_position = 0
            else:
                player_in_position += 1
    return players

def fixtures(teams):

    rotation = teams.copy()

    fixture_list = []
    for i in range(0, len(teams)-1):
        fixture_list.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixture_list

def make_fixture_list(teams):
    matches = fixtures(teams)
    all_matches = []    
    for match in matches:
        n = len(match)
        all_matches.extend(list(zip(match[0:n//2], reversed(match[n//2:n]))))
    reversed_matches = [(y,x) for x,y in all_matches]
    return all_matches + reversed_matches

#PLAYER, TEAM, POSITION, POINTS, GOALS, ASSISTS, MINUTES, GOALS CONCEDED, BONUS, BPS, CLEAN SHEETS, YELLOW, RED

def get_teams_fixtures(team, fixture_list):
    matches = []
    for fixtures in fixture_list:
        #for match in fixtures:
        if team in fixtures:
                matches.append(fixtures)
    return matches

def make_player_goals(player):
    goals = []
    position = player[3:6]
    priority = player[6:]
    if position == "GKP":
        goals = [0] * 38
    elif position == "DEF":
        if priority <= "5":
            goals.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,2],k=38))
        else:
            goals.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,0,1,1,2],k=38))
    elif position == "MID":
        if priority <= "4":
            goals.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,3],k=38))
        else:
            goals.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,1,1,1,2,2],k=38))
    elif position == "FWD":
        if priority <= "3":
            goals.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,3,3],k=38))
        else:
            goals.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,1,1,1,2],k=38))
    return goals
                
def make_player_assists(player):
    assists = []
    position = player[3:6]
    priority = player[6:]
    if position == "GKP":
        assists = [0] * 38
    elif position == "DEF":
        if priority <= "5":
            assists.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,2],k=38))
        else:
            assists.extend(random.choices([0,0,0,0,0,0,0,0,0,0,0,0,1,1],k=38))
    elif position == "MID":
        if priority <= "4":
            assists.extend(random.choices([0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,3],k=38))             
        else:
            assists.extend(random.choices([0,0,0,0,0,0,0,0,0,1,1,1,1,1,2,2],k=38))
    elif position == "FWD":
        if priority <= "3":
            assists.extend(random.choices([0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,3],k=38))
        else:
            assists.extend(random.choices([0,0,0,0,0,0,0,0,0,1,1,1,1,1,2,2],k=38))
    return assists

def make_player_minutes(player):
    minutes = []
    position = player[3:6]
    priority = player[6:]
    if position == "GKP":
        if priority == "1":
            minutes.append(random.choices([90,0],[0.99,0.01],k=38))
        elif priority == "2":
            minutes.append(random.choices([90,0],[0.01,0.99],k=38))
        else:
            minutes.append([0.0]*38)
    elif position == "DEF":
        if priority <= "5":
            minutes.append(random.choices([90,80,60,45,0],[0.8,0.1,0.05,0.05,0.01], k=38))
        else:
            minutes.append(random.choices([90,80,60,45,0],[0.4,0.2,0.2,0.2,0.8], k=38))
    elif position == "MID":
        if priority <= "4":
            minutes.append(random.choices([90,80,60,45,0],[0.6,0.2,0.1,0.1,0.01], k=38))
        else:
            minutes.append(random.choices([90,80,60,45,0],[0.2,0.4,0.2,0.2,0.8], k=38))
    elif position == "FWD":
        if priority <= "3":
            minutes.append(random.choices([90,80,60,45,0],[0.75,0.3,0.2,0.1,0.01], k=38))
        else:
            minutes.append(random.choices([90,80,60,45,0],[0.1,0.3,0.3,0.3,0.8],k=38))
    return minutes[0]

def make_player_bonus(player):
    bonus = []
    position = player[3:6]
    priority = player[6:]
    if position == "GKP":
        bonus = [0] * 38
    elif position == "DEF":
        if priority <= "5":
            bonus.extend(random.choices([0,1,2,3],[0.8,0.1,0.05,0.025],k=38))
        else:
            bonus.extend(random.choices([0,1,2,3],[0.9,0.5,0.01,0.0025],k=38))
    elif position == "MID":
        if priority <= "4":
            bonus.extend(random.choices([0,1,2,3],[0.7,0.5,0.2,0.1],k=38))
        else:
            bonus.extend(random.choices([0,1,2,3],[0.8,0.2,0.1,0.01],k=38))
    elif position == "FWD":
        if priority <= "3":
            bonus.extend(random.choices([0,1,2,3],[0.5,0.4,0.2,0.1],k=38))
        else:
            bonus.extend(random.choices([0,1,2,3],[0.8,0.2,0.1,0.05],k=38))
    return bonus

def make_player_clean_sheet(player):
    clean_sheets = []
    position = player[3:6]
    priority = player[6:]
    if position == "GKP":
        if priority <= "1":
            clean_sheets.extend(random.choices([0,1],[0.4,0.6],k=38))
        elif priority <= "2":
            clean_sheets.extend(random.choices([0,1],[0.05,0.95],k=38))
        else:
            clean_sheets.extend(random.choices([0,1],[0.01,0.99],k=38))
    elif position == "DEF":
        if priority <= "5":
            clean_sheets.extend(random.choices([0,1],[0.4,0.6],k=38))
        else:
            clean_sheets.extend(random.choices([0,1],[0.2,0.8],k=38))
    elif position == "MID":
        if priority <= "4":
            clean_sheets.extend(random.choices([0,1],[0.4,0.6],k=38))
        else:
            clean_sheets.extend(random.choices([0,1],[0.2,0.8],k=38))
    elif position == "FWD":
        clean_sheets.extend([0]*38)
    return clean_sheets

def make_player_cards(player):
    yellow = []
    red = []
    position = player[3:6]
    priority = player[6:]
    if position == "GKP":
        yellow = [0] * 38
        red = [0] * 38
    elif position == "DEF":
        if priority <= "5":
            yellow.extend(random.choices([0,1],[0.6,0.4],k=38))
        else:
            yellow.extend(random.choices([0,1],[0.8,0.2],k=38))
    elif position == "MID":
        if priority <= "4":
            yellow.extend(random.choices([0,1],[0.7,0.3],k=38))
        else:
            yellow.extend(random.choices([0,1],[0.4,0.6],k=38))
    elif position == "FWD":
        if priority <= "3":
            yellow.extend(random.choices([0,1],[0.75,0.25],k=38))
        else:
            yellow.extend(random.choices([0,1],[0.9,0.1],k=38))
    for card in yellow:
        if card == 0:
            red.extend(random.choices([0,1],[0.98,0.02]))
        else:
            red.append(0)
    return yellow, red

def make_player_points(player, minutes, goals, assists, goals_conceded, bonus, clean_sheets, yellow_cards, red_cards):
    position = player[3:6]
    calc_points = 0
    if minutes >= 60:
        calc_points += 2
    elif minutes > 0:
        calc_points += 1
    calc_points += assists * 3
    calc_points += bonus
    calc_points -= yellow_cards
    calc_points -= red_cards * 3
    if position == "GKP":
        calc_points += clean_sheets * 4
        calc_points += goals * 6
        calc_points -= goals_conceded // 2
    elif position == "DEF":
        calc_points += clean_sheets * 4
        calc_points += goals * 6
        calc_points -= goals_conceded // 2
    elif position == "MID":
        calc_points += clean_sheets
        calc_points += goals * 5
    elif position == "FWD":
        calc_points += goals * 4    
    return calc_points

def generate_price(player):
    prices = []
    position = player[3:6]
    player_num = player[6:]
    if position == "GKP":
        if player_num == "1":
            prices.append(random.choice([4.5,5.0, 5.0, 5.0, 5.5]))
        elif player_num == "2":
            prices.append(random.choice([4.0,4.5,4.5,4.5,5.0]))
        elif player_num == "3":
            prices.append(random.choice([4.0,4.0,4.0,4.5,4.5]))
    elif position == "DEF":
        if player_num <= "5":
            prices.append(random.choice([4.5,5.0,5.0,5.5,6.0]))
        else:
            prices.append(random.choice([4.0,4.5,4.5,5.0,5.5]))
    elif position == "MID":
        if player_num <= "5":
            prices.append(random.choice([5.5,6.0,6.5,7.0,7.5,5.5,6.0,6.5,7.0,7.5,5.5,6.0,6.5,7.0,7.5,8.0,8.0,8.0,8.5,9.0,9.5,10.0, 12.5]))
        else:
            prices.append(random.choice([4.5,5.0,5.5,6.0,6.5]))
    elif position == "FWD":
        if player_num <= "3":
            prices.append(random.choice([6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,12.0]))
        else:
            prices.append(random.choice([5.0,5.5,6.0,6.5,7.0]))
    return prices[0]

#makes data for a single team
#PLAYER, TEAM, POSITION, PRICE, FIXTURE, GOALS, ASSISTS, MINUTES, GOALS CONCEDED, BONUS, BPS, CLEAN SHEETS, YELLOW, RED, POINTS
def make_player_data(players, team_fixture_list):
    team_data = []
    goals_conceded = random.choices([0,1,2,3,4,5],[0.6,0.3,0.2,0.05,0.03,0.02],k=38)[0]
    for player in players:
        position = player[3:6]
        price = generate_price(player)
        goals = make_player_goals(player)
        assists = make_player_assists(player)
        minutes = make_player_minutes(player)
        bonus = make_player_bonus(player)
        clean_sheet = make_player_clean_sheet(player)
        yellow, red = make_player_cards(player)
        for i in range(38):       
            if minutes[i] == 0:
                goals_conceded = 0
                goals[i] = 0
                assists[i] = 0
                bonus[i] = 0
                clean_sheet[i] = 0
                yellow[i] = 0
                red[i] = 0
        player_data = []
        player_data.extend([player, player[0:3], position, price])
        for i,fixture in enumerate(team_fixture_list):
            player_data.append(fixture)
            #generate random stats and calculate points
            player_data.extend([goals[i]] + [assists[i]] + [minutes[i]] + [goals_conceded] + [bonus[i]] + [clean_sheet[i]] + [yellow[i]] + [red[i]])
            points = make_player_points(player, minutes[i], goals[i], assists[i], goals_conceded, bonus[i], clean_sheet[i], yellow[i], red[i])
            player_data.append(points) 
        team_data.append(player_data)
    return team_data

players = make_players(teams)

all_fixture_list = make_fixture_list(teams)
team_fixture_list = get_teams_fixtures("ARS", all_fixture_list)

new_data = []
for i,team in enumerate(teams):
    team_fixture_list = get_teams_fixtures(team, all_fixture_list)
    new_data.append(make_player_data(players[i*30:i*30+30], team_fixture_list))

headers = ["PLAYER", "TEAM", "POSITION", "PRICE"] #"FIXTURE", "GOALS", "ASSISTS", "MINUTES", "GOALS CONCEDED", "BONUS", "BPS", "CLEAN SHEETS", "YELLOW", "RED", "POINTS"]
for i in range(1,39):
    headers.extend(["FIXTURE " + str(i), "GOALS " + str(i), "ASSISTS " + str(i), "MINUTES " + str(i), "GOALS CONCEDED " + str(i), "BONUS " + str(i), "CLEAN SHEETS " + str(i), "YELLOW " + str(i), "RED " + str(i), "POINTS " + str(i)])


csv_file = "fake_gameweek_data" + str(2) + ".csv"
with open(csv_file, 'w', newline='') as file:
    # Create a CSV writer object
    csv_writer = csv.writer(file)

    csv_writer.writerow(headers)

    for team in new_data:
        for row in team:
            csv_writer.writerow(row)
    print(f'Data has been added to {csv_file}.')