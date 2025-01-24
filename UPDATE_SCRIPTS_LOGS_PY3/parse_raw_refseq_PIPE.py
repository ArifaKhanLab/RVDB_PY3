#!/usr/bin/env python3

import sys
import gzip
import os
import re

#### Jaysheel: adding os.path + #!
#### using os.path.join instead string concat using +

homedir = sys.argv[1]
scriptdir = os.path.join(homedir, 'UPDATE_SCRIPTS_LOGS')
datetag = sys.argv[2]
currentvs = sys.argv[3]
refseq_viral_zipfilenames = sys.argv[4:]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
refseqdir = os.path.join(wdir, 'RefSeq_raw_data_' + datetag)
logdir = os.path.join(refseqdir, 'log')


refseq_viral_zipfilenames = [os.path.join(refseqdir, refseq_viral_zipfilename) for refseq_viral_zipfilename in
                             refseq_viral_zipfilenames]

#### Jaysheel: duplicate found in line 14
# logdir = os.path.join(refseqdir, 'log')

####################################################################################################
######## Simple function to reformat a raw NCBI Viral fast file to have 2 lines /entry      ########
######## and output two files, phage and eukaryotic viral + archaea                         ########
####################################################################################################
def parse_raw_refseqviral(refseq_viral_unzipfilename):
    ##    print 'parsing '+raw_ncbi_viral_filename+' into phage and eukaryotic viral + archael sequences'
    outf1_name = os.path.join(refseqdir, 'viral.genomic.eukviral.fasta')
    outf2_name = os.path.join(refseqdir, 'viral.genomic.phage.fasta')

    logf.write('Refseq viral unzip filename for eukaryotic entries: ' + outf1_name + '\n')
    logf.write('Refseq viral unzip filename for phage entries: ' + outf2_name + '\n')

    outf1 = open(outf1_name, 'w')
    outf2 = open(outf2_name, 'w')

    phage_names_fn = os.path.join(logdir, 'phage_kws.txt')
    phage_names_inf = open(phage_names_fn, "r")

    #### Jaysheel:  make sure each file read is striped of new line char and extra spaces.
    phage_names = phage_names_inf.read().strip().split('\n')
    # phage_names = list(map(lambda x: x.rstrip(), phage_names_inf.readlines()))
    phage_names_inf.close()

    p = 0
    e = 0

    eukviralaccs = []
    phageaccs = []

    #### Jaysheel:  add file mode
    inf = open(refseq_viral_unzipfilename, "r")
    phage = False
    seq = ''

    for i, line in enumerate(inf):
        if i == 0:
            header = line.strip()
            acc = header.split('|')[2]
            for phage_name in phage_names:
                # replace "in" with regex so that the keyword is found at the start of the word in
                # in the header and not a substring.
                if phage_name in header.lower():
                    phage = True
                    break
            continue
        if line.startswith('>'):
            if phage:
                outf2.write(header + '\n' + seq + '\n')
                p += 1
                phageaccs.append(acc)
                phage = False
            else:
                outf1.write(header + '\n' + seq + '\n')
                e += 1
                eukviralaccs.append(acc)
                phage = False

            header = line.strip()
            acc = header.split('|')[2]
            seq = ''

            for phage_name in phage_names:
                # replace "in" with regex so that the keyword is found at the start of the word in
                # in the header and not a substring.
                if phage_name in header.lower():
                    phage = True
                    break
        else:
            seq += line.strip()

    if phage:
        outf2.write(header + '\n' + seq + '\n')
        p += 1
    else:
        outf1.write(header + '\n' + seq + '\n')
        e += 1

    inf.close()

    ##    print "read and reformatted "+str(e)+" eukaryotic viral + archaeal viral sequences"
    ##    print "read and reformatted "+str(p)+" phage sequences"
    outf1.close()
    outf2.close()

    outf3 = open(os.path.join(refseqdir, 'viral.genomic.eukviral.accs.txt'), 'w')
    outf4 = open(os.path.join(refseqdir, 'viral.genomic.phage.accs.txt'), 'w')

    outf3.write('\n'.join(eukviralaccs))
    outf4.write('\n'.join(phageaccs))

    logf.write(
        str(len(eukviralaccs)) + ' eukaryotic viral entries and ' + str(len(phageaccs)) + ' phage entries' + '\n')

    outf3.close()
    outf4.close()

logf = open(os.path.join(logdir, 'unzip_log_refseqviral.txt'), 'w')
logf.write('RefSeq viral zipfilenames: ' + ','.join(refseq_viral_zipfilenames) + '\n')

refseq_viral_unzipfilename = os.path.join(refseqdir, 'viral.genomic.fna')
unzipf = open(refseq_viral_unzipfilename, 'w')
logf.write('RefSeq viral unzipfilename: ' + refseq_viral_unzipfilename + '\n')

for fn in refseq_viral_zipfilenames:
    seq = ''
    #### Jaysheel: Add with, convert bytes arr to str using decode()
    with gzip.open(fn, 'rb') as fh:
        for i, line in enumerate(fh):
            line = line.decode()
            if line.startswith('>'):
                if not i == 0:
                    unzipf.write(header + '\n' + seq + '\n')
                    seq = ''
                sl = line.strip().split()
                acc = sl[0].split('>')[1]
                desc = ' '.join(sl[1:])
                header = '>acc|REFSEQ|' + acc + '|' + desc
            else:
                seq += line.strip()
    unzipf.write(header + '\n' + seq + '\n')
unzipf.close()

parse_raw_refseqviral(refseq_viral_unzipfilename)
logf.close()