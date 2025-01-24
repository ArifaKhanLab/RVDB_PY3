#!/usr/bin/env python3

import argparse, json
import warnings, sys, os, re
import pprint, pickle

class PIPELINE:
    pp = pprint.PrettyPrinter(indent=4)

    def __init__(self):
        '''Default constructor'''

        # private variables here
        self.basedir = "/work/jaysheel/rvdb"
        self.date = "jun.2022"
        self.data = "RVDBv24.1"
        self.version = "24.1"
        self.bin = os.path.dirname(__file__)

        parser = argparse.ArgumentParser(description='RVDB new DB Release pipeline', add_help=True)

        parser.add_argument('-b', action="store", required=False, dest="basedir",
                            help="Path of base dir where all files will be stored. e.g: \
                                 /work/jaysheel/rvdb")
        parser.add_argument('-t', action="store", required=False, dest="date", help="Release date eg: jun.2022")
        parser.add_argument('-d', action="store", required=False, dest="data",
                            help="data dir under basedir where all raw files are stored")
        parser.add_argument('-v', action="store", required=False, type=float, dest="version",
                            help="Version new DB release, usually the postfix of datadir. e.g: 24.1")

        parser.parse_args(namespace=self)

    def main(self):

        # # 1. parse raw refseq pipe
        # print("############## 1. parse_raw_refseq_PIPE ##############")
        #
        # viral_file_list = []
        #
        # #### open refseq folder and get all viral files.
        # file_list = os.listdir(os.path.join(self.basedir, self.data, "RefSeq_raw_data_" + self.date))
        #
        # for f in file_list:
        #     if f.endswith('.genomic.fna.gz'):
        #         viral_file_list.append(f)
        #
        # cmd = self.bin + "/parse_raw_refseq_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " " + " ".join(viral_file_list)
        # self.run_command(cmd)
        #
        # #2 multiple gzunzip pipe
        # print("############## 2. multiple_gzunzip_PIPE.py ##############")
        # viral_file_list = []
        #
        # #### open refseq folder and get all viral files.
        # file_list = os.listdir(os.path.join(self.basedir, self.data, "RefSeq_raw_data_" + self.date))
        #
        # for f in file_list:
        #     if f.endswith('.genomic.gbff.gz'):
        #         viral_file_list.append(f)
        #
        # cmd = self.bin + "/multiple_gzunzip_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " " + " ".join(viral_file_list) + " viral.genomic.gbff"
        # self.run_command(cmd)
        #
        # #3. fileops pipe
        # print("############## 3. fileops_PIPE.py ##############")
        #
        # cmd = self.bin + "/fileops_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " gbff 1000000"
        # self.run_command(cmd)
        #
        # # 4. rs acc mapping PIPE
        # print("############## 4. rs_acc_mapping_PIPE.py ##############")
        #
        # cmd = self.bin + "/rs_acc_mapping_PIPE.py " + self.basedir + " " + self.date + " " + self.version
        # self.run_command(cmd)
        #
        # # 5. vdbunzip reforat gb to fasta
        # print("############## 5. VDBunzip_reformat_gb_to_fasta_PIPE.py ##############")
        #
        # cmd = self.bin + "/VDBunzip_reformat_gb_to_fasta_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " gb"
        # self.run_command(cmd)
        #
        # # 6. vdbupdate checkpoint2
        # print("############## 6. VDBupdate_checkpoint2_PIPE.py ##############")
        #
        # release_file = ""
        #
        # #### open refseq folder and get all viral files.
        # file_list = os.listdir(os.path.join(self.basedir, self.data))
        #
        # for f in file_list:
        #     if f.startswith('gb_releasenotes_v'):
        #         release_file = f
        #
        # cmd = self.bin + "/VDBupdate_checkpoint2_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " " + release_file
        # self.run_command(cmd)

        # 7. SEM-R poskw gb
        print("############## 7. SEM-R_june62018_PIPE.py poskw ##############")

        cmd = self.bin + "/SEM-R_june62018_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " poskw gb"
        self.run_command(cmd)

        # 8. SEM-R sizemirna gb
        print("############## 8. SEM-R_june62018_PIPE.py sizemirna ##############")

        cmd = self.bin + "/SEM-R_june62018_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " sizemirna gb"
        self.run_command(cmd)

        # 9. SEM-R negkw gb
        print("############## 9. SEM-R_june62018_PIPE.py negkw ##############")

        cmd = self.bin + "/SEM-R_june62018_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " negkw gb"
        self.run_command(cmd)

        # 10. VDBunzip tpa
        print("############## 10. VDBunzip_tpa_PIPE.py ##############")

        cmd = self.bin + "/VDBunzip_tpa_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " fsa_nt.gz"
        self.run_command(cmd)

        # 11. SEM-R poskw gb
        print("############## 11. SEM-R_june62018_PIPE.py poskw tpa ##############")

        cmd = self.bin + "/SEM-R_june62018_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " poskw tpa"
        self.run_command(cmd)

        # 12. SEM-R sizemirna gb
        print("############## 12. SEM-R_june62018_PIPE.py sizemirna tpa ##############")

        cmd = self.bin + "/SEM-R_june62018_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " sizemirna tpa"
        self.run_command(cmd)

        # 13. SEM-R negkw gb
        print("############## 13. SEM-R_june62018_PIPE.py negkw tpa ##############")

        cmd = self.bin + "/SEM-R_june62018_PIPE.py " + self.basedir + " " + self.date + " " + self.version + " negkw tpa"
        self.run_command(cmd)

    def run_command(self, cmd):
        print(cmd)
        os.system(cmd)

    def __del__(self):
        ''' Default destructor '''


if __name__ == "__main__":
    obj = PIPELINE()
    obj.main()
