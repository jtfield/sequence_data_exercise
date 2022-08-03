#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""

import os
import argparse
import pandas as pd
# import re
# import pathlib
# import subprocess

def parse_args():
    parser = argparse.ArgumentParser(prog='add_distances_to_diff_data.py', \
        description='Combine summary difference files and add distance metrics.')
    # parser.add_argument('--metadata_csv', default=False, help='metadata csv with info on samples from the tree.')
    parser.add_argument('--summary_dir', help='Directory of csv files of the summaries of differences.')
    # parser.add_argument('--dist_csv', help='csv file of distances between taxa in the summary files.')
    # parser.add_argument('--remove_from_names', default='_removed', help='a string you want to remove from the names in your table.')
    return parser.parse_args()

def main():
    args = parse_args()

    tables_to_combine = []

    list_of_files = os.listdir(args.summary_dir)

    for num, file in enumerate(list_of_files):

        abs_path = os.path.abspath(file)
        # print(abs_path)

        read_table= pd.read_csv(abs_path)
        # print(read_table)

        # read_table['taxon_name'] = read_table['taxon_name'].replace(args.remove_from_names, '')
        # read_table['ref_name'] = read_table['ref_name'].replace(args.remove_from_names, '')

        tables_to_combine.append(read_table)

    combined_table = pd.concat(tables_to_combine)

    # print(combined_table)

    combined_table.to_csv('combined_summary_diffs.csv')



if __name__ == '__main__':
    main()
