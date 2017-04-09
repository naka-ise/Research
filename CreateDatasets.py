from M2Crypto.PGP.packet import packet
from subprocess import Popen, PIPE
import re
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import numpy as np
import scapy
from scapy.all import *
import time
import matplotlib.pyplot as plt


def main():
    ##### PARAMS #####
    intervals_ar = [0, 0.0001]
    pctSize_ar= [56,100]    #bytes
    count_ar = [1000,5000]

    PathToSave = "/root/Desktop/datasets/" + time.strftime("%d_%m_%I:%M")


    dst = "192.168.3.13"
    trials = 100

    ##### END- PARAMS #####

    for interval in intervals_ar:
        for packetSize in pctSize_ar:
            for count in count_ar:
                rtt_vec = np.zeros([count, trials])
                #x = 0.3
                #print "FINISHED: interval: {0} ".format(x.__str__())
                for iteration in range(trials):
                    str_cmd = "ping -c {0} -i {1} -s {2} {3}".format(count, interval, packetSize,dst);

                    #send ICMP and fill rtt_vec
                    row=0
                    for line in run_command(str_cmd.split()):
                        if line == "\n":
                            continue;
                        line_parts = line.split();
                        if line_parts[0] == "PING" or line_parts[0] == "" or line_parts[0] == "---" or line_parts[
                            0] == "rtt" or line_parts[0] == count.__str__():
                            continue
                        rtt_vec[row,iteration] = line_parts[6].split('=')[1]
                        #print (line_parts[6])
                        row = row+1
                    print "FINISHED: interval: {0} , pct_size: {1}, count: {2}, trial {3}".format(interval.__str__(),packetSize,count,iteration)
                createCSVfile(rtt_vec,interval,packetSize,count,PathToSave)


def createCSVfile(array,interval,packetSize,count,PathToSave):
    if not os.path.exists(PathToSave):
       os.makedirs(PathToSave)

    np.savetxt(PathToSave+"/Int={0}_PcSz={1}_Cnt={2}.csv".format(interval.__str__(),packetSize,count),array, delimiter=",",fmt='%.3f')


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


#start main
if __name__ == "__main__":
    main()