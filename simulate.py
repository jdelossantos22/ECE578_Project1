from numpy.random.mtrand import randint
import simpy
import numpy as np
import random
import node
import math

import parameters

class CSMS:
    def __init__(self, env, arrival_rate, vcs=False):
        self.vcs = False
        self.env = env
        self.arrival_rate = arrival_rate
        self.col_A = 0
        self.col_C = 0
        self.tx_A = 0
        self.tx_C = 0
        self.srcs = []
        self.dest = []
        self.srcs.append(node.Node(env, 0, "A", arrival_rate, vcs))
        self.srcs.append(node.Node(env, 1, "C", arrival_rate, vcs))
        self.dest.append(node.Node(env, 2, "B", arrival_rate, vcs))
        self.dest.append(node.Node(env, 3, "D", arrival_rate, vcs))
        


    def run(self):
        while True:
            next_interarrival = self.srcs[0].generate_interarrival()
            print(next_interarrival)
            yield self.env.timeout(100)
            self.env.process(self.srcs[0].send(self.srcs[1], self.dest[0]))
            self.env.process(self.srcs[1].send(self.srcs[0], self.dest[1]))

            

class Simulation:
    def __init__(self):
        self.env = simpy.Environment()
        self.vcs = False
        self.arr_rate = pm.LAMBDA[0]
        for i in range(len(pm.LAMBDA)):
            csms = CSMS(self.env, pm.LAMBDA[i])

    def run():
        pass

def generate_interarrival():
    return np.random.exponential(1/(parameters.SLOT_DUR*200), int(1/(parameters.SLOT_DUR*200))*10)

def main():
    #CSMS
    #DIFS + BACKOFF + FRAME + SIFS + ACK
    #CSMS/CA VCS
    #DIFS + BACKOFF + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
    '''
    env = simpy.Environment()
    #env.run(until=10)
    csms = CSMS(env,100)
    env.process(csms.run())
    env.run(until=300)
    return
    '''
    
    print(1/(parameters.SLOT_DUR*100))
    interarrivals = generate_interarrival()
    interarrivals = [math.floor(x) for x in interarrivals]
    for x in interarrivals:
        print(x)
    print(len(interarrivals))


if __name__ == "__main__":
    main()