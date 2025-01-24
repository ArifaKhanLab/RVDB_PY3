#!/usr/bin/env python3

#### Jaysheel: adding os.path + #!
#### using os.path.join instead string concat using +

import sys
import gzip
import os

homedir = sys.argv[1]
date = sys.argv[2]
currentvs = sys.argv[3]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
refseqdir = os.path.join(wdir, 'RefSeq_raw_data_' + date)

zipfilenames = sys.argv[4:-1]
zipfilenames = [os.path.join(refseqdir, zipfilename) for zipfilename in zipfilenames]
unzipfn = os.path.join(refseqdir, sys.argv[-1])

unzipf = open(unzipfn, 'w')
for zipfilename in zipfilenames:
    fh = gzip.open(zipfilename, 'rb')
    for i, line in enumerate(fh):
        #### Jaysheel: convert bytes array to string using decode
        line = line.decode()
        unzipf.write(line)

    fh.close()
unzipf.close()

print(unzipfn)
