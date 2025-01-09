'''
BEFORE RUNNING:
Update gameweek number in autmate_everything.py, data_scraping/get_next_gameweeks_fixtures.py, data_scraping/get_previous_gameweeks_outcomes.py,
machine_learning.py, fix_html_files/fix_previous_teams_subdirectories, fix_html_files/fix_transfer_recommendations and best_teams/get_best_teams.py
Ensure all logos for teams are in the website/webpages/logos folder, essential to check for newly promoted teams
Ensure all player names in html files are formatted correctly, i.e. if multiple names instead of just a surname change to their known as
'''

# from data_scraping import get_previous_seasons_data
# from data_scraping import clean_previous_seasons_data
# from data_scraping import get_previous_gameweeks_outcomes
# from data_scraping import get_next_gameweeks_fixtures
# import machine_learning

# import combine_current_seasons_data

gameweek = 21

clubs = {
    'Arsenal': 'ARS',
    'Aston Villa': 'AVL',
    'Bournemouth': 'BOU',
    'Brentford': 'BRE',
    'Brighton': 'BRI',
    'Burnley': 'BUR',
    'Chelsea': 'CHE',
    'Crystal Palace': 'CRY',
    'Everton': 'EVE',
    'Fulham': 'FUL',
    'Ipswich': 'IPS',
    'Leeds': 'LEE',
    'Leicester': 'LEI',
    'Liverpool': 'LIV',
    'Luton': 'LUT',
    'Manchester City': 'MCI',
    'Man City': 'MCI',
    'Manchester United': 'MUN',
    'Man United': 'MUN',
    'Man Utd': 'MUN',
    'Newcastle': 'NEW',
    "Nott'm Forest": 'NFO',
    'Norwich': 'NOR',
    'Sheffield United': 'SHU',
    'Southampton': 'SOU',
    'Spurs': 'TOT',
    'Watford': 'WAT',
    'West Brom': 'WBA',
    'West Ham': 'WHU',
    'Wolves': 'WOL'
}


import re

def remove_accents(s):
    s = re.sub(r'[àáâãå]', 'a', s)
    s = re.sub(r'[ÀÁÂÃÅ]', 'A', s)
    s = re.sub(r'[èéêë]', 'e', s)
    s = re.sub(r'[ÈÉÊË]', 'E', s)
    s = re.sub(r'[ìíîï]', 'i', s)
    s = re.sub(r'[ÌÍÎÏ]', 'I', s)
    s = re.sub(r'[òóôõö]', 'o', s)
    s = re.sub(r'[ÒÓÔÕÖ]', 'O', s)
    s = re.sub(r'[ùúûü]', 'u', s)
    s = re.sub(r'[ÙÚÛÜ]', 'U', s)
    s = re.sub(r'[ýÿ]', 'y', s)
    s = re.sub(r'[Ý]', 'Y', s)
    s = re.sub(r'[ć]', 'c', s)
    s = re.sub(r'[Ć]', 'C', s)
    s = re.sub(r'[ñń]', 'n', s)
    s = re.sub(r'[ÑŃ]', 'N', s)
    return s

from best_teams import best_team_no_transfers
import pandas as pd
import os
from datetime import date
#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

years = [f"{current_year - i}-{str(current_year - i + 1)[2:]}" for i in range(2)]

try:
    os.mkdir(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{years[0]}\machine learning\predicted_best_teams")
except FileExistsError:
    pass

#from best_teams import get_best_teams

def team_to_html_strings(data_path,results_path):
    builder = best_team_no_transfers.FantasyTeamBuilder(data_path)
    builder.read_csv_data()
    builder.get_player_points()
    team, price = builder.get_best_team()
    html_strings = []
    num_defenders, num_midfielders, num_forwards = 0, 0, 0
    for i,player in enumerate(team):
        full_name = player[0].split(" ")
        if len(full_name) == 2:
            name = full_name[1]
        else:
            name = player[0]
        name = remove_accents(name)
        if (player[2] == "GKP" or player[2] == "GK") and i == 0:
            html_strings.append(f'<div class="player goalkeeper"><img src="../../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><br>{name}<br>Price: {player[3]}<br>Points: {player[-1]}</div>')
        elif player[2] == "DEF" and i < 11:
            html_strings.append(f'<div class="player defender"><img src="../../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><br>{name}<br>Price: {player[3]}<br>Points: {player[-1]}</div>')
        elif player[2] == "MID" and i < 11:
            html_strings.append(f'<div class="player midfielder"><img src="../../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><br>{name}<br>Price: {player[3]}<br>Points: {player[-1]}</div>')
        elif player[2] == "FWD" and i < 11:
            html_strings.append(f'<div class="player forward"><img src="../../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><br>{name}<br>Price: {player[3]}<br>Points: {player[-1]}</div>')
        else: #bench player
            num = 0
            if player[2] == 'GK' or player[2] == 'GKP':
                player[2] = 'GKP'
                html_strings.append(f'<div class="player"><h6>{player[2]}</h6><img src="../../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><br>{name}<br>Price: {player[3]}<br>Points: {player[-1]}</div>')
            else:
                if player[2] == 'DEF':
                    num_defenders += 1
                    num = num_defenders
                elif player[2] == 'MID':
                    num_midfielders += 1
                    num = num_midfielders
                elif player[2] == 'FWD':
                    num_forwards += 1
                    num = num_forwards
                html_strings.append(f'<div class="player"><h6>{player[2]} {num}</h6><img src="../../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><br>{name}<br>Price: {player[3]}<br>Points: {player[-1]}</div>')
    total_points = sum([player[-1] for player in team[:11]])
    if len(str(total_points)) > 6:
        html_strings.append(f'<h6>Total xP (Starting Lineup Only): {round(total_points,2)}</h6>')
    else:
        html_strings.append(f'<h6>Total Points (Starting Lineup Only): {total_points}</h6>')
    html_strings.append(f'<h6>Total Cost: {round(price,1)}</h6>')
    with open(results_path, 'w') as f:
        for string in html_strings:
            f.write(string + "\n")


for year in years:
    data_path = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\cleaned last 3 seasons data\cleaned_data_for_{year}_season.csv"
    results_path = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\html_strings_{year}.txt"
    if year == years[0]:
        # best team so far this season
        data_path = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\results\combined_data_{year}_so_far.csv"
        results_path = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\html_strings_{year}.txt"
        team_to_html_strings(data_path,results_path)
        #predictions for next gameweek
        data_path = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\machine learning\gameweek_{gameweek}_predictions.csv"
        results_path = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\machine learning\gameweek_{gameweek}_html_strings.txt"
    
    team_to_html_strings(data_path,results_path)

from fix_html_files import fix_previous_teams_folder
from fix_html_files import fix_previous_teams_subdirectories
from fix_html_files import fix_transfer_recommendations

