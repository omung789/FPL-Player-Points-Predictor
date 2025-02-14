import os
import pandas as pd
from datetime import date

# get current date to determine the current season
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
if current_month < 7:
    current_year = current_year - 1

year = f"{current_year}-{str(current_year + 1)[2:]}"

current_path = os.getcwd()
data_dir = os.path.join(current_path, f"data/{year}/results")

gameweek_num = 25   
columns = ['PLAYER', 'TEAM', 'POSITION']
gameweeks = [i for i in range(1, gameweek_num)]

for gameweek in gameweeks:
    columns.append(f"PRICE {gameweek}")
    columns.append(f"MINUTES {gameweek}")
    columns.append(f"POINTS {gameweek}")

final_df = pd.DataFrame(columns=columns)

df = pd.read_csv(data_dir + "/gameweek_1_results.csv", index_col=0)
    
for player in df["name"].unique():
    print(player)
    player_df = df[df["name"] == player]
    player_info = [player, player_df["team"].values[0], player_df["position"].values[0]]
    for gameweek in gameweeks:
        gameweek_df = pd.read_csv(data_dir + f"/gameweek_{gameweek}_results.csv", index_col=0)
        gameweek_df = gameweek_df[gameweek_df["name"] == player]
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

print(final_df.head(5))

final_df.to_csv(data_dir + f"/combined_data_{year}_so_far.csv")
