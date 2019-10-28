import serial

def process_gngga(str):
	list = str.split(",")
	#list format - id, time, lat, NS, long, EW, quality, num sats, horizontal dilution of precision, alt, units alt, Geoid separation, units sep, Age of differential corrections, ID of station providing differential corrections, check sum
	list[14:15]=list[14].split("*")
	dict = {"time":list[1], "lat":list[2],"NS":list[3], "long":list[4],"EW":list[5], "quality":list[6], "numSV":list[7], "HDOP":list[8], "alt":list[9], "uAlt":list[10], "sep":list[11], "uSep":list[12], "diffAge":list[13],"diffStation":list[14], "cs":list[15]}
	return dict

def loc():
        serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
	gps_success = 0

        while gps_success != 1:
                gps_str = serialPort.readline()
                if gps_str.find('GGA')>0:
                        gps_msg = process_gngga(gps_str)
                        gps_success = 1
                else:
                        gps_success = 0
                        #gps_msg = {"lat":"GPS Acquesition Failed","NS":'',"long":'',"EW":'',"alt":'',"uAlt":''}        

        gps_loc = str(gps_msg['lat']+" "+gps_msg['NS']+" "+gps_msg['long']+" "+gps_msg['EW']+" "+gps_msg['alt']+" "+gps_msg['uAlt'])

	return gps_loc

