#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thur April 12 2018
@author: Mingyi Xue

Users can run this module directly to convert '.mgf' files to chemdistiller input files.
Usage in command line: python MGF2ChemDistiller.py <input_file> (<output_folder>)
                       python MGF2ChemDistiller.py <input_folder> (<output_folder>)
"""

import os
import sys
from chemdistiller.io.cdinput import CD
from chemdistiller.io.mgfinput import MGFfile

#import pandas
#import re

if __name__=='__main__':
    if sys.byteorder!='little':
        #print('Only little endian machines currently supported! bye bye ....');
        quit();

    chemdistiller_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."));
    sys.path.append(chemdistiller_path);


class MGFParser:
    """
    MGFParser is aimed at output a '.txt' file for chemdistiller input
    from a given '.mgf' file.
    """
    def __init__(self, fname, output_folder=''):
        print("Trying to convert MGF files to chemdistiller inputs...")
        self.fname=[]
        self.tmp_fname = ''
        # chemdistiller input path
        if os.path.isdir(fname):
            for f in os.listdir(fname):
                self.fname.append(os.path.join(fname,f))
            self.tmp_fname = os.path.join(fname,"default")
        elif os.path.isfile(fname):
            self.fname.append(fname)
            self.tmp_fname = os.path.join(os.path.split(fname)[0],
                                          "default")
        self.cds = []
        self.output=False
        if len(output_folder)>0:
                self.tmp_fname=output_folder
                self.output=True
                print("The output directory is:" + self.tmp_fname)
        else:
            print("Using default output directory:"+self.tmp_fname)
        if os.path.exists(self.tmp_fname)==False:
            os.mkdir(self.tmp_fname)
        self.count = 1
        # in case one mgf file has several begin ions...end ions
        # chunks and face a filename collision

    def mgf2cd(self):
        # return a chemdistiller input filename
        files=[]
        for file in self.fname:
            if os.path.isfile(file):
                if os.path.splitext(os.path.basename(file))[1] == '.mgf':
                    self.proc_single_file(file)
        return self.cds

    def proc_single_file(self, file):
        # create empty chemditiller structure
        MGF = MGFfile(file)
        mgfs = MGF.get_mgfs()
        for mgf in mgfs:
            CD_DEFAULT_PARAMS = {
                'db_molecule_name': '',
                'exactmass': '',
                'formula': '',
                'fpt_0': '',
                'fptcount': '',
                'global_index': '',
                'inchi': '',
                'level': '1',
                'mode': '',
                'peaks': '',
                'charge': '',
                'ion_type': ''
            }
            CD_DEFAULT_SUB_PARAMS = {
                'charge': '',
                'collision_energy': '-1.0',
                'collision_record': '',
                'dbsource': '',
                'exactmass': '',
                'formula': '',
                'inchi': '',
                'level': '2',
                'mode': '',
                # compulsory parameter for level 1
                'precursor_ion': '',
                'precursor_mz': '',
                'peaks': ''
            }
            cd=CD(CD_DEFAULT_PARAMS,CD_DEFAULT_SUB_PARAMS)
            cd.gen_from_mgf(mgf)
            # convert mgf parameters to chemdistiller parameters
            n,e = os.path.splitext(os.path.basename(file))
            tmp_file = os.path.join(self.tmp_fname, n+'.txt')
            if os.path.exists(tmp_file)==False:
                self.count = 1
            else:
                while os.path.exists(tmp_file):
                    self.count += 1
                    tmp_file = os.path.join(self.tmp_fname, n+'_'+str(self.count)+'.txt')
            cd.write_cd(tmp_file)
            # write parameters of cd to files
            self.cds.append(tmp_file)


if __name__=='__main__':
    # a simple test for this module
    if len(sys.argv)==1:
        print("python MGF2ChemDistiller.py <input_file> (<output_folder>)")
        quit()
    elif len(sys.argv)==2:
        mgf_parser = MGFParser(sys.argv[1])
        mgf_parser.mgf2cd()
        print("input folder:" + sys.argv[1])
    elif len(sys.argv)==3:
        mgf_parser = MGFParser(sys.argv[1], sys.argv[2])
        mgf_parser.mgf2cd()
    else:
        print("parameter error...\n")
        print("python MGF2ChemDistiller.py <input_file> (<output_folder>)")
        quit()


