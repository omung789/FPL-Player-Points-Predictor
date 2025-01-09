import csv
import pandas as pd
import os
import time

class FantasyTeamBuilder:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.new_data = []
        self.points_minutes_indexes = []
        self.gkp_player_points = []
        self.def_player_points = []
        self.mid_player_points = []
        self.fwd_player_points = []

    #need to add values indexes, dividing by 10 to get the actual price
    def read_csv_data(self):
        with open(self.csv_file, 'r', newline='',encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            self.new_data = [row for row in csv_reader]

            for i, header in enumerate(headers):
                if "MINUTES" in header:
                    self.points_minutes_indexes.append(i)
                if "POINTS" in header:
                    self.points_minutes_indexes.append(i)
    #need to fix indexes inside all if statements
    def get_player_points(self):
        for row in self.new_data:
            if row[3] == "GKP" or row[3] == "GK":
                self.gkp_player_points.extend([[row[1], row[2], row[3], float(row[4])/10] + ([float(row[i]) for i in self.points_minutes_indexes])])
            elif row[3] == "DEF":
                self.def_player_points.extend([[row[1], row[2], row[3], float(row[4])/10] + ([float(row[i]) for i in self.points_minutes_indexes])])
            elif row[3] == "MID":
                self.mid_player_points.extend([[row[1], row[2], row[3], float(row[4])/10] + ([float(row[i]) for i in self.points_minutes_indexes])])
            elif row[3] == "FWD":
                self.fwd_player_points.extend([[row[1], row[2], row[3], float(row[4])/10] + ([float(row[i]) for i in self.points_minutes_indexes])])

    def get_total_player_points(self, team):
        for player in team:
            if player[2] == "GKP" or player[2] == "GK":
                player.extend([sum(player[5::2])])
            elif player[2] == "DEF":
                player.extend([sum(player[5::2])])
            elif player[2] == "MID":
                player.extend([sum(player[5::2])])
            elif player[2] == "FWD":
                player.extend([sum(player[5::2])])

    def sort_points_by_total(self, temp_gkp, temp_def, temp_mid, temp_fwd):
        temp_gkp.sort(key=lambda x: x[-1], reverse=True)
        temp_def.sort(key=lambda x: x[-1], reverse=True)
        temp_mid.sort(key=lambda x: x[-1], reverse=True)
        temp_fwd.sort(key=lambda x: x[-1], reverse=True)

    def sort_points_by_gameweek(self, temp_gkp, temp_def, temp_mid, temp_fwd, gameweek):
        #PLAYER,TEAM,POSITION,PRICE,MINUTES,POINTS
        temp_gkp.sort(key=lambda x: x[2 * gameweek + 3], reverse=True)
        temp_def.sort(key=lambda x: x[2 * gameweek + 3], reverse=True)
        temp_mid.sort(key=lambda x: x[2 * gameweek + 3], reverse=True)
        temp_fwd.sort(key=lambda x: x[2 * gameweek + 3], reverse=True)

    def sort_points_by_gameweek_low_to_high(self, temp_def, temp_mid, temp_fwd, gameweek):
        #gameweek 1 is index 5, gameweek 2 is index 7 etc.
        #temp_gkp.sort(key=lambda x: x[2 * gameweek + 3])
        temp_def.sort(key=lambda x: x[2 * gameweek + 3])
        temp_mid.sort(key=lambda x: x[2 * gameweek + 3])
        temp_fwd.sort(key=lambda x: x[2 * gameweek + 3])

    #sorts players by price (lowest to highest)
    def sort_players_by_price(self, temp_gkp, temp_def, temp_mid, temp_fwd):
        temp_gkp.sort(key=lambda x: float(x[3]))
        temp_def.sort(key=lambda x: float(x[3]))
        temp_mid.sort(key=lambda x: float(x[3]))
        temp_fwd.sort(key=lambda x: float(x[3]))

    def get_max_points_for_specific_gameweeks(self, players, gameweeks):
        points_list = []
        for player in players:
            num = 0
            #[2:] to only look at gameweeks, not player info
            for gameweek in gameweeks[2:]:
                num += (player[2 * gameweek + 3])
            points_list.append(num)
        max_points = max(points_list)
        index = points_list.index(max_points)
        return players[index]
    
    def find_gameweeks_with_zero_mins(self, team):
        team_gameweeks = []
        for player in team:
            #[position, price]
            player_gameweeks = [player[2], player[3]]
            for gameweek in range(1, len(player) // 2 - 1):
                if player[2 * gameweek + 2] == 0:
                    player_gameweeks.append(gameweek)
            if len(player_gameweeks) > 2:
                team_gameweeks.append(player_gameweeks)
        return team_gameweeks
    
    def get_dict_of_zero_mins(self, team):
        get_zero_mins = self.find_gameweeks_with_zero_mins(team)
        zero_mins_dict = {}
        for zero_min in get_zero_mins:
            for index in zero_min[2:]:
                if index in zero_mins_dict and zero_mins_dict[index] != 3:
                    zero_mins_dict[index] += 1
                else:
                    zero_mins_dict[index] = 1
        return zero_mins_dict


    def max_3_per_team(self, players):
        team_count = {}
        for player in players:
            if player[1] in team_count:
                team_count[player[1]] += 1
            else:
                team_count[player[1]] = 1
        return max(team_count.values()) <= 3
    
    def valid_formations(self, team):
        positions = {"DEF": 0, "MID": 0, "FWD": 0} 
        for player in team:
            if player[2] == "DEF":
                positions["DEF"] += 1
            elif player[2] == "MID":
                positions["MID"] += 1
            elif player[2] == "FWD":
                positions["FWD"] += 1

        formations = ["343", "352", "433", "442", "451", "523", "532", "541"]
        if str(positions["DEF"]) +  str(positions["MID"]) + str(positions["FWD"]) in formations:
            return True
        return False
    
    def get_formation(self, team):
        positions = {"DEF": 0, "MID": 0, "FWD": 0} 
        for player in team:
            if player[2] == "DEF":
                positions["DEF"] += 1
            elif player[2] == "MID":
                positions["MID"] += 1
            elif player[2] == "FWD":
                positions["FWD"] += 1
        return str(positions["DEF"]) +  str(positions["MID"]) + str(positions["FWD"])
    
    def sort_team_by_position(self, team):
        gkp = [player for player in team if player[2] == "GKP" or player[2] == "GK"]
        defenders = [player for player in team if player[2] == "DEF"]
        midfielders = [player for player in team if player[2] == "MID"]
        forwards = [player for player in team if player[2] == "FWD"]
        return gkp + defenders + midfielders + forwards
    
    def print_team(self, team):
        print("-------------------")
        for player in team:
            print(player[0], player[-1])

    def add_goalkeeper(self, team, temp_gkp, price):
        index = 0
        while (len(team) < 11):
            if self.max_3_per_team([temp_gkp[index]] + team):
                team = [temp_gkp[index]] + team
                price += float(temp_gkp[index][3])
                temp_gkp.pop(index)
                break
            index += 1
        return team, price
    
    # def get_points_total(self, team, gameweek):
    #     total = 0
    #     for player in team[:11]:
    #         total += player[gameweek + 2]
    #     return total
    
    def get_best_team(self):
        temp_gkp = self.gkp_player_points.copy()
        temp_def = self.def_player_points.copy()
        temp_mid = self.mid_player_points.copy()
        temp_fwd = self.fwd_player_points.copy()

        self.get_total_player_points(temp_gkp)
        self.get_total_player_points(temp_def)
        self.get_total_player_points(temp_mid)
        self.get_total_player_points(temp_fwd)

        self.sort_points_by_total(temp_gkp, temp_def, temp_mid, temp_fwd)

        # for player in temp_def:
        #     print(player[0], player[-1])
        

        price = 0.0
        team = []
        max_defenders, max_midfielders, max_forwards = 5, 5, 3
        #min_goalkeepers, min_defenders, min_midfielders, min_forwards = 1, 3, 2, 1
        max_players = 11
        num_defenders, num_midfielders, num_forwards = 0, 0, 0

        while len(team) < max_players - 1 : # -1 because we will add a goalkeeper after
            next_players = []
            # to ensure we don't use an illegal formation
            if num_defenders == max_defenders:
                max_midfielders = 4
            if num_midfielders == max_midfielders: 
                max_defenders = 4
                max_forwards = 2
            if num_forwards == max_forwards:
                max_midfielders = 4
                
            if num_defenders < max_defenders:
                while self.max_3_per_team([temp_def[0]] + team) == False:
                    temp_def.pop(0)
                next_players.append(temp_def[0])
            if num_midfielders < max_midfielders:
                while self.max_3_per_team([temp_mid[0]] + team) == False:
                    temp_mid.pop(0)
                next_players.append(temp_mid[0])
            if num_forwards < max_forwards:
                while self.max_3_per_team([temp_fwd[0]] + team) == False:
                    temp_fwd.pop(0)
                next_players.append(temp_fwd[0])
            next_player = max(next_players, key=lambda x: x[-1])
            team.append(next_player)
            price += float(next_player[3])

            if next_player in temp_def:
                num_defenders += 1
                temp_def.remove(next_player)
            elif next_player in temp_mid:
                num_midfielders += 1
                temp_mid.remove(next_player)
            elif next_player in temp_fwd:
                num_forwards += 1
                temp_fwd.remove(next_player)
        
        max_defenders, max_midfielders, max_forwards = 5, 5, 3

        #if formation is not valid, then we need to change the team
        if self.valid_formations(team) == False:
            #can only be these formations 550, 253
            #if 5 defenders, then 550, either change a defender or midfielder to a forward
            if len([player for player in team if "DEF" in player[0]]) == 5:
                worst_player = min(team, key=lambda x: x[-1])
                next_player = max(temp_def + temp_mid, key=lambda x: x[-1])
                if "DEF" in next_player[0]:
                    temp_def.remove(next_player)
                else:
                    temp_mid.remove(next_player)
                team.remove(worst_player)
                team.append(next_player)
            #otherwise it must be 253, so change a forward or midfielder to a defender
            else:
                worst_player = min([player for player in team if "MID" or "FWD" in player[0]], key=lambda x: x[-1])
                next_player = max(temp_def, key=lambda x: x[-1])
                temp_def.remove(next_player)
                team.remove(worst_player)
                team.append(next_player)
            price -= float(worst_player[3])
            price += float(next_player[3])

        team = self.sort_team_by_position(team)
        
        team, price = self.add_goalkeeper(team, temp_gkp, price)

        team_defenders, team_midfielders, team_forwards = 5, 5, 3
        #need to add bench players, ensuring that price is <= 100
        self.sort_players_by_price(temp_gkp, temp_def, temp_mid, temp_fwd)
        bench = []

        while num_defenders < team_defenders:
            if self.max_3_per_team([temp_def[0]] + team + bench):
                bench.append(temp_def[0])
                price += float(temp_def[0][3])
                num_defenders += 1
            temp_def.pop(0)
        while num_midfielders < team_midfielders:
            if self.max_3_per_team([temp_mid[0]] + team + bench):
                bench.append(temp_mid[0])
                price += float(temp_mid[0][3])
                num_midfielders += 1
            temp_mid.pop(0)
        while num_forwards < team_forwards:
            if self.max_3_per_team([temp_fwd[0]] + team + bench):
                bench.append(temp_fwd[0])
                price += float(temp_fwd[0][3])
                num_forwards += 1
            temp_fwd.pop(0)
        while self.max_3_per_team([temp_gkp[0]] + team) == False:
            temp_gkp.pop(0)
        bench, price = self.add_goalkeeper(bench, temp_gkp, price)
        # self.print_team(team)
        # print("price:", price)

        # print("bench1:",bench)

        while price > 100:
            team = self.sort_team_by_position(team)
            #we have cheapest bench possible, so need to reduce price of starting 11
            defenders = [player for player in team if player[2] == "DEF"]
            midfielders = [player for player in team if player[2] == "MID"]
            forwards = [player for player in team if player[2] == "FWD"]

            self.sort_points_by_total([], defenders, midfielders, forwards)

            #find the next player with best points to put into team
            bench_defenders = [player for player in bench if player[2] == "DEF"]
            bench_midfielders = [player for player in bench if player[2] == "MID"]
            bench_forwards = [player for player in bench if player[2] == "FWD"]

            #check if bench players can be next best fit for team, if so put them in contention for next player
            if len(bench_defenders) > 0:
                next_player = max(bench_defenders, key=lambda x: x[-1])
                temp_def.append(next_player)
            
            if len(bench_midfielders) > 0:
                next_player = max(bench_midfielders, key=lambda x: x[-1])
                temp_mid.append(next_player)

            if len(bench_forwards) > 0:
                next_player = max(bench_forwards, key=lambda x: x[-1])
                temp_fwd.append(next_player)

            self.sort_points_by_total(temp_gkp, temp_def, temp_mid, temp_fwd)
            
            next_players = [temp_def[0]] + [temp_mid[0]] + [temp_fwd[0]]

            players_removed_from_team = []

            next_players.sort(key=lambda x: x[-1], reverse=True)
            team.sort(key=lambda x: x[-1])
            for player in team:
                temp_team = team.copy()
                temp_team.remove(player)
                for i in range(0, len(next_players)):
                    next_player = next_players[i]
                    if player[2] != "GKP" and next_player[2] != "GK":
                        if float(next_player[3]) < float(player[3]) and self.max_3_per_team([next_player] + temp_team) and self.valid_formations([next_player] + temp_team):
                            team.remove(player)
                            players_removed_from_team.append(player)
                            team.append(next_player)
                            price -= float(player[3])
                            price += float(next_player[3])
                            if next_player in bench:
                                bench.remove(next_player)
                                price -= float(next_player[3])
                                if next_player[2] == "DEF":
                                    num_defenders -= 1
                                    while num_defenders < team_defenders:
                                        new_bench_player = min(temp_def, key=lambda x: x[3])
                                        if self.max_3_per_team([new_bench_player] + team + bench) and temp_def[0][0][:3] != next_player[0][:3]:
                                            bench.append(new_bench_player)
                                            price += float(new_bench_player[3])
                                            num_defenders += 1
                                        temp_def.remove(new_bench_player)
                                elif next_player[2] == "MID":
                                    num_midfielders -= 1
                                    while num_midfielders < team_midfielders:
                                        new_bench_player = min(temp_mid, key=lambda x: x[3])
                                        if self.max_3_per_team([new_bench_player] + team + bench) and temp_mid[0][0][:3] != next_player[0][:3]:
                                            bench.append(new_bench_player)
                                            price += float(new_bench_player[3])
                                            num_midfielders += 1
                                        temp_mid.remove(new_bench_player)
                                elif next_player[2] == "FWD":
                                    num_forwards -= 1
                                    while num_forwards < team_forwards:
                                        new_bench_player = min(temp_fwd, key=lambda x: x[3])
                                        if self.max_3_per_team([new_bench_player] + team + bench) and temp_fwd[0][0][:3] != next_player[0][:3]:
                                            bench.append(new_bench_player)
                                            price += float(new_bench_player[3])
                                            num_forwards += 1
                                        temp_fwd.remove(new_bench_player)
                            if next_player in temp_def:
                                temp_def.pop(0)
                                num_defenders += 1
                            elif next_player in temp_mid:
                                temp_mid.pop(0)
                                num_midfielders += 1
                            elif next_player in temp_fwd:
                                temp_fwd.pop(0)
                                num_forwards += 1
                            if player[2] == "DEF":
                                num_defenders -= 1
                            elif player[2] == "MID":
                                num_midfielders -= 1
                            elif player[2] == "FWD":
                                num_forwards -= 1
                            break
                if player not in team:
                    break
                if player == team[-1]:
                    #no changes made to team, so need to remove next contenders
                    temp_def.pop(0)
                    temp_mid.pop(0)
                    temp_fwd.pop(0)
                    break

            #if player added plays in different position to player removed
            #will have too many of 1 position and not enough of another, so need to replace from bench
            # print("bench rn:",bench)
            if num_defenders > team_defenders:
                worst_player = max([player for player in bench if player[2] == "DEF"], key=lambda x: x[3])
                temp_bench = bench.copy()
                temp_bench.remove(worst_player)
                if num_midfielders < team_midfielders:
                    next_player = min(temp_mid, key=lambda x: x[3])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_mid.remove(next_player)
                        next_player = min(temp_mid, key=lambda x: x[3])
                    temp_mid.remove(next_player)
                    price += float(next_player[3])
                    price -= float(worst_player[3])
                    num_midfielders += 1
                    num_defenders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
                elif num_forwards < team_forwards:
                    next_player = max(temp_fwd, key=lambda x: x[-1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_fwd.remove(next_player)
                        next_player = max(temp_fwd, key=lambda x: x[-1])
                    temp_fwd.remove(next_player)
                    price += float(next_player[3])
                    price -= float(worst_player[3])
                    num_forwards += 1
                    num_defenders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
            elif num_midfielders > team_midfielders:
                worst_player = max([player for player in bench if player[2] == "MID"], key=lambda x: x[1])
                temp_bench = bench.copy()
                temp_bench.remove(worst_player)
                if num_defenders < team_defenders:
                    next_player = max(temp_def, key=lambda x: x[-1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_def.remove(next_player)
                        next_player = max(temp_def, key=lambda x: x[-1])
                    temp_def.remove(next_player)
                    price += float(next_player[3])
                    price -= float(worst_player[3])
                    num_defenders += 1
                    num_midfielders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
                elif num_forwards < team_forwards:
                    next_player = max(temp_fwd, key=lambda x: x[-1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_fwd.remove(next_player)
                        next_player = max(temp_fwd, key=lambda x: x[-1])
                    temp_fwd.remove(next_player)
                    price += float(next_player[3])
                    price -= float(worst_player[3])
                    num_forwards += 1
                    num_midfielders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
            elif num_forwards > team_forwards:
                worst_player = max([player for player in bench if player[2] == "FWD"], key=lambda x: x[3])
                temp_bench = bench.copy()
                temp_bench.remove(worst_player)
                if num_midfielders < team_midfielders:
                    next_player = max(temp_mid, key=lambda x: x[-1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_mid.remove(next_player)
                        next_player = max(temp_mid, key=lambda x: x[-1])
                    temp_mid.remove(next_player)
                    price += float(next_player[3])
                    price -= float(worst_player[3])
                    num_midfielders += 1
                    num_forwards -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
                elif num_defenders < team_defenders:
                    next_player = max(temp_def, key=lambda x: x[-1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_def.remove(next_player)
                        next_player = max(temp_def, key=lambda x: x[-1])
                    temp_def.remove(next_player)
                    price += float(next_player[3])
                    price -= float(worst_player[3])
                    num_defenders += 1
                    num_forwards -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
    
        # need to pick bench players that provide best points when starting 11 players didn't play
        min_defenders, min_midfielders, min_forwards = 3, 2, 1

        zero_mins = self.find_gameweeks_with_zero_mins(team)
        #sort by length of zero mins, so that we can replace players with most gameweeks missed
        zero_mins = sorted(zero_mins, key=lambda x: len(x), reverse=True)
        
        #put goalkeeper at the front of the list if in list
        gk_in_zero_mins = len([player for player in zero_mins if player[0] == "GKP" or player[0] == "GK"]) > 0
        if gk_in_zero_mins:
            # print("gk in zero mins:", zero_mins)
            for i in range(len(zero_mins)):
                if zero_mins[i][0] == "GKP" or zero_mins[i][0] == "GK":
                    zero_mins = [zero_mins[i]] + zero_mins[:i] + zero_mins[i+1:]
                    break
            zero_mins = zero_mins[:4]
            # print("gk in front of zero mins:", zero_mins)
        else:
            zero_mins = zero_mins[:3]
        zero_mins_copy = zero_mins.copy()
        # self.print_team(team)
        # print("price:", price)
        # print("zero mins:", zero_mins)
        #need to check if benches have players in the positions that can be used to alter starting lineup
        #formations = ["343", "352", "433", "442", "451", "523", "532", "541"]
        max_points_players = []
        foo = 0
        while zero_mins:
            foo += 1
            #looks for best replacements for players that didn't play in specific gameweeks
            if zero_mins[0][0] == "GKP" or zero_mins[0][0] == "GK":
                max_points_player = self.get_max_points_for_specific_gameweeks(temp_gkp + [player for player in bench if (player[2] == "GKP" or player[2] == "GK") and player not in max_points_players], zero_mins[0])
            elif zero_mins[0][0] == "DEF": 
                if self.get_formation(team) == "343":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + [player for player in bench if (player[2] == "DEF") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "352":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + [player for player in bench if (player[2] == "DEF") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "451":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "433":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_mid + [player for player in bench if (player[2] == "DEF" or player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "442":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_mid + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "523":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + [player for player in bench if (player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "532":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + temp_fwd + [player for player in bench if (player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "541":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + temp_fwd + [player for player in bench if (player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
            elif zero_mins[0][0] == "MID":
                if self.get_formation(team) == "343":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_mid + [player for player in bench if (player[2] == "DEF" or player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "352":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "451":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "433":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_mid + [player for player in bench if (player[2] == "DEF" or player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "442":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_mid + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "523":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + [player for player in bench if (player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "532":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + temp_fwd + [player for player in bench if (player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "541":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + temp_fwd + [player for player in bench if (player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
            elif zero_mins[0][0] == "FWD":
                if self.get_formation(team) == "343":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + temp_def + [player for player in bench if (player[2] == "DEF" or player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "352":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "451":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_fwd + [player for player in bench if (player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "433":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + temp_def + [player for player in bench if (player[2] == "DEF" or player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "442":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_def + temp_mid + temp_fwd + [player for player in bench if (player[2] == "DEF" or player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "523":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_mid + [player for player in bench if (player[2] == "MID") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "532":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_fwd + temp_mid + [player for player in bench if (player[2] == "MID" or player[2] == "FWD") and player not in max_points_players], zero_mins[0])
                elif self.get_formation(team) == "541":
                    max_points_player = self.get_max_points_for_specific_gameweeks(temp_fwd + [player for player in bench if (player[2] == "FWD") and player not in max_points_players], zero_mins[0])

            max_points_players.append(max_points_player)
            # print("zero_mins_player",zero_mins)
            # print("max_points_player:", max_points_player)
            # print("bench:",bench)
            #break
            # print("max_points_player:", max_points_player)
            # print("max_points_players:", max_points_players)
            # print("team:",team)
            # print("bench:",bench)        

            if max_points_player in temp_gkp:
                temp_gkp.remove(max_points_player)
            elif max_points_player in temp_def:
                temp_def.remove(max_points_player)
            elif max_points_player in temp_mid:
                temp_mid.remove(max_points_player)
            elif max_points_player in temp_fwd:
                temp_fwd.remove(max_points_player)

            #dont replace old max_point_players with new one
            try:
                bench_same_position = max([player for player in bench if player[2] == max_points_player[2] and player not in max_points_players], key=lambda x: x[3])
            except ValueError:
                # print("no bench same position")
                #if max_points_player has the same value as cheapest bench player of same position at this point, then no replacments possible for zero_mins_player
                if max_points_player[3] == min([player for player in bench if player[2] == max_points_player[2]], key=lambda x: x[3])[3]:
                    zero_mins.pop(0)
                continue

            if max_points_player in bench:
                if max_points_player[2] == "GKP" or max_points_player[2] == "GK":
                    bench = [max_points_player] + bench[1:]
                    # print("bench69:",bench)
                else:
                    # print("bench:",bench)
                    index = bench.index(max_points_player)
                    # print("index:",index)
                    length_players_from_max_points_players_in_bench = len([player for player in bench if player in max_points_players]) + 1
                    print("length_players_from_max_points_players_in_bench:",length_players_from_max_points_players_in_bench)
                    
                    bench.pop(index)
                    # print("bench2:",bench)
                    bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player] + bench[length_players_from_max_points_players_in_bench:]
                    # print("bench10:",bench)
                zero_mins_player = zero_mins.pop(0)

                #if player in team has the same number of points as max_points_player, but has more points
                #in the weeks where player didn't play, should be max_points_player, so swap them
                for bench_player in bench:
                    players_with_same_points = [player for player in team if player[-1] == bench_player[-1]]
                    if players_with_same_points:
                        max_points_player2 = self.get_max_points_for_specific_gameweeks(players_with_same_points + [bench_player], zero_mins_player)
                        if max_points_player2[-1] == bench_player[-1] and max_points_player2 in team:
                            temp_team = team.copy()
                            temp_team.remove(max_points_player2)
                            if self.valid_formations([bench_player] + temp_team):
                                max_points_players.remove(max_points_player)
                                team_player_index = team.index(max_points_player2)
                                bench_player_index = bench.index(bench_player)
                                #team[team_player_index], bench[bench_player_index] = bench[bench_player_index], team[team_player_index]
                                team[team_player_index] = bench[bench_player_index]
                                bench.pop(bench_player_index)
                                max_points_players.append(max_points_player2)
                                length_players_from_max_points_players_in_bench = len([player for player in bench if player in max_points_players]) + 1
                                # print("bench11 length_player:",length_players_from_max_points_players_in_bench)
                                bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player2] + bench[length_players_from_max_points_players_in_bench:]
                                # print("bench11:",bench)
                                # print("foo:",foo)
                                break
                continue
            #should check if max 3 per team works with just team if not team + bench, and if so change bench player
            temp_bench = bench.copy()
            temp_bench.remove(bench_same_position)

            # print(price - float(bench_same_position[3]) + float(max_points_player[3]) <= 100)
            # print(self.max_3_per_team([max_points_player] + team))
            # print(bench_same_position not in max_points_players)
            if price - float(bench_same_position[3]) + float(max_points_player[3]) <= 100 and self.max_3_per_team([max_points_player] + team) and bench_same_position not in max_points_players:
                length_players_from_max_points_players_in_bench = len([player for player in bench if player in max_points_players]) + 1
                if price - float(bench_same_position[3]) + float(max_points_player[3]) <= 100 and self.max_3_per_team([max_points_player] + team + temp_bench):
                    # print("bench32:",bench)
                    bench.remove(bench_same_position)
                    # print("bench22:",bench)
                    bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player] + bench[length_players_from_max_points_players_in_bench:]
                    # print("bench12:",bench)
                    price -= float(bench_same_position[3])
                    price += float(max_points_player[3])
                #if this branch is reached then subsequent if statement should always be true
                else:
                    same_team_bench = [player for player in bench if player[1] == max_points_player[1]]
                    if len(same_team_bench) > 0:
                        bench.remove(same_team_bench[0])
                        price -= float(same_team_bench[0][3])
                        if same_team_bench[0][2] == "GKP" or same_team_bench[0][2] == "GK":
                            while len([player for player in bench if player[2] == "GKP" or player[2] == "GK"]) == 0:
                                new_bench_player = min(temp_gkp, key=lambda x: x[3])
                                if self.max_3_per_team([new_bench_player] + team + bench) and temp_gkp[0][1] != max_points_player[1] and price + float(new_bench_player[3]) + float(max_points_player[3]) <= 100:
                                    bench = [new_bench_player] + bench
                                    # print("bench33:",bench)
                                    price += float(new_bench_player[3])
                                temp_gkp.remove(new_bench_player)
                        if same_team_bench[0][2] == "DEF":
                            num_defenders -= 1
                            while num_defenders < team_defenders:
                                new_bench_player = min(temp_def, key=lambda x: x[3])
                                if self.max_3_per_team([new_bench_player] + team + bench) and temp_def[0][1] != max_points_player[1] and price + float(new_bench_player[3]) + float(max_points_player[3]) <= 100:
                                    bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player] + bench[length_players_from_max_points_players_in_bench:]
                                    price += float(new_bench_player[3])
                                    num_defenders += 1
                                temp_def.remove(new_bench_player)
                        elif same_team_bench[0][2] == "MID":
                            num_midfielders -= 1
                            while num_midfielders < team_midfielders:
                                new_bench_player = min(temp_mid, key=lambda x: x[3])
                                if self.max_3_per_team([new_bench_player] + team + bench) and temp_mid[0][1] != max_points_player[1] and price + float(new_bench_player[3]) + float(max_points_player[3]) <= 100:
                                    bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player] + bench[length_players_from_max_points_players_in_bench:]
                                    price += float(new_bench_player[3])
                                    num_midfielders += 1
                                temp_mid.remove(new_bench_player)
                        elif same_team_bench[0][2] == "FWD":
                            num_forwards -= 1
                            while num_forwards < team_forwards:
                                new_bench_player = min(temp_fwd, key=lambda x: x[3])
                                if self.max_3_per_team([new_bench_player] + team + bench) and temp_fwd[0][1] != max_points_player[1] and price + float(new_bench_player[3]) + float(max_points_player[3]) <= 100:
                                    bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player] + bench[length_players_from_max_points_players_in_bench:]
                                    price += float(new_bench_player[3])
                                    num_forwards += 1
                                temp_fwd.remove(new_bench_player)
                if max_points_player not in bench:
                    if max_points_player[2] == "GKP" or max_points_player[2] == "GK":
                        bench = [max_points_player] + bench
                    else:
                        #put bench player that produces most points first so they are first to be subbed on
                        length_players_from_max_points_players_in_bench = len([player for player in bench if player in max_points_players]) + 1
                        bench = bench[:length_players_from_max_points_players_in_bench] + [max_points_player] + bench[length_players_from_max_points_players_in_bench:]
                zero_mins_player = zero_mins.pop(0)

            #if min number of players in a position in starting lineup, and all bench players of that position are max_points_players, then remove all players of that position from zero_mins
            if len([player for player in team if player[2] == "DEF"]) == min_defenders and len([player for player in team if player[2] == "DEF"]) + len([player for player in max_points_players if player[2] == "DEF"]) == max_defenders:
                zero_mins = [player for player in zero_mins if player[0] != "DEF"]
            if len([player for player in team if player[2] == "MID"]) == min_midfielders and len([player for player in team if player[2] == "MID"]) + len([player for player in max_points_players if player[2] == "MID"]) == max_midfielders:
                zero_mins = [player for player in zero_mins if player[0] != "MID"]
            if len([player for player in team if player[2] == "FWD"]) == min_forwards and len([player for player in team if player[2] == "FWD"]) + len([player for player in max_points_players if player[2] == "FWD"]) == max_forwards:
                zero_mins = [player for player in zero_mins if player[0] != "FWD"]
            
            
            # print("max_points_players end of func:",max_points_players)

        return self.sort_team_by_position(team) + bench, price
        

if __name__ == "__main__":
    years = ["2020-21","2021-22","2022-23"]
    years = ["2023-24","2024-25"]
    for year in years:
        builder = FantasyTeamBuilder(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\cleaned last 3 seasons data\cleaned_data_for_{year}_season.csv")
        builder.read_csv_data()
        builder.get_player_points()
        team, price = builder.get_best_team()
        builder.print_team(team)
        print("Price: ", price)
        print("---------------")
        df = pd.DataFrame(team)
        try:
            os.mkdir(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}")
        except FileExistsError:
            pass
        df.to_csv(fr"C:\Users\omung\OneDrive - University College London\UCL\Final Year Project\Python\data\{year}\team_{year}_no_transfers.csv", index=False)
    #print("Total points: ", builder.get_points_total(team, i))