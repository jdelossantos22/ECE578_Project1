import simpy
import parameters
import random

class Node:
    def __init__(self, env, id, name, src, dest, vcs=False):
        self.env = env
        self.id = id
        self.name = name
        self.backoff = -1
        self.isSensing = False
        self.cont_window = parameters.CW_0
        self.vsc = vcs
        self.prevArrival = 0
        #CSMS
        #DIFS + BACKOFF + FRAME + SIFS + ACK
        self.nav = parameters.FRAME_SIZE + parameters.SIFS_DUR + parameters.ACK
        if vcs == True:
            self.nav += parameters.RTS + parameters.SIFS + parameters.CTS
        #CSMS/CA VCS
        #DIFS + BACKOFF + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK

    def send(self):
        difs = parameters.DIFS_DUR
        if self.backoff = -1:
            self.backoff = randint(0, self.cont_window-1)
        senseTimeout = difs + self.backoff
        while True:
            try:
                while senseTimeout > 0: #difs + backoff period sensing channell
                    print("Node %s is sensing" % self.name)
                    yield(self.env.timeout(1))
                    senseTimeout -= 1
                    if (self.env.now < senseTimeout):
                        self.backoff -= 1
                print("Channel was idle")
                self.env.process(self.send_frame()) #channel idle, sending fram
                self.env.timeout(parameters.SIFS_DUR) #sifs dur wait for ack
                self.env.process(self.receive_ack()) #ack received
                self.backoff = -1


            except simpy.Interrupt:
                self.env.timeout(self.nav)
                if self.backoff == 0:
                    self.backoff = random.randint(0,self.cont_window-1)
                    timeout = parameters.DIFS_DUR + self.backoff
                elif timeout > backoff:
                    timeout = parameters.DIFS_DUR + backoff
                
                else:
                    backoff = timeout
                    timeout = parameters.DIFS_DUR + backoff
                continue

    def send_frame(self):
        print("Node %s starts sending frame at %d" % (self.name, self.env.now))
        self.env.timeout(parameters.FRAME_SIZE)
        print("Frame sent to %s at %d. Wait for ACK" % (self.dest.name, self.env.now))
    
    def receive_ack(self):
        self.env.timeout(parameters.ACK)
        print("Received ACK at %d" % self.env.now)
