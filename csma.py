
import numpy as np
import random
import parameters
import math

class Node:
    def __init__(self, id, name, vcs=False):
        self.id = id
        self.name = name
        self.cont_wind = parameters.CW_0
        self.packets = []
        self.backoff = -1
        self.nav = parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
        if vcs == True:
            self.nav += parameters.RTS + parameters.SIFS_DUR*2 + parameters.CTS

    def generate_backoff(self):
        print("Source %s has a contention window of %d" % (self.name,self.cont_wind))
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
    def __init__(self, arrival_rate=1000,vcs=False, sim_duration=2000):
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
            print(traffic)
            self.srcs[n].packets = [500, 800, 1000, 1500]#traffic
        


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
            print("This is round %d of the simulation at time %d" % (roundCount,self.clock))
            next_packet_time = math.inf
            next_packet_src_index = -1
            #finding minimum on next packets from the two sources
            collision = False
            for i in range(len(self.srcs)):
                
                if len(self.srcs[i].packets) and self.srcs[i].packets[0] < next_packet_time:
                   
                    next_packet_src_index = i
                    next_packet_time = self.srcs[i].packets[0]
                    #print(next_packet_time)
            #
            print("The next packet is from source %s at time %d" % (self.srcs[next_packet_src_index].name,next_packet_time))
            #print(next_packet_time)
            #set clock to next packet time
            self.clock = next_packet_time
            print("Packet arrived/ready for transmission at %d" % self.clock)
            #generate backoff of source

            if self.srcs[next_packet_src_index].backoff == -1:
                self.srcs[next_packet_src_index].generate_backoff()
            #Sense Timeout = DIFS duration + backoff
            print("Source %s has a backoff of %d" % (self.srcs[next_packet_src_index].name, self.srcs[next_packet_src_index].backoff))
            senseTimeout = self.clock + parameters.DIFS_DUR + self.srcs[next_packet_src_index].backoff
            print(senseTimeout)
            #sense if another packet started difs during sensing period
            self.sense_busy_medium(senseTimeout, next_packet_src_index)

            collision = self.isCollision(next_packet_src_index)
            self.clock = senseTimeout

            
            '''
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
            if not collision:
                self.clock += parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
                print("Frame sent at %d" % self.clock)

                self.srcs[next_packet_src_index].packets.pop(0)
                self.srcs[next_packet_src_index].backoff = -1
            else:
                print("Handling collision advancing clock by nav and multiplying current contention window by 2")
                self.handle_collision()

    def handle_collision(self):
        self.clock += self.srcs[0].nav
        for n in self.srcs:
            n.packets = [x + n.nav for x in n.packets]
            n.cont_wind *= 2

    def isCollision(self, p_index):
        for i in range(len(self.srcs)):
            if i != p_index:
                if self.srcs[i] == 0:
                    return True
        return False
            
        
    def sense_busy_medium(self, senseTimeout, p_index):
        for i in range(len(self.srcs)):
            if i != p_index:
                if self.srcs[i].packets[0] < senseTimeout:
                    #if other packets arrival falls before timeOut
                    #figure out how much backoff is taken/expended
                    #subtract that from generated backoff
                    expended_backoff = senseTimeout - (self.srcs[i].packets[0] + parameters.DIFS_DUR)
                    self.srcs[i].generate_backoff()
                    print("Source %s backoff is %d" % (self.srcs[i].name, self.srcs[i].backoff))
                    self.srcs[i].backoff -= expended_backoff
                    print("Source %s backoff is %d" % (self.srcs[i].name, self.srcs[i].backoff))


    


def main():
    #(self, arrival_rate=1000,vcs=False, sim_duration=2000):
    csma = CSMA(parameters.LAMBDA[0], False, parameters.SIM_DUR*10000)
    #interarrival = csma.generate_interarrival()
    #print(interarrival)
    #@print(len(interarrival))
    csma.transmit()
    '''
    csma.generate_traffic()
    print("Source A traffic:")
    print(csma.srcs[0].packets)
    print("Source C traffic:")
    print(csma.srcs[1].packets)
    '''


if __name__  == "__main__":
    main()