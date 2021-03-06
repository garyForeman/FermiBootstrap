#! /usr/bin/env python

#
# Author: Gary Foreman
# Last Modified: June 13, 2014
# Selects a random sample of photons from the Fermi photon list, and writes
# them to new fits files
#

from __future__ import print_function

import numpy as np
import os
import pyfits
import sys


NAXIS2 = 'NAXIS2'


def bootstrap_realization(realization, filename, photonList, photonData,
                          counts):
    """Create random samples of the photon list and write them to fits files"""

    np.random.seed()
    indices = np.random.randint(0, counts, size=counts)
    photons = np.sort(photonList[indices])
    bootstrapHDU = pyfits.BinTableHDU(photonData[1].data[photons],
                                      photonData[1].header)

    bootstrapHDU.header[NAXIS2] = counts
    bootstrapList = pyfits.HDUList([photonData[0], bootstrapHDU,
                                    photonData[2]])
    # Here we assume filename ends in .fits
    fn, ext = os.path.splitext(filename)
    outfile = '%s_bs_%d%s' % (fn, realization, ext)

    if os.path.isfile(outfile):
        os.remove(outfile)

    bootstrapList.writeto(outfile)


def gtbootstrap(filename, realizationNumber, emin=100., emax=300000.):
    """Function for creating bootstrapped realizations from a Fermi photon
    fits file (filename). Performs realizationNumber realizations, and writes
    each to a separate fits file. This function has the ability to perform
    energy filtering so that bootstrapped samples do not include photons that
    will be filtered by gt_apps.filter anyway. The default energy range is
    100 MeV to 300 GeV, which is the default energy range used for Fermi
    database queries."""

    photonList = np.array([], dtype=np.int32)
    counts = 0

    try:
        with pyfits.open(filename) as photonData:
            # Create a list of photons that are within the energy limits
            for i in range(photonData[1].header[NAXIS2]):
                energy = photonData[1].data[i]["ENERGY"]
                if energy >= emin and energy <= emax:
                    photonList = np.append(photonList, i)
                    counts += 1

            for realization in xrange(realizationNumber):
                bootstrap_realization(realization, filename, photonList,
                                      photonData, counts)

    except Exception:
        print("ERROR:", filename, "not found", file=sys.stderr)
        return

if __name__ == "__main__":
    import argparse as ap

    helpString = "Produce bootstrap samples of a Fermi photon file list."
    parser = ap.ArgumentParser(description=helpString)
    parser.add_argument(
        "filename", help="The fits file you wish to bootstrap",
        metavar='<path>')
    parser.add_argument(
        "realizationNumber", type=int,
        help="Number of bootstrap realizations you wish to generate",
        metavar='<realizations>')
    parser.add_argument(
        "--emin", type=float, default=100.,
        help="Lower energy bound you wish to filter (MeV)",
        metavar='<min_energy>')
    parser.add_argument(
        "--emax", type=float, default=300000.,
        help="Upper energy bound you wish to filter (MeV)",
        metavar='<max_energy>')

    args = parser.parse_args()

    gtbootstrap(args.filename, args.realizationNumber, args.emin, args.emax)
