from csma import NUM_COLS, NUM_TX, THROUGHPUT
import matplotlib.pyplot as plt
import parameters
import numpy as np
#plot data

KBITSFRAMESIZE = 12

def condense_columns(matrix, columns):
    joinedsrc = list()
    
    k = 0
    for row in matrix:
        joinedsrc.append(list())
        for i in range(0,round(len(row)/columns)):
            temp = 0
            for j in range(0, columns):
                temp += row[columns*i+j]
            joinedsrc[k].append(temp)
        k += 1
    
    return joinedsrc

def plot_data(stats, srcnumber):
    
    consdensedThroughput = condense_columns(stats[THROUGHPUT], srcnumber)
    t = np.transpose(consdensedThroughput)
    fmt = [".-k", ".:c", ".-b", ".:r"]
    labels = list()
    #labels.append("Bandwidth")
    labels.append("Cumulative Poisson Traffic Rate")
    labels.append("Common CSMA")
    labels.append("Common CSMA/VC")
    labels.append("Hidden CSMA")
    labels.append("Hidden CSMA/VC")
    #plt.hlines(y=12*1000, xmin=0, xmax = 1000,linestyles= "--")
    arrivalRate = np.array(parameters.LAMBDA)
    #fig,axs = plt.subplots(5)
    plt.figure()
    plt.plot(arrivalRate,2*KBITSFRAMESIZE*arrivalRate,"--")
    for row in range(0,len(t)):
        plt.plot(arrivalRate, t[row], fmt[row])
    plt.xlabel("λ (kbs)")
    plt.ylabel("Throughput (kbs)")
    plt.title("CSMA/CA Throughtput vs Arrival Rate")
    plt.legend(labels)
    plt.axis([0, 1000,0,KBITSFRAMESIZE*1000])
    plt.tight_layout()

    plt.figure()
    plt.plot(arrivalRate,2*KBITSFRAMESIZE*arrivalRate,"--")
    print(stats[NUM_COLS])
    condensedCollisions = condense_columns(stats[NUM_COLS], srcnumber)
    c = np.transpose(condensedCollisions)
    for row in range(0,len(c)):
        plt.plot(arrivalRate, c[row], fmt[row])
    plt.xlabel("λ (kbs)")
    plt.ylabel("Number of Collisions (kbs)")
    plt.title("CSMA/CA Collisions vs Arrival Rate")
    plt.legend(labels)
    plt.axis([0, 1000,0,KBITSFRAMESIZE*1000])
    plt.tight_layout()

    plt.figure()
    plt.plot(arrivalRate,2*KBITSFRAMESIZE*arrivalRate,"--")
    print(stats[NUM_TX])
    condensedTX = condense_columns(stats[NUM_TX], srcnumber)
    tx = np.transpose(condensedTX)
    for row in range(0,len(tx)):
        plt.plot(arrivalRate, tx[row], fmt[row])
    plt.xlabel("λ (kbs)")
    plt.ylabel("Number of Transmissions (kbs)")
    plt.title("CSMA/CA Transmissions vs Arrival Rate")
    plt.legend(labels)
    plt.axis([0, 1000,0,KBITSFRAMESIZE*1000])
    plt.tight_layout()


    plt.show()

    

    return

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

