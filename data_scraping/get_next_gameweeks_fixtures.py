import os
import pandas as pd
import requests
import numpy as np
from datetime import date
#gets the next gameweek's fixtures for all players, uses date to get actual next gameweek fixtures no gameweek variable needed
#have to update gameweek variable manually for data storage purposes

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

year = f"{current_year}-{str(current_year + 1)[2:]}"

def get_n_last_gameweeks(last_3_gameweeks_df, final_df, stats_to_average):
    for stat in stats_to_average:
        final_df[f'{stat}_mean_last_3_gw'] = 0

    for player in last_3_gameweeks_df['name'].unique():
        player_df = last_3_gameweeks_df[last_3_gameweeks_df['name'] == player]
        temp_df = final_df[final_df['name'] == player]
        for stat in stats_to_average:
            nums = player_df[f'{stat}'].tolist()
            nums = [float(i) if i != "" else 0 for i in nums]
            while len(nums) > 3:
                nums.pop(0)
            mean = sum(nums) / len(nums)
            temp_df[f'{stat}_mean_last_3_gw'] = mean
            final_df[final_df['name'] == player] = temp_df

    return final_df

current_gameweek = requests.get(f"https://fantasy.premierleague.com/api/event-status/").json()
#{'status': [{'bonus_added': True, 'date': '2024-03-09', 'event': 28, 'points': 'r'}, {'bonus_added': True, 'date': '2024-03-10', 'event': 28, 'points': 'r'}, 
#{'bonus_added': True, 'date': '2024-03-11', 'event': 28, 'points': 'r'}, {'bonus_added': True, 'date': '2024-03-13', 'event': 28, 'points': 'r'}], 'leagues': 'Updating'}

#change to next gameweek
gameweek = 23

all_data = requests.get(f"https://fantasy.premierleague.com/api/bootstrap-static/").json()


player_data = all_data["elements"]
#,name,position,team,kickoff_time,value,was_home,yellow_cards,opponent,gameweek,season,team Goal scored,team Goal conceded,match_result
ids = []
names = []
positions = []
player_teams = []
kickoff_times = []
costs = []
is_homes = []
home_teams = []
away_teams = []

def get_team(all_data, team_id):
    teams = all_data["teams"]
    teams_with_ids = {}
    for team in teams:
        teams_with_ids[team["id"]] = team["name"]
    return teams_with_ids[team_id]

for player in player_data:
    id = player["id"]
    fixtures_data = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{id}/").json()
    fixture = fixtures_data["fixtures"][0]
    print(fixture)



    if fixture["event"] > gameweek:
        continue

    # will be not a player, but instead manager, which we dont want to add to the team of best players
    if player["element_type"] > 4:
        continue

    ids.append(player["id"])
    names.append(player["first_name"] + " " + player["second_name"])
    
    positions.append(player["element_type"])

    player_teams.append(player["team"])
    costs.append(player["now_cost"])

    kickoff_times.append(fixture["kickoff_time"])
    is_homes.append(fixture["is_home"])

    
    home_team_id = fixture["team_h"]
    away_team_id = fixture["team_a"]
    home_teams.append(get_team(all_data, home_team_id))
    away_teams.append(get_team(all_data, away_team_id))


df = pd.DataFrame(columns=["id", "name", "position", "team", "kickoff_time", "value", "was_home", "opponent", "gameweek", "season"])
df["id"] = ids
df["name"] = names

positions_dict = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}
positions = [positions_dict[position] for position in positions]
df["position"] = positions

df["team"] = np.where(is_homes, home_teams, away_teams)
df["kickoff_time"] = kickoff_times
df["kickoff_time"] = pd.to_datetime(df["kickoff_time"]).dt.hour
df["value"] = costs
df["was_home"] = is_homes
df["opponent"] = np.where(is_homes, away_teams, home_teams)
df["gameweek"] = gameweek
df["season"] = year

current_dir = os.path.dirname(__file__)
results_dir = f"{current_dir}/../data/{year}/results"
last_3_gameweeks_data = []
counter = 1
while len(last_3_gameweeks_data) < 3 and gameweek - counter > 0:
    if os.path.exists(f"{results_dir}/gameweek_{gameweek - counter}_results.csv"):
        last_3_gameweeks_data.insert(0, pd.read_csv(f"{results_dir}/gameweek_{gameweek - counter}_results.csv"))
    counter += 1
stats_to_average = stats_to_average = ["assists","bonus","bps","clean_sheets","creativity","goals_conceded","goals_scored","ict_index","influence","minutes","own_goals","penalties_missed","penalties_saved","red_cards","saves","selected","threat","total_points","transfers_balance","transfers_in","transfers_out","yellow_cards","goals scored (team)","goals conceded (team)","result"]
df = get_n_last_gameweeks(pd.concat(last_3_gameweeks_data), df, stats_to_average)
os.makedirs(f"{current_dir}/../data/{year}/fixtures", exist_ok=True)
df.to_csv(f"{current_dir[:-14]}/data/{year}/fixtures/gameweek_{gameweek}_fixtures.csv", index=False)