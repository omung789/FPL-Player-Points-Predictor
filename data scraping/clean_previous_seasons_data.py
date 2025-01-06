import os
from scipy import stats
import pandas as pd
import numpy as np
from datetime import date

#get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

#previous seasons to get data from
# in 2023-24 season, seasons = ['2020-21', '2021-22', '2022-23']
seasons = [f"{current_year - i - 1}-{str(current_year - i)[2:]}" for i in range(3)]
seasons.reverse()

current_directory = os.path.dirname(os.path.realpath(__file__))
data_dir = current_directory[:-14] + "/data"



columns = ['PLAYER', 'TEAM', 'POSITION']
gameweeks = [i for i in range(1, 39)]

for gameweek in gameweeks:
    columns.append(f"PRICE {gameweek}")
    columns.append(f"MINUTES {gameweek}")
    columns.append(f"POINTS {gameweek}")

for season in seasons:
    if os.path.exists(data_dir + f"/cleaned last 3 seasons data/cleaned_data_for_{season}_season.csv"):
        print(f"Data for {season} season already exists")
        continue
    df = pd.read_csv(data_dir + f"/data_for_{season}_season.csv", index_col=0)
    final_df = pd.DataFrame(columns=columns)
    for player in df["name"].unique():
        print(player)
        player_df = df[df["name"] == player]
        player_info = [player, player_df["team"].values[0], player_df["position"].values[0]]
        for gameweek in gameweeks:
            gameweek_df = player_df[player_df["gameweek"] == gameweek]
            if gameweek_df.shape[0] == 0:
                # find the closest gameweek as player did not play in this gameweek, so we can find their value
                gameweeks_list = player_df['gameweek'].unique().tolist()
                closest_gameweek = min(gameweeks_list, key=lambda y: abs(y - gameweek))
                closest_value = player_df[player_df['gameweek'] == closest_gameweek]['value'].iloc[0]
                player_info.extend([closest_value,0,0])
            elif gameweek_df.shape[0] == 1:
                player_info.extend([gameweek_df["value"].values[0], gameweek_df["minutes"].values[0], gameweek_df["total_points"].values[0]])
            elif gameweek_df.shape[0] >= 2:
                mins, points = 0, 0
                for i in range(df.shape[0]):
                    mins = sum(gameweek_df['minutes'].tolist())
                    points = sum(gameweek_df['total_points'].tolist())
                player_info.extend([gameweek_df["value"].values[0], mins, points])
        final_df = pd.concat([final_df, pd.DataFrame([player_info], columns=final_df.columns)])

    print(final_df)

    final_df.to_csv(data_dir + "/cleaned last 3 seasons data/" + f"cleaned_data_for_{season}_season.csv")

