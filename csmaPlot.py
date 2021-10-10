from csma import NUM_COLS, NUM_TX, THROUGHPUT
import matplotlib.pyplot as plt
import parameters
import numpy as np
#plot data

KBITSFRAMESIZE = 12
TITLES = ["Node A: Throughput T (Kbps) vs rate λ (frames/sec)",
"Node C: Throughput T (Kbps) vs rate λ (frames/sec)",
"Node A: Number of Collisions N vs rate λ (frames/sec)",
"Node C: Number of Collisions N vs rate λ (frames/sec)",
"Fairness Index FI vs rate λ (frames/sec)"
]

def condense_columns(matrix, columns):
    joinedsrc = list()
    
    k = 0
    #row = lambda
    for row in matrix:
        joinedsrc.append(list())
        
        for i in range(0,round(len(row)/columns)):
            #print(i)
            temp = 0
            for j in range(0, columns):
                temp += row[columns*i+j]
                #print(temp)
            joinedsrc[k].append(temp)
        k += 1
    print(joinedsrc)
    return joinedsrc

#srcNumber 0 = A, 1 = C
def extract_data_by_source(matrix, srcNumber):
    joinedsrc = list()
    for row in matrix:
        temp = list()
        for i in range(srcNumber,len(row),2):
            temp.append(row[i])
        joinedsrc.append(temp)
    return joinedsrc


def plot_data(stats, srcnumber):
    
    consdensedThroughput = condense_columns(stats[THROUGHPUT], srcnumber)
    #t = np.transpose(consdensedThroughput)
    fmt = [".-k", ".:c", ".-b", ".:r"]
    labels = list()
    #labels.append("Bandwidth")
    #labels.append("Cumulative Poisson Traffic Rate")
    labels.append("Common CSMA")
    labels.append("Common CSMA/VC")
    labels.append("Hidden CSMA")
    labels.append("Hidden CSMA/VC")
    #plt.hlines(y=12*1000, xmin=0, xmax = 1000,linestyles= "--")
    arrivalRate = np.array(parameters.LAMBDA)
    #fig,axs = plt.subplots(5)
    #plt.figure()
    #plt.plot(arrivalRate,2*KBITSFRAMESIZE*arrivalRate,"--")
    #fig, ax = plt.subplots(3,2)

    '''
    for row in range(0,len(t)):
        plt.plot(arrivalRate, t[row], fmt[row])
    plt.xlabel("λ (kbs)")
    plt.ylabel("Throughput (kbs)")
    plt.title("CSMA/CA Throughtput vs Arrival Rate")
    plt.legend(labels)
    plt.axis([0, 1000,0,KBITSFRAMESIZE*1000])
    plt.tight_layout()
    '''
    xLabel = "λ (kbs)"
    yLabel = ["Throughput T (Kbps)", "Number of Collisions"]
    keys = [THROUGHPUT, NUM_COLS]
    #print(keys)
    for i in range(0,len(TITLES)-1,2):
        data = extract_data_by_source(stats[keys[round(i/2)]], 0)
        #print(data)
        plot(arrivalRate,data,TITLES[i],labels, fmt, xLabel, yLabel[round(i/2)])
        data = extract_data_by_source(stats[keys[round(i/2)]], 1)
        plot(arrivalRate,data,TITLES[i+1],labels, fmt, xLabel, yLabel[round(i/2)])
    
    fairnessIndex = calc_fairness_index(stats)
    print(fairnessIndex)
    plot_fairness_index(arrivalRate, fairnessIndex, TITLES[-1], labels, fmt, xLabel, "Fairness Index FI")

    plt.show()

    

    return

def plot_fairness_index(arrivalRate, data,title,labels,fmt, xLabel, yLabel):
    data_t = np.transpose(data)
    plt.figure()
    #plt.plot(arrivalRate, data)
    for r in range(len(data_t)):
        plt.plot(arrivalRate, data_t[r], fmt[r])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend(labels)
    #plt.yticks(np.arange(0, KBITSFRAMESIZE*1000,2000))
    plt.axis([0,1000,0,2])
    plt.tight_layout()

def calc_fairness_index(stats):
    cols = stats[NUM_COLS]
    tx = stats[NUM_TX]
    fairnessIndex = list()
    for r in range(len(cols)):
        topologies = list()
        for i in range(0,len(cols[r]),2):
            colA = cols[r][i]
            colC = cols[r][i+1]
            txA = tx[r][i]
            txC = tx[r][i+1]
            tA = colA + txA
            tC = colC + txC
            fIndex = tA/tC
            topologies.append(fIndex)
        fairnessIndex.append(topologies)

    return fairnessIndex

def find_max(data):
    max = 0
    for row in data:
        for col in row:
            if col > max:
                max = col
    return max + 1000

def plot(arrivalRate, data,title,labels,fmt, xLabel, yLabel):
    data_t = np.transpose(data)
    yMax = find_max(data)
    if yLabel == "Throughput T (Kbps)":
        yMax = KBITSFRAMESIZE*1000
    plt.figure()
    #plt.plot(arrivalRate, data)
    for r in range(len(data_t)):
        plt.plot(arrivalRate, data_t[r], fmt[r])
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend(labels)
    #plt.yticks(np.arange(0, KBITSFRAMESIZE*1000,2000))
    plt.axis([0,1000,0,yMax])
    plt.tight_layout()

def collect_data(csma,stats, l):
    #stats[NUM_COLS].append(csma.).
    cols = list()
    txs = list()
    tps = list()
    for n in csma.srcs:
        cols.append(n.col)
#        print(n.tx)
        txs.append(n.tx)
        tps.append(round(KBITSFRAMESIZE*n.tx/parameters.SIM_DUR)) #kb/s
    if 0 <= l < len(stats[NUM_COLS]):
        stats[NUM_COLS][l] = np.append(stats[NUM_COLS][l],cols)
        stats[NUM_TX][l] = np.append(stats[NUM_TX][l],txs)
        stats[THROUGHPUT][l] = np.append(stats[THROUGHPUT][l],tps)
    else:
        stats[NUM_COLS].append(np.asarray(cols))
        stats[NUM_TX].append(np.asarray(txs))
        stats[THROUGHPUT].append(np.asarray(tps))

    #print(stats)
    return stats


#if __name__=="__main__":

