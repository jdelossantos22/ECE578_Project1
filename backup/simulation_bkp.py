from numpy.random.mtrand import randint
import simpy
import numpy as np
import random

import parameters as pm


'''
Statistics
CSMA/CA and CSMA/CA VCS
6 LAMBDAS
TWO TOPOLOGY
Throughput
Collisions Ca, Cb
Transmissions Na, Nb
Fairness Index F1 Fraction of time A transmits over time B transmits
'''

class Node:
    def __init__(self, env, id, name, src, dest):
        self.env = env
        self.id = id
        self.name = name
        self.backoff_freeze = -1

    def sifs(self):
        print('Start SIFS at %d' % self.env.now)
        yield self.env.timeout(pm.SIFS_DUR)

    def difs(self):
        print('Start DIFS at %d' % self.env.now)
        yield self.env.timeout(pm.DIFS_DUR)

    def backoff(self):
        #neeed a collision tracker
        #need a contention window holder
        self.b = randint(0, self.CW -1)
        print('Start DIFS at %d' % self.env.now)
        yield self.env.timeout(self.b)

    def send_rts(self):
        print('Start RTS at %d' % self.env.now)
        yield self.env.timeout(pm.RTS)

    def send_cts(self):
        print('Start CTS at %d' % self.env.now)
        yield self.env.timeout(pm.CTS)

    def send_frame(self):
        print('Sending FRAME at %d' % self.env.now)
        yield self.env.timeout(pm.FRAME_SIZE) #THIS IS NOT RIGHT THIS IS SIZE NOT DURATION

    def send_ack(self):
        print('Start ACK at %d' % self.env.now)
        yield self.env.timeout(pm.ACK)

    def generate_interarrival(self):
        return np.random.exponential(1/self.arr_rate)

class CSMS:
    def __init__(self, env, arrival_rate, vcs=False):
        self.vcs = False
        self.env = env
        self.arrival_rate = arrival_rate
        #TIME ID

    def run():
        return

    

class Simulation:
    def __init__(self):
        self.clock = 0
        self.env = simpy.Environment()
        self.vcs = False
        self.arr_rate = pm.LAMBDA[0]
        for x in range(len(pm.LAMBDA)):
            csms = CSMS(self.env, self.arr_rate)
            #csms = CSMS(self.env, self.arr_rate, vcs=True)


    def generate_interarrival(self):
        return np.random.exponential(1/self.arr_rate)

def main():
    #CSMS
    #DIFS + BACKOFF + FRAME + SIFS + ACK
    #CSMS/CA VCS
    #DIFS + BACKOFF + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
    #env = simpy.Environment()
    #env.run(until=10)
    return


if __name__ == "__main__":
    main()