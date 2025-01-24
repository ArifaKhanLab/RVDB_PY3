#!/usr/bin/env python3

import sys
import os

# sys.path.append('F:\\TOOLBOX')

from sequence_record_functions_PIPE import get_accs_flatfile as getaccs
from sequence_record_functions_PIPE import get_accs_fastafile as getaccsfa
from sequence_record_functions_PIPE import get_filenames as getfns

homedir = sys.argv[1]
datetag = sys.argv[2]
currentvs = sys.argv[3]
removeaccsfn = sys.argv[4]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
gbdir = os.path.join(wdir, 'GenBank_raw_data_' + datetag)
refseqdir = os.path.join(wdir, 'RefSeq_raw_data_' + datetag)
tpadir = os.path.join(wdir, 'TPA_raw_data_' + datetag)
gb_negkwdir = os.path.join(gbdir, 'negkw_out_' + datetag)
tpa_negkwdir = os.path.join(tpadir, 'negkw_out_' + datetag)
dupaccsfn = os.path.join(refseqdir, 'refseq_viral_originalaccs.txt')

postags = ['OK', 'VRL']
negtags = ['FLAG', 'AMB', 'headers']
gbfns = getfns(gb_negkwdir, postags, negtags)
tpafns = getfns(tpa_negkwdir, postags, negtags)
allfns = []

allfns.append(os.path.join(refseqdir, 'viral.genomic.eukviral.fasta'))
allfns.extend(gbfns)
allfns.extend(tpafns)

removeaccs = getaccs(os.path.join(wdir, removeaccsfn))
dupaccs = getaccs(dupaccsfn)


c = 0
match = False
written = set([])
with open(os.path.join(wdir, 'U-RVDBv' + currentvs + '.fasta'), 'w') as outf:
    for fn in allfns:
        inf = open(fn, "r")
        for line in inf:
            if line.startswith('>acc'):
                acc = line.split('|')[2].split('.')[0]
                if acc in removeaccs or acc in dupaccs or acc in written:
                    match = False
                else:
                    match = True
                    written.add(acc)
                    c += 1
            if match:
                outf.write(line.strip() + '\n')
        inf.close()
