"""This version handels all power data as intergers and so is being upgraded to use floating point
numbers, improving precision. This is still the latest working version.

This file:
	Downloads data from RADIAL AIR

	Splits the string recieved - into power, time and location

	Checks that the time isn't the same as previous strings (string is new)

	Checks that the power is not 0, if so then there is an error on the Pi as no data is being 
	collected

	A rolling average is collected from the first 5 results 

	Otherwise the data is checked to see if it is more than 5% different from the rolling average
		If it is then the data is flagged as an anomoly
		Otherwise it is added to the list as part of the rolling average
"""

import os
import time as t

local_root = open("local.root","r").readline()[:-1]
air_ip = ip = open("radial_air.ip","r").readline()[:-1]


def prepend_file(filename, line):
	"""Allows data to be prepended to file (rarther than appended)"""
	with open(filename, "r+") as fil:
		content = fil.read()
		fil.seek(0, 0)
		fil.write(line.rstrip("\r\n")+"\n"+content)

local = local_root+"data_dump/wifi.txt"
average = [0, 0, 0, 0, 0]
list_counter = 4
test_counter = 0
last_time = int(0)
log_file = local_root+"log.txt"

while True:
	os.system("scp pi@"+air_ip+":/home/pi/RADIAL_INT/wifi.txt "+local_root+"data_dump")
	with open(local) as f:
		try:
			content= f.readlines()
			content.reverse()
			for i in content:
				list=i.split(",")
				if len(list)==3:
					power=int(list[0])
					time=list[1]
					time=int(time.split(".")[0])
					location=list[2]
					if time>last_time:
						last_time=time
						time = str(time)
						disp_line = str(power)+","+time+","+location
						#prepend_file(log_file,disp_line)
						if power == 0:
							print("Error on pi, restart may be required")
						elif test_counter <= 4 and power!=0:
							print("List conter = ", list_counter)
							average[list_counter] = power
							list_counter += 1
							if list_counter >= 4:
								list_counter = 0
							test_counter += 1
							print disp_line

						else:
							average_real = (average[0]+average[1]+average[2]+average[3]+average[4])/5
							disp_line = disp_line[:-1]
							disp_line += ',' + str(average_real)
							if power <= 1.05*average_real or power >= 0.95*average_real:
								print 'Anomalous Data'
								print disp_line
								prepend_file(log_file, disp_line)
							else:
								average[list_counter] = power
								list_counter += 1
								if list_counter >= 5:
									list_counter = 0
								print disp_line
				#Else data is not needed

		except Exception, error:
	   		print error
			print("An error occured, continuing anyway")			
	
	t.sleep(1)
