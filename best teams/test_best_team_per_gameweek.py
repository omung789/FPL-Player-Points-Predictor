from best_team_per_gameweek import FantasyTeamBuilder
import unittest
import os
import subprocess

subprocess.run(["python", "move_data_to_csv.py"])

#PLAYER,TEAM,POSITION,PRICE,FIXTURE 1,GOALS 1,ASSISTS 1,MINUTES 1,GOALS CONCEDED 1,BONUS 1,CLEAN SHEETS 1,YELLOW 1,RED 1,POINTS 1

class TestBestTeamPerGameweek(unittest.TestCase):
    def test_basic_best_team1(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/gameweek_tests', 'test_data1.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        self.assertEqual(team[:11], [["LIVGKP1", 4.0, 6],["NFODEF1", 4.0, 12],["BOUDEF3", 4.0, 6],["WHUDEF1", 4.0, 5],["WOLDEF2", 4.0, 5],["LIVMID2", 4.0, 8],["BHAMID3", 4.0, 6],["LUTMID3", 4.0, 5],["LUTFWD3", 4.0, 15],["NEWFWD2", 4.0, 12],["MCIFWD1", 4.0, 10]])

    def test_basic_best_team2(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/gameweek_tests', 'test_data2.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        self.assertEqual(team, [["LIVGKP1", 4.0, 6],["NFODEF1", 8.0, 12],["BOUDEF3", 6.0, 6],["WHUDEF1", 5.0, 5],["WOLDEF2", 4.0, 5],["LIVMID2", 10.0, 8],["BHAMID3", 7.0, 6],["LUTMID3", 5.0, 5],["LUTFWD3", 20.0, 15],["NEWFWD2", 4.0, 12],["MCIFWD1", 4.0, 10], ['ARSGKP1', 4.0, 5], ['EVEDEF2', 4.0, 0], ['MCIMID3', 4.0, 4], ['CHEMID2', 6.0, 0]])
    
    #need to replace a player with a cheaper one after 15 selected due to price being > 100
    def test_basic_best_team3(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/gameweek_tests', 'test_data3.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        self.assertEqual(team, [["LIVGKP1", 4.0, 6],["NFODEF1", 8.0, 12],["BOUDEF3", 6.0, 6],["WHUDEF1", 5.0, 5],["WOLDEF2", 4.0, 5],["ARSMID1", 10.0, 10],["LIVMID2", 10.0, 8],["BHAMID3", 7.0, 6],["LUTFWD3", 20.0, 15],["NEWFWD2", 4.0, 12],["MCIFWD1", 4.0, 10], ['ARSGKP1', 4.0, 5], ['EVEDEF2', 4.0, 0], ['MCIMID3', 4.0, 4], ['LUTMID3', 5.0, 5]])
    
    #next best player on bench, should be moved to starting lineup
    def test_basic_best_team4(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/gameweek_tests', 'test_data4.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        self.assertEqual(team.sort(), [['LIVGKP1', 4.0, 6], ['NFODEF1', 8.0, 12], ['BOUDEF3', 6.0, 6], ['WHUDEF1', 5.0, 5], ['ARSMID1', 10.0, 10], ['LIVMID2', 10.0, 8], ['CHEMID2', 6.0, 6], ['LUTMID3', 4.0, 5], ['LUTFWD3', 20.0, 15], ['NEWFWD2', 
5.0, 12], ['MCIFWD1', 4.0, 10], ['ARSGKP1', 4.0, 5], ['WOLDEF2', 4.0, 0], ['BREDEF2', 4.0, 0], ['BURMID5', 4.0, 0]].sort())
        
    #next best player is in team that has 3 players already, with one of them being a bench player, should be moved to starting lineup and bench player removed
    def test_basic_best_team5(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/gameweek_tests', 'test_data5.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        self.assertEqual(team.sort(), [['LIVGKP1', 4.0, 6], ['NFODEF1', 8.0, 12], ['BOUDEF3', 6.0, 6], ['WHUDEF1', 5.0, 5], ['LUTMID1', 10.0, 10], ['LIVMID2', 10.0, 8], ['CHEMID2', 6.0, 6], ['LUTMID3', 4.5, 5], ['LUTFWD3', 20.0, 15], ['NEWFWD2', 5.0, 12], ['MCIFWD1', 4.0, 10], ['ARSGKP1', 4.0, 5], ['WOLDEF2', 4.0, 0], ['BREDEF2', 4.0, 0], ['BURMID5', 4.5, 0]].sort())

    #next best player would require formation change
    def test_basic_best_team6(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'tests/gameweek_tests', 'test_data6.csv')
        builder = FantasyTeamBuilder(csv_file_path)

        builder.read_csv_data()
        builder.get_player_points()

        team, price = builder.get_best_team()
        self.assertEqual(team, [['LIVGKP1', 4.0, 6], ['BOUDEF3', 7.7, 10], ['WHUDEF1', 7.7, 12], ['NFODEF1', 11.7, 32], ['LUTMID1', 7.7, 10], ['BHAMID3', 7.7, 10], ['CHEMID2', 7.7, 11], ['LIVMID2', 7.7, 12], ['LUTMID3', 6.0, 5], ['NEWFWD2', 7.7, 7], ['LUTFWD3', 7.7, 7], ['ARSGKP1', 4.0, 5], ['EVEDEF2', 4.0, 0], ['WOLDEF2', 4.0, 0], ['BREFWD2', 4.0, 0]])


if __name__ == '__main__':
    unittest.main()