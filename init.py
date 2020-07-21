#%%
import json
import numpy as np
from itertools import combinations
from pprint import pprint as pp
from datetime import datetime, timedelta 
def create_balanced_round_robin(players):
    """ Create a schedule for the players in the list and return it"""
    s = []
    if len(players) % 2 == 1: players = players + [None]
    # manipulate map (array of indexes for list) instead of list itself
    # this takes advantage of even/odd indexes to determine home vs. away
    n = len(players)
    map = list(range(n))
    mid = n // 2
    for i in range(n-1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        round = []
        for j in range(mid):
            t1 = players[l1[j]]
            t2 = players[l2[j]]
            if j == 0 and i % 2 == 1:
                # flip the first match only, every other round
                # (this is because the first match always involves the last player in the list)
                round.append((t2, t1))
            else:
                round.append((t1, t2))
        s.append(round)
        # rotate list by n/2, leaving last element at the end
        map = map[mid:-1] + map[:mid] + map[-1:]
    return [match for matches in s for match in matches if all(match)]
    
class Tournement(object):
    
    def __init__(self, tournament_name):
        self.tournament_name = tournament_name
        self.config = self.get_config()
        self.teams = self.config['teams']
        self.no_teams = len(self.config['teams'])
        self.no_pools = len(self.config['pool_sizes'])
        self.no_fields = self.config['no_fields']
        self.pool_sizes = self.config['pool_sizes']
        self.game_duration = self.config['game_duration']
        self.pause = self.config['pause']
        self.no_matches = self.config['no_matches']
        self.pools =  self.get_pools()
        self.start_tournament = self.get_start_time()
        

    def get_config(self):    
        with open('./tournements/'+self.tournament_name+'.json') as config:
             return json.load(config)

    def create_schedule(self):
        self.get_games()
        self.divide_games()
        pass
    
    def get_start_time(self):
        h, m = self.config["start_tournament"].split(':')
        return timedelta(minutes=int(m), hours=int(h))

    
    def get_pools(self):
        teams = np.arange(0,self.no_teams,1)
        # np.random.shuffle(teams)
       
        pools = []
        tmp = 0
        for idx in np.cumsum(self.pool_sizes):
            pool = [self.teams[i] for i in list(teams[tmp:idx])]
            pools.append(pool)
            tmp = idx
    	
        return pools
    
    def get_games(self):
        self.games = []
        for pool in self.pools:
            self.games.append(create_balanced_round_robin(pool))
        
        self.all_games =[]
        for i in range(max([len(pool_games) for pool_games in self.games])):
            for j in range(self.no_pools):
                try:
                    self.all_games.append(self.games[j][i])
                except IndexError:
                    pass
                
    def divide_games(self):
        self.fields = [[] for _ in range(self.no_fields)]
        for i, game in enumerate(self.all_games):
            # print(game, i, self.no_fields)
            field = i % self.no_fields
            self.fields[field].append(game)
    
    def get_times(self):
        self.round_times = ([str(self.start_tournament + i * timedelta(minutes=15)) for i in range(len(self.match_rounds))])

    def get_time_schedule(self):
        self.get_times()
        for time, match_round in zip(self.round_times,self.match_rounds):
            print(time,match_round)
        pass

    def get_match_rounds(self):
        self.match_rounds = []
        for i in range(max([len(games) for games in self.fields])):
            match_round = []
            for j in range(self.no_fields):
                try:
                    match_round.append(self.fields[j][i])
                except IndexError:
                    # self.match_rounds.append(match_round)
                    continue
            self.match_rounds.append(match_round)
    
    def print_schedule(self):
        self.get_time_schedule()
        
if __name__ == "__main__":
    t = Tournement("config4")
    t.create_schedule()
    t.get_match_rounds()
    t.print_schedule()
    t.get_times()
    
    # print(create_balanced_round_robin(['a1','a2','a3','a4']))
    pass

# %%
