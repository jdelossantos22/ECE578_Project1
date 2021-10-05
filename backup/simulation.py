import numpy as np
import random as rand

DIFS = 4
SIFS = 2
ACK = 4
FRAME = 100
CW0 = 4
MESSAGE = DIFS + FRAME + SIFS+ACK

messegesAsent = 0
messegesBsent = 0

packets =[[900, 1000, 2000], [800, 1200, 2000]]
i = 0
arrivals = [list(),list()]
for lists in packets:
    temp = 0
    for number in lists:
        temp += number
        arrivals[i].append(temp)
    i += 1

transmissions = [list(), list()]
backoff = rand.randint(0,CW0-1)
transmissions[0][0].append({arrivals[0][0] + DIFS + backoff , backoff})
backoff = rand.randint(0,CW0-1)
transmissions[1][0].append({arrivals[1][0] + DIFS + backoff , backoff})
for i in range(len(arrivals)):
    for j in range(1,len(arrivals[i])):
        backoff = rand.randint(0,CW0-1)
        if arrivals[i][j]-arrivals[i][j-1] > MESSAGE + CW0:
            transmissions[i].append({arrivals[i][j] + DIFS + backoff , backoff})
        else:
            transmissions[i].append({transmissions[i][j-1] + FRAME + SIFS + ACK + DIFS + backoff, backoff})

collisionOffset = 0
collisions = list()

for transmission in transmissions[0]:
    if transmission + collisionOffset in transmissions[1]:
        collisions.append(transmission)
        collisionsOffset = FRAME + SIFS + ACK + DIFS
        indexA = transmissions[0].index(transmissions)
        indexB = transmissions[1].index(transmissions)
        backoff = rand.randint(0,CW0-1)
        transmissions[0].insert({indexA+1,MESSAGE+backoff,backoff})
        transmissions[1].insert




    