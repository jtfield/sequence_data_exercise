#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""

import os
import argparse
import re
import pandas as pd
# import pathlib
# import subprocess

def parse_args():
    parser = argparse.ArgumentParser(prog='multi_diff_counter.py', \
        description='Compare original sequences to ref_based sequences. One alignment of original sequences and one of ref based sequences.')
    # parser.add_argument('--metadata_csv', default=False, help='metadata csv with info on samples from the tree.')
    parser.add_argument('--true_seqs', help='The sequences you are stating as true.')
    parser.add_argument('--diffs_folder', help='folder with differences csv files.')
    return parser.parse_args()

def main():
    args = parse_args()

    diffs_files = os.listdir(args.diffs_folder)

    stuff_to_strip = ['unambig_differences_', '.csv']

    true_seq_contents = open(args.true_seqs, 'r').read()

    split_true_seqs = true_seq_contents.split(">")

    for file in diffs_files:

        if stuff_to_strip[0] in file:
            query_tax = file.strip(stuff_to_strip[0]).strip(stuff_to_strip[1])

            file_path = args.diffs_folder + file

            print(file_path)
            diffs = pd.read_csv(file_path)

            columns = diffs.columns

            ref_name = columns[2].strip('_removed')
            print(ref_name)
            ref_seq = ''
            for chunk in split_true_seqs:
                if ref_name in chunk:

                    ref_name_and_seq = chunk.split('\n',1)

                    ref_seq = ref_name_and_seq[1]
                    print(ref_name_and_seq[0])
                    # print("compare")

                    # for idx, row in diffs.iterrows():
                    #
                    #     pos = row[0]
                    #     query_nuc = row[2]
                    #
                    #     print(row)
                    #     print(pos)
                    #     print(query_nuc)
                    #     print(ref_seq[pos])










if __name__ == '__main__':
    main()
