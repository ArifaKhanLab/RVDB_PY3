#!/usr/bin/env python3

import sys
import os
import csv

# sys.path.append('E:\\TOOLBOX')

from sequence_record_functions_PIPE import get_accs_flatfile as getaccs
from sequence_record_functions_PIPE import get_accs_fastafile as getaccsfa
from sequence_record_functions_PIPE import get_filenames as getfns

#### PARSE INPUT ARGUMENTS
homedir = sys.argv[1]
datetag = sys.argv[2]
currentvs = sys.argv[3]
previous_urvdb_filename = sys.argv[4]

##homedir='E:'
##datetag='apr.2018'
##currentvs='13.0'

#### SET DIRECTORY STRUCTURE
wdir = os.path.join(homedir, 'RVDBv' + currentvs)
refseqdir = os.path.join(wdir, 'RefSeq_raw_data_' + datetag)
gbdir = os.path.join(wdir, 'GenBank_raw_data_' + datetag)
tpadir = os.path.join(wdir, 'TPA_raw_data_' + datetag)
gb_negkwdir = os.path.join(gbdir, 'negkw_out_' + datetag)
tpa_negkwdir = os.path.join(tpadir, 'negkw_out_' + datetag)
dupaccsfn = os.path.join(refseqdir, 'refseq_viral_originalaccs.txt')

#### GET ALL UNIQUE ACCESSIONS FROM refseq_viral_originalaccs.txt
dupaccs = getaccs(dupaccsfn)

#################################################################################################################
def write_update_accs_outfile(postags, negtags, accstype):
    print("writing out + accessions, those that are RefSeq eukaryotic or pass SEM-R_PIPE screen")

    with open(os.path.join(wdir, 'RVDBv' + currentvs + '_accs' + accstype + '.txt'), 'w') as outf:
        if accstype == 'OK':
            refseq_accs = getaccs(os.path.join(refseqdir, 'viral.genomic.eukviral.accs.txt'))
            outf.write('\n'.join(refseq_accs) + '\n')

        print("finished collecting RefSeq Viral accessions")
        gbfns = getfns(gb_negkwdir, postags, negtags)

        for gbfn in gbfns:
            # print(gbfn)
            gbaccsfa = getaccsfa(gbfn)
            gbaccs = []

            for gbacc in gbaccsfa:
                if not gbacc.split('.')[0] in dupaccs:
                    gbaccs.append(gbacc)

            if len(gbaccs):
                outf.write('\n'.join(list(gbaccs)) + '\n')

        print("finished collecting GenBank+ accessions")
        tpafns = getfns(tpa_negkwdir, postags, negtags)

        for tpafn in tpafns:
            tpaaccs = getaccsfa(tpafn)
            if len(tpaaccs):
                outf.write('\n'.join(list(tpaaccs)) + '\n')

        print("finished collecting TPA+ accessions")


#################################################################################################################
def make_review_sheets(previous_urvdb_filename):
    oldaccs = getaccsfa(previous_urvdb_filename)
    newaccs = getaccs(os.path.join(wdir, 'RVDBv' + currentvs + '_accsOK.txt'))

    d1 = set(oldaccs).difference(set(newaccs))
    d2 = set(newaccs).difference(set(oldaccs))

    # Jaysheel Bhavsar var not being used.
    # i1 = set(oldaccs).intersection(set(newaccs))

    d1out = []
    d2out = []

    print("writing out headers for entries present in: " + previous_urvdb_filename + " but not in update v" + currentvs)

    with open(previous_urvdb_filename, "r") as inf:
        for line in inf:
            if line.startswith('>acc'):
                sl = line.strip().split('|')
                acc = sl[2]
                if acc in d1:
                    d1out.append(sl[1:])

    #### Jaysheel Bhavsar: use with statement
    with open(os.path.join(wdir, 'RVDBv' + currentvs + '.missing.csv'), 'w', newline='') as outf:
        writer = csv.writer(outf, dialect='unix')

        d1out.insert(0, ['SOURCE', 'ACCESSION', 'DESCRIPTION'])
        writer.writerows(d1out)

    #### Jaysheel: unused var
    #match = False

    with open(os.path.join(refseqdir, 'viral.genomic.eukviral.fasta')) as inf:
        for line in inf:
            if line.startswith('>acc'):
                sl = line.strip().split('|')
                acc = sl[2]
                if acc in d2:
                    d2out.append(sl[1:])

    postags = ['OK', 'VRL']
    negtags = ['FLAG', 'AMB', 'headers']

    gbfns = getfns(gb_negkwdir, postags, negtags)
    tpafns = getfns(tpa_negkwdir, postags, negtags)

    readfns = []
    readfns.extend(list(set(gbfns)))
    readfns.extend(list(set(tpafns)))

    print("writing out headers for entries present in update v" + currentvs + " that were not present in the previous version, " + previous_urvdb_filename)
    for fn in readfns:
        #print(fn)
        #### open file to process only if it has data.
        if os.stat(fn).st_size:
            with open(fn, "r") as inf:
                for line in inf:
                    if line.startswith('>acc'):
                        sl = line.strip().split('|')
                        acc = sl[2]
                        if acc in d2:
                            d2out.append(sl[1:])

    #### Jaysheel Bhavsar: use with statement
    with open(os.path.join(wdir, 'RVDBv' + currentvs + '.new.csv'), 'w', newline='') as outf:
        writer = csv.writer(outf, dialect='unix')
        d2out.insert(0, ['SOURCE', 'ACCESSION', 'DESCRIPTION'])
        writer.writerows(d2out)


#################################################################################################################
#### START OF MAIN HERE
#################################################################################################################

#### SET VARIABLES
postags = ['OK', 'VRL']
negtags = ['FLAG', 'headers']
accstype = 'OK'

write_update_accs_outfile(postags, negtags, accstype)

#### SET VARIABLES
postags = ['AMB']
# Jaysheel Bhavsar, no need to recreate negtags here above assignment is not changed.
#negtags = ['FLAG', 'headers']
accstype = 'AMB'

write_update_accs_outfile(postags, negtags, accstype)

#### WRITE FINAL REVIEW FILE
make_review_sheets(previous_urvdb_filename)
