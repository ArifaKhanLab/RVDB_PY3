#!/usr/bin/env python3

import sys
import gzip
import os
#### Jaysheel: need to install BioPython package
# sys.path.append('C:\\Python27\\Lib\\site-packages')
from Bio import SeqIO

homedir = sys.argv[1]
datetag = sys.argv[2]
currentvs = sys.argv[3]
gzfiletag = sys.argv[4]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
gbdir = os.path.join(wdir, 'GenBank_raw_data_' + datetag)
refseqdir = os.path.join(wdir, 'RefSeq_raw_data_' + datetag)

logf = open(os.path.join(gbdir, 'log', 'unzip_log_gb.txt'), 'w')

logf.write('raw data download directory: ' + gbdir + '\n')
logf.write('gzfiletag: ' + gzfiletag + '\n')
logf.write('datetag: ' + datetag + '\n')
logf.write('begin unzipped filenames\n')

unzipfilenames = []
neighboraccs_filename = os.path.join(refseqdir, 'neighbor_accs.txt')

#### Jaysheel: add file mode and clean up line split
inf = open(neighboraccs_filename, "r")
# neighbors = set(inf.read().strip().split('\n'))
neighbors = set(list(map(lambda x: x.strip(), inf.readlines())))
inf.close()

for fn in os.listdir(gbdir):
    if not fn.startswith(gzfiletag) or not fn.endswith('.gz'):
        continue

    unzipfn = fn.replace('.gz', '.' + datetag)

    logf.write(unzipfn + '\n')

    unzipfilenames.append(unzipfn)
    unzipf = open(os.path.join(gbdir, unzipfn), 'w')
    
    ### Pei-Ju: Remove "encoding='latin-1'" to avoid the error occurred by running the script under Windows
    #with gzip.open(os.path.join(gbdir, fn), 'rt', encoding='latin-1') as fh:
    #with gzip.open(os.path.join(gbdir, fn), 'rt') as fh:
    #with gzip.open(os.path.join(gbdir, fn), 'rt', encoding='UTF-16') as fh:
    with gzip.open(os.path.join(gbdir, fn), 'rt', encoding='latin-1') as fh:
        for g, gb_record in enumerate(SeqIO.parse(fh, 'genbank')):
            acc = gb_record.annotations['accessions'][0]
            organism = gb_record.annotations['organism']
            tax_line = ("; ").join(gb_record.annotations['taxonomy'])
            feat = gb_record.features
            disc = gb_record.description
            seqlen = len(gb_record)
            #### old way removed as of BioPython v1.73
            #seq = gb_record.seq.tostring()
            #### as of BioPython v1.45
            seq = str(gb_record.seq)
            acc = gb_record.id
            source = gb_record.annotations['source']
            key = gb_record.annotations['keywords']
            file_type = gb_record.annotations['data_file_division']
            date = gb_record.annotations['date']

            if acc.split('.')[0] in neighbors:
                db = 'NEIGHBOR'
            else:
                db = 'GENBANK'

            #### Jaysheel
            #### Explisitly add "." at the end of
            header = '>acc|' + db + '|' + acc + '|' + disc + '|' + organism + '|' + file_type + '|' + date
            unzipf.write(header + '\n' + seq + '\n')

    unzipf.close()

logf.write('end unzipped filenames\n')
logf.close()
