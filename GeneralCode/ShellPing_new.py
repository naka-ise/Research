from subprocess import Popen, PIPE
import re
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import numpy as np
import scapy
from scapy.all import *
import time
import matplotlib.pyplot as plt

def sendPing(count, interval,dest):
    rtt =0;
    str_cmd = "ping -q -c {0} -i {1} {2}".format(count,interval,dest);
    cmd = Popen(str_cmd.split(' '), stdout=PIPE)
    output = cmd.communicate()[0]
    match = re.search('(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\/(\d+\.\d+)\s+ms', output)
    if not (match is None):
       rtt=float(match.group(2))
       print rtt;
    else:
        print "fail"

    return rtt;


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def main():
    PathToSave = "/root/Desktop/rtt_plot/histograms/"
    dateForFolder = time.strftime("%d_%m_%I:%M")
    mat_rtt = np.zeros((1, 11))
    dest="10.0.0.138";
    i=0;
    count=10000;
    finalPath = PathToSave + str(count) + "pcs_" + dateForFolder

    if not os.path.exists(finalPath):
        os.makedirs(finalPath)


    for interval in np.arange(0,0.01,0.001):
       # mat_rtt[0][i]=sendPing(count,interval,dest);
       str_cmd = "ping -c {0} -i {1} {2}".format(count, interval, dest);
       j=0;
       rtt_vec = np.zeros((count))
       for line in run_command(str_cmd.split()):
           if line=="\n":
               continue;
           line_parts = line.split();
           if line_parts[0] == "PING"  or line_parts[0] == "" or line_parts[0] == "---" or line_parts[0] == "rtt" or line_parts[0] == count.__str__():
               continue
           rtt_vec[j] = line_parts[6].split('=')[1]
           print (line_parts[6])
           j+=1
       #mat_rtt[0][i] = run_command(str_cmd);
       create_Histogram(rtt_vec,interval,finalPath);
       i+=1

    print("DONE!")

def create_Histogram(vecotr,interval,path):
    #ids = [x for x in range(len(vecotr))]
    #t= np.arange(0,110.0,010.0);
    bins = np.arange(0,10.0,0.1)
    plt.hist(vecotr,bins,histtype='bar',rwidth=0.1);
    plt.title('RTT Histogram of {0} interval rate ({1})'.format(interval,dest))
    plt.xlabel("RTT time [ms]");
    plt.ylabel("# of packet")
    #plt.show();
   # path = path + "/" + "hist_" + str(interval) + ".png"
    plt.savefig(path + "/" + "hist_" + str(interval) + ".jpg")
    plt.close()


if __name__ == "__main__":
    main()

 # t = np.arange(0, 110.0, 010.0);
 # plt.plot(t, mat_rtt[0]);
 # plt.xlabel("interval [ms]");
 # plt.ylabel("RTT time [ms]")
 # plt.show();
