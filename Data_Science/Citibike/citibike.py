import requests
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections
import datetime


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

con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
	station_vals=df[col].tolist()
	station_id = col[1:]
	station_change = 0
	for k,v in enumerate(station_vals):
		if k < len(station_vals) - 1:
			station_change += abs(station_vals[k] - station_vals[k+1])
		hour_change[int(station_id)] = station_change

def keywithmaxval(d):
	"""FInd the key with the greatest value"""
	return max(d, key=lambda k: d[k])

max_station = keywithmaxval(hour_change)

cur.execute("SELECT id, stationName, latitude, longitude FROM citibike_reference WHERE id = ?",(max_station,))
data=cur.fetchone()
print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
print("With %d bicycles coming and going in the hour between %s and %s" % (
    hour_change[max_station],
    datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
))

plt.bar(hour_change.keys(), hour_change.values())
plt.show()