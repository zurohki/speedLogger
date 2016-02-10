#!/usr/bin/python

import os
import time
import datetime
import csv
import sys
import ConfigParser


# speedTest() will perform an actual speed test via speedtest-cli
def speedTest():
	results = os.popen(path + "speedtest-cli --simple").read().rstrip('\n').split('\n')
	log('SpeedTest Results: ' + str(results))
	return results

# Sent 100 pings to pingTarget. You probably want to put your ISP in here.
def pingTest():
	loss = os.popen("ping -c 300 -i 0.5 " + pingTarget + " | egrep -o [0-9]+%\ packet\ loss | cut -d\  -f1").read().rstrip('\n')
	log('Packet Loss: ' + loss)
	return loss

def processResults(results):
	# Get the numbers from the results. Splitting means we don't get trailing spaces.
	ping = results[0].split()[1]
	down = results[1].split()[1]
	up = results[2].split()[1]
	# Now grab a timestamp to throw on the beginning of output
	timestamp = str(time.time())
	log('Timestamp: ' + timestamp)
	log('Ping: ' + ping)
	log('Down: ' + down)
	log('Up: ' + up)
	return timestamp + '\t' + ping + '\t' + down + '\t' + up

# Append this run to the data.dat file.
def outputToFile(results, loss):
	outputFile = open(path + 'data.dat', 'a')
	outputFile.write(results + '\t' + loss)
	log('Output: ' + results + '\t' + loss)
	outputFile.write('\n')
	outputFile.close()
	return

# Draw the graph.
def plot():
	log('Plotting...')
	os.system('cd ' + path + ' && gnuplot plot.gp')
	return

# Upload the resulting SVG to your web server or copy it somewhere. Entirely optional.
def upload():
	log('Uploading...')
	os.system('scp speedLogger.svg gnuplot_svg.js speedLogger.html ' + destServer)
	return

def log(logtext):
	# Change this to a 0 if you don't want the script spamming the console.
	if verboseLogging:
		print logtext
	return

def loadconfig():
	config = ConfigParser.RawConfigParser()
	config.read('speedLogger.conf')
	global path
	global destServer
	global pingTarget
	global verboseLogging
	global uploadToServer
	path = config.get('speedLogger', 'scriptPath')
	destServer = config.get('speedLogger', 'destServer')
	pingTarget = config.get('speedLogger', 'pingTarget')
	verboseLogging = config.get('speedLogger', 'verboseLogging')
	uploadToServer = config.get('speedLogger', 'uploadToServer')
	return


path = ''
destServer = ''
pingTarget = ''
verboseLogging = ''
uploadToServer = ''
loadconfig()

log('Starting at: ' + os.popen('date').read().rstrip('\n'))
results = speedTest()
loss = pingTest()
results = processResults(results)
outputToFile(results, loss)
plot()
if uploadToServer:
	upload()
log('Finished at: ' + os.popen('date').read().rstrip('\n'))
