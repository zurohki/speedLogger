#!/usr/bin/gnuplot
# Gnuplot script file for plotting data in file "data.dat"
# This file is called plot.gp
#################################

set terminal svg mouse jsdir "." size 1600,900 enhanced
set output "speedLogger.svg"

# the following is to eliminate a transparent background on SVG output terminal (best left alone, but you can change the #DCDCDC for another colour if you like)
set object 1 rect from screen 0, 0, 0 to screen 1, 1, 0 behind
set object 1 rect fc  rgb "#DCDCDC"  fillstyle solid 1.0

# sets all parms (best left alone)
set xdata time
set timefmt '%s'
set format x '%d-%b-%y | %H:%M'
set xtics rotate by 45 right

set title 'speedLogger throughput/network-congestion plot.'
set xlabel 'date and time'
set ylabel 'Speed (Mbps)'
set y2label 'Packet Loss (%)'

# The below Y range should be set to end on your upper-limit for your connection plus a bit more to fit in the legend up the top right without the plot overlapping it.
set yrange [0:30]
set y2range [0:30]

# replaces the small notches on both the x and y axis with horizontal gridlines up and across the graph
set tic scale 0
set grid ytics
set grid xtics

set ytics 5 nomirror tc lt 1
set y2tics 5 nomirror tc lt 2

## now plot the thing (best left alone EXCEPT for the timezone adjustment -see last comment in this block of comments (starts with "NOTE: ")
# <PLOT: Description>
# 1st line plots: DOWN: line
# 2nd line plots: DOWN: boxes
# 3rd line plots: UP: line
# 4th line plots: UP: boxes
# 5th line plots: ping: line
# 6th line plots: ping: boxes
# 7-12 lines add values
# 13th line plots: LEGEND: DOWN
# 14th line plots: LEGEND: UP
# 15th line plots: LEGEND: LOSS
# NOTE: "11*60*60" is an offset (in seconds) for GMT+10 timezone. It should really be 10*60*60 but the extra hour is for DST:

plot \
"data.dat" using ($1 + 11*60*60):3 lt rgb '#483D8B' smooth unique notitle , \
"data.dat" using ($1 + 11*60*60):3 lt rgb '#483D8B' pt 4 ps 0.5 notitle , \
"data.dat" using ($1 + 11*60*60):4 lt rgb '#A52A2A' smooth unique notitle , \
"data.dat" using ($1 + 11*60*60):4 lt rgb '#A52A2A' pt 4 ps 0.5 notitle , \
"data.dat" using ($1 + 11*60*60):5 lt rgb '#009e73' smooth unique notitle axes x1y2 , \
"data.dat" using ($1 + 11*60*60):5 lt rgb '#009e73' pt 4 ps 0.5 notitle axes x1y2 , \
"data.dat" every 2 using ($1 + 11*60*60):3:(sprintf("%.02f", $3)) with labels offset char 0,0.35 font 'verdana,2' notitle , \
"data.dat" every 2::1 using ($1 + 11*60*60):3:(sprintf("%.02f", $3)) with labels offset char 0,-0.35 font 'verdana,2' notitle , \
"data.dat" every 2 using ($1 + 11*60*60):4:(sprintf("%.02f", $4)) with labels offset char 0,0.35 font 'verdana,2' notitle , \
"data.dat" every 2::1 using ($1 + 11*60*60):4:(sprintf("%.02f", $4)) with labels offset char 0,-0.35 font 'verdana,2' notitle , \
"data.dat" every 2 using ($1 + 11*60*60):5:(sprintf("%.02f", $5)) with labels offset char 0,0.35 font 'verdana,2' notitle axes x1y2, \
"data.dat" every 2::1 using ($1 + 11*60*60):5:(sprintf("%.02f", $5)) with labels offset char 0,-0.35 font 'verdana,2' notitle axes x1y2, \
1 / 0 title "download" with linespoints linestyle 4 lt rgb '#483D8B' , \
1 / 0 title "upload" with linespoints linestyle 4 lt rgb '#A52A2A' , \
1 / 0 title "packet loss" with linespoints linestyle 4 lt rgb '#009e73'

# now must "set output" in order to finish writing the SVG file (specifically, </svg>).
# GNUPlot works in such a way that multiple plots might be written to an SVG and therefore
# it leaves the SVG open for further writing. "set output" closes the output and writes
# that final </svg> tag.
set output
