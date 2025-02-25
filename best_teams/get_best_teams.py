from datetime import date
#import best_team_no_transfers
import pandas as pd
import os
import numpy as np
#from abbreviate_team_names import clubs

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

current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

year = f"{current_year}-{str(current_year + 1)[2:]}"

gameweek = 27
predictions_df = pd.read_csv(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\machine learning\gameweek_{gameweek}_predictions.csv")
predictions_df = predictions_df.sort_values(by='Linear Regression POINTS Predictions', ascending=False)

predicted_gkp = predictions_df[predictions_df['POSITION'] == 'GKP'].head(5)
predicted_def = predictions_df[predictions_df['POSITION'] == 'DEF'].head(8)
predicted_mid = predictions_df[predictions_df['POSITION'] == 'MID'].head(8)
predicted_fwd = predictions_df[predictions_df['POSITION'] == 'FWD'].head(8)

    
predicted_players_df = pd.concat([predicted_gkp, predicted_def, predicted_mid, predicted_fwd])
predicted_players_df.drop(columns=['id','MINUTES'], inplace=True)
predicted_players_df['Linear Regression POINTS Predictions'] = predicted_players_df['Linear Regression POINTS Predictions'].round(2)
predicted_players_list = predicted_players_df.values.tolist()
print(predicted_players_list[0])

html_strings = []
for i, player in enumerate(predicted_players_list):
    if predicted_players_list[i-1][2] != player[2] and i != 0:
        print("\n")
    full_name = player[0].split(" ")
    if len(full_name) == 2:
        name = full_name[1]
    else:
        name = player[0]
    remove_accents(name)
    string = f'<div class="player-info"><img src="../logos/{clubs[player[1]]}.png" alt="{player[1]} Logo"><p>{name}<br>Price: {float(player[3]) / 10}<br>xP: {round(player[4],2)}</p></div>'
    html_strings.append(string)

with open(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\machine learning\predicted_best_teams\predicted_best_players_{year}_gw{gameweek}.txt", "w") as file:
    for string in html_strings:
        file.write(string)
        file.write("\n")
#predicted_players_df.to_csv(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\2023-24\machine learning\predicted best teams\predicted_best_players_{year}_gw{gameweek}.csv", index=False)
