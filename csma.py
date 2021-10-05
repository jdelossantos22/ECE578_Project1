
import numpy as np
import random
import parameters
import math

class Node:
    def __init__(self, id, name, vcs=False):
        self.id = id
        self.name = name
        self.cont_wind = parameters.CW_0

    def generate_backoff(self):
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
    def __init__(self, arrival_rate=100,vcs=False, sim_duration=300):
        self.clock = 0
        self.arrival_rate = arrival_rate
        self.sim_duration = sim_duration
        self.vcs = False
        self.packet_counter = 0
        self.srcs = []
        self.dest = []
        self.nodes = []
        self.medium = []
        self.srcs.append(Node(0,"A", self.vcs))
        self.srcs.append(Node(1,"C", self.vcs))
        self.dest.append(Node(3,"B", self.vcs))
        self.dest.append(Node(4,"D", self.vcs))
        for i in range(len(self.srcs)):
            self.nodes.append(self.srcs[i])
            self.nodes.append(self.dest[i])


    def advance_time(self):
        pass
    
    def generate_interarrival(self):
        #uncomment code when ready for exponential distro
        # np.random.exponential(1/(parameters.SLOT_DUR*200), int(1/(parameters.SLOT_DUR*200))*10)
        #final form
        #interarrivals = math.floor(np.random.exponential(1/(parameters.SLOT_DUR*self.arrival_rate)), int(1/(parameters.SLOT_DUR*200))*10)

        #testing 
        #interarrivals = math.floor(np.random.exponential(1/(parameters.SLOT_DUR*self.arrival_rate)), 5)
        interarrivals = [100, 100, 100]
        interarrivals = [math.floor(x) for x in interarrivals]
        return interarrivals

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
        while self.clock < self.sim_duration:
            packets = self.generate_next_packet()
            self.medium += packets
            p_time = math.inf
            p_index = 0

            for i in range(len(packets)):
                if(packets[i].t_arrival < p_time):
                    p_time = packets[i].t_arrival
                    p_index = i
            #[p.t_arrival for p in packets]#next_arrival = min(p_time)
            print(p_time)
            self.clock += p_time
            print("Next Arrival is %d from Node %s" % (self.clock, packets[i].src.name))
            #packets[p_index].src.generate_backoff()
            #timeout = parameters.DIFS_DUR+packets[p_index].src.backoff
            #print("DIFS + backoff is %d" % timeout)
            print("DIFS commenced at Node %s at time %d" % (packets[p_index].src.name, self.clock))
            self.clock += parameters.DIFS_DUR
            print("DIFS commenced at Node %s at time %d" % (packets[p_index].src.name, self.clock))
            self.sense_busy_medium(packets[p_index])
            #starting sensing period
            '''
            for i in range(timeout):
                for other in packets:
                    if other != packets[p_index]:
                        #if self.

                self.clock += 1
                timeout -= 1
            '''

        
    def sense_busy_medium(self,packet):
        for other in self.medium:
            if other != packet:
                if other.t_arrival < self.clock:
                    pass



    


def main():
    csma = CSMA()
    interarrival = csma.generate_interarrival()
    print(interarrival)
    #csma.transmit()


if __name__  == "__main__":
    main()