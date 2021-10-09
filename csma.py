
import numpy as np
import random
import parameters
import math
import pandas as pd
import matplotlib.pyplot as plt
from csmaPlot import *

class Node:
    def __init__(self, id, name, vcs=False):
        self.id = id
        self.name = name
        self.cont_wind = parameters.CW_0
        self.packets = []
        self.backoff = -1
        self.tx = 0
        self.col = 0
        self.tp = 0
        self.nav = parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
        if vcs == True:
            self.nav += parameters.RTS + parameters.SIFS_DUR*2 + parameters.CTS

    def generate_backoff(self):
        #print("Source %s has a contention window of %d" % (self.name,self.cont_wind))
        if self.cont_wind >= parameters.CW_MAX:
            self.cont_window = parameters.CW_MAX
        self.backoff = random.randint(0,self.cont_wind-1)

        return self.backoff
    
    
class Packet:
    def __init__(self, id, src,dest, packet_arrival, vcs=False):
        self.id = id
        self.src = src
        self.dest = dest
        self.t_arrival = packet_arrival
        self.vcs = vcs
        self.done = False
        self.isCollided = False
        self.nav = parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
        if vcs == True:
            self.nav += parameters.RTS + parameters.SIFS_DUR*2 + parameters.CTS
        self.src.generate_backoff()


