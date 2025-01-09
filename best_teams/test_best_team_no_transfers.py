from best_team_no_transfers import FantasyTeamBuilder
import unittest
import os
import subprocess

subprocess.run(["python", "move_data_to_csv.py"])

#PLAYER,TEAM,POSITION,PRICE,FIXTURE 1,GOALS 1,ASSISTS 1,MINUTES 1,GOALS CONCEDED 1,BONUS 1,CLEAN SHEETS 1,YELLOW 1,RED 1,POINTS 1

class TestBestTeamPerGameweek(unittest.TestCase):
    def test_basic_best_team1(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), '../tests/no_transfers_tests', 'test_data1.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        print("team in test file",team)
        self.assertEqual(team, [['LIVGKP1', 'LIV', 'GKP', 4.0, 90, 6, 90, 6, 12], ['NFODEF1', 'NFO', 'DEF', 4.0, 90, 12, 90, 2, 14], ['BOUDEF3', 'BOU', 'DEF', 4.0, 90, 6, 90, 6, 12], ['WHUDEF1', 'WHU', 'DEF', 4.0, 90, 5, 90, 6, 11], ['WOLDEF2', 'WOL', 'DEF', 4.0, 60, 5, 60, 4, 9], ['LIVMID2', 'LIV', 'MID', 4.0, 90, 8, 60, 4, 12], ['ARSMID1', 'ARS', 'MID', 4.0, 0, 0, 90, 10, 10], ['LUTMID2', 'LUT', 'MID', 4.0, 90, 4, 90, 4, 8], ['LUTFWD3', 'LUT', 'FWD', 4.0, 90, 15, 90, 12, 27], ['NEWFWD2', 'NEW', 'FWD', 4.0, 60, 12, 90, 7, 19], ['MCIFWD1', 'MCI', 'FWD', 4.0, 90, 10, 60, 6, 16], ['ARSGKP1', 'ARS', 'GKP', 4.0, 0, 0, 90, 6, 6], ['BHAMID3', 'BHA', 'MID', 4.0, 90, 6, 90, 2, 8], ['LUTMID3', 'LUT', 'MID', 4.0, 60, 5, 90, 2, 7], ['EVEDEF2', 'EVE', 'DEF', 4.0, 0, 0, 0, 0, 0]])
    
    def test_basic_best_team2(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), '../tests/no_transfers_tests', 'test_data2.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        print("test2 ------------------------------------")
        team, price = builder.get_best_team()
        print(team)
        #LUTMID2 and BHAMID3 have the same points, but BHAMID3 has more points when ARSMID1 didnt play, so should be first on bench and LUTMID2 should be in the team
        self.assertEqual(team, [['LIVGKP1', 'LIV', 'GKP', 4.0, 90, 6, 90, 6, 12], ['NFODEF1', 'NFO', 'DEF', 4.0, 90, 12, 90, 2, 14], ['BOUDEF3', 'BOU', 'DEF', 4.0, 90, 6, 90, 6, 12], ['WHUDEF1', 'WHU', 'DEF', 4.0, 90, 5, 90, 6, 11], ['WOLDEF2', 'WOL', 'DEF', 4.0, 60, 5, 60, 4, 9], ['LIVMID2', 'LIV', 'MID', 4.0, 0, 0, 60, 12, 12], ['ARSMID1', 'ARS', 'MID', 4.0, 0, 0, 90, 10, 10], ['LUTMID2', 'LUT', 'MID', 4.0, 90, 4, 90, 4, 8], ['LUTFWD3', 'LUT', 'FWD', 4.0, 90, 15, 90, 12, 27], ['NEWFWD2', 'NEW', 'FWD', 4.0, 60, 12, 90, 7, 19], ['MCIFWD1', 'MCI', 'FWD', 4.0, 90, 10, 60, 6, 16], ['ARSGKP1', 'ARS', 'GKP', 4.0, 0, 0, 90, 6, 6], ['BHAMID3', 'BHA', 'MID', 4.0, 90, 6, 90, 2, 8], ['LUTMID3', 'LUT', 'MID', 4.0, 60, 5, 90, 2, 7], ['EVEDEF2', 'EVE', 'DEF', 4.0, 0, 0, 0, 0, 0]])

if __name__ == '__main__':
    unittest.main()