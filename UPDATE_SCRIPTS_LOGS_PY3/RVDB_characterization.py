#!/usr/bin/env python3

import re
import os
import sys

##################################################################################################
########## Positive keywords, positive regular expressions.                            ###########
########## Keywords < 5 characters in length receive flanking ' ' (single whitespace)  ###########
########## on either side, with two exceptions: 'virus' and 'viral'.                   ###########
##################################################################################################
poskws = [' copia ', ' env ', ' erv ', ' gag ', ' gipsy ', ' herv ', 'harlequin', ' iap ', ' ltr ', ' mdg3 ', ' mdg1 ',
          ' merv ', ' pol ', ' rt gene ', ' sire ', ' vlp ', 'blastopia', 'capsid', ' delta element', 'dutpase',
          'endogenous', 'envelop', 'erranti', 'gypsy element', 'gypsy like', 'gypsy type', ' iap ltr ',
          'insertion element',
          'integrase', 'intracisternal a particle', ' long terminal repeat', ' ltr ', 'micropia',
          'polycomb response element',
          'polyprotein', 'provir', 'replicase', 'retrovir', 'retroelement', 'retrotranspos', 'reverse transc', 'spuma',
          ' ty element',
          ' ty insertion', 'viral', 'virales', 'viridae', 'virion', 'viroid', 'virus']

##################################################################################################
########## Retroelement / retrotransposon - specific words/regexes/rules               ###########
##################################################################################################
########## Base retroelement / retrotransposon keywords
retrokws = ['retrotranspos', 'retro transpos', 'retroelem', 'blastopia ', ' copia ', ' delta element', ' gipsy ',
            ' gypsy element', ' gypsy like ', ' gypsy type ',
            'insertion element', ' mdg1 ', ' mdg3 ', 'micropia', ' sire ', ' ty element', ' ty insertion']
########## Matches Ty elements of the following form: ty1, ty 2 - for retroelements / retrotransposons
pos_ty_finder = re.compile('\s{1}ty\s{0,1}[0-9]{1}\s{1}')


########## Positive rules are all for retrotransposons that "say" tranpos- or other criteria (missed by simple keywords above)

def retrotransposon_positive_rules(description_s):
    ds = description_s
    retro = []
    if 'transpos' in ds:
        if ' bel ' in ds:
            retro.append('transpos + bel')
        if ' pao ' in ds:
            retro.append('transpos + pao')
        if ' roo ' in ds:
            retro.append('transpos + roo')
        if 'morgane' in ds:
            retro.append('transpos + morgane')
    return retro


neg_retro_kws = ['virus', 'retrotransposon line ']
neg_isolatety_finder = re.compile('\sisolate\sty[1-9]*\s')


def retrotransposon_negative_rules(description_s):
    nonretro = []
    ds = description_s
    if ' fst ' in ds:
        if ' ty1 ' in ds or ' ty 1 ' in ds:
            nonretro.append(' fst + ty1 / ty 1 ')
    return nonretro


##################################################################################################
########## Endogenous retrovirus - specific words/regexes/rules                        ###########
##################################################################################################
########## Base endogenous retrovirus keywords
erkws = ['endogenous retrovir', ' erv ', ' herv ', ' merv ', ' serv ', 'harlequin', ' iap ltr ',
         'intracisternal a particle', 'erranti']
########## Matches HERVs of the following form: HERV, HERVE, HERV-I,  HERV I, HERV9, HERV 9, HERV-FC
pos_herv_finder = re.compile('\s{1}herv\s{0,1}[a-z0-9]{0,2}\s{1}')
########## Matches HMLs of the following form: hml1, hml 2
pos_hml_finder = re.compile('\s{1}hml\s{0,1}[0-9]{1}\s{1}')


########## Positive rules for endogenous retroviruses (missed by simple keywords above)
def endogenous_retrovirus_positive_rules(description_s):
    ds = description_s
    er = []
    if 'endogenous' in ds:
        if 'virus' in ds or 'viral' in ds:
            if ' cerv ' in ds:
                er.append('endogenous retrovirus cerv')
            if 'spodoptera' in ds and 'frugiperda' in ds:
                er.append('spodoptera frugiperda endogenous retrovirus')
            if 'baboon' in ds:
                er.append('baboon endogenous retrovirus')
    return er


##################################################################################################
########## Endogenous virus - specific words/regexes/rules                             ###########
##################################################################################################
########## Base endogenous virus keywords
evkws = ['endogenous virus', 'endogenous viral']

##################################################################################################
########## Exogenous virus (non-specific) words/regexes/rules                          ###########
##################################################################################################
########## Base exogenous virus keywords
vkws = ['viral', 'virales', 'viridae', 'virion', 'viroid', 'virus']


##################################################################################################
########## Retrotransposon - specific words/regexes/rules                              ###########
##################################################################################################


