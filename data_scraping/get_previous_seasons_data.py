import os
import numpy as np
import pandas as pd
from datetime import date

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1
    
columns_to_be_removed=["xP","opponent_team","expected_assists","expected_goal_involvements","expected_goals","expected_goals_conceded","team_h_score","team_a_score","element","round","fixture","starts"]

def get_mean_last_n_gameweeks(df, stats_to_average, window_size=3):

    # Sort the DataFrame by player, season, and gameweek
    df.sort_values(by=['name', 'season', 'gameweek'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    for stat in stats_to_average:
        # Create a new column to store the rolling mean of the stat for each player and season
        df[f'{stat}_mean_last_3_gw'] = df.groupby(['name', 'season'])[stat].rolling(window=window_size, min_periods=1 ).mean().reset_index(drop=True)

    # Shift mean values by 1 for each player and season
    for stat in stats_to_average:
        # Group by player, season, and apply the operation
        for (player, season), group_df in df.groupby(['name', 'season']):
            nums = group_df[f'{stat}_mean_last_3_gw'].tolist()
            nums = [0] + nums[:-1]
            try:
                df.loc[group_df.index, f'{stat}_mean_last_3_gw'] = nums
            except ValueError:
                print(player, season, stat)
    
    return df

#previous years to get data from
# in 2023-24 season, years = ['2020-21', '2021-22', '2022-23']
# and previous years = ['2019-20', '2020-21', '2021-22']

years = [f"{current_year - i - 1}-{str(current_year - i)[2:]}" for i in range(3)]
years.reverse()

gameweeks = ["gameweek" + str(i) for i in range(1, 39)]


list_all_dfs = []
for i, year in enumerate(years):
    list_dfs = []
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(current_dir[:-14] + f"/data/data_for_{year}_season.csv"):
        print(f"Data already exists for {year} season")
        continue

    print(year)

    # get opponent_team
    teams = pd.read_csv(
        f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/teams.csv",
        encoding="latin-1",
    )[["id", "name"]]
    teams.columns = ["opponent_team", "opponent"]

    for gameweek in range(1, 39):
        print(gameweek)
        # get gameweek data
        df = pd.read_csv(
            f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/gws/gw{gameweek}.csv"
        )

        # merge team data
        df = df.merge(teams, left_on="opponent_team", right_on="opponent_team")

        df["gameweek"] = gameweek
        df["season"] = year

        # append to list of dataframes
        list_dfs.append(df)
        list_all_dfs.append(df)

    all_data = pd.concat(list_dfs)
    
    #save data for each season seperately for future use
    
    all_data.sort_values(by=["name", "gameweek"], inplace=True)
    all_data.to_csv(current_dir[:-14] + f"/data/data_for_{year}_season.csv")
    
all_data = pd.concat(list_all_dfs)

all_data_home=all_data[all_data["was_home"]==True]
all_data_away=all_data[all_data["was_home"]==False]
all_data_home["goals scored (team)"]=all_data_home["team_h_score"]
all_data_home["goals conceded (team)"]=all_data_home["team_a_score"]
all_data_away["goals conceded (team)"]=all_data_away["team_h_score"]
all_data_away["goals scored (team)"]=all_data_away["team_a_score"]
all_data=pd.concat([all_data_home,all_data_away])
result = all_data["goals scored (team)"] - all_data["goals conceded (team)"]
all_data["result"] = np.where(result > 0, 3, np.where(result < 0, 0, 1))

all_data.drop(columns_to_be_removed,axis=1,inplace=True)

all_data["kickoff_time"] = pd.to_datetime(all_data["kickoff_time"]).dt.hour
#76319
all_data.drop_duplicates(["name","gameweek","season","team","opponent"],inplace=True)

all_data.sort_values(by=["name", "season", "gameweek"], inplace=True)

stats_to_average = ["assists","bonus","bps","clean_sheets","creativity","goals_conceded","goals_scored","ict_index","influence","minutes","own_goals","penalties_missed","penalties_saved","red_cards","saves","selected","threat","total_points","transfers_balance","transfers_in","transfers_out","yellow_cards","goals scored (team)","goals conceded (team)","result"]

all_data = get_mean_last_n_gameweeks(all_data, stats_to_average, window_size=3)

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = current_dir[:-14] + "/data"
all_data.to_csv(data_dir + "/combined_previous_seasons_data.csv")

#delete files in the directory that are not from the last 3 seasons
files_in_directory = os.listdir(data_dir)

file_names_in_code = ["combined_previous_seasons_data.csv", "fake data"]
for year in years:
    file_names_in_code.append(f"data_for_{year}_season.csv")

missing_files = [file for file in files_in_directory if file not in file_names_in_code]

if missing_files:
    print("The following files are in the directory but not listed in the Python code:")
    for file in missing_files:
        path = data_dir + "/" + file
        if os.path.isfile(path):
            print(file)
            os.remove(path)
        else:
            print(f"{file} is a directory and will not be removed.")
else:
    print("All files in the directory are listed in the Python code.")

#,name,position,team,xP,assists,bonus,bps,clean_sheets,creativity,element,fixture,goals_conceded,goals_scored,ict_index,influence,kickoff_time,minutes,opponent_team,own_goals,penalties_missed,penalties_saved,red_cards,round,saves,selected,team_a_score,team_h_score,threat,total_points,transfers_balance,transfers_in,transfers_out,value,was_home,yellow_cards,opponent,gameweek,season,expected_assists,expected_goal_involvements,expected_goals,expected_goals_conceded,starts
#,name,position,team,xP,assists,bonus,bps,clean_sheets,creativity,element,fixture,goals_conceded,goals_scored,ict_index,influence,kickoff_time,minutes,opponent_team,own_goals,penalties_missed,penalties_saved,red_cards,round,saves,selected,team_a_score,team_h_score,threat,total_points,transfers_balance,transfers_in,transfers_out,value,was_home,yellow_cards,last_season_position,percent_value,position rank,match_result,goals_scored_ex,assists_ex,total_points_ex,minutes_ex,goals_conceded_ex,creativity_ex,influence_ex,threat_ex,bonus_ex,bps_ex,ict_index_ex,clean_sheets_ex,red_cards_ex,yellow_cards_ex,selected_by_percent_ex,now_cost_ex,season,GW,opponent,opponent_last_season_position,element_type_ex,expected_assists,expected_goal_involvements,expected_goals,expected_goals_conceded,starts
