import math
#CONSTANTS
FRAME_SIZE = 100 #1500*8 #1500 bytes * 8 bits
SLOT_DUR = 10*pow(10,-6)
SIFS_DUR = 1
CW_0 = 4
CW_MAX = 1024
LAMBDA = [100,200, 300, 500, 700, 1000]#[]100]
#uncomment of testing only first labmda
#LAMBDA = [1000]
ACK = RTS = CTS = 2
DIFS_DUR = 2
SIM_DUR = 10#10 #Simulation TIme 10 Seconds = 100,000 *10 = 1,000, 000
#