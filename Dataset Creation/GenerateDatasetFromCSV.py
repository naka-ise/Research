import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import csv
import os
import glob


def main():
    #################### CHANGE HERE !! ####################
    BenignFolderPath="/root/Desktop/datasets/20_04_06:02_BENIGN"
    AttackedFolderPath="/root/Desktop/datasets/20_04_06:16_ATTACKED"
    #########################################################

    benignFiles=sorted(glob.glob(BenignFolderPath+"/*.csv"))
    attackedFiles=sorted(glob.glob(AttackedFolderPath+"/*.csv"))

    for bf,af in zip(benignFiles,attackedFiles):
        b_base=str(bf)[str(bf).index("Int="):str(bf).index("_BENIGN")]
        a_base=str(af)[str(af).index("Int="):str(af).index("_ATTACKED")]
        if(a_base!=b_base):
            print "Iterate files not the same"
        else:
            print bf
            print af
        print "********"

        output_base = str(bf).split("BENIGN")[0]
        output_temp = output_base+"_temp.csv"
        output_folder = BenignFolderPath + "/FeaturesDS/"
        output_final = BenignFolderPath + "/FeaturesDS/"+b_base+"_Dataset.csv"

        #create output folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        StartProcess((bf,af),output_temp)
        FinalFix(output_temp,output_final)

        #Output dataset will be saved in the
    print "#### PROCESS COMPLETED! ####"

def StartProcess(CSV_to_Process, outputDS):#attacked=0->benign | attacked=1->attacked
    # create dataset csv output file (espcialy headers)
    with open(outputDS, 'a') as out:
        csv_out= csv.writer(out)
        csv_out.writerow(["Trial_Num","Max","Min","Std","Mean","Delta","Median","FFT_Index(0)","FFT_Val(0)","FFT_Index(1)","FFT_Val(1)",
                      "FFT_Index(2)","FFT_Val(2)","FFT_Index(3)","FFT_Val(3)","FFT_Index(4)","FFT_Val(4)",
                      "FFT_Index(5)","FFT_Val(5)","FFT_Index(6)","FFT_Val(6)","FFT_Index(7)","FFT_Val(7)",
                      "FFT_Index(8)","FFT_Val(8)","FFT_Index(9)","FFT_Val(9)","Energy","Q1","Q2","Q3","Q4",
                      "Hist0","Hist1","Hist2","Hist3","Hist4","Hist5","Hist6","Hist7","Hist8","Hist9","Hist10","Hist11",
                      "Hist12","Hist13","Hist14","Hist15","Hist16","Hist17","Hist18","Hist19","Hist20","Hist21","Hist22","Hist23",
                      "Hist24","Hist25","Hist26","Hist27","Hist28","Hist29","Attacked?"])


    t_lable="No"
    for file in (CSV_to_Process):
        data = np.genfromtxt(file, delimiter=',', defaultfmt='%.3f')
        for iter in range(100):
            trial = data[:, ][:, iter]
            PacketCount = trial.size

            #Basic Statistics Features#
            t_max=np.amax(trial)
            t_min=np.amin(trial)
            t_mean= np.mean(trial)
            t_sum= sum(trial)
            t_std=np.std(trial)
            t_median=np.median(trial)
            t_delta=t_max-t_min

            #QUARTINELES
            t_Q1=np.percentile(trial,25)
            t_Q2=np.percentile(trial,50)
            t_Q3=np.percentile(trial,75)
            t_Q4=np.percentile(trial,100)

            #HISTOGRAM
            hist=np.histogram(trial,bins=30,range=(0,1))
            hist_map=map(str,hist[0])
            t_hist=",".join(hist_map)


            #FFT
            fy=np.abs(fft(trial))
            fft_array = [i for i in sorted(enumerate(fy[0:PacketCount/2]), key=lambda x: x[1], reverse=True)][1:11]
            ax= [i[1][:2] for i in enumerate(fft_array)]
            lst=map(str,ax)
            fft_line=",".join(lst).replace("(","").replace(")","")
            #ENERGY
            t_energy=sum(pow(fy[0:PacketCount],2))/PacketCount


            #PRINT INSTANCE TO FILE
            with open(outputDS, 'a') as out:
                csv_out= csv.writer(out)
                csv_out.writerow([iter,t_max,t_min,t_std,t_mean,t_delta,t_median,fft_line,t_energy,t_Q1,t_Q2,t_Q3,t_Q4,t_hist,t_lable])

        #Change lable after first iteration
        t_lable="Yes"



def FinalFix(before_fix,after_fix):
    f1= open(before_fix,'r')
    f2= open(after_fix,'w')
    for line in f1:
        f2.write(line.replace('"',""))
    f1.close()
    f2.close()
    os.remove(before_fix) #remove old

if __name__ == "__main__":
    main()
