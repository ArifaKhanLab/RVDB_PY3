#!/usr/bin/env python3

import os.path
import re
import sys

# fhd = open("test.txt", "r")
# data = set(list(map(lambda x: x.strip(), fhd.readlines())))
# fhd.close()
# print(data)
#
# fhd = open("test.txt", "r")
# data = fhd.readlines()
# fhd.close()
# print(data)
#
# with open("test.txt", "r") as file:
#     for i, line in enumerate(file):
#         print(line, i)
list = [" phage",
"corticovir",
"cystovir",
"fusellovir",
" inovir",
"plectrovir",
"levivir",
"lipothrixvir",
"microvir",
"myovir",
"plasmavir",
"podovir",
"rudivir",
"siphovir",
"tectivir"]

header = "acc|REFSEQ|NC_030458.1|Chimpanzee faeces associated microphage 3 isolate CPNG_29300, complete genome"
for l in list:
    pattern = re.compile("[\s\|]" + l, flags=re.IGNORECASE)
    if l in header:
        print(l)
        print("Found pattern")

list = ['DEFINITION  Uncultured bacterium gene for 16S rRNA, partial sequence, clone: 2', '            of cluster I.', 'ACCESSION   AB000684', 'VERSION     AB000684.1', 'KEYWORDS    ENV.', 'SOURCE      uncultured bacterium', '  ORGANISM  uncultured bacterium', '            Bacteria; environmental samples.', 'REFERENCE   1', '  AUTHORS   Inagaki,F., Hayashi,S., Doi,K., Motomura,Y., Izawa,E. and Ogata,S.', '  TITLE     Microbial participation in the formation of siliceous deposits from', '            geothermal water and analysis of the extremely thermophilic', '            bacterial community', '  JOURNAL   FEMS Microbiol. Ecol. 24, 41-48 (1997)', 'REFERENCE   2  (bases 1 to 275)', '  AUTHORS   Inagaki,F., Hayashi,S., Doi,K., Motomura,Y., Izawa,E. and Ogata,S.', '  TITLE     Direct Submission', '  JOURNAL   Submitted (24-JAN-1997) Fumio Inagaki, Faculty of Agriculture,', '            Kyushu University, Microbial Genetic Division, Institute of Genetic', '            Resourses; Higashi-ku Hakozaki 6-10-1, Fukuoka-shi, Fukuoka 812-81,', '            Japan (E-mail:inagaki@agr.kyushu-u.ac.jp, Tel:+81-92-642-3059,', '            Fax:+81-92-642-3059)']

print("I am here")