class CSMA:
    def __init__(self, arrival_rate=1000,vcs=False, sim_duration=2000, hidden=False):
        self.clock = 0
        self.arrival_rate = arrival_rate
        self.sim_duration = sim_duration
        self.vcs = vcs
        self.hidden = hidden
        self.packet_counter = 0
        self.srcs = []
        self.dest = []
        self.nodes = []
        self.medium = []
        self.srcs.append(Node(0,"A", self.vcs))
        self.srcs.append(Node(1,"C", self.vcs))
        self.dest.append(Node(2,"B", self.vcs))
        self.dest.append(Node(3,"D", self.vcs))
        for i in range(len(self.srcs)):
            self.nodes.append(self.srcs[i])
            self.nodes.append(self.dest[i])
        self.generate_traffic()


    def advance_time(self):
        pass
    
    def generate_interarrival(self):
        #uncomment code when ready for exponential distro
        # np.random.exponential(1/(parameters.SLOT_DUR*200), int(1/(parameters.SLOT_DUR*200))*10)
        #final form
        #interarrivals = math.floor(np.random.exponential(1/(parameters.SLOT_DUR*self.arrival_rate)), int(1/(parameters.SLOT_DUR*self.arrival_rate))*10)
        interarrivals = np.random.exponential(1/self.arrival_rate, int(self.arrival_rate)*parameters.SIM_DUR)
        interarrivals = [math.floor(x/parameters.SLOT_DUR) for x in interarrivals]

        #testing 
        #interarrivals = math.floor(np.random.exponential(1/(parameters.SLOT_DUR*self.arrival_rate)), 5)
        #interarrivals = [100, 100, 100]
        #interarrivals = [math.floor(x) for x in interarrivals]
        return interarrivals

    def generate_traffic(self):
        for n in range(len(self.srcs)):
            interarrivals = self.generate_interarrival()
            time = 0
            traffic = []
            for i in interarrivals:
                time += i
                traffic.append(time)
            #print(traffic)
            #print(len(traffic))
            #uncomment for testing collisions
            #self.srcs[n].packets = [500, 800, 1000, 1500]
            #print(self.srcs[n].packets)
            self.srcs[n].packets=traffic#[500, 800, 1000, 1500]

    def generate_more_traffic(self,n, time):
        interarrivals = self.generate_interarrival()
        #time = 0
        traffic = []
        for i in interarrivals:
            time += i
            traffic.append(time)
        self.srcs[n].packets = traffic


    def generate_next_packet(self):
        #generate the next two packets from the two sources
        packets = []
        for i in range(len(self.srcs)):
                t = self.generate_interarrival()
                p = Packet(self.packet_counter, self.srcs[i], self.dest[i],t,self.vcs)
                packets.append(p)
                self.packet_counter +=1
        return packets

    def transmit(self):
        roundCount = 0
        while self.clock < self.sim_duration:
            roundCount += 1
            #print("This is round %d of the simulation at time %d" % (roundCount,self.clock))
            
            #finding minimum on next packets from the two sources
            collision = False
            queueEmpty = False
            

            
            #generating backoff and generating more traffic if needed
            for i in range(len(self.srcs)):
                #if there is no freeze(backoff == -1), generate a backoff
                if self.srcs[i].backoff == -1:
                    self.srcs[i].generate_backoff()
                if len(self.srcs[i].packets) == 0:
                    #generate more packets
                    self.generate_more_traffic(i, self.clock)
            #handling if next arrival is less than clock
            for n in self.srcs:
                if n.packets[0] < self.clock:
                    n.packets[0] = self.clock

            #CHANGE THIS FOR LOOP
            next_packet_time = math.inf
            next_packet_src_index = 0
            temp_backoff = 0
            #initial grab of which index is lower
            for i in range(len(self.srcs)):
                #find next packet time, which is least time
                if len(self.srcs[i].packets) > 0:
                    #print(self.srcs[i].packets[0])
                    #THe current packets next arrivat + difs + backoff
                    curr_packet_sense= self.srcs[i].packets[0]+ parameters.DIFS_DUR+self.srcs[i].backoff
                    #the current latest next packet arrival time + difs + backoff
                    next_packet_sense = next_packet_time + parameters.DIFS_DUR + temp_backoff

                    if curr_packet_sense < next_packet_sense:
                        next_packet_src_index = i
                        next_packet_time = self.srcs[i].packets[0]
                        temp_backoff = self.srcs[i].backoff
                    
                    
                    #if next arrival is equal to each other
                    elif curr_packet_sense == next_packet_sense:
                        '''
                        a = self.srcs[next_packet_src_index].backoff
                        c = self.srcs[i].backoff
                        #print(a)
                        #print(c)
                        if c == a:
                            collision = True
                        elif c < a:
                            next_packet_src_index = i
                            next_packet_time = self.srcs[i].packets[0]
                        '''
                        next_packet_src_index = i
                        #next_packet_time = self.srcs[i].packets[0]
                        collision = True
                        #if not self.vcs and self.hidden:
                        #    collision = False
                    #print(next_packet_time)
                    #handling hidden node topology
                    #if self.hidden and not self.vcs and next_packet_sense <= curr_packet_sense and curr_packet_sense < next_packet_sense + self.srcs[next_packet_src_index].nav - parameters.DIFS_DUR - self.srcs[i].backoff :
                    #    next_packet_src_index = i
                    #    collision = True

            
            if self.hidden:
                next_packet_start = next_packet_time + parameters.DIFS_DUR + self.srcs[next_packet_src_index].backoff
                next_packet_end = next_packet_time + parameters.DIFS_DUR + self.srcs[next_packet_src_index].backoff + self.srcs[next_packet_src_index].nav
                for i in range(len(self.srcs)):
                    #handling hidden node topology
                    
                    if i != next_packet_src_index:
                        curr_packet_start = self.srcs[i].packets[0] + parameters.DIFS_DUR + self.srcs[i].backoff
                        if not self.vcs and next_packet_start <= curr_packet_start and curr_packet_start < next_packet_end :
                            #next_packet_src_index = i
                            collision = True
            

            #
            #print(next_packet_time)
            if next_packet_time == math.inf:
                break
            
            if next_packet_time < self.clock:
                next_packet_time = self.clock
            #print(next_packet_time)
            
            #print(senseTimeout)
            #sense if another packet started difs during sensing period
            if not collision:
                #print("The next packet is from source %s at time %d" % (self.srcs[next_packet_src_index].name,next_packet_time))
                #print(next_packet_time)
                #set clock to next packet time
                
                self.clock = next_packet_time
                #print("Packet arrived/ready for transmission at %d" % self.clock)

                #Sense Timeout = DIFS duration + backoff
                #print("Source %s has a backoff of %d" % (self.srcs[next_packet_src_index].name, self.srcs[next_packet_src_index].backoff))
                senseTimeout = self.clock + parameters.DIFS_DUR + self.srcs[next_packet_src_index].backoff
                if (self.vcs == True):
                    senseTimeout += parameters.RTS + parameters.SIFS_DUR
                    #print("Source %s sent RTS at time %d" %(self.srcs[next_packet_src_index].name, senseTimeout))
                self.sense_busy_medium(senseTimeout, next_packet_src_index)
                #collision = self.isCollision(next_packet_src_index)
                self.clock = senseTimeout
                #handle vcs 
                if(self.vcs == True):
                    self.clock += parameters.CTS + parameters.SIFS_DUR
                    #print("Source %s received CTS at time %d" %(self.srcs[next_packet_src_index].name, self.clock))
                self.clock += parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
                #print("Frame sent at %d" % self.clock)
                self.srcs[next_packet_src_index].tx += 1
                self.srcs[next_packet_src_index].packets.pop(0)
                self.srcs[next_packet_src_index].backoff = -1
                self.srcs[next_packet_src_index].cont_wind = parameters.CW_0
                
            else:
                #print("Handling collision advancing clock by nav and multiplying current contention window by 2")
                self.handle_collision(next_packet_src_index)

        #print(self.clock)
        for i in range(len(self.srcs)):
            print("Source %s:" % self.srcs[i].name)
            print("Successful Transmissions: %d" % self.srcs[i].tx)
            print("Collisions: %d" % self.srcs[i].col)

    def handle_vcs(self):
        self.clock += parameters.RTS + parameters.SIFS_DUR


    def handle_collision(self, index):
        self.clock += self.srcs[index].nav
        later_time = 0
        diff = 0
        for n in self.srcs:
            n.backoff = -1
            n.col += 1
            #CHANGE THIS LINE
            #n.packets = [x + n.nav for x in n.packets]
            n.cont_wind *= 2
            if n.cont_wind >= parameters.CW_MAX:
                n.cont_wind = parameters.CW_MAX
            #if n.packets[0] > later_time and self.hidden:
                #diff = n.packets[0] - later_time
                #later_time = n.packets[0]
        self.clock += diff

    def isCollision(self, p_index):
        for i in range(len(self.srcs)):
            if i != p_index:
                if self.srcs[i].backoff == 0:
                    return True
        return False
            
        
    def sense_busy_medium(self, senseTimeout, p_index):
        #print(senseTimeout)
        #print(p_index)
        for i in range(len(self.srcs)):
            if i != p_index:
                if len(self.srcs[i].packets) > 0 and self.srcs[i].packets[0] < senseTimeout:
                    #print(self.srcs[i].packets[0])
                    #if other packets arrival falls before timeOut
                    #figure out how much backoff is taken/expended
                    #subtract that from generated backoff
                    difference = self.srcs[i].packets[0] + parameters.DIFS_DUR
                    expended_backoff = senseTimeout - (difference)
                    if self.srcs[i].backoff == -1:
                        self.srcs[i].generate_backoff()
                    #print(expended_backoff)
                    #("Source %s backoff is %d" % (self.srcs[i].name, self.srcs[i].backoff))
                    self.srcs[i].backoff -= expended_backoff
                    #print("Source %s backoff freeze is %d" % (self.srcs[i].name, self.srcs[i].backoff))

