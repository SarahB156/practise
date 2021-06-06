#
#  NAME
#    problem_set1.py
#
#  DESCRIPTION
#    Open, view, and analyze raw extracellular data
#    In Problem Set 1, you will write create and test your own spike detector.
#

import numpy as np
import matplotlib.pylab as plt
import matplotlib.pyplot as plt2
from collections import Counter

def load_data(filename):
    """
    load_data takes the file name and reads in the data.  It returns two 
    arrays of data, the first containing the time stamps for when they data
    were recorded (in units of seconds), and the second containing the 
    corresponding voltages recorded (in units of microvolts - uV)
    """
    data = np.load(filename)[()];
    return np.array(data['time']), np.array(data['voltage'])
    
def bad_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTime - all the times where a spike (action potential) was detected
         
    This function is bad at detecting spikes!!! 
        But it's formated to get you started!
    """
    
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print ("Can't run - the vectors aren't the same length!")
        APTimes = []
        return APTimes
    
    numAPs = np.random.randint(0,len(time))//10000 #and this is why it's bad!!
 
    # Now just pick 'numAPs' random indices between 0 and len(time)
    APindices = np.random.randint(0,len(time),numAPs)
    
    # By indexing the time array with these indices, we select those times
    APTimes = time[APindices]
    
    # Sort the times
    APTimes = np.sort(APTimes)
    
    return APTimes
    
def good_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to t he voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTime - all the times where a spike (action potential) was detected
    """
    import numpy as np    
    APTimes = []
    t=[]  
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print ("Can't run - the vectors aren't the same length!")
    
    else:
        np.absolute(voltage) #Turns voltages into absolute values to not worry about negative spikes. 
        stdV=np.std(voltage) #Gets standard deviation of voltage readings.                
        APTime=time[voltage>(3*stdV)] #To get voltages larger than 5 standard deviations of the mean 
        APRemove =[] ## Makes an empty list to hold the index of action potentials to remove
        count =0 # starts a count
        lastindex=len(APTime)-1 ## this is to get the index of the last APTime
        for s in APTime: ## for each of the AP Times...
            if count == 0: ## keep going if count is 0
                count = count +1  
            elif count >=1 and count !=lastindex: ## if count is larger than 1 and also not the last index
                if (APTime[count+1]-APTime[count]) <=0.001:  ## another if to figure out if same AP or not
                    count=count+1 
                    APRemove.append(count) ##Append the index of repeated AP to APremove.
                else:
                    count=count+1 ## If not then just add 1 to count
            else:    
                count= count+1 ## Add another to the count as well. 
                
        APTimeslist= np.delete(APTime, APRemove) ## Makes a new list without APRemove values.
        APTimes= np.asarray(APTimeslist) ## Makes list into array
        return APTimes
            
            
            
def get_actual_times(dataset):
    """
    Load answers from dataset
    This function takes the following input:
        dataset - name of the dataset to get answers for

    This function returns the following output:
        APTimes - spike times
    """  
    
    return np.load(dataset)
    
def detector_tester(APTimes, actualTimes):
    """
    returns percentTrueSpikes (% correct detected) and falseSpikeRate
    (extra APs per second of data)
    compares actual spikes times with detected spike times
    This only works if we give you the answers!
    """
    
    JITTER = 0.025 #2 ms of jitter allowed
    
    #first match the two sets of spike times. Anything within JITTER_MS
    #is considered a match (but only one per time frame!)
    
    #order the lists
    detected = np.sort(APTimes)
    actual = np.sort(actualTimes)
    
    #remove spikes with the same times (these are false APs)
    temp = np.append(detected, -1)
    detected = detected[plt.find(plt.diff(temp) != 0)]
 
    #find matching action potentials and mark as matched (trueDetects)
    trueDetects = [];
    for sp in actual:
        z = plt.find((detected >= sp-JITTER) & (detected <= sp+JITTER))
        if len(z)>0:
            for i in z:
                zz = plt.find(trueDetects == detected[i])
                if len(zz) == 0:
                    trueDetects = np.append(trueDetects, detected[i])
                    break;
    percentTrueSpikes = 100.0*len(trueDetects)/len(actualTimes)
    
    #everything else is a false alarm
    totalTime = (actual[len(actual)-1]-actual[0])
    falseSpikeRate = (len(APTimes) - len(actualTimes))/totalTime

    print ('Action Potential Detector Performance performance: ')
    print ('     Correct number of action potentials = ') + str(len(actualTimes))
    print ('     Percent True Spikes = ') + str(percentTrueSpikes)
    print ('     False Spike Rate = ') + str(falseSpikeRate) + (' spikes/s')
    print 
    return {'Percent True Spikes':percentTrueSpikes, 'False Spike Rate':falseSpikeRate}
    
    
def plot_spikes(time,voltage,APTimes,titlestr):
    """
    plot_spikes takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the raw voltage signal
    and indicating the location of detected spikes with red tick marks (|)
    """
   
    fig1=plt.figure()
    plt.plot(time,voltage) ##Plots time versus voltage
    plt.xlabel("Time(s)") ##Adds an x label
    plt.ylabel("Voltage (uV)") ##Adds a y label
    plt.title(titlestr) ##Adds a title that is determined by titlestr string.
    hold = True ##Keeps the plot so that we can add AP Times
    howmanyAPTimes = len(APTimes) ## Checks how many APs there are in APTimes
    maxV=max(voltage)+50 ## gets the maximum voltage and adds 50 uV
    
    plt.plot(APTimes, np.ones(howmanyAPTimes)+maxV, 'r|') ## Plots the AP Times
    ## as X Y coordinates, note that it adds the maxV parameter above to each of the
    ## 1s in the array of AP times.
    plt.show() ## Makes the plot pop out.   
    
def plot_waveforms(time,voltage,APTimes,titlestr):
    """
    plot_waveforms takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the waveforms for each
    detected action potential
    """
    Count = 0
    SR= time[1]-time[0] #This is the duration of one index in time.
    DurationIndex = 0.003/SR  #this is number of indeces in 3 ms  
    for n in APTimes:
        CurrentAPT= APTimes[Count] ##This figures out when spike occured from 
        ##APTimes input
        for i, j in enumerate(time): ## This for loop figures out the TimeIndex
        ## by using enumerate which makes a vector with index values and the actual 
        ## values
            if j == CurrentAPT: ## if the time value is the same as the APT time
                TimeIndex=i ## Then time index is recorded
        IndexBefore=TimeIndex-DurationIndex ## Figure out Time before
        IndexAfter=TimeIndex+DurationIndex ## Figure out Time After AP    
        VoltageforPlot = voltage[IndexBefore: IndexAfter] ##Get voltage data for current AP
        TimeforPlot = np.linspace(-0.003, 0.003, len(VoltageforPlot)) ##Set a standard time axis for all plots        
         
        fig = plt.figure(2) # Plots a second figure. 
        plt.plot(TimeforPlot,VoltageforPlot) ##Plots time versus voltage
        plt.xlabel("Time(s)") ##Adds an x label
        plt.ylabel("Voltage (uV)") ##Adds a y label
        plt.title(titlestr) ##Adds a title that is determined by titlestr string.
        hold = True ##Keeps the plot so that we can add AP Times        
        Count = Count +1 ## Adds to the count to keep the for loop going.
    '''     
    print SR
    ##print Duration3ms
    print DurationIndex
    print TimeIndex
    print IndexBefore
    print IndexAfter
    print len(TimeforPlot)
    print len(VoltageforPlot)'''

        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    t,v = load_data('spikes_hard_test.npy')    
    actualTimes = get_actual_times('spikes_hard_practice_answers.npy')
    APTime = bad_AP_finder(t,v)    
    APTimes = good_AP_finder(t,v)
    plot_spikes(t,v,APTimes,'Action Potentials in Raw Signal ')
    plot_waveforms(t,v,APTimes,'Waveforms')
    detector_tester(APTimes,actualTimes)


