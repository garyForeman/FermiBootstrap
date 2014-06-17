#! /usr/bin/env python

################################################################################
#Author: Gary Foreman
#Last Modified: June 13, 2014
#Selects a random sample of photons from the Fermi photon list, and writes them
#to new fits files
################################################################################

import numpy as np
import os
import pyfits

def gtbootstrap(filename, realizationNumber, emin=100., emax=300000.):
    """Function for creating bootstrapped realizations from a Fermi photon
    fits file (filename). Performs realizationNumber realizations, and writes
    each to a separate fits file. This function has the ability to perform 
    energy filtering so that bootstrapped samples do not include photons that
    will be filtered by gt_apps.filter anyway. The default energy range is
    100 MeV to 300 GeV, which is the default energy range used for Fermi
    database queries."""

    try:
        photonData = pyfits.open(filename)
    except:
        print "ERROR:", filename, "not found"
        return

    photonList = np.array([], dtype=np.int32)
    counts = 0

    #Create a list of photons that are within the energy limits
    for i in range(photonData[1].header["NAXIS2"]):
        energy = photonData[1].data[i]["ENERGY"]
        if energy >= emin and energy <= emax:
            photonList = np.append(photonList, i)
            counts += 1

    #Create random samples of the photon list and write them to fits files
    for realization in xrange(realizationNumber):
        np.random.seed()
        indices = np.random.randint(0, counts, size=counts)
        bootstrapHDU = \
            pyfits.BinTableHDU(photonData[1].data[np.sort(photonList[indices])],
                               photonData[1].header)
        bootstrapHDU.header["NAXIS2"] = counts
        bootstrapList = pyfits.HDUList([photonData[0], bootstrapHDU, 
                                        photonData[2]])
        #Here we assume filename ends in .fits
        outfile = filename[:-len(".fits")] + "_bs_" + str(realization) + \
                  filename[-len(".fits"):]
        if os.path.isfile(outfile): os.remove(outfile)
        bootstrapList.writeto(outfile)

    photonData.close()

if __name__ == "__main__":
    import argparse as ap

    helpString = "Produce bootstrap samples of a Fermi photon file list."
    parser = ap.ArgumentParser(description=helpString)
    parser.add_argument("filename", help="The fits file you wish to bootstrap")
    parser.add_argument("realizationNumber", type=int, 
                        help="Number of bootstrap realizations you wish to " + \
                             "generate")
    parser.add_argument("emin", type=float, default=100., 
                        help = "Lower energy bound you wish to filter.")
    parser.add_argument("emax", type=float, default=300000.,
                        help = "Upper energy bound you wish to filter.")

    args = parser.parse_args()

    gtbootstrap(args.filename, args.realizationNumber, args.emin, args.emax)
