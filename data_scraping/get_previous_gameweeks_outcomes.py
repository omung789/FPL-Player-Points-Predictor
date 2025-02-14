import os
import numpy as np
import pandas as pd
from datetime import date

import requests

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

year = f"{current_year}-{str(current_year + 1)[2:]}"
current_dir = os.path.dirname(__file__)
results_dir = f"{current_dir}/../data/{year}/results"
os.makedirs(results_dir, exist_ok=True)

def get_team(all_data, team_id):
    teams = all_data["teams"]
    teams_with_ids = {}
    for team in teams:
        teams_with_ids[team["id"]] = team["name"]
    return teams_with_ids[team_id]

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


all_data = requests.get(f"https://fantasy.premierleague.com/api/bootstrap-static/").json()
player_data = all_data["elements"]

# put upcoming gameweek number here
gameweeks = 25
last_3_gameweeks_data = []
for gameweek in range(1, gameweeks):
    print(f"Getting gameweek {gameweek} results")
    player_gameweek_data = []
    if os.path.exists(f"{results_dir}/gameweek_{gameweek}_results.csv"):
        print(f"Gameweek {gameweek} results already exist")
        continue
    
    for player in player_data:
        #print("player:\n",player)
        # will be not a player, but instead manager, which we dont want to add to the team of best players
        if player["element_type"] > 4:
            continue
        id = player["id"]
        all_gameweek_results = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{id}/").json()["history"]
        current_gameweek_results = [result for result in all_gameweek_results if result["round"] == gameweek]
        if len(current_gameweek_results) == 0:
            print(f"Player {id} has no data for gameweek {gameweek}")
            continue
        for gameweek_results in current_gameweek_results:
        #,name,position,team,assists,bonus,bps,clean_sheets,creativity,goals_conceded,goals_scored,ict_index,influence,kickoff_time,minutes,own_goals,penalties_missed,penalties_saved,red_cards,saves
        #,selected,threat,total_points,transfers_balance,transfers_in,transfers_out,value,was_home,yellow_cards,opponent,gameweek,season,team Goal scored,team Goal conceded,match_result
            name = player["first_name"] + " " + player["second_name"]
            position = player["element_type"]
            positions_dict = {1: 'GKP', 2: 'DEF', 3: 'MID', 4: 'FWD'}
            position = positions_dict[position]
            player_team = get_team(all_data, player["team"])
            gameweek_results["name"] = name
            gameweek_results["position"] = position
            gameweek_results["team"] = player_team
            gameweek_results["opponent"] = get_team(all_data, gameweek_results["opponent_team"])
            gameweek_results["season"] = year
            if gameweek_results["was_home"]:
                gameweek_results["goals scored (team)"] = gameweek_results["team_h_score"]
                gameweek_results["goals conceded (team)"] = gameweek_results["team_a_score"]
            else:
                gameweek_results["goals scored (team)"] = gameweek_results["team_a_score"]
                gameweek_results["goals conceded (team)"] = gameweek_results["team_h_score"]
            
            if gameweek_results["goals scored (team)"] > gameweek_results["goals conceded (team)"]:
                gameweek_results["result"] = 3
            elif gameweek_results["goals scored (team)"] < gameweek_results["goals conceded (team)"]:
                gameweek_results["result"] = 0
            elif gameweek_results["goals scored (team)"] == gameweek_results["goals conceded (team)"]:
                gameweek_results["result"] = 1
            #shouldn't happen
            else:
                gameweek_results["result"] = -1
            player_gameweek_data.append(gameweek_results)
        
    df = pd.DataFrame(player_gameweek_data)
    df["kickoff_time"] = pd.to_datetime(df["kickoff_time"]).dt.hour
    df.rename(columns={'element': 'id'}, inplace=True)
    df.rename(columns={'round': 'gameweek'}, inplace=True)

    #if gameweeks were skipped earlier in code then we need to get the last 3 gameweeks data from the csv files
    counter = 1
    while len(last_3_gameweeks_data) < 3 and gameweek - counter > 0:
        if os.path.exists(f"{results_dir}/gameweek_{gameweek - counter}_results.csv"):
            last_3_gameweeks_data.insert(0, pd.read_csv(f"{results_dir}/gameweek_{gameweek - counter}_results.csv"))
        counter += 1

    #add mean stats for the last 3 gameweeks to the dataframe
    stats_to_average = ["assists","bonus","bps","clean_sheets","creativity","goals_conceded","goals_scored","ict_index","influence","minutes","own_goals","penalties_missed","penalties_saved","red_cards","saves","selected","threat","total_points","transfers_balance","transfers_in","transfers_out","yellow_cards","goals scored (team)","goals conceded (team)","result"]
    if last_3_gameweeks_data:
        last_3_gameweeks_df = pd.concat(last_3_gameweeks_data)
        df = get_n_last_gameweeks(last_3_gameweeks_df, df, stats_to_average)
    else:
        for stat in stats_to_average:
            df[f'{stat}_mean_last_3_gw'] = 0

    columns_to_remove = ["fixture", "opponent_team", "team_h_score", "team_a_score", "starts", "expected_goals", "expected_assists","expected_goal_involvements",'expected_goals_conceded']
    df.drop(columns=columns_to_remove, inplace=True)
    df.to_csv(f"{results_dir}/gameweek_{gameweek}_results.csv", index=False)

    last_3_gameweeks_data.append(df)
    if len(last_3_gameweeks_data) > 3:
        last_3_gameweeks_data.pop(0)
    print(f"Saved gameweek {gameweek} results")
    