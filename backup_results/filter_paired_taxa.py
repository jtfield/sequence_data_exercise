#!/usr/bin/env python3

import os
import argparse
import pandas as pd



def parse_args():
    parser = argparse.ArgumentParser(prog='remove taxa from tree', \
        description='After running EP on multiple reference sequences, analyze the results.')
    parser.add_argument('--csv_file', default=False, help='input csv file. Uses the csv format of taxon,taxon,nuc_count,nuc_count,distance.')

    return parser.parse_args()

def main():
    args = parse_args()

    csv = pd.read_csv(args.csv_file)

    # remove_dupe_comparisons(csv)

    # bin_data(csv)

    get_unbiased_nucs(csv)

def bin_data(csv):

    print(csv.columns)
    bins = [0.000, 0.005, 0.010, 0.015, 0.02, 0.025, 0.030, 0.035]

    binned_distances = pd.cut(csv['distance'], bins=bins)

    # binned_distances = pd.qcut(csv['distance'], q=10)
    # print(binned_distances)
    print(binned_distances.value_counts())

    # grouped_bins = csv.groupby(pd.cut(csv['distance'],bins=bins)).size()

    grouped_bins = csv.groupby(binned_distances).size()
    print(grouped_bins)


def get_unbiased_nucs(csv):
    print(csv.columns)

    csv['unbiased_nucs'] = csv['diffs_to_true'] - csv['diffs_to_true_matching_ref']
    # print(csv)

    



def remove_dupe_comparisons(csv):

    csv_columns = csv.columns
    no_dupes_df = pd.DataFrame(columns=csv_columns)
    already_counted_taxa = []

    count = 0
    for idx, row in csv.iterrows():
        taxa_pair = (row['taxon_name'], row['ref_name'])
        reverse_pair = (row['ref_name'], row['taxon_name'])

        if taxa_pair not in already_counted_taxa or reverse_pair not in already_counted_taxa:
            count+=1
            already_counted_taxa.append(taxa_pair)
            already_counted_taxa.append(reverse_pair)
            no_dupes_df = no_dupes_df.append(row)

    print(count)

    no_dupes_df.to_csv('no_duplicate_comparisons_updated_summary_diffs.csv')






if __name__ == '__main__':
    main()
