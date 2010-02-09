#!/usr/bin/env python
# File created on 09 Feb 2010
#file filter_otus_by_sample.py

from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Pre-release"
 
from optparse import make_option
from qiime.util import parse_command_line_parameters
from qiime.filter_otus_by_sample import filter_samples,process_extract_samples
from qiime.make_3d_plots import create_dir
from cogent import LoadSeqs
from qiime.parse import fields_to_dict

script_description = """This script removes unwanted samples from the otu file\
generated by pick_otus and a sequence file"""

script_usage = """

Example 1: Filter otus and a sequence set

Usage: filter_otus_by_sample.py [options] {-i input_otu_path -f fasta_file \
-s samples_to_extract}

[] indicates optional input (order unimportant)
{} indicates required input (order unimportant)

Example usage: filter_otus_by_sample.py -i otus.txt -f seqs.fna \
-s 'ControlA,ControlB' -o './Directory'
"""

required_options = [\
 make_option('-i', '--input_otu_path', help='Path to OTU file containing \
sequence ids assigned to each OTU (i.e., resulting OTU file from pick_otus.py)\
'),
 make_option('-f', '--fasta_file', help='Path to FASTA file containing all \
sequences (i.e., resulting FASTA file from split_libraries.py)'),
 make_option('-s', '--samples_to_extract', help='This is a list of sample \
ids, which should be removed from the OTU file')
 # Example required option
 #make_option('-i','--input_dir',help='the input directory'),\
]

optional_options = [\
 make_option('-o', '--dir_path',\
     help='This is the location where the resulting output should be \
written [default=%default]',default='')
 # Example optional option
 #make_option('-o','--output_dir',help='the output directory [default: %default]'),\
]


def main():
    """opens files as necessary based on prefs"""
    option_parser, opts, args = parse_command_line_parameters(
      script_description=script_description,
      script_usage=script_usage,
      version=__version__,
      required_options=required_options,
      optional_options=optional_options)

    data = {}

    fasta_file = opts.fasta_file

    # load the input alignment
    data['aln'] = LoadSeqs(fasta_file,aligned=False)

    #Load the otu file
    otu_path=opts.input_otu_path
    otu_f = open(otu_path, 'U')
    otus = fields_to_dict(otu_f)
    otu_f.close()

    data['otus']=otus
    #Determine which which samples to extract from representative seqs
    #and from otus file
    if opts.samples_to_extract:
      prefs=process_extract_samples(opts.samples_to_extract)

    filepath=opts.fasta_file
    filename=filepath.strip().split('/')[-1]
    filename=filename.split('.')[0]

    dir_path = create_dir(opts.dir_path,'filtered_by_otus')

    try:
      action = filter_samples
    except NameError:
      action = None
    #Place this outside try/except so we don't mask NameError in action
    if action:
      action(prefs, data, dir_path,filename)

if __name__ == "__main__":
    main()