#!/usr/bin/env python

import os
import pandas as pd

class PlayerMap:
    def __init__(self):
        self.DIR = 'fantasydata'
        self.PLAYER_FN = u'Player.2008-2013.csv'        
        self.FIELDS = ['PlayerID',
                       'Name',
                       'FirstName',
                       'LastName',
                       'Team']

        self.player_map_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                      self.DIR,
                                                      self.PLAYER_FN),
                                         index_col = False)
        self.player_map_df = self.player_map_df[self.FIELDS]

    def get_player_name(self, id):
        idx = (self.player_map_df['PlayerID'] == id)
        try:
            return self.player_map_df.ix[idx]['Name'].iloc[0]
        except IndexError:
            print "Cannot seem to find that PlayerID.  Please try again."

    def get_team_from_id(self, id):
        idx = (self.player_map_df['Team'])
        try:
            return self.player_map_df.ix[idx]['Team'].iloc[0]
        except IndexError:
            print "Cannot seem to find that PlayerID.  Please try again."

    def get_id_from_name(self, fn, ln, team):
        idx = ((self.player_map_df['FirstName'] == fn) &
               (self.player_map_df['LastName'] == ln) &
               (self.player_map_df['Team'] == team))
        try:
            return self.player_map_df.ix[idx]['PlayerID'].iloc[0]
        except IndexError:
            print "Cannot seem to find a player with that first and last name."

if __name__ == "__main__":
    pm = PlayerMap()
    pn = pm.get_player_name(4807)
    print pn
    pn = pm.get_player_name(23498234)
    pid = pm.get_id_from_name('Adrian', 'Peterson', 'MIN')
    print pid