##################################################################################################
########## Main function for identifying/counting entries by biological category       ###########
########## i.e. retroelements/retrotransposons, endogenous retroviruses,               ###########
########## endogenous viruses, and other (exogenous) viruses                           ###########
##################################################################################################
def characterize_by_biological_category(wdir, infilename, tofilter, filterset):
    cdict = dict()
    c = 0
    entries = []

    with open(os.path.join(wdir, infilename), "r") as inf:
        for i, line in enumerate(inf):
            if line.startswith('>acc'):
                entries.append(line.strip())

    for entry in entries:
        acc = entry.split('|')[1].strip()

        if tofilter:
            if not acc in filterset:
                continue

        c += 1
        d = ' '.join(entry.strip().split('|')[3:])
        ds = simplify_description(d)
        hasposkws = ithas_poskws(entry, ds)
        isretro = isit_retro(entry, ds)

        if isretro == 'badline':
            isretro = False
        ##            print cluster

        iser = isit_er(entry, ds)
        isev = isit_ev(entry, ds)
        isv = isit_v(entry, ds)
        entry = '>acc' + entry

        if isretro:
            try:
                existing = cdict['retro']
            except KeyError:
                existing = []
            existing.append(entry)
            cdict['retro'] = existing
        else:
            if iser:
                try:
                    existing = cdict['er']
                except KeyError:
                    existing = []
                existing.append(entry)
                cdict['er'] = existing
            else:
                if isev:
                    try:
                        existing = cdict['ev']
                    except KeyError:
                        existing = []
                    existing.append(entry)
                    cdict['ev'] = existing
                else:
                    if isv:
                        try:
                            existing = cdict['v']
                        except KeyError:
                            existing = []
                        existing.append(entry)
                        cdict['v'] = existing
                    else:
                        try:
                            existing = cdict['other']
                        except KeyError:
                            existing = []
                        existing.append(entry)
                        cdict['other'] = existing

    print(str(c) + ' entries characterized')

    outf = open(wdir + '\\' + 'char_output_log.txt', 'w')

    outf.write('Characterization complete\n')
    outf.write(str(len(cdict['v'])) + ' exogenous viral sequences\n')
    outf.write(str(len(cdict['ev'])) + ' endogenous nonretroviral sequences\n')
    outf.write(str(len(cdict['er'])) + ' endogenous retroviral sequences\n')
    outf.write(str(len(cdict['retro'])) + ' LTR-retrotransposon sequences\n')
    outf.write(str(len(cdict['other'])) + ' unclassified viral gene/fragment sequences\n')
    outf.close()

    return cdict


##################################################################################################
########## Writes output file for biological categories                                ###########
##################################################################################################
def write_characterization_output(wdir, rvdb_filename, cdict):
    outf_ex = open(os.path.join(wdir, rvdb_filename + '.EX.headers.txt'), 'w')
    outf_enrv = open(os.path.join(wdir, rvdb_filename + '.ENRV.headers.txt'), 'w')
    outf_erv = open(os.path.join(wdir, rvdb_filename + '.ERV.headers.txt'), 'w')
    outf_retro = open(os.path.join(wdir, rvdb_filename + '.LTR-RETRO.headers.txt'), 'w')
    outf_other = open(os.path.join(wdir, rvdb_filename + '.UNASSIGNED.headers.txt'), 'w')

    outf_ex.write('\n'.join(cdict['v']))
    outf_enrv.write('\n'.join(cdict['ev']))
    outf_erv.write('\n'.join(cdict['er']))
    outf_retro.write('\n'.join(cdict['retro']))
    outf_other.write('\n'.join(cdict['other']))

    outf_ex.close()
    outf_enrv.close()
    outf_erv.close()
    outf_retro.close()
    outf_other.close()


##################################################################################################
########## Retrieves characeterized sequences                                          ###########
##########   (i.e. output of write_characterization_output)                            ###########
##################################################################################################
def get_characterized_output(wdir, rvdb_filename):

    ex_fn = os.path.join(wdir, rvdb_filename + '.EX.headers.txt')
    with open(ex_fn, "r") as ex_inf:
        # ex_heads = ex_inf.read().strip().split('\n')
        ex_heads = list(map(lambda x: x.strip(), ex_inf.readlines()))

    enrv_fn = os.path.join(wdir, rvdb_filename + '.ENRV.headers.txt')
    with open(enrv_fn, "r") as enrv_inf:
        #enrv_heads = enrv_inf.read().strip().split('\n')
        enrv_heads = list(map(lambda x: x.strip(), enrv_inf.readlines()))

    erv_fn = os.path.join(wdir, rvdb_filename + '.ERV.headers.txt')
    with open(erv_fn, "r") as erv_inf:
        #erv_heads = erv_inf.read().strip().split('\n')
        erv_heads = list(map(lambda x: x.strip(), erv_inf.readlines()))

    retro_fn = os.path.join(wdir, rvdb_filename + '.LTR-RETRO.headers.txt')
    with open(retro_fn, "r") as retro_inf:
        #retro_heads = retro_inf.read().strip().split('\n')
        retro_heads = list(map(lambda x: x.strip(), retro_inf.readlines()))

    other_fn = os.path.join(wdir, rvdb_filename + '.UNASSIGNED.headers.txt')
    with open(other_fn, "r") as other_inf:
        #other_heads = other_inf.read().strip().split('\n')
        other_heads = list(map(lambda x: x.strip(), other_inf.readlines()))

    cdict2 = dict()
    for ex_head in ex_heads:
        acc = ex_head.split('|')[2]
        cdict2[acc] = 'EX'

    for enrv_head in enrv_heads:
        acc = enrv_head.split('|')[2]
        cdict2[acc] = 'ENRV'

    for erv_head in erv_heads:
        acc = erv_head.split('|')[2]
        cdict2[acc] = 'ERV'

    for retro_head in retro_heads:
        acc = retro_head.split('|')[2]
        cdict2[acc] = 'LTR-RETRO'

    for other_head in other_heads:
        acc = other_head.split('|')[2]
        cdict2[acc] = 'OTHER'

    return cdict2


