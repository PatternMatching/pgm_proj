# Want to play with Pandas discretization

import pandas as pd
import matplotlib.pyplot as plt
from numpy import np

GOOGLE_DRIVE_DIR = u'C:\\Users\\e18349\\Google Drive\\Fantasy Data\\'

PLAYER_GAME_2008_FN = u'PlayerGame.2008.csv'
PLAYER_GAME_2009_FN = u'PlayerGame.2009.csv'
PLAYER_GAME_2010_FN = u'PlayerGame.2010.csv'
PLAYER_GAME_2011_FN = u'PlayerGame.2011.csv'
PLAYER_GAME_2012_FN = u'PlayerGame.2012.csv'
PLAYER_GAME_2013_FN = u'PlayerGame.2013.csv'

# Get player-game data for the 2013 season
player_game_2013_df = pd.read_csv(GOOGLE_DRIVE_DIR + PLAYER_GAME_2013_FN, index_col = 89)

# Want to analyze starting runningbacks
rb_player_game_2013_df = player_game_2013_df[ (player_game_2013_df['Position'] == 'RB') & 
                                              (player_game_2013_df['Started'] == 'Y') ]

st_rb_fant_pts = rb_player_game_2013_df['FantasyPoints']
fp_desc = st_rb_fant_pts.describe()

# Freedman-Diaconis can be used to select size of bins in a histogram:
#   bin_size = 2 IQR(x) n^{-1/3}
q3 = fp_desc['75%']
q1 = fp_desc['25%']
iqr = q3 - q1
n = len(st_rb_fant_pts)
bin_size = 2*iqr*n**(-1.0/3.0)

# Plot histogram of the fantasy points using FD bin sizing
plt.figure()
num_bins = (max(st_rb_fant_pts)-min(st_rb_fant_pts))/bin_size + 1
bin_list = np.linspace(min(st_rb_fant_pts), max(st_rb_fant_pts), num_bins)
plt.hist(st_rb_fant_pts, bin_list)