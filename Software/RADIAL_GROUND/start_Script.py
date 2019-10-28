"""Starts scripts on pi, and calls download/processing file simultaniously"""
from multiprocessing import Process
import os
import time

print("\n\nStarting RADIAL\n\nThis may take a few seconds\n\n")

air_ip = ip = open("radial_air.ip","r").readline()[:-1]

os.system('ssh pi@'+air_ip+' sudo killall python')
os.system('ssh pi@'+air_ip+' sudo /etc/init.d/ssh restart')

time.sleep(5)

def start_topblock():
        """Starts top_block.py (GNU radio file) on pi"""
        os.system("ssh pi@"+air_ip+" 'python /home/pi/RADIAL_INT/top_block.py'")

def start_process():
        """Starts simple_process.py (data processing file) on pi"""
        os.system("ssh pi@"+air_ip+" 'python /home/pi/RADIAL_INT/simple_process.py'")
        
def start_download():
        """Starts download script on ground"""
	import download_file

if __name__=="__main__":
        """Starts processes"""
        p1 = Process(target=start_topblock)
        p1.start()
        p2 = Process(target=start_process)
        p2.start()
	time.sleep(10)
	p3 = Process(target=start_download)
	p3.start()
