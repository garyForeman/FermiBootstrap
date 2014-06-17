#! /usr/bin/env python

################################################################################
#Author: Gary Foreman
#Last Modified: June 16, 2014
#Multithreaded wrapper for gtbootstrap. Note threading is performed across 
#photon files, NOT across the number of realizations. This code will not benefit
#from using more processes than the number of photon files listed in your events
#list. If you want to split work across number of realizations, I recommend
#submitting multiple instances of this code in separate run directories to 
#avoid filenaming conflicts.
################################################################################

import argparse
import itertools as it
from multiprocessing import Pool
from gtbootstrap import gtbootstrap

def argumentReduce(argIterator):
    """Reduces the number of arguments for the function used by Pool. The first
    element of argList is the filename, the second is the realizationNumber,
    followed by emin and emax."""
    gtbootstrap(*argIterator)

def gtbootstrap_mp():
    helpString = "Multithreaded wrapper for the gtbootstrap function. " + \
                 "Parses command line arguments, and devides work based on " + \
                 "the number of photon files given in the events list."

    parser = argparse.ArgumentParser(description=helpString)
    parser.add_argument("jobs", type=int, 
                        help="The number of threads you wish to use.")
    parser.add_argument("eventsList", 
                        help="File containing your list of photon files.")
    parser.add_argument("realizationNumber", type=int,
                        help="Number of bootstrap realizations you wish to " + \
                             "generate.")
    parser.add_argument("emin", type=float, default=100., 
                         help="Lower energy bound you wish to filter.")
    parser.add_argument("emax", type=float, default=300000.,
                        help="Upper energy bound you wish to filter.")
    args = parser.parse_args()

    with open(args.eventsList) as evtsFile:
        photonFiles = evtsFile.readlines()

    numFiles = len(photonFiles)

    for i in xrange(numFiles): 
        photonFiles[i] = photonFiles[i].replace("\n", "")

    iterator = it.izip(photonFiles, it.repeat(args.realizationNumber),
                       it.repeat(args.emin), it.repeat(args.emax))

    pool = Pool(processes = args.jobs)
    pool.map(argumentReduce, iterator, chunksize=1)
    pool.close()

if __name__ == '__main__':
    gtbootstrap_mp()
