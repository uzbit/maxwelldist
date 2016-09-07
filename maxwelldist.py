#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

# Constants
BOLTZMANN_K = 1.3806488e-23 # J/K
H_MASS = 1.673534e-27 # Mass of hydrogen atom (Kg)

# Variables
TEMP = 600 # Kelvin
ATOMS_MASS = 1*H_MASS # Kg
NUM_ATOMS = 20000 
MAX_SPEED = 10000 # Velocity is a vector, speed (m/s) is magnitude of that vector. 
ATOMS_PER_BIN = 100

def MaxwellSpeedDist(s, m, T):
    # See wikipedia: https://en.wikipedia.org/wiki/Maxwell%E2%80%93Boltzmann_distribution
    s2 = s*s
    twokT = 2 * BOLTZMANN_K * T
    coeff = 4 * np.pi * (m / (np.pi * twokT)) ** (3./2.)
    return coeff * s2 * np.exp(-m * s2 / (twokT))
    
def theorySpeedDist():
    tsd = list()
    spds = list()
    for s in xrange(0, MAX_SPEED, 1):
        tsd.append(MaxwellSpeedDist(s, ATOMS_MASS, TEMP))
        spds.append(s)
    
    pctCovered = sum(tsd)
    print "Sanity check: ", pctCovered, pctCovered >= 0.99 
    return spds, tsd
    
def MCSpeedDist(maxProb):
    count = 0
    mcsd = list()
    while (len(mcsd) < NUM_ATOMS):
        s = np.random.random() * MAX_SPEED
        prob = MaxwellSpeedDist(s, ATOMS_MASS, TEMP)
        
        if np.random.random() * maxProb <= prob:
            mcsd.append(s)
        count += 1
    
    print "MC Loops: %d, Loops/Particle: %f" % (count, float(count)/NUM_ATOMS)
    return mcsd
    
def main():
    spds, tsd = theorySpeedDist()
    mcsd = MCSpeedDist(max(tsd))
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.hist(mcsd, bins = NUM_ATOMS/ATOMS_PER_BIN)
    ax2.plot(spds, ATOMS_PER_BIN*np.array(tsd), 'r-')
    plt.show()
  
if __name__ == "__main__":
    main()

