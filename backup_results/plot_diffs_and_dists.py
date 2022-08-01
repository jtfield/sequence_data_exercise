#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""

import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import re
# import pathlib
# import subprocess

def parse_args():
    parser = argparse.ArgumentParser(prog='pull_distances_to_summaries.py', \
        description='Pull the distances from a all-to-all distances csv file.')
    parser.add_argument('--diffs_dists_csv', help='csv file of distances between taxa in the summary files.')
    return parser.parse_args()

def main():
    args = parse_args()

    data_table = pd.read_csv(args.diffs_dists_csv)

    fig = plt.figure()

    ax=fig.add_axes([0,0,1,1])

    ax.scatter(data_table['diffs_to_true'], data_table['distance'])

    plt.show()



if __name__ == '__main__':
    main()
