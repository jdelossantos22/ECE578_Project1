import simpy
import parameters
import random
import numpy as np
import math

class Node:
    def __init__(self, env, id, name, arr_rate, vcs=False):
        self.env = env
        self.id = id
        self.name = name
        self.backoff = -1
        self.isSensing = False
        self.cont_window = parameters.CW_0
        self.vsc = vcs
        self.prevArrival = 0
        self.arr_rate = arr_rate
        self.isSending = False
        #self.sendInterrupt = self.env.process(self.send())
        
        #CSMS
        #DIFS + BACKOFF + FRAME + SIFS + ACK
        self.nav = parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
        if vcs == True:
            self.nav += parameters.RTS + parameters.SIFS + parameters.CTS
        #CSMS/CA VCS
        #DIFS + BACKOFF + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK

    def send(self, other_src, dest):
       # self.env.timeout(10)
        self.arrival = self.env.now
        print("Packet Arrive at %s at %d" % (self.name, self.env.now))
        
        difs = parameters.DIFS_DUR
        if self.backoff == -1:
            self.backoff = random.randint(0, self.cont_window-1)
        print("%s backoff is %d" % (self.name, self.backoff))
        senseTimeout = difs + self.backoff
        #print("hEre")
        while True:
            try:
            
                while senseTimeout > 0: #difs + backoff period sensing channell
                    print("Node %s is sensing" % self.name)
                    yield self.env.timeout(1)
                    time = self.env.now
                    #print(senseTimeout)
                    senseTimeout -= 1
                    if (self.env.now < senseTimeout):
                        self.backoff -= 1
                    if (other_src.isSending == True and self.backoff != other_src.backoff):
                        self.env.timeout(other_src.nav)
                        print(self.backoff)
                        print(other_src.backoff)
                        print("%s: Other src is sending. Pausing TX at %d" % (self.name, time))
                        #self.env.process(self.send()).interrupt()
                        return
                    
                    
                    
                
                #print("Channel was idle")
                #print(self.env.now)
                #print("Node %s starts sending frame at %d" % (self.name, self.env.now))
                #self.env.process.interrupt()
                
                self.env.process(self.send_frame(dest)) #channel idle, sending fram
                yield self.env.timeout(parameters.SIFS_DUR) #sifs dur wait for ack
                self.env.process(self.receive_ack()) #ack received
                self.backoff = -1
                self.isSending = False
                return

        
            except simpy.Interrupt:
                #print("INterrupt")
                #self.env.timeout(self.nav)
                if self.backoff == 0:
                    self.backoff = random.randint(0,self.cont_window-1)
                    timeout = parameters.DIFS_DUR + self.backoff
                elif timeout > backoff:
                    timeout = parameters.DIFS_DUR + backoff
                
                else:
                    backoff = timeout
                    timeout = parameters.DIFS_DUR + backoff
                continue
        
            

    def send_frame(self, dest):
        print("Frame sent to %s at %d. Wait for ACK" % (dest.name, self.env.now))
        self.isSending = True
        self.sentTime = self.env.now
        yield self.env.timeout(parameters.FRAME_SIZE)
        
    
    def receive_ack(self):
        yield self.env.timeout(parameters.ACK)
        print("Received ACK at %d" % self.env.now)

    def generate_interarrival(self):
        return np.random.exponential(1/self.arr_rate)
