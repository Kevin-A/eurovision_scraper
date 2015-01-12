#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib2,json
import sqlite3
import urllib2
import os
import time
import random
from pycountry import *

# Initialize database
conn = sqlite3.connect('data.sqlite')

# Returns the countries from the database
def grabCountries():
	query = 'SELECT DISTINCT(toParticipant) FROM votes'
	c = conn.cursor()
	c.execute(query)
	countries = c.fetchall()
	
	return [x[0] for x in countries];

# Due to the way names are written on the Eurovision pages (and thus stored in the database)
# some filtering has to be applied. This is also the place where some results are disposed of
# due to countries splitting or combining. I didn't feel like including those.
def getCode(country):
	""" Returns the code of a country """
	code = country.replace('&', 'and').replace('The Netherlands', 'Netherlands').replace('F.Y.R. Macedonia', 'Macedonia, Republic of').replace('Moldova', 'Moldova, Republic of').replace('Russia', 'Russian Federation')
	return pycountry.countries.get(name=code).alpha2


def convertToCode(data):
	newData = {}
	for obj in data:
		code = getCode(obj)
		
		newData[code] = {}
		
		# now the arrays
		for toP, points in data[obj]:
			newData[code][getCode(toP)] = points
		
	return newData

# The initializer
def main():

	# Grab countries from the database
	countries = grabCountries()
	
	data = {}
	
	# For each country, start calculating the point it gives to other countries
	for country in countries:
		data[country] = []
		query = 'SELECT toParticipant, SUM(points) as total, SUM(points)*1.0/COUNT(DISTINCT(year))AS average, COUNT(DISTINCT(year)) AS years \
				 FROM votes \
				 WHERE fromParticipant = ? \
				 GROUP BY toParticipant \
				 ORDER BY average' 
		c = conn.cursor()
		c.execute(query, [country])
		votes = c.fetchall()
		
		# Add votes
		for vote in votes:
			data[country].append([ vote[0], vote[2] ])

		# Add countries with 0 votes
		for country2 in countries: 
			found = False
			
			# Loop through all votes this country gave
			for vote in data[country]:

				# Check if this vote is equal to country2, that means we do not add it
				if vote[0] == country2:
					found = True
					break
			
			# country was not in the list, add it
			if found is False:
				data[country].append([country2, 0.0])

	# Store
	with open('blockvotes.json', 'wb') as fp:
		json.dump(data, fp)
	
	data = convertToCode(data)
	
	# Store
	with open('blockvotes_code.json', 'wb') as fp:
		json.dump(data, fp)	
		
	conn.close()
	return 0

# Starting point
if __name__ == '__main__':
	main()