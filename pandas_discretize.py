# Want to play with Pandas discretization

from __future__ import division

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools as it

def conv_ps(x):
    if x == 'Natural Grass':
        return 'NaturalGrass'
    else:
        return x

def get_all_playergames():
    DATA_DIR = 'fantasydata'

    PLAYER_GAME_2008_FN = u'PlayerGame.2008.csv'
    PLAYER_GAME_2009_FN = u'PlayerGame.2009.csv'
    PLAYER_GAME_2010_FN = u'PlayerGame.2010.csv'
    PLAYER_GAME_2011_FN = u'PlayerGame.2011.csv'
    PLAYER_GAME_2012_FN = u'PlayerGame.2012.csv'
    PLAYER_GAME_2013_FN = u'PlayerGame.2013.csv'

    print 'About to read in all of the CSV\'s....'
    
    player_game_2008_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                   DATA_DIR,
                                                   PLAYER_GAME_2008_FN),
                                      index_col = False,
                                      converters = {'PlayingSurface':conv_ps})
    player_game_2009_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                   DATA_DIR,
                                                   PLAYER_GAME_2009_FN),
                                      index_col = False,
                                      converters = {'PlayingSurface':conv_ps})
    player_game_2010_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                   DATA_DIR,
                                                   PLAYER_GAME_2010_FN),
                                      index_col = False,
                                      converters = {'PlayingSurface':conv_ps})
    player_game_2011_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                   DATA_DIR,
                                                   PLAYER_GAME_2011_FN),
                                      index_col = False,
                                      converters = {'PlayingSurface':conv_ps})
    player_game_2012_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                   DATA_DIR,
                                                   PLAYER_GAME_2012_FN),
                                      index_col = False,
                                      converters = {'PlayingSurface':conv_ps})
    
    # Concatenate all annual dataframes
    player_game_df = pd.concat([player_game_2008_df,
                                player_game_2009_df,
                                player_game_2010_df,
                                player_game_2011_df,
                                player_game_2012_df])

    return player_game_df

def get_cond_prob(field_val_dict, parent_vals_dict, data):
    target_field = field_val_dict.keys()[0]
    target_val = field_val_dict[target_field]

    parent_fields = parent_vals_dict.keys()
    parent_vals = parent_vals_dict.values()

    ss = []
    target_ss = (data[target_field] == target_val)

    num_df = pd.DataFrame(target_ss)
    den_df = pd.DataFrame()

    for idx, field in enumerate(parent_fields):
        par_idx = pd.DataFrame(data[field] == parent_vals[idx])
        num_df = pd.concat([num_df, par_idx], axis=1, ignore_index=True)
        den_df = pd.concat([den_df, par_idx], axis=1, ignore_index=True)

    num_idx = num_df.all(axis=1)
    den_idx = den_df.all(axis=1)

    if len(data[den_idx]) == 0:
        return 0
    else:
        return len(data[num_idx])/len(data[den_idx])

def get_bif_prob_entry(field, parent_dict, data):
    if parent_dict.has_key(field):
        # This is a conditional probability
        to_return = ("probability ( " + 
                     field + 
                     " | " + 
                     parent_dict[field] + 
                     " ) {\n")
        # Want cartesian product of values by field
        field_vals = data[field].unique()
        parents = parent_dict[field].split(", ")
        parent_val_set = [data[x].dropna().unique() for x in parents]
        parent_vals = it.product(*parent_val_set)
        for this_val_set in parent_vals:
            parent_vals_dict = dict(zip(parents, this_val_set))
            probs = []
            for f_val in field_vals:
                field_val_dict = {field : f_val}
                probs.append(get_cond_prob(field_val_dict, parent_vals_dict, data))
            to_return += ("  (" + 
                          ', '.join([str(x) for x in this_val_set]) +
                          ") " +
                          ', '.join([str(x) for x in probs]) + ";\n")
        to_return += "}\n"
    else:
        to_return = "probability ( " + field + " ) {\n  table "
        # Just get the unconditional prior probability
        probs = []
        for val in data[field].unique():
            idx = (data[field] == val)
            probs.append(len(data.ix[idx])/len(data))
        
        to_return += ', '.join([str(x) for x in probs]) + ";\n}\n"

    return to_return


##### Main Execution #####

if __name__ == "__main__":
    pg_df = get_all_playergames()

    emp_ps_idx = (pg_df['PlayingSurface'] == '')
    pg_df.loc[emp_ps_idx, 'PlayingSurface'] = 'Grass'

    # Want to isolate starting runningbacks
    st_rb_idx = (pg_df['Position'] == 'RB') & (pg_df['Started'] == 'Y')
    st_rb_pg_df = pg_df.ix[st_rb_idx]

    # Let's pare the data down to a few desired fields
    rb_fields = ['PlayerID',
                 'Name',
                 'HomeOrAway',
                 'Opponent',
                 'PlayingSurface',
                 'RushingYards',
                 'ReceivingYards',
                 'OffensiveTouchdowns',
                 'FantasyPoints']

    st_rb_pg_df = st_rb_pg_df[rb_fields]

    # Have some continuous inputs - want to discretize by quantiles
    # and replace with discretization label
    rushing_yds = st_rb_pg_df['RushingYards']
    rush_yds_disc = pd.qcut(rushing_yds, 3, labels = ['low','normal','high'])

    receiving_yds = st_rb_pg_df['ReceivingYards']
    rec_yds_disc = pd.qcut(receiving_yds, 3, labels = ['low','normal','high'])

    fp = st_rb_pg_df['FantasyPoints']
    fp_disc = pd.qcut(fp, 3, labels = ['low','normal','high'])
    
    # Now want to replace continuous data with discretized
    st_rb_pg_df['RushingYards'] = rush_yds_disc
    st_rb_pg_df['ReceivingYards'] = rec_yds_disc
    st_rb_pg_df['FantasyPoints'] = fp_disc

    # Want to calculate the probability that FP == 'High' given that
    # RB was playing AWAY
    #num_idx = (st_rb_pg_df['FantasyPoints'] == 'high') & (st_rb_pg_df['HomeOrAway'] == 'AWAY')
    #den_idx = (st_rb_pg_df['HomeOrAway'] == 'AWAY')
    #p_fp_high_away = len(st_rb_pg_df.ix[num_idx])/len(st_rb_pg_df.ix[den_idx])
    #print 'Prob(FP == \'High\' | HomeOrAway == \'AWAY\') =', p_fp_high_away

    #num_idx = (st_rb_pg_df['FantasyPoints'] == 'high') & (st_rb_pg_df['HomeOrAway'] == 'HOME')
    #den_idx = (st_rb_pg_df['HomeOrAway'] == 'HOME')
    #p_fp_high_away = len(st_rb_pg_df.ix[num_idx])/len(st_rb_pg_df.ix[den_idx])
    #print 'Prob(FP == \'High\' | HomeOrAway == \'HOME\') =', p_fp_high_away

    #num_idx = (st_rb_pg_df['FantasyPoints'] == 'high') & (st_rb_pg_df['PlayingSurface'] == 'Dome')
    #den_idx = (st_rb_pg_df['PlayingSurface'] == 'Dome')
    #p_fp_high_away = len(st_rb_pg_df.ix[num_idx])/len(st_rb_pg_df.ix[den_idx])
    #print 'Prob(FP == \'High\' | PlayingSurface == \'Dome\') =', p_fp_high_away

    # Now, would like to create a .bif file to represent the Bayesian Network that we'd
    # like to use to answer questions about which runningback to start
    RB_BIF_FN = 'rb.bif'

    f = open(RB_BIF_FN, 'w')
    f.truncate()

    f.write("network unknown {\n}\n")

    # Node range declarations
    
    for field in rb_fields:
        if field != 'Name':
            vals = [str(x) for x in pd.unique(st_rb_pg_df[field])]
            f.write("variable " + 
                    field + 
                    " {\n  type discrete [ " +
                    str(len(vals)) +
                    " ] { " +
                    ', '.join(vals) +
                    " };\n}\n")

    # CPT declarations
    
    # First will denote which of the fields have parents (and who the parents are)
    parent_dict = { "RushingYards" : "PlayerID, Opponent, HomeOrAway, PlayingSurface",
                    "ReceivingYards" : "PlayerID, Opponent, HomeOrAway, PlayingSurface",
                    "OffensiveTouchdowns" : "PlayerID, Opponent, HomeOrAway, PlayingSurface",
                    "FantasyPoints" : "RushingYards, ReceivingYards, OffensiveTouchdowns" }

    for field in rb_fields:
        if field != 'Name':
            f.write(get_bif_prob_entry(field, parent_dict, st_rb_pg_df))

    f.close()
