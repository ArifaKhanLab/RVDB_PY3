#!/usr/bin/env python3

#### Jaysheel: adding os.path + #!
#### using os.path.join instead string concat using +

import os.path
import sys


def segment_file(infilename, nrows, recstart, recend):
    #### Jaysheel: commented variables are never used
    # a = 0
    # b = 0
    filetype = '.' + infilename.split('.')[-1]

    segmented_filenames = []

    #### Jaysheel: this seem to be just going number of rows in a file, cleaning up the code little bit
    # inf = open(infilename)
    # ##  print 'Counting number of rows from input file: '+infilename
    # for i, line in enumerate(inf):
    #     a = 1
    # totalrows = i
    # inf.close()
    with open(infilename, "r") as fp:
        for i, line in enumerate(fp):
            pass
    totalrows = i

    starts = range(0, totalrows, nrows)

    for s, start in enumerate(starts):
        #### Jaysheel: add file mode
        inf = open(infilename, "r")

        outfilename = infilename.replace(filetype, '_' + str(start) + '_' + str(start + nrows) + filetype)
        segmented_filenames.append(outfilename)
        ##      Writing output file
        outf = open(outfilename, 'w')
        r = 0
        for i, line in enumerate(inf):
            if s == 0:
                if i < start:
                    continue
            else:
                if i < firstnewrow:
                    continue
            r += 1
            outf.write(line)
            if line.startswith(recend):
                if r > nrows:
                    firstnewrow = i + 1
                    break
        inf.close()
        outf.close()
    return segmented_filenames


homedir = sys.argv[1]
date = sys.argv[2]
currentvs = sys.argv[3]
filetype = sys.argv[4]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
refseqdir = os.path.join(wdir, 'RefSeq_raw_data_' + date)
input_filename = os.path.join(refseqdir, 'viral.genomic.gbff')

if filetype == 'gbff':
    recstart = 'LOCUS'
    recend = '//\n'

nrows = int(sys.argv[5])
segmented_filenames = segment_file(input_filename, nrows, recstart, recend)

for segmented_filename in segmented_filenames:
    #### Jaysheel: update print statment to function
    print(segmented_filename)
