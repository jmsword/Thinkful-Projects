import requests
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections


r = requests.get('http://www.citibikenyc.com/stations/json')

key_list = []
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)


#22 Stations 'Not In Service'
#Mean available bikes INCLUDING 'Not In Service' stations: 9.5
#Median available bikes INCLUDING 'Not In Service' stations: 7

#Mean available bikes EXCLUDING 'Not In Service' stations: 9.9
#Median available bikes EXCLUDING 'Not In Service' stations: 8

#Mean & Median both increase when we exclude 'Not In Service' stations.

df = json_normalize(r.json()['stationBeanList'])
#df2 = df[df.statusValue == 'In Service']

#print(df2['availableBikes'].mean())

con = lite.connect('citi_bike.db')
cur = con.cursor()

#Create reference table to store static information
with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#Reuseable SQL statement
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#For loop to populate the reference table created above with values
with con:
    for station in r.json()['stationBeanList']:
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#CREATE AVAILABLE BIKES TABLE

#Extract 'id' column from the DataFrame and put the values into a list
station_ids = df['id'].tolist()
#Add an '_' to the front of the id number and also add the data type INT for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

#create the 'available bikes' table
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

#LOOP GOES HERE

for i in range(60):
	r = requests.get('http://www.citibikenyc.com/stations/json')
	exec_time = parse(r.json()['executionTime'])
#change S to d at end of time string
	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%S'),))
	con.commit()

	#Create default dictionary to store available bikes by station
	id_bikes = collections.defaultdict(int)
	
	for station in r.json()['stationBeanList']:
		id_bikes[station['id']] = station['availableBikes']

	for k, v in id_bikes.items():
		cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%S') + ";")
	con.commit()

	time.sleep(60)

con.close()