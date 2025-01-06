import best_team_no_transfers
import pandas as pd
import os
import numpy as np
gameweek = 31
year = "2023-24"

# # builder = best_team_no_transfers.FantasyTeamBuilder(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\machine learning\gameweek_{gameweek}_predictions.csv")
# # builder.read_csv_data()
# # builder.get_player_points()
# # team, price = builder.get_best_team()
# # builder.print_team(team)
# # print("Price: ", price)
# # print("---------------")
# # df = pd.DataFrame(team)
# # df.to_csv(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\2023-24\machine learning\predicted best teams\predicted_team_{year}_gw{gameweek}.csv", index=False)


# current_season_results_directory = fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\results"
# gw_dir = os.listdir(current_season_results_directory)
# number_of_gameweeks = len([name for name in gw_dir if name.endswith(".csv") and name.startswith("gameweek")])


# player_data = []
# for gameweek in range(number_of_gameweeks):
#     filename = f"gameweek_{gameweek+1}_results.csv"
#     if os.path.isfile(os.path.join(current_season_results_directory, filename)):
#         if filename.endswith(".csv") and filename.startswith("gameweek"):
#             gw_df = pd.read_csv(os.path.join(current_season_results_directory, filename))
#             player_data.extend(gw_df[['name', 'team', 'position']].values.tolist())

# # Remove duplicates from player data list
# unique_player_data = list(set(map(tuple, player_data)))

# # Convert unique player data back to list of lists
# unique_player_data = [list(player) for player in unique_player_data]

# new_df = pd.DataFrame(unique_player_data, columns=['PLAYER', 'TEAM', 'POSITION'])
# new_df['PRICE'] = np.nan

# for player in unique_player_data:
#     player_name = player[0]
#     for i in range(number_of_gameweeks):
#         filename = fr"gameweek_{i+1}_results.csv"
#         if os.path.isfile(os.path.join(current_season_results_directory, filename)):
#             if filename.endswith(".csv") and filename.startswith("gameweek"):
#                 gw_df = pd.read_csv(os.path.join(current_season_results_directory, filename))
#                 if player_name in gw_df['name'].values:
#                     player_minutes = gw_df[gw_df['name'] == player_name]['minutes'].values[0]
#                     new_df.loc[new_df['PLAYER'] == player_name, f'MINUTES {i+1}'] = player_minutes
#                     player_points = gw_df[gw_df['name'] == player_name]['total_points'].values[0]
#                     new_df.loc[new_df['PLAYER'] == player_name, f'POINTS {i+1}'] = player_points
#                     #if we find a value for the player, and the player value has not already been set, then we can set the value
#                     if pd.isnull(new_df.loc[new_df['PLAYER'] == player_name, 'PRICE'].values[0]):
#                         new_df.loc[new_df['PLAYER'] == player_name, 'PRICE'] = gw_df[gw_df['name'] == player_name]['value'].values[0]
#                 else:
#                     new_df.loc[new_df['PLAYER'] == player_name, f'MINUTES {i+1}'] = 0
#                     new_df.loc[new_df['PLAYER'] == player_name, f'POINTS {i+1}'] = 0
                    
#     player_index = unique_player_data.index(player)
#     print("progress: ", ((player_index + 1)/ len(unique_player_data)) * 100, "%")


# print(new_df.columns)
# print(new_df[new_df['PLAYER'] == "Kevin Schade"])
# new_df.replace("", 0, inplace=True)
# new_df.fillna(0, inplace=True)
# new_df.to_csv(os.path.join(current_season_results_directory, fr"combined_data_{year}_so_far.csv"))

# builder = best_team_no_transfers.FantasyTeamBuilder(os.path.join(current_season_results_directory, fr"combined_data_{year}_so_far.csv"))
# builder.read_csv_data()
# builder.get_player_points()
# print(builder.def_player_points)
# team, price = builder.get_best_team()
# builder.print_team(team)
# print("Price: ", price)
# print("---------------")
# df = pd.DataFrame(team)
# df.to_csv(os.path.join(current_season_results_directory, fr"best_team_{year}_so_far.csv"), index=False)
gameweek = 31
predictions_df = pd.read_csv(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\2023-24\machine learning\gameweek_{gameweek}_predictions.csv")
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
    string = f'<div class="player-info"><img src="../../logos/{player[1]}.png" alt="{player[1]} Logo"><p>{player[0]}<br>Price: {float(player[3]) / 10}<br>xP: {player[4]}</p></div>'
    html_strings.append(string)
    print(string)
#predicted_players_df.to_csv(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\2023-24\machine learning\predicted best teams\predicted_best_players_{year}_gw{gameweek}.csv", index=False)
