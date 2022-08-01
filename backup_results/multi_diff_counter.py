#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""

import os
import argparse
import re
import pathlib
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(prog='multi_diff_counter.py', \
        description='Compare original sequences to ref_based sequences. One alignment of original sequences and one of ref based sequences.')
    # parser.add_argument('--metadata_csv', default=False, help='metadata csv with info on samples from the tree.')
    parser.add_argument('--true_seqs', help='The sequences you are stating as true.')
    parser.add_argument('--ref_seqs', help='The sequences you are stating as reference assembled.')
    return parser.parse_args()

def main():
    args = parse_args()

    true_fi = os.path.basename(args.true_seqs).split('/')[-1]
    ref_fi = os.path.basename(args.ref_seqs).split('/')[-1]

    outdir_name = "differences_raw_data_" + ref_fi
    data_outdir = os.mkdir(outdir_name)
    abs_outdir = os.path.abspath(outdir_name)

    true_fi = true_fi.strip(".fasta")
    ref_fi = ref_fi.strip(".fas")
    ref_fi = ref_fi.strip(".aln")
    ref_fi = ref_fi.strip(".fasta")

    summary = open(abs_outdir + "/diff_summary_" + str(true_fi) + "_" + str(ref_fi) + ".csv", "w")
    summary.write("taxon_name, ref_name, diffs_to_true\n")

    true_seqs_contents = open(args.true_seqs).read()
    ref_seqs_contents = open(args.ref_seqs).read()

    split_ref_seqs = ref_seqs_contents.split(">")

    for chunk in split_ref_seqs:
        if len(chunk) > 1:
            split_name_and_seq = chunk.split("\n", 1)
            ref_based_name = split_name_and_seq[0]
            ref_based_seq = split_name_and_seq[1].strip()

            ref_name_and_seq_regex = '(' + ref_based_name + '\s.+)\s'
            # print(ref_name_and_seq_regex)
            compiled_re = re.compile(ref_name_and_seq_regex)

            find_seq = re.findall(compiled_re, true_seqs_contents)

            if find_seq:
                split_found_seq = find_seq[0].split('\n')
                true_name = split_found_seq[0]
                true_seq = split_found_seq[1].strip()

                print("Sequence {f1} from ref based seqs is {l1} bp".format(f1=ref_based_name,l1=len(ref_based_seq)))
                print("Sequence {f2} from true seqs is {l2} bp".format(f2=true_name,l2=len(true_seq)))

                assert(len(ref_based_seq) == len(true_seq))

                diff_dict = {}
                for i, char in enumerate(true_seq):
                    if char.lower() != ref_based_seq[i].lower():
                        diff_dict[i] = (char.lower(), ref_based_seq[i].lower())


                print("The sequences differ at {d} sites".format(d=len(diff_dict)))

                bases=set(['a','t','g','c'])
                not_gap_diff = 0

                differences = open(abs_outdir + "/differences_" + true_name + ".csv", "w")

                keylist = list(diff_dict.keys())
                keylist.sort()

                differences.write("positions, " + true_fi + ", " + ref_fi + "\n")

                for i in keylist:
                    diff = diff_dict[i]
                    if set(diff).issubset(bases):
                        not_gap_diff += 1
                    differences.write("{i}, {b1}, {b2}\n".format(i=i, b1=diff[0], b2=diff[1]))

                differences.close()

                print("Of those {d} sites, {ng} are not a gap or an ambiguity code in one taxon".format(d=len(diff_dict), ng=not_gap_diff))
                # summary = open("diff_summary_" + str(true_fi) + "_" + str(ref_fi) + ".txt", "w")

                summary.write("{t}, {r}, {d}\n".format(t=true_name, r=ref_fi, d=not_gap_diff))


    summary.close()



if __name__ == '__main__':
    main()