#plot data
NUM_COLS = "cols"
NUM_TX = "tx"
THROUGHPUT = "throughput"

def main():
    #(self, arrival_rate=1000,vcs=False, sim_duration=2000):
    #for l in parameters.LAMBDA
    num_cols = list()
    num_tx = list()
    throughput = list()
    stats = {}
    stats[NUM_COLS] = num_cols
    stats[NUM_TX] = num_tx
    stats[THROUGHPUT] = throughput
    for i in range(len(parameters.LAMBDA)):
        print("Simulation parameters(Arrival Rate = %d)" % parameters.LAMBDA[i])
        #simduration = 10*100,000
        
        #interarrival = csma.generate_interarrival()
        #print(interarrival)
        #@print(len(interarrival))
        print("CSMA")
        csma = CSMA(parameters.LAMBDA[i], False, parameters.SIM_DUR*100000)
        csma.transmit()
        stats = collect_data(csma,stats,i)

        print("CSMA/VCS")
        csma_vcs = CSMA(parameters.LAMBDA[i], True, parameters.SIM_DUR*100000)
        csma_vcs.transmit()
        stats = collect_data(csma_vcs,stats,i)

        print("CSMA - HIDDEN")
        csma_hidden = CSMA(parameters.LAMBDA[i], False, parameters.SIM_DUR*100000,True)
        csma_hidden.transmit()
        stats = collect_data(csma_hidden,stats,i)

        print("CSMA/VCS - HIDDEN")
        csma_hidden_vcs = CSMA(parameters.LAMBDA[i], True, parameters.SIM_DUR*100000,True)
        csma_hidden_vcs.transmit()
        stats = collect_data(csma_hidden_vcs,stats,i)
    #for k,v in stats.items():
        #print(k)
        #print(v)
    plot_data(stats, 2)


if __name__  == "__main__":
    main()