#####################################################################################################
########## Auxiliary functions for main function characterize_creps_by_biological_category ##########
#####################################################################################################

def isit_retro(cluster, ds):
    foundkws = []
    foundregexes = []
    foundrules = []
    foundnegkws = []
    foundnegregexes = []
    foundnegrules = []
    isretro = False
    badline = False

    ##### Screen for positive retro criteria #####
    for poskw in retrokws:
        if poskw in ds:
            foundkws.append(poskw)

    tys = pos_ty_finder.findall(ds)

    if len(tys) > 0:
        foundregexes.extend(list(set(tys)))

    foundrules = retrotransposon_positive_rules(ds)

    if len(foundkws) > 0 or len(foundregexes) > 0 or len(foundrules) > 0:
        isretro = True

    ##### Screen for negative retro criteria #####
    for negkw in neg_retro_kws:
        if negkw in ds:
            foundnegkws.append(negkw)

    isolatetys = neg_isolatety_finder.findall(ds)
    foundnegregexes.extend(isolatetys)
    foundnegrules = retrotransposon_negative_rules(ds)

    if len(foundnegkws) > 0 or len(foundnegregexes) > 0 or len(foundnegrules) > 0:
        isretro = False

    return isretro


def isit_er(cluster, ds):
    foundkws = []
    foundregexes = []
    foundrules = []
    iser = False

    for poskw in erkws:
        if poskw in ds:
            foundkws.append(poskw)

    hervs = pos_herv_finder.findall(ds)

    if len(hervs) > 0:
        foundregexes.extend(list(set(hervs)))

    hmls = pos_hml_finder.findall(ds)

    if len(hmls) > 0:
        foundregexes.extend(list(set(hmls)))

    foundrules = endogenous_retrovirus_positive_rules(ds)

    if len(foundkws) > 0 or len(foundregexes) > 0 or len(foundrules) > 0:
        iser = True

    return iser


def isit_ev(cluster, ds):
    foundkws = []
    isev = False

    for poskw in evkws:
        if poskw in ds:
            foundkws.append(poskw)

    if len(foundkws) > 0:
        isev = True

    return isev


def isit_v(cluster, ds):
    foundkws = []
    isv = False

    if '|VRL|' in cluster:
        isv = True

    for poskw in vkws:
        if poskw in ds:
            foundkws.append(poskw)

    if len(foundkws) > 0:
        isv = True

    return isv


########## Takes a standard GenBank entry description and simplifies the format - all non-alphanumeric characters replaced by a single whitespace character each (' '),
########## underscore is replaced by a single whitespace  (' '), the description is made lowercase, then a single whitespace is added to either side
########## is added to the beginning and end
def simplify_description(description):
    description_s = re.sub(r'\W+', ' ', description)
    description_s = description_s.replace('_', ' ')
    description_s = description_s.lower()
    description_s = description_s.strip()
    description_s = ' ' + description_s + ' '

    return description_s


def initialize_cdict(cdict):
    cdict['retro'] = []
    cdict['er'] = []
    cdict['ev'] = []
    cdict['v'] = []
    cdict['other'] = []

    return cdict


def ithas_poskws(cluster, ds):
    hasposkws = []

    for poskw in poskws:
        if poskw in ds:
            hasposkws.append(poskw)

    hasposkws = sorted(list(set(hasposkws)))

    return hasposkws


def get_headers(fasta_filename):
    headers = dict()
    with open(fasta_filename) as inf:
        for i, line in enumerate(inf):
            if line.startswith('>gi'):
                gi = line.strip().split('|')[1]
                headers[gi] = line

    return headers


##################################################################################################
########## Execute command block                                                       ###########
##################################################################################################

homedir = sys.argv[1]
datetag = sys.argv[2]
currentvs = sys.argv[3]

wdir = os.path.join(homedir, 'RVDBv' + currentvs)
rvdb_filename = sys.argv[4]

print(rvdb_filename)
filterset_filename = sys.argv[5]

from sequence_record_functions_PIPE import get_accs_flatfile as getaccs

try:
    filterset = getaccs(filterset_filename)
    tofilter = True
except IOError:
    filterset = set([])
    tofilter = False

cdict = characterize_by_biological_category(wdir, rvdb_filename, tofilter, filterset)
write_characterization_output(wdir, rvdb_filename, cdict)
