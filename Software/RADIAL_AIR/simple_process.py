#Simpler version of process_data.py due to intermittant output of power as 0

import struct
import time
#import serial
import gps


def follow(file):
        file.seek(0,2)
        while True:
                line = file.readline()
                if not line:
                        time.sleep(0.1)
                        continue
                yield line

def prepend_file(filename,line):
        with open(filename, "r+") as fil:
                content=fil.read()
                fil.seek(0,0)
                fil.write(line.rstrip("\r\n")+"\n"+content)

def truncate_file(filename, trunc_pos):
        with open(filename, "r+") as fil:
                fil.truncate(trunc_pos)

read_file = open("/home/pi/Power_detection_bands/wifi.raw", "r+")
#write_file = "/home/pi/Power_detection_bands/wifi.txt"

truncate_len =[0,0,0,0,0,0,0,0,0,0]
truncate_counter = 0

read_lines = follow(read_file)

#serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

for line in read_lines:
	power = struct.unpack_from('h', line)
	power = str(power[0])
        time_read = str(time.time())
	"""The commented part bellow causes the power to cometimes be written as 0
	
	gps_success = 0
        
        while gps_success != 1:
		gps_str = serialPort.readline()
		if gps_str.find('GGA')>0:
        		gps_msg = gps.process_gngga(gps_str)
                	gps_success = 1
		else:
			gps_success = 0
			#gps_msg = {"lat":"GPS Acquesition Failed","NS":'',"long":'',"EW":'',"alt":'',"uAlt":''}        
	
	gps_loc = str(gps_msg['lat']+" "+gps_msg['NS']+" "+gps_msg['long']+" "+gps_msg['EW']+" "+gps_msg['alt']+" "+gps_msg['uAlt'])
	"""

#The use of the GPS causes the script to return the value 0 as the radio power
#To turn off comment the first gps_loc line and uncomment second
#This error is deffinatly caused by the script becuase when GPS and script
#Run separatly error does not occure

	gps_loc = gps.loc()
#	gps_loc = "GPS Turned off to make it work"
	read_file.truncate(0)

	write_data = power+ ", " + time_read+", "+gps_loc

	prepend_file("/home/pi/Power_detection_bands/wifi.txt", write_data)
	
	print write_data

	if truncate_counter<=9:
        	truncate_len[truncate_counter]=len(write_data)+1
                truncate_counter+=1
        else:
                truncate_counter=0
                truncate_len[truncate_counter]=len(write_data)+1

        truncate_pos = sum(truncate_len)
        truncate_file("/home/pi/Power_detection_bands/wifi.txt", truncate_pos)

