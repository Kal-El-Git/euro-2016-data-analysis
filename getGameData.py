import urllib,json
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import sys 

# country data from github 
response = urllib.urlopen('https://raw.githubusercontent.com/Kal-El-Git/FootballData/master/openFootballData/countries.json')
countryJsonObj = json.loads(response.read())

# a dictionary for conutries
country_list = ["France","Germany","Belgium", "Wales", "Poland","Portugal","Iceland","Italy"]
country_dict ={}
for country in countryJsonObj:
	if country['name'] in country_list:
		cid = country['id']
		country_dict[cid]=country['name']
print country_dict

# games data from github 
game_response = urllib.urlopen('https://raw.githubusercontent.com/Kal-El-Git/FootballData/master/openFootballData/games.json')
game_text = json.loads(game_response.read())


# extract games only played by targeted countries
"""
games_by_countries = []
for game in game_text:
	if game['team1']['country_id'] in country_dict or game['team2']['country_id'] in country_dict:
		games_by_countries.append(game)
"""


# for a specific country, total games played and total winning 
"""
country_id = 127 # Germany:109 Portugla: 120, Poland: 127 
wins = 0
plays =0
for game in game_text:
	if game['team1']['country_id']==country_id or game['team2']['country_id']==country_id:
		plays+=1
	if ( game['team1']['country_id']==country_id and game['winner']==1 ) or (game['team2']['country_id']==country_id and game['winner']==2):
		wins+=1
print "plays: ",plays
print "wins: ", wins 
"""

# compare two teams' statistic in a histogram
team1 = sys.argv[1]
team2 = sys.argv[2]
cid1,cid2=0,0

for cid in country_dict:
	if country_dict[cid].lower()== team1.lower():
 		cid1 = cid
	if country_dict[cid].lower()==team2.lower():
		cid2= cid

 

wins_1 = 0
plays_1 =0
for game in game_text:
	if game['team1']['country_id']==cid1 or game['team2']['country_id']==cid1:
		plays_1+=1
	if ( game['team1']['country_id']==cid1 and game['winner']==1 ) or (game['team2']['country_id']==cid1 and game['winner']==2):
		wins_1+=1

wins_2 = 0
plays_2 =0
for game in game_text:
	if game['team1']['country_id']==cid2 or game['team2']['country_id']==cid2:
		plays_2+=1
	if ( game['team1']['country_id']==cid2 and game['winner']==1 ) or (game['team2']['country_id']==cid2 and game['winner']==2):
		wins_2+=1
# plot 
x= np.arange(2)
games= [plays_1,plays_2]
wins=[wins_1,wins_2]

fig, ax =plt.subplots()
rects1 = plt.bar(x,games,color='g')
rects2 = plt.bar(x,wins,color='b')

ax.set_ylabel("Games")
ax.legend((rects1[0],rects2[0]),('Games',"Win"))
plt.title("Statistics of two teams")
plt.xlabel("Team")

print "Team1", "games: ",games[0],"wins: ", wins[0],"winning rate:", wins[0]/float(games[0])
print "Team2", "games: ",games[1],"wins: ", wins[1],"winning rate:",wins[1]/float(games[1])

plt.show() 


"""
# for games played two countries in history 
cid1 = 127 #poland
cid2 = 120 #portugal

# poland and portugal' last game was in 2012, a draw
team1_win =0
total_games =0
for game in games_by_countries:
	if ( game['team1']['id']==cid1 and game['team2']['id']==cid2 ) or ( game['team1']['id']== cid2 and game['team2']['id']==cid1):
		total_games +=1	
	if (game['team1']['id']==cid1 and game['winner']==1 ) or ( game['team2']['id']== cid1 and game['winner']==2 ):
		team1_win+=1

print "played: ", total_games, "   poland wins: ", team1_win
"""		


"""
#
# Regression of Winning on scores and scores by the opponent
# 

# Collect wins and scores
wins = []
scores1 =[]
scores2 =[]
for game in game_text:
	if game['winner']==1:
		wins.append(1.0)
	elif game['winner']==2:
		wins.append(0.0)
	else:
		wins.append(0.5)
	if game['score1']:
		scores1.append(game['score1'])
	else:
		scores1.append(0)
	if game['score2']:
		scores2.append(game['score2'])
	else:
		scores2.append(0)
wins = np.array(wins)

# use score difference 
scores1 = np.array(scores1)
scores2 = np.array(scores2)
score_diff = scores1-scores2


# store into a dataframe
data= { 'wins':wins, 'score_diff': score_diff}
column_names = ['wins','score_diff']

df = pd.DataFrame(data,columns=column_names)

log = sm.Logit(df['wins'],df['score_diff'])
result = log.fit()

print result.summary()
"""
