#!/usr/bin/env python3

import os
import argparse
import re
import pathlib
import subprocess
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(prog='single_taxon_multi_diff_counter.py', \
        description='Compare original sequences to ref_based sequences. One alignment of original sequences and one of ref based sequences.')
    # parser.add_argument('--metadata_csv', default=False, help='metadata csv with info on samples from the tree.')
    # parser.add_argument('--true_seqs', help='The sequences you are stating as true.')
    parser.add_argument('--comparisons_dir', help='directory of sequence comparison directories.')
    parser.add_argument('--query_taxon',help='the taxon label your attempting to analyze.')
    # parser.add_argument('--dists_table', help='the table of pairwise distances.')
    return parser.parse_args()

def main():
    args = parse_args()

    columns = ['taxon_name','ref_name','all_diffs','diffs_to_true','diffs_to_true_matching_ref']

    summary_df = pd.DataFrame(columns=columns)

    for fil in os.listdir(args.comparisons_dir):
        if fil.startswith('diff_summary_75_ref_'):
            path_to_file = os.path.abspath(fil)

            print(path_to_file)

            file_contents = pd.read_csv(path_to_file)
            # print(file_contents)

            for idx, line in file_contents.iterrows():
                # print(line)
                if args.query_taxon in line['taxon_name']:
                    # print(line)

                    summary_df = summary_df.append(line)
                    # summary_df = summary_df.concat(line)
    #
    # print(summary_df)
    summary_df.to_csv('diff_summary_75_query_' + args.query_taxon + '.csv')










if __name__ == '__main__':
    main()
