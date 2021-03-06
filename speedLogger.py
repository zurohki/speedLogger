#!/usr/bin/python

import os
import time
import datetime
import csv
import sys
import ConfigParser


# speedTest() will perform an actual speed test via speedtest-cli
def speedTest():
	log('Running speed test...')
	results = os.popen(path + "speedtest-cli --simple").read().rstrip('\n').split('\n')
	log('Speed test results: ' + results[0] + ', ' + results[1] + ', ' + results[2])
	return results

# Sent 100 pings to pingTarget. You probably want to put your ISP in here.
def pingTest():
	log('Running packet loss test...')
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

def waitForLoop():
	global lastLoopStart
	global loopDelay
	runTime = float(time.time() - lastLoopStart)
	log('Testing took ' + str(int(runTime)) + ' seconds. Waiting ' + str(int(float(loopDelay) - runTime)) + ' more seconds for the next run. Press CTRL + C to quit.')
	try:
		while float(time.time() - lastLoopStart) < float(loopDelay):
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		sys.exit()
	return

def loadconfig():
	config = ConfigParser.RawConfigParser()
	config.read('speedLogger.conf')
	global path
	global destServer
	global pingTarget
	global verboseLogging
	global uploadToServer
	global doLoops
	global loopDelay
	path = config.get('speedLogger', 'scriptPath')
	destServer = config.get('speedLogger', 'destServer')
	pingTarget = config.get('speedLogger', 'pingTarget')
	verboseLogging = config.get('speedLogger', 'verboseLogging')
	uploadToServer = config.get('speedLogger', 'uploadToServer')
	doLoops = config.get('speedLogger', 'doLoops')
	loopDelay = config.get('speedLogger', 'loopDelayInSeconds')
	return


path = ''
destServer = ''
pingTarget = ''
verboseLogging = ''
uploadToServer = ''
doLoops = ''
loopDelay = ''
loadconfig()

while True:
	log('Starting at: ' + os.popen('date').read().rstrip('\n'))
	lastLoopStart = time.time()
	results = speedTest()
	loss = pingTest()
	results = processResults(results)
	outputToFile(results, loss)
	plot()
	if uploadToServer:
		upload()
	log('Finished at: ' + os.popen('date').read().rstrip('\n'))
	if doLoops:
		waitForLoop()
	else:
		break
