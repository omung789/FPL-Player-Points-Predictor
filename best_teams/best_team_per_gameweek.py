import csv

class FantasyTeamBuilder:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.new_data = []
        self.points_indexes = []
        self.gkp_player_points = []
        self.def_player_points = []
        self.mid_player_points = []
        self.fwd_player_points = []

    def read_csv_data(self):
        with open(self.csv_file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            self.new_data = [row for row in csv_reader]

            for i, header in enumerate(headers):
                if "POINTS" in header:
                    self.points_indexes.append(i)

    def get_player_points(self):
        for row in self.new_data:
            if "GKP" in row[0]:
                self.gkp_player_points.extend([[row[0], float(row[3])] + ([int(row[i]) for i in self.points_indexes])])
            elif "DEF" in row[0]:
                self.def_player_points.extend([[row[0], float(row[3])] + ([int(row[i]) for i in self.points_indexes])])
            elif "MID" in row[0]:
                self.mid_player_points.extend([[row[0], float(row[3])] + ([int(row[i]) for i in self.points_indexes])])
            elif "FWD" in row[0]:
                self.fwd_player_points.extend([[row[0], float(row[3])] + ([int(row[i]) for i in self.points_indexes])])

    #sort a list of lists by a specific index
    def sort_points_by_gameweek(self, temp_gkp, temp_def, temp_mid, temp_fwd, gameweek):
        temp_gkp.sort(key=lambda x: x[gameweek + 1], reverse=True)
        temp_def.sort(key=lambda x: x[gameweek + 1], reverse=True)
        temp_mid.sort(key=lambda x: x[gameweek + 1], reverse=True)
        temp_fwd.sort(key=lambda x: x[gameweek + 1], reverse=True)

    def sort_points_by_gameweek_low_to_high(self, temp_def, temp_mid, temp_fwd, gameweek):
        #self.gkp_player_points.sort(key=lambda x: x[gameweek + 1])
        temp_def.sort(key=lambda x: x[gameweek + 1])
        temp_mid.sort(key=lambda x: x[gameweek + 1])
        temp_fwd.sort(key=lambda x: x[gameweek + 1])

    #sorts players by price (lowest to highest)
    def sort_players_by_price(self, temp_gkp, temp_def, temp_mid, temp_fwd):
        temp_gkp.sort(key=lambda x: float(x[1]))
        temp_def.sort(key=lambda x: float(x[1]))
        temp_mid.sort(key=lambda x: float(x[1]))
        temp_fwd.sort(key=lambda x: float(x[1]))

    def max_3_per_team(self, players):
        team_count = {}
        for player in players:
            if player[0][:3] in team_count:
                team_count[player[0][:3]] += 1
            else:
                team_count[player[0][:3]] = 1
        return max(team_count.values()) <= 3
    
    def valid_formations(self, team):
        positions = {"DEF": 0, "MID": 0, "FWD": 0} 
        for player in team:
            if player[0][3:6] == "DEF":
                positions["DEF"] += 1
            elif player[0][3:6] == "MID":
                positions["MID"] += 1
            elif player[0][3:6] == "FWD":
                positions["FWD"] += 1

        formations = ["343", "352", "433", "442", "451", "523", "532", "541"]
        if str(positions["DEF"]) +  str(positions["MID"]) + str(positions["FWD"]) in formations:
            return True
        return False
    
    def sort_team_by_position(self, team):
        gkp = [player for player in team if "GKP" in player[0]]
        defenders = [player for player in team if "DEF" in player[0]]
        midfielders = [player for player in team if "MID" in player[0]]
        forwards = [player for player in team if "FWD" in player[0]]
        return gkp + defenders + midfielders + forwards
    
    def get_best_team(self, gameweek=1):
        temp_gkp = self.gkp_player_points.copy()
        temp_def = self.def_player_points.copy()
        temp_mid = self.mid_player_points.copy()
        temp_fwd = self.fwd_player_points.copy()

        self.sort_points_by_gameweek(temp_gkp, temp_def, temp_mid, temp_fwd, gameweek)

        price = 0.0
        team = []
        max_defenders, max_midfielders, max_forwards = 5, 5, 3
        #min_goalkeepers, min_defenders, min_midfielders, min_forwards = 1, 3, 2, 1
        max_players = 11
        num_defenders, num_midfielders, num_forwards = 0, 0, 0

        while len(team) < max_players - 1 : # -1 because we will add a goalkeeper after
            next_players = []
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
            next_player = max(next_players, key=lambda x: x[2])
            team.append(next_player)
            price += float(next_player[1])

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
            if len([player for player in team if "DEF" in player[0]]) == 5:
                worst_player = min(team, key=lambda x: x[gameweek + 1])
                next_player = max(temp_def + temp_mid, key=lambda x: x[gameweek + 1])
                if "DEF" in next_player[0]:
                    temp_def.remove(next_player)
                else:
                    temp_mid.remove(next_player)
                team.remove(worst_player)
                team.append(next_player)
            else:
                worst_player = min([player for player in team if "MID" or "FWD" in player[0]], key=lambda x: x[gameweek + 1])
                next_player = max(temp_def, key=lambda x: x[gameweek + 1])
                temp_def.remove(next_player)
                team.remove(worst_player)
                team.append(next_player)
            price -= float(worst_player[1])
            price += float(next_player[1])

        team = self.sort_team_by_position(team)
        
        team, price = self.add_goalkeeper(team, temp_gkp, price)

        team_defenders, team_midfielders, team_forwards = 5, 5, 3
        #need to add bench players, ensuring that price is <= 100
        self.sort_players_by_price(temp_gkp, temp_def, temp_mid, temp_fwd)
        bench = []
        
        while num_defenders < team_defenders:
            if self.max_3_per_team([temp_def[0]] + team + bench):
                bench.append(temp_def[0])
                price += float(temp_def[0][1])
                num_defenders += 1
            temp_def.pop(0)
        while num_midfielders < team_midfielders:
            if self.max_3_per_team([temp_mid[0]] + team + bench):
                bench.append(temp_mid[0])
                price += float(temp_mid[0][1])
                num_midfielders += 1
            temp_mid.pop(0)
        while num_forwards < team_forwards:
            if self.max_3_per_team([temp_fwd[0]] + team + bench):
                bench.append(temp_fwd[0])
                price += float(temp_fwd[0][1])
                num_forwards += 1
            temp_fwd.pop(0)
        while self.max_3_per_team([temp_gkp[0]] + team) == False:
            temp_gkp.pop(0)
        bench, price = self.add_goalkeeper(bench, temp_gkp, price)

        while price > 100:
            team = self.sort_team_by_position(team)
            #we have cheapest bench possible, so need to reduce price of starting 11
            defenders = [player for player in team if "DEF" in player[0]]
            midfielders = [player for player in team if "MID" in player[0]]
            forwards = [player for player in team if "FWD" in player[0]]

            self.sort_points_by_gameweek_low_to_high(defenders, midfielders, forwards, gameweek)

            #find the next player with best points to put into team
            bench_defenders = [player for player in bench if "DEF" in player[0]]
            bench_midfielders = [player for player in bench if "MID" in player[0]]
            bench_forwards = [player for player in bench if "FWD" in player[0]]

            #check if bench players can be next best fit for team, if so put them in contention for next player
            if len(bench_defenders) > 0:
                next_player = max(bench_defenders, key=lambda x: x[gameweek + 1])
                temp_def.append(next_player)
            
            if len(bench_midfielders) > 0:
                next_player = max(bench_midfielders, key=lambda x: x[gameweek + 1])
                temp_mid.append(next_player)

            if len(bench_forwards) > 0:
                next_player = max(bench_forwards, key=lambda x: x[gameweek + 1])
                temp_fwd.append(next_player)

            self.sort_points_by_gameweek(temp_gkp, temp_def, temp_mid, temp_fwd, gameweek)
            
            next_players = [temp_mid[0]] + [temp_mid[0]] + [temp_fwd[0]]

            players_removed_from_team = []

            next_players.sort(key=lambda x: x[gameweek + 1], reverse=True)
            team.sort(key=lambda x: x[gameweek + 1])
            for player in team:
                temp_team = team.copy()
                temp_team.remove(player)
                for i in range(0, len(next_players)):
                    next_player = next_players[i]
                    if player[0][3:6] != "GKP":
                        if float(next_player[1]) < float(player[1]) and self.max_3_per_team([next_player] + temp_team) and self.valid_formations([next_player] + temp_team):
                            team.remove(player)
                            players_removed_from_team.append(player)
                            team.append(next_player)
                            price -= float(player[1])
                            price += float(next_player[1])
                            if next_player in bench:
                                bench.remove(next_player)
                                price -= float(next_player[1])
                                if next_player[0][3:6] == "DEF":
                                    num_defenders -= 1
                                    while num_defenders < team_defenders:
                                        new_bench_player = min(temp_def, key=lambda x: x[1])
                                        if self.max_3_per_team([new_bench_player] + team + bench) and temp_def[0][0][:3] != next_player[0][:3]:
                                            bench.append(new_bench_player)
                                            price += float(new_bench_player[1])
                                            num_defenders += 1
                                        temp_def.remove(new_bench_player)
                                elif next_player[0][3:6] == "MID":
                                    num_midfielders -= 1
                                    while num_midfielders < team_midfielders:
                                        new_bench_player = min(temp_mid, key=lambda x: x[1])
                                        if self.max_3_per_team([new_bench_player] + team + bench) and temp_mid[0][0][:3] != next_player[0][:3]:
                                            bench.append(new_bench_player)
                                            price += float(new_bench_player[1])
                                            num_midfielders += 1
                                        temp_mid.remove(new_bench_player)
                                elif next_player[0][3:6] == "FWD":
                                    num_forwards -= 1
                                    while num_forwards < team_forwards:
                                        new_bench_player = min(temp_fwd, key=lambda x: x[1])
                                        if self.max_3_per_team([new_bench_player] + team + bench) and temp_fwd[0][0][:3] != next_player[0][:3]:
                                            bench.append(new_bench_player)
                                            price += float(new_bench_player[1])
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
                            if player[0][3:6] == "DEF":
                                num_defenders -= 1
                            elif player[0][3:6] == "MID":
                                num_midfielders -= 1
                            elif player[0][3:6] == "FWD":
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
            if num_defenders > team_defenders:
                worst_player = max([player for player in bench if "DEF" in player[0]], key=lambda x: x[1])
                temp_bench = bench.copy()
                temp_bench.remove(worst_player)
                if num_midfielders < team_midfielders:
                    next_player = min(temp_mid, key=lambda x: x[1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_mid.remove(next_player)
                        next_player = min(temp_mid, key=lambda x: x[1])
                    temp_mid.remove(next_player)
                    price += float(next_player[1])
                    price -= float(worst_player[1])
                    num_midfielders += 1
                    num_defenders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
                elif num_forwards < team_forwards:
                    next_player = max(temp_fwd, key=lambda x: x[gameweek + 1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_fwd.remove(next_player)
                        next_player = max(temp_fwd, key=lambda x: x[gameweek + 1])
                    temp_fwd.remove(next_player)
                    price += float(next_player[1])
                    price -= float(worst_player[1])
                    num_forwards += 1
                    num_defenders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
            elif num_midfielders > team_midfielders:
                worst_player = max([player for player in bench if "MID" in player[0]], key=lambda x: x[1])
                temp_bench = bench.copy()
                temp_bench.remove(worst_player)
                if num_defenders < team_defenders:
                    next_player = max(temp_def, key=lambda x: x[gameweek + 1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_def.remove(next_player)
                        next_player = max(temp_def, key=lambda x: x[gameweek + 1])
                    temp_def.remove(next_player)
                    price += float(next_player[1])
                    price -= float(worst_player[1])
                    num_defenders += 1
                    num_midfielders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
                elif num_forwards < team_forwards:
                    next_player = max(temp_fwd, key=lambda x: x[gameweek + 1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_fwd.remove(next_player)
                        next_player = max(temp_fwd, key=lambda x: x[gameweek + 1])
                    temp_fwd.remove(next_player)
                    price += float(next_player[1])
                    price -= float(worst_player[1])
                    num_forwards += 1
                    num_midfielders -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
            elif num_forwards > team_forwards:
                worst_player = max([player for player in bench if "FWD" in player[0]], key=lambda x: x[1])
                temp_bench = bench.copy()
                temp_bench.remove(worst_player)
                if num_midfielders < team_midfielders:
                    next_player = max(temp_mid, key=lambda x: x[gameweek + 1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_mid.remove(next_player)
                        next_player = max(temp_mid, key=lambda x: x[gameweek + 1])
                    temp_mid.remove(next_player)
                    price += float(next_player[1])
                    price -= float(worst_player[1])
                    num_midfielders += 1
                    num_forwards -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)
                elif num_defenders < team_defenders:
                    next_player = max(temp_def, key=lambda x: x[gameweek + 1])
                    while self.max_3_per_team([next_player] + team + temp_bench) == False:
                        temp_def.remove(next_player)
                        next_player = max(temp_def, key=lambda x: x[gameweek + 1])
                    temp_def.remove(next_player)
                    price += float(next_player[1])
                    price -= float(worst_player[1])
                    num_defenders += 1
                    num_forwards -= 1
                    bench.remove(worst_player)
                    bench.append(next_player)

        team = self.sort_team_by_position(team)
        return team + bench, price
    
    def print_team(self, team, gameweek):
        print("-------------------")
        print("Gameweek", gameweek+1)
        for player in team:
            print(player[0], player[1], player[gameweek+2])

    def add_goalkeeper(self, team, temp_gkp, price):
        index = 0
        while (len(team) < 11):
            if self.max_3_per_team([temp_gkp[index]] + team):
                team = [temp_gkp[index]] + team
                price += float(temp_gkp[index][1])
                temp_gkp.pop(index)
                break
            index += 1
        return team, price
    
    def get_points_total(self, team, gameweek):
        total = 0
        for player in team[:11]:
            total += player[gameweek + 2]
        return total
    
if __name__ == "__main__":
    gameweeks = 38
    for i in range(0, gameweeks):
        builder = FantasyTeamBuilder("fake_gameweek_data1.csv")
        builder.read_csv_data()
        builder.get_player_points()
        team, price = builder.get_best_team(i+1)
        builder.print_team(team, i)
        print("Price: ", price)
        print("Total points: ", builder.get_points_total(team, i))