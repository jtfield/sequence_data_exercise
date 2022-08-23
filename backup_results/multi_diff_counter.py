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
    parser.add_argument('--query_seqs', help='The sequences you are stating as reference assembled.')
    return parser.parse_args()

def main():
    args = parse_args()

    true_fi = os.path.basename(args.true_seqs).split('/')[-1]
    query_fi = os.path.basename(args.query_seqs).split('/')[-1]

    true_seqs_contents = open(args.true_seqs).read()
    query_seqs_contents = open(args.query_seqs).read()

    split_query_seqs = query_seqs_contents.split(">")

    ref_name = query_fi.strip('_removed.aln')

    outdir_name = "differences_raw_data_ref_" + ref_name
    true_fi = true_fi.strip(".fasta")
    # outdir_name = outdir_name.strip('.csv').strip('.aln')
    data_outdir = os.mkdir(outdir_name)
    abs_outdir = os.path.abspath(outdir_name)

    # query_fi = query_fi.strip(".fas")
    # query_fi = query_fi.strip(".aln")
    # query_fi = query_fi.strip(".fasta")
    #
    summary = open(abs_outdir + "/diff_summary_query" + str(true_fi) + "_ref_" + str(ref_name) + ".csv", "w")
    summary.write("taxon_name,ref_name,all_unambig_identical,all_ambiguous_diffs,unambiguous_diffs_to_true,unambiguous_diffs_to_true_matching_ref\n")
    #
    for chunk in split_query_seqs:
        if len(chunk) > 1:
            split_name_and_seq = chunk.split("\n", 1)
            ref_based_name = split_name_and_seq[0]
            ref_based_seq = split_name_and_seq[1].strip()

            ref_based_name_and_seq_regex = '(' + ref_based_name + '\s.+)\s'

            actual_ref_name_and_seq_regex = '(' + ref_name + '\s.+)\s'

            print(ref_based_name_and_seq_regex)
            print(actual_ref_name_and_seq_regex)

            compiled_re = re.compile(ref_based_name_and_seq_regex)

            find_seq = re.findall(compiled_re, true_seqs_contents)

            compiled_ref_re = re.compile(actual_ref_name_and_seq_regex)

            find_ref_seq = re.findall(compiled_ref_re, true_seqs_contents)

            if find_seq:
                if find_ref_seq:
                    split_found_seq = find_seq[0].split('\n')
                    true_name = split_found_seq[0]
                    true_seq = split_found_seq[1].strip()

                    split_found_ref_seq = find_ref_seq[0].split('\n')
                    true_ref_name = split_found_ref_seq[0]
                    true_ref_seq = split_found_ref_seq[1].strip()

                    print("Sequence {f1} from ref based seqs is {l1} bp".format(f1=ref_based_name,l1=len(ref_based_seq)))
                    print("Sequence {f2} from true seqs is {l2} bp".format(f2=true_name,l2=len(true_seq)))
                    print("Sequence {f3} from true seqs is {l3} bp".format(f3=ref_name,l3=len(true_ref_seq)))

                    assert(len(ref_based_seq) == len(true_seq) == len(true_ref_seq))

                    bases=set(['a','t','g','c'])
                    diff_dict = {}
                    identical_unambiguous_bases = 0

                    for i, char in enumerate(true_seq):
                        if char.lower() != ref_based_seq[i].lower():
                            diff_dict[i] = (char.lower(), ref_based_seq[i].lower(), true_ref_seq[i].lower())

                        elif char.lower() == ref_based_seq[i].lower():
                            if char.lower() in bases:
                                identical_unambiguous_bases+=1


                    print("The sequences differ at {d} sites".format(d=len(diff_dict)))

                    not_gap_diff = 0
                    not_gap_diff_matching_ref = 0

                    differences = open(abs_outdir + "/differences_" + true_name + ".csv", "w")
                    unam_differences = open(abs_outdir + "/unambig_differences_" + true_name + ".csv", "w")

                    keylist = list(diff_dict.keys())
                    keylist.sort()

                    differences.write("positions," + "true_seq_" + true_name + "," + "ref_based_" + true_name + "," + "actual_ref_" + ref_name + "\n")
                    unam_differences.write("positions," + "true_seq_" + true_name + "," + "ref_based_" + true_name + "," + "actual_ref_" + ref_name + "\n")

                    for i in keylist:
                        diff = diff_dict[i]
                        if set(diff).issubset(bases):
                            not_gap_diff += 1
                            unam_differences.write("{i},{b1},{b2},{b3}\n".format(i=i, b1=diff[0], b2=diff[1], b3=diff[2]))
                            if diff[1] == diff[2]:
                                not_gap_diff_matching_ref += 1
                        differences.write("{i},{b1},{b2},{b3}\n".format(i=i, b1=diff[0], b2=diff[1], b3=diff[2]))

                    differences.close()
                    unam_differences.close()

                    print("Of those {d} sites, {ng} are not a gap or an ambiguity code in one taxon. Of the unambiguous sites, {rb} sites match the ref site".format(d=len(diff_dict), ng=not_gap_diff, rb=not_gap_diff_matching_ref))
                # summary = open("diff_summary_" + str(true_fi) + "_" + str(ref_fi) + ".txt", "w")

                    summary.write("{t},{r},{ui},{ad},{d},{b}\n".format(t=true_name, r=ref_name, ui=identical_unambiguous_bases ,ad=len(diff_dict), d=not_gap_diff, b=not_gap_diff_matching_ref))


    summary.close()



if __name__ == '__main__':
    main()
