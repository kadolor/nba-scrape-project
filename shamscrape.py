from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import csv
import unicodedata 
import pandas as pd
from pandas import DataFrame
import re
import wikipedia

"""
	This script scrapes nba statistics and payroll data and organizes that data into dataframes.
    Copyright (C) 2016  Kelly-Ann R. Dolor

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Salaries for '07-'09
"""

years_salary = ["2007","2008","2009"]

results_list_salary_0709 = []

for year in years_salary:
	html = urllib2.urlopen("http://data.shamsports.com/content/pages/data/salaries/"+year+"/index.jsp").read()
	soup = BeautifulSoup(html)

	salary_soup= soup.find_all(width="140")
	team_soup= soup.find_all(width="240")
	rank_soup= soup.find_all(width="20")


	salaries = [i.text for i in salary_soup]
	salaries = [x.encode('utf-8') for x in salaries]
	salaries = [x.replace("$","") for x in salaries]
	salaries = [x.replace(",","") for x in salaries]
	salaries = [x.replace(".","") for x in salaries]
	salaries = [int(x) for x in salaries]



	team = [i.text for i in team_soup]
	team = [i.encode('utf-8') for i in team]
	team = [str(i) for i in team]
	team = [i.strip('\n') for i in team]
	team = [i.replace('\r\n',"") for i in team]
	team = [i.replace('              ',"") for i in team]
	# print team
	rank = [i.text for i in rank_soup]
	rank = [i.encode('utf-8') for i in rank]
	# print rank

	team_rank_list = dict(zip(team,salaries))
	# print team_rank_list

	df = pd.DataFrame(team_rank_list.items())
	df.columns = ['Team', 'Salary']
	df.insert(1, 'Year',year)
	# df['Rank'] = df.groupby(['Year'])['Salary'].rank(ascending=False, method='max')
	results_list_salary_0709.append(df)

frame_salary_0709 = pd.concat(results_list_salary_0709)
frame_salary_0709 = frame_salary_0709.replace(to_replace="Seattle Superdupersonics",value="Seattle SuperSonics")	

frame_salary_0709.to_csv('salary_rank_0709.csv') #This prints the FULL salary DF for 2007-2009

years_salary_residual = []

results_list_salary_1015 = []

for i in range(2010,2016):
	x = str(i)
	years_salary_residual.append(x)


for year in years_salary_residual:
	html = urllib2.urlopen("http://data.shamsports.com/content/pages/data/salaries/"+year+"/index.jsp").read()
	# html = open("shamsports08.html")
	soup = BeautifulSoup(html)

	salary_soup= soup.find_all(width="130")
	team_soup= soup.find_all(width="190")
	rank_soup= soup.find_all(width="30")


	salaries = [i.text for i in salary_soup]
	salaries = [x.encode('utf-8') for x in salaries]
	salaries = [x.replace("$","") for x in salaries]
	salaries = [x.replace(",","") for x in salaries]
	salaries = [x.replace(".","") for x in salaries]
	salaries = [int(x) for x in salaries]

	team = [i.text for i in team_soup]
	team = [i.encode('utf-8') for i in team]
	team = [str(i) for i in team]
	team = [i.strip('\n') for i in team]
	team = [i.replace('\r\n',"") for i in team]
	team = [i.replace('              ',"") for i in team]
	del team[0]
	del team[30:]

	# print team
	rank = [i.text for i in rank_soup]
	rank = [i.encode('utf-8') for i in rank]
	del rank[:30]
	# print rank

	team_rank_list = dict(zip(team,salaries))
	# print team_rank_list

	df = pd.DataFrame(team_rank_list.items())
	df.columns = ['Team', 'Salary']
	df.insert(1, 'Year',year)
	results_list_salary_1015.append(df)

frame_salary_1015 = pd.concat(results_list_salary_1015,ignore_index=True) #This prints the salary rank DF for 2010-2015
frame_salary_1015.loc[87,'Team']='New Jersey Nets'
#frame_salary_1015['Rank'] = frame_salary_1015.groupby(['Year'])['Salary'].rank(ascending=False)


