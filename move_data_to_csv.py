import csv
import os

NUM_TESTS = 6

for i in range(NUM_TESTS):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'tests\\gameweek_tests', f'test_data{i+1}.csv')
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PLAYER", "TEAM", "POSITION", "PRICE", "POINTS 1"])
        if i == 0:
            gkp_player_points1 = [["ARSGKP1", "ARS", "GKP", 4.0, 5],["LIVGKP1", "LIV", "GKP", 4.0, 6]]
            def_player_points1 = [["NFODEF1", "NFO", "DEF", 4.0, 12],["EVEDEF2", "EVE", "DEF", 4.0, 0],["BOUDEF3", "BOU", "DEF", 4.0, 6],["WHUDEF1", "WHU", "DEF", 4.0, 5],["WOLDEF2", "WOL", "DEF", 4.0, 5]]
            mid_player_points1 = [["ARSMID1", "ARS", "MID", 4.0, 0],["LIVMID2", "LIV", "MID", 4.0, 8],["BHAMID3", "BHA", "MID", 4.0, 6],["CHEMID2", "CHE", "MID", 4.0, 0],["LUTMID3", "LUT", "MID", 4.0, 5]]
            fwd_player_points1 = [["MCIFWD1", "MCI", "FWD", 4.0, 10],["NEWFWD2", "NEW", "FWD", 4.0, 12],["LUTFWD3", "LUT", "FWD", 4.0, 15]]
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)
        elif i == 1:
            gkp_player_points1 = [["ARSGKP1", "ARS", "GKP", 4.0, 5],["LIVGKP1", "LIV", "GKP", 4.0, 6]]
            def_player_points1 = [["NFODEF1", "LIV", "GKP", 8.0, 12],["EVEDEF2", "LIV", "GKP", 4.0, 0],["BOUDEF3", "LIV", "GKP", 6.0, 6],["WHUDEF1", "LIV", "GKP", 5.0, 5],["WOLDEF2", "LIV", "GKP", 4.0, 5]]
            mid_player_points1 = [["ARSMID1", "LIV", "GKP", 10.0, 0],["LIVMID2", "LIV", "GKP", 10.0, 8],["BHAMID3", "LIV", "GKP", 7.0, 6],["CHEMID2", "LIV", "GKP", 6.0, 0],["LUTMID3", "LIV", "GKP", 5.0, 5],["MCIMID3", "LIV", "GKP", 4.0, 4]]
            fwd_player_points1 = [["MCIFWD1", "LIV", "GKP", 4.0, 10],["NEWFWD2", "LIV", "GKP", 4.0, 12],["LUTFWD3", "LIV", "GKP", 20.0, 15]]
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)
        elif i == 2:
            gkp_player_points1 = [["ARSGKP1", "LIV", "GKP", 4.0, 5],["LIVGKP1", "LIV", "GKP", 4.0, 6]]
            def_player_points1 = [["NFODEF1", "LIV", "GKP", 8.0, 12],["EVEDEF2", "LIV", "GKP", 4.0, 0],["BOUDEF3", "LIV", "GKP", 6.0, 6],["WHUDEF1", "LIV", "GKP", 5.0, 5],["WOLDEF2", "LIV", "GKP", 4.0, 5],["WOLDEF2", "LIV", "GKP", 4.0, 0]]
            mid_player_points1 = [["ARSMID1", "LIV", "GKP", 10.0, 10],["LIVMID2", "LIV", "GKP", 10.0, 8],["BHAMID3", "LIV", "GKP", 7.0, 6],["CHEMID2", "LIV", "GKP", 6.0, 0],["LUTMID3", "LIV", "GKP", 5.0, 5],["MCIMID3", "LIV", "GKP", 4.0, 4]]
            fwd_player_points1 = [["MCIFWD1", "LIV", "GKP", 4.0, 10],["NEWFWD2", "LIV", "GKP", 4.0, 12],["LUTFWD3", "LIV", "GKP", 20.0, 15]]
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)
        elif i == 3:
            gkp_player_points1 = [["ARSGKP1", "LIV", "GKP", 4.0, 5],["LIVGKP1", "LIV", "GKP", 4.0, 6]] #8
            def_player_points1 = [["NFODEF1", "LIV", "GKP", 8.0, 12],["EVEDEF2", "LIV", "GKP", 4.0, 0],["BOUDEF3", "LIV", "GKP", 6.0, 6],["WHUDEF1", "LIV", "GKP", 5.0, 5],["WOLDEF2", "LIV", "GKP", 4.0, 0],["BREDEF2", "LIV", "GKP", 4.0, 0],["BURDEF2", "LIV", "GKP", 4.0, 0]] #27
            mid_player_points1 = [["ARSMID1", "LIV", "GKP", 10.0, 10],["LIVMID2", "LIV", "GKP", 10.0, 8],["BHAMID3", "LIV", "GKP", 7.0, 6],["CHEMID2", "LIV", "GKP", 6.0, 6],["LUTMID3", "LIV", "GKP", 4.0, 5],["MCIMID3", "LIV", "GKP", 4.5, 0],["BURMID5", "LIV", "GKP", 4.0, 0]] #41.5
            fwd_player_points1 = [["MCIFWD1", "LIV", "GKP", 4.0, 10],["NEWFWD2", "LIV", "GKP", 5.0, 12],["LUTFWD3", "LIV", "GKP", 20.0, 15],["BREFWD2", "LIV", "GKP", 4.0, 0]] #29
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)
        elif i == 4:
            gkp_player_points1 = [["ARSGKP1", "LIV", "GKP", 4.0, 5],["LIVGKP1", "LIV", "GKP", 4.0, 6]] #8
            def_player_points1 = [["NFODEF1", "LIV", "GKP", 8.0, 12],["EVEDEF2", "LIV", "GKP", 4.0, 0],["BOUDEF3", "LIV", "GKP", 6.0, 6],["WHUDEF1", "LIV", "GKP", 5.0, 5],["WOLDEF2", "LIV", "GKP", 4.0, 0],["BREDEF2", "LIV", "GKP", 4.0, 0],["BURDEF2", "LIV", "GKP", 4.0, 0]] #27
            mid_player_points1 = [["LUTMID1", "LIV", "GKP", 10.0, 10],["LIVMID2", "LIV", "GKP", 10.0, 8],["BHAMID3", "LIV", "GKP", 7.0, 6],["CHEMID2", "LIV", "GKP", 6.0, 6],["LUTMID3", "LIV", "GKP", 4.5, 5],["LUTMID2", "LIV", "GKP", 4.0, 4],["BURMID5", "LIV", "GKP", 4.5, 0]] #41.5
            fwd_player_points1 = [["MCIFWD1", "LIV", "GKP", 4.0, 10],["NEWFWD2", "LIV", "GKP", 5.0, 12],["LUTFWD3", "LIV", "GKP", 20.0, 15],["BREFWD2", "LIV", "GKP", 4.0, 0]] #29
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)
        elif i == 5:
            gkp_player_points1 = [["ARSGKP1", "LIV", "GKP", 4.0, 5],["LIVGKP1", "LIV", "GKP", 4.0, 6]] #8
            def_player_points1 = [["NFODEF1", "LIV", "GKP", 11.7, 32],["EVEDEF2", "LIV", "GKP", 4.0, 0],["BOUDEF3", "LIV", "GKP", 7.7, 10],["WHUDEF1", "LIV", "GKP", 7.7, 12],["WOLDEF2", "LIV", "GKP", 4.0, 0],["BREDEF2", "LIV", "GKP", 7.7, 0],["BURDEF2", "LIV", "GKP", 7.7, 0],["CHEDEF2", "LIV", "GKP", 7.7, 0],["EVEDEF2", "LIV", "GKP", 7.7, 0]] #27
            mid_player_points1 = [["LUTMID1", "LIV", "GKP", 7.7, 10],["LIVMID2", "LIV", "GKP", 7.7, 12],["BHAMID3", "LIV", "GKP", 7.7, 10],["CHEMID2", "LIV", "GKP", 7.7, 11],["LUTMID3", "LIV", "GKP", 6.0, 5],["NFOMID2", "LIV", "GKP", 7.7, 4],["BURMID5", "LIV", "GKP", 4.0, 0],["CHEMID5", "LIV", "GKP", 7.7, 0],["EVEMID5", "LIV", "GKP", 7.7, 0]] #41.5
            fwd_player_points1 = [["MCIFWD1", "LIV", "GKP", 7.7, 7],["NEWFWD2", "LIV", "GKP", 7.7, 7],["LUTFWD3", "LIV", "GKP", 7.7, 7],["BREFWD2", "LIV", "GKP", 4.0, 0]] #29
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)                  

NUM_NO_TRANSFERS_TESTS = 2

for i in range(NUM_NO_TRANSFERS_TESTS):
    csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/no_transfers_tests', f'test_data{i+1}.csv')
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PLAYER", "TEAM", "POSITION", "PRICE", "MINUTES 1", "POINTS 1", "MINUTES 2", "POINTS 2"])
        if i == 0:
            gkp_player_points1 = [["ARSGKP1", "ARS", "GKP", 4.0, 0, 0, 90, 6],["LIVGKP1", "LIV", "GKP", 4.0, 90, 6, 90, 6]]
            def_player_points1 = [["NFODEF1", "NFO", "DEF", 4.0, 90, 12, 90, 2],["EVEDEF2", "EVE", "DEF", 4.0, 0, 0, 0, 0],["BOUDEF3", "BOU", "DEF", 4.0, 90, 6, 90, 6],["WHUDEF1", "WHU", "DEF", 4.0, 90, 5, 90, 6],["WOLDEF2", "WOL", "DEF", 4.0, 60, 5, 60, 4], ["NFODEF2", "WOL", "DEF", 4.0, 60, 0, 60, 0], ["BREDEF2", "BRE", "DEF", 4.0, 90, 0, 90, 0], ["BURDEF2", "BUR", "DEF", 4.0, 90, 0, 90, 0], ["CHEDEF2", "CHE", "DEF", 4.0, 90, 0, 90, 0], ["EVEDEF2", "EVE", "DEF", 4.0, 90, 0, 90, 0]]
            mid_player_points1 = [["ARSMID1", "ARS", "MID", 4.0, 0, 0, 90, 10],["LIVMID2", "LIV", "MID", 4.0, 90, 8, 60, 4],["BHAMID3", "BHA", "MID", 4.0, 90, 6, 90, 2],["CHEMID2", "CHE", "MID", 4.0, 0, 0, 0, 0],["LUTMID3", "LUT", "MID", 4.0, 60, 5, 90, 2], ["LUTMID2", "LUT", "MID", 4.0, 90, 4, 90, 4], ["BURMID5", "BUR", "MID", 4.0, 0, 0, 0, 0], ["CHEMID5", "CHE", "MID", 4.0, 0, 0, 0, 0], ["EVEMID5", "EVE", "MID", 4.0, 0, 0, 0, 0]]
            fwd_player_points1 = [["MCIFWD1", "MCI", "FWD", 4.0, 90, 10, 60, 6],["NEWFWD2", "NEW", "FWD", 4.0, 60, 12, 90, 7],["LUTFWD3", "LUT", "FWD", 4.0, 90, 15, 90, 12]]
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)

        elif i == 1:
            gkp_player_points1 = [["ARSGKP1", "ARS", "GKP", 4.0, 0, 0, 90, 6],["LIVGKP1", "LIV", "GKP", 4.0, 90, 6, 90, 6]]
            def_player_points1 = [["NFODEF1", "NFO", "DEF", 4.0, 90, 12, 90, 2],["EVEDEF2", "EVE", "DEF", 4.0, 0, 0, 0, 0],["BOUDEF3", "BOU", "DEF", 4.0, 90, 6, 90, 6],["WHUDEF1", "WHU", "DEF", 4.0, 90, 5, 90, 6],["WOLDEF2", "WOL", "DEF", 4.0, 60, 5, 60, 4], ["NFODEF2", "WOL", "DEF", 4.0, 60, 0, 60, 0], ["BREDEF2", "BRE", "DEF", 4.0, 90, 0, 90, 0], ["BURDEF2", "BUR", "DEF", 4.0, 90, 0, 90, 0], ["CHEDEF2", "CHE", "DEF", 4.0, 90, 0, 90, 0], ["EVEDEF2", "EVE", "DEF", 4.0, 90, 0, 90, 0]]
            mid_player_points1 = [["ARSMID1", "ARS", "MID", 4.0, 0, 0, 90, 10],["LIVMID2", "LIV", "MID", 4.0, 0, 0, 60, 12],["BHAMID3", "BHA", "MID", 4.0, 90, 6, 90, 2],["CHEMID2", "CHE", "MID", 4.0, 0, 0, 0, 0],["LUTMID3", "LUT", "MID", 4.0, 60, 5, 90, 2], ["LUTMID2", "LUT", "MID", 4.0, 90, 4, 90, 4], ["BURMID5", "BUR", "MID", 4.0, 0, 0, 0, 0], ["CHEMID5", "CHE", "MID", 4.0, 0, 0, 0, 0], ["EVEMID5", "EVE", "MID", 4.0, 0, 0, 0, 0]]
            fwd_player_points1 = [["MCIFWD1", "MCI", "FWD", 4.0, 90, 10, 60, 6],["NEWFWD2", "NEW", "FWD", 4.0, 60, 12, 90, 7],["LUTFWD3", "LUT", "FWD", 4.0, 90, 15, 90, 12]]
            for player in gkp_player_points1:
                writer.writerow(player)
            for player in def_player_points1:
                writer.writerow(player)
            for player in mid_player_points1:
                writer.writerow(player)
            for player in fwd_player_points1:
                writer.writerow(player)








