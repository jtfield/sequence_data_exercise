#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""

import os
import argparse
import pandas as pd
import numpy as np
# import re
# import pathlib
# import subprocess

def parse_args():
    parser = argparse.ArgumentParser(prog='pull_distances_to_summaries.py', \
        description='Pull the distances from a all-to-all distances csv file.')
    parser.add_argument('--dist_csv', help='csv file of distances between taxa in the summary files.')
    parser.add_argument('--summary_csv', help='csv file of nucleotide differences summaries.')
    parser.add_argument('--output_csv', default='updated_summary_diffs.csv', help='csv with data from both inputs.')
    return parser.parse_args()

def main():
    args = parse_args()

    distance_table = pd.read_csv(args.dist_csv)

    distance_table.columns = distance_table.columns.str.replace(' ', '_')

    distance_table['tax_names'] = distance_table['tax_names'].str.replace(' ', '_')

    # print(distance_table)

    summary_table = pd.read_csv(args.summary_csv)

    summary_table.columns = summary_table.columns.str.replace(' ', '')

    # summary_table['ref_names'] = distance_table['tax_names'].str.replace(' ', '_')

    summary_table['distance'] = np.nan

    distance_table = distance_table.set_index('tax_names')

    print(summary_table.columns)

    print(distance_table.columns)

    # print(distance_table['tax_names'])

    for idx, row in summary_table.iterrows():

        query_taxon = row['taxon_name'].replace(' ', '')

        ref_taxon = row['ref_name'].replace(' ', '')

        print(query_taxon)
        print(ref_taxon)

        found_dist = distance_table.at[query_taxon, ref_taxon]
        print(found_dist)

        summary_table.at[idx, 'distance'] = found_dist

    # print(summary_table)

    summary_table.to_csv(args.output_csv)


if __name__ == '__main__':
    main()
