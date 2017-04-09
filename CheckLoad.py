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

############### PARAMS ################
totalPacketNum = 10000
global packetsize
dest = "www.bgu.ac.il";
FixedInterval = 0.0
PathToSave = "/root/Desktop/rtt_plot/LoadTesting/10000packet_increasedSize (FixedScale)"
global img_counter
############### END - PARAMS ################

def main():

    #dateForFolder = time.strftime("%d_%m_%I:%M")
    mat_rtt = np.zeros((1, totalPacketNum+1))
    #i=0;
    #finalPath = PathToSave + str(totalPacketNum) + "pcs_" + dateForFolder

   # if not os.path.exists(finalPath):
    #    os.makedirs(finalPath)
    img_counter = 1
    packetsize = 65507
    for x in range(0,10):
       # packetsize = packetsize + (x*50)
        str_cmd = "ping -c {0} -i {1} -s {2} {3}".format(totalPacketNum,FixedInterval,packetsize,dest);
        j=0;
        rtt_vec = np.zeros((totalPacketNum))
        for line in run_command(str_cmd.split()):
               if line=="\n":
                   continue;
               line_parts = line.split();
               if line_parts[0] == "PING"  or line_parts[0] == "" or line_parts[0] == "---" or line_parts[0] == "rtt" or line_parts[0] == totalPacketNum.__str__():
                   continue
               rtt_vec[j] = line_parts[7].split('=')[1]
               print (line_parts[7])
               j+=1
           #mat_rtt[0][i] = run_command(str_cmd);
        create_graph(rtt_vec,PathToSave,packetsize,img_counter);
        img_counter = img_counter +1
        print("DONE!")



def create_graph(vecotr,path,size,img_c):
    #ids = [x for x in range(len(vecotr))]
    #t= np.arange(0,110.0,010.0);
    #bins = np.arange(0,10.0,0.1)
    #plt.hist(vecotr,bins,histtype='bar',rwidth=0.1);
    plt.ylim([0,30])
    plt.plot(np.arange(1,totalPacketNum+1,1),vecotr)
    plt.title('RTT load testing of #{0} packet to {1} [{2}Bytes ICMP Packet]'.format(totalPacketNum,dest,size))
    plt.xlabel("packet #");
    plt.ylabel("RTT [ms]")
    #plt.show();
   # path = path + "/" + "hist_" + str(interval) + ".png"
    plt.savefig(PathToSave + "/figure_" + str(img_c)+".jpg")
    plt.close()
    img_counter = img_c +1



def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


if __name__ == "__main__":
    main()
