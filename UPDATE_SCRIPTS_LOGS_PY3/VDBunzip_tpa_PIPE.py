#!/usr/bin/env python3

import gzip
import sys
import os

homedir = sys.argv[1]
datetag = sys.argv[2]
currentvs = sys.argv[3]
tpafiletag = sys.argv[4]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
tpadir = os.path.join(wdir, 'TPA_raw_data_' + datetag)
print(tpadir)

logf = open(os.path.join(tpadir, 'log', 'unzip_log_tpa.txt'), 'w')

logf.write('raw data download directory: ' + wdir + '\n')
logf.write('tpafiletag: ' + tpafiletag + '\n')
logf.write('datetag: ' + datetag + '\n')
logf.write('begin unzipped TPA filenames\n')

unzipfilenames = []

for fn in os.listdir(tpadir):
    if not tpafiletag in fn or not fn.endswith('.gz'):
        continue
    if not fn == 'tpa_cu.fsa_nt.gz':
        continue

    print(fn)

    unzipfn = fn.replace('.gz', '.seq.' + datetag)
    unzipfilenames.append(unzipfn)
    unzipf = open(os.path.join(tpadir, unzipfn), 'w')

    seq = ''
    c = 0

    #### Jaysheel: open file using with, convert bytes to str using decode
    with gzip.open(os.path.join(tpadir, fn), 'rb') as fh:
        for i, line in enumerate(fh):
            line = line.decode()
            if line.startswith('>'):
                if i != 0:
                    unzipf.write(header + '\n' + seq + '\n')
                    seq = ''

                sl = line.strip().split()
                acc = sl[0].split('>')[1]
                desc = ' '.join(sl[1:])
                header = '>acc|TPA|' + acc + '|' + desc
            else:
                seq += line.strip()
            if i - c == 1000000:
                print(i)
                c = i

    unzipf.write(header + '\n' + seq + '\n')
    unzipf.close()

for unzipfn in unzipfilenames:
    logf.write(unzipfn)
    print(unzipfn)
