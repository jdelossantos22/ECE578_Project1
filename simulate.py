from numpy.random.mtrand import randint
import simpy
import numpy as np
import random

import parameters as pm

class CSMS:
    def __init__(self, env, arrival_rate, vcs=False):
        self.vcs = False
        self.env = env
        self.arrival_rate = arrival_rate
        self.col_A = 0
        self.col_C = 0
        self.tx_A = 0
        self.tx_C = 0


    def run(self):
        while True:

            print("Start Round")
            yield self.env.timeout(pm.DIFS_DUR)
            print("DIFS end at %d" % self.env.now)
            #a.generate_backoff
            #c.generate_backoff
            #if a < c:
                #yield self.env.timeout(backoff_period)
            #else:
            ##yield self.env.timeout(backoff_period)
            backoff_period = randint(0,pm.CW_0)
            print("Backoff Period is %d" % backoff_period)
            yield self.env.timeout(backoff_period)
            print("BACKOFF PERIOD end at %d" % self.env.now)
            yield(self.env.timeout(pm.FRAME_SIZE))
            print("FRAME SENT at %d" % self.env.now)
            yield(self.env.timeout(pm.SIFS_DUR))
            print("WAIT FOR ACK(SIFS) at %d" % self.env.now)
            yield(self.env.timeout(pm.ACK))
            print("ACK received at %d" % self.env.now)

            

class Simulation:
    def __init__(self):
        self.env = simpy.Environment()
        self.vcs = False
        self.arr_rate = pm.LAMBDA[0]
        for i in range(len(pm.LAMBDA)):
            csms = CSMS(self.env, pm.LAMBDA[i])

    def run():
        pass

def main():
    #CSMS
    #DIFS + BACKOFF + FRAME + SIFS + ACK
    #CSMS/CA VCS
    #DIFS + BACKOFF + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
    env = simpy.Environment()
    #env.run(until=10)
    csms = CSMS(env,100)
    env.process(csms.run())
    env.run(until=120)
    return


if __name__ == "__main__":
    main()