frame_salary_1015.to_csv('salary_rank_1015.csv')

completed_salary_df = frame_salary_0709.append(frame_salary_1015) # COMPLETED Salary DF 2007-2015
completed_salary_df.to_csv('salary_rank_0715.csv', index=True)
years_standings = []

results_list_standings = []

for i in range(2007,2016):
	x = str(i)
	years_standings.append(x)

for year in years_standings:
	html = urllib2.urlopen("http://www.basketball-reference.com/leagues/NBA_"+year+".html").read()
	soup = BeautifulSoup(html)

	team_standings_soup = soup.find_all('tr', {'class':"full_table"})
	team_standings_soup = [i.text for i in team_standings_soup]
	team_standings_soup = [i.encode('ascii', 'ignore') for i in team_standings_soup]
	team_standings_soup = [i.replace("\n",",") for i in team_standings_soup]
	team_standings_soup = [str(i) for i in team_standings_soup]
	team_standings_soup = [i.split(',') for i in team_standings_soup]

	df = pd.DataFrame(team_standings_soup)
	df = df.drop(df.columns[[5,6,7,8,9]], axis = 1)
	df.columns=['Rank','Team','Wins','Losses','Winning pct']
	df.insert(1,'Year',year)
	df['Team'] = df['Team'].str.replace('\(.*?\)','')
	df['Team'] = df['Team'].str.replace('*','')
	results_list_standings.append(df)

frame_standings = pd.concat(results_list_standings) # This prints the standings without conferences
frame_standings.to_csv('standings_rank.csv')

"""
This code below is used to add a column that designates which conference (Eastern or Western) a team belongs to 
"""
completed_salary_copy = completed_salary_df.copy()
team = []
conference = []

eastern = 'Eastern Conference'
western = 'Western Conference'

filtered_df_by_team = completed_salary_copy['Team']
filtered_df_by_team = filtered_df_by_team.drop_duplicates()
filtered_df_by_team = filtered_df_by_team.replace(to_replace="Minnesota \r\n        Timberwolves",value="Minnesota Timberwolves")

for i in filtered_df_by_team:
	x =  wikipedia.summary(i, sentences=3)
	if eastern in x:
		team.append(i)
		conference.append(eastern)
	elif western in x:
		team.append(i)
		conference.append(western)
	elif i == "Seattle SuperSonics":
		team.append(i)
		conference.append(western)	
	else:
		print i #prints what isnt classified as eastern or western


dictionary_of_team_conferences = zip(team,conference)

conference_list = pd.DataFrame(dictionary_of_team_conferences)
conference_list.columns = ['Team', 'Conference']
conference_list.to_csv('conference_list.csv')


"""
End of conference code
"""
standings_df_with_conferences = pd.merge(frame_standings,conference_list, on='Team',how='outer')
standings_df_with_conferences = standings_df_with_conferences.replace(to_replace="New Orleans/Oklahoma City Hornets",value="New Orleans Hornets")
standings_df_with_conferences.to_csv('standings_df_with_conferences.csv')

standings_and_salary_combined_dfs = pd.merge(standings_df_with_conferences,completed_salary_df, on=['Year','Team'], how='inner')
standings_and_salary_combined_dfs.to_csv('completed_salaries_and_standings.csv')

eastern_conference_master = standings_and_salary_combined_dfs[standings_and_salary_combined_dfs.Conference=='Eastern Conference']
eastern_conference_master['Salary Rank'] = eastern_conference_master.groupby(['Year'])['Salary'].rank(ascending=False)
eastern_conference_master['Conference Rank'] = eastern_conference_master.groupby(['Year'])['Winning pct'].rank(ascending=False)


eastern_conference_master.to_csv('eastern_conference_master.csv')

knicks_master = eastern_conference_master[eastern_conference_master.Team=='New York Knicks']
knicks_master.to_csv('knicks_master.csv')