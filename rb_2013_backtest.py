#!/usr/bin/env python

from __future__ import division

from player_map import PlayerMap
from dynamic_recarray import DynamicRecArray

import os
import pandas as pd
import numpy as np
import rb_bn

class RbBacktest:
    def __init__(self, year):
        self.year = year
        self.DIR = 'fantasydata'
        self.FN_PREFIX = 'PlayerGame.'
        self.FN_END = '.csv'
        self.filename = self.FN_PREFIX + str(self.year) + self.FN_END
        self.pg_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                              self.DIR,
                                              self.filename))

    def get_recs_for_player(self, id):
        idx = (self.pg_df['PlayerID'] == id)
        return self.pg_df.ix[idx]

    def get_tot_fp_for_player(self, id):
        idx = (self.pg_df['PlayerID'] == id)
        return np.sum(self.pg_df.ix[idx]['FantasyPoints'])

    def get_st_rb_recs_for_wk(self, wk_num):
        idx = ((self.pg_df['Week'] == wk_num) & 
               (self.pg_df['Position'] == 'RB') &
               (self.pg_df['Started'] == 'Y'))
        return self.pg_df.ix[idx]
        
if __name__ == "__main__":
    rb_bg = rb_bn.create_bbn()
    pm = PlayerMap()
    bktest = RbBacktest(2013)
    
    ids_in_network = rb_bg.domains['PlayerID']

    for wk_num in range(1, 17):
        recs = bktest.get_st_rb_recs_for_wk(wk_num)

        # Now we know who is starting and how they did
        # in a particular week

        p_fp_high_recs = DynamicRecArray([('name', 'a25'), 
                                          ('prob', 'f4')])

        for idx, rec in recs.iterrows():
            pid = rec['PlayerID']
            name = pm.get_player_name(pid)
            opp = rec['Opponent']
            h_or_a = rec['HomeOrAway']

            if str(pid) in ids_in_network:
                m = rb_bg.query(PlayerID = str(pid), 
                                Opponent = str(opp),
                                HomeOrAway = str(h_or_a))
                
                p_high_fp = m[('FantasyPoints', 'high')]
                p_fp_high_recs.append((name, p_high_fp))

            else:
                print name, "was not a runningback prior to 2013.  Cannot analyze."

        p_fp_high_recs.sort('prob', desc=True)

        print "In week", wk_num, "you should start", p_fp_high_rec_arr[0]['name']
        print "Opponent:", opp
        print "Home or Away:", h_or_a
        print "He has a", p_fp_high_rec_arr[0]['prob'], "probabilty of a high score"
