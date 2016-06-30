import json
import numpy as np
import sys


# team name as argument
team_name = sys.argv[1]

# open a file for each team
f = open(team_name+'-players.json')
# load into a json object
json_obj = json.loads(f.read())

# parse json object, extract information

ages = []
num_player = 0
goals =0
# special player
special_num =0

# a dict that keeps track of numbers of players on different positions. G-Goal Keeper, F-Forward, M-Middlefield, D-Defender 
positions = {'G':0,'F':0,'M':0,'D':0}

# average caps(national games) 
avg_caps = 0.0 

for player in json_obj['sheets']['Players']:
	dob_year = float(player['date of birth'][-4:])
	age = 2016 - dob_year
	ages.append(age)
	goals+=int(player['goals for country'])
	if len(player['special player? (eg. key player, promising talent, etc)'])>0:
		special_num+=1
	avg_caps+= int(player['caps'])
	# dict key is the first char in 'position'
	positions[player['position'][0]]+=1
avg_age=np.mean(ages)
avg_caps= avg_caps/len(ages)

#Historically, perfect age in the World Cup is 27.5
age_diff = abs(avg_age-27.5)
print
print "TEAM INfO of "+team_name.capitalize()

print "age difference to peak performance: ", age_diff 
print "age max: ", max(ages), "age min: ",min(ages)
print "total goals: ", goals
print "special player number: ", special_num
print "average caps: ",avg_caps,'\n'

print "position distribution:\n", positions
