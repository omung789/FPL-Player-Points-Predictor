import os
from datetime import date

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

year = f"{current_year}-{str(current_year + 1)[2:]}"

gameweek = 29

cur_dir = os.getcwd()
file_location = cur_dir + '/website/webpages/transfer_recommendations/index.html'
best_players_location = cur_dir + '/data/' + year + f'/machine learning/predicted_best_teams/predicted_best_players_{year}_gw{gameweek}.txt'
html_strings_dir = cur_dir + '/data/' + year + '/machine learning/gameweek_' + str(gameweek) + '_html_strings.txt'

def get_num_spaces(line):
    num_spaces = 0
    for i in range(len(line)):
        if line[i] == ' ':
            num_spaces += 1
        else:
            break
    return num_spaces

with open(file_location, 'r') as f:
    text = f.readlines()
    #print(text)

    with open(html_strings_dir, 'r') as f:
        html_strings = f.readlines()

    with open(best_players_location, 'r') as f:
        best_players = f.readlines()

    for i,line in enumerate(text):
        print(i)
        if i == 38:
            print("here",line)
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line, (num_spaces) * ' ' + f'<h1>Gameweek {gameweek}</h1>\n')
            text[i] = line
        elif 'Total xP' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line,(num_spaces) * ' ' + html_strings[-2])
            text[i] = line
        elif 'Total Cost' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line,(num_spaces) * ' ' + html_strings[-1])
            text[i] = line
        elif 'player goalkeeper' in line:
            num_spaces = get_num_spaces(text[i])
            line = line.replace(line,(num_spaces) * ' ' + html_strings[0])
            text[i] = line
            start_of_outfield = i + 1
        elif '<div class="bench">' in line:
            num_spaces = get_num_spaces(text[i])
            for j in range(4):
                text[i + j + 1] = (num_spaces + 2) * ' ' + html_strings[11 + j]
            break

    new_team = []

    num_spaces = get_num_spaces(text[start_of_outfield])

    num_defenders, num_midfielders, num_forwards = 0, 0, 0
    for i in range(1,11):
        if 'defender' in html_strings[i]:
            if num_defenders == 0:
                new_team.append((num_spaces - 2) * ' ' + '<div class="defenders">\n')
            num_defenders += 1
            new_team.append(num_spaces * ' ' + html_strings[i])
        elif 'midfielder' in html_strings[i]:
            if num_midfielders == 0:
                new_team.append((num_spaces - 2) * ' ' + '</div>\n')
                new_team.append((num_spaces - 2) * ' ' + '<div class="midfielders">\n')
            num_midfielders += 1
            new_team.append(num_spaces * ' ' + html_strings[i])
        elif 'forward' in html_strings[i]:
            if num_forwards == 0:
                new_team.append((num_spaces - 2) * ' ' + '</div>\n')
                new_team.append((num_spaces - 2) * ' ' + '<div class="forwards">\n')
            num_forwards += 1
            new_team.append(num_spaces * ' ' + html_strings[i])
    new_team.append((num_spaces - 2) * ' ' + '</div>\n')

    for i in range(start_of_outfield, start_of_outfield + len(new_team)):
        text[i] = new_team[i - start_of_outfield]

    start_of_outfield += 29
    num_goalkeepers, num_defenders, num_midfielders, num_forwards = 0, 0, 0, 0
    num_spaces = get_num_spaces(text[start_of_outfield])

    text[start_of_outfield - 4] = (num_spaces - 6) * ' ' + f'<h1>Best Players for Gameweek {gameweek} for Each Position</h1>\n'

    while num_goalkeepers < 5:
        text[start_of_outfield] = (num_spaces) * ' ' + best_players[num_goalkeepers]
        start_of_outfield += 1
        num_goalkeepers += 1
    
    start_of_outfield += 3

    while num_defenders < 8:
        text[start_of_outfield] = (num_spaces) * ' ' + best_players[num_goalkeepers + num_defenders]
        start_of_outfield += 1
        num_defenders += 1

    start_of_outfield += 3
    
    while num_midfielders < 8:
        text[start_of_outfield] = (num_spaces) * ' ' + best_players[num_goalkeepers + num_defenders + num_midfielders]
        start_of_outfield += 1
        num_midfielders += 1

    start_of_outfield += 3
    
    while num_forwards < 8:
        text[start_of_outfield] = (num_spaces) * ' ' + best_players[num_goalkeepers + num_defenders + num_midfielders + num_forwards]
        start_of_outfield += 1
        num_forwards += 1


    with open(file_location, 'w') as f:
        for line in text:
            f.write(line)