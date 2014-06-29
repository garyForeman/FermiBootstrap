FermiBootstrap
==============

Author: Gary Foreman  
email: gforema2@illinois.edu  
[Fermi Gamma-ray Space Telescope data access](http://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi)

Requirements
------------
- numpy
- pyfits


Serial
------

`gtbootstrap.py` generates a user specified number of bootstrapped realizations
of a user specified Fermi photon file. Code also includes capability to perform
energy filtering such that the bootstrapped files need not contain photons you
will throw away when you run `gt_apps.filter`.

Example
```bash
$ ./gtbootstrap.py -h
usage: gtbootstrap.py [-h] [--emin <min_energy>] [--emax <max_energy>]
                      <path> <realizations>

Produce bootstrap samples of a Fermi photon file list.

positional arguments:
  <path>               The fits file you wish to bootstrap
  <realizations>       Number of bootstrap realizations you wish to generate

optional arguments:
  -h, --help           show this help message and exit
  --emin <min_energy>  Lower energy bound you wish to filter (MeV)
  --emax <max_energy>  Upper energy bound you wish to filter (MeV)

```

This will create 10 realizations of `L1406121050095451CC7F93_PH00.fits` with 
photons in the energy range of 200 MeV to 20 GeV. The realizations are named 
`L1406121050095451CC7F93_PH00_bs_[0-9].fits`:

```bash
$ ./gtbootstrap.py L1406121050095451CC7F93_PH00.fits 10 --emin 200.0 --emax 20000.0
```


Parallel
--------

`gtbootstrap_mp.py` generates a user specified number of bootstrapped
realizations of a list of Fermi photon files. This code is a parallel wrapper
for the gtbootstrap.py code and distributes work by calling the gtbootstrap
function with a different photon file name for each thread. This means, in its
current version, this code will not benefit from using more processors, `N_p`,
than number of photon files, `N_f`; the extra `N_p - N_f` threads would remain
idle.  If you wish, for exampe, to use 20 threads to generate 20 realizations
of 10 photon files, I recommend running one instance of `gtbootstrap_mp.py` to
generate the first 10 realizations on 10 processors, and a second instance to
generate the next 10 realization on 10 separate processors. If you wish to do
this, make sure you use two separate run directories to avoid name conflicts of
the output files.

Example
```bash
$ ./gtbootstrap_mp.py -h
usage: gtbootstrap_mp.py [-h] [--emin <min_energy>] [--emax <max_energy>]
                         <jobs> <path> <realizations>

Multithreaded wrapper for the gtbootstrap function. Parses command line
arguments, and devides work based on the number of photon files given in the
events list.

positional arguments:
  <jobs>               The number of threads you wish to use.
  <path>               File containing your list of photon files.
  <realizations>       Number of bootstrap realizations you wish to generate.

optional arguments:
  -h, --help           show this help message and exit
  --emin <min_energy>  Lower energy bound you wish to filter (MeV).
  --emax <max_energy>  Upper energy bound you wish to filter (MeV).
```

This will create 10 realizations of each of the photon files listed in
`SMC_70m_events.list` with photons in the energy range of 200 MeV to 20 GeV. 
The task will create pool of nine parallel threads (one per photon file). :

```bash
$ ./gtbootstrap_mp.py 9 SMC_70m_events.list 10 --emin 200. --emax 20000.
```

The content of `SMC_70m_events.list` is:

```
<PATH>/L1406121050095451CC7F93_PH00.fits
<PATH>/L1406121050095451CC7F93_PH01.fits
<PATH>/L1406121050095451CC7F93_PH02.fits
<PATH>/L1406121050095451CC7F93_PH03.fits
<PATH>/L1406121050095451CC7F93_PH04.fits
<PATH>/L1406121050095451CC7F93_PH05.fits
<PATH>/L1406121050095451CC7F93_PH06.fits
<PATH>/L1406121050095451CC7F93_PH07.fits
<PATH>/L1406121050095451CC7F93_PH08.fits
```
