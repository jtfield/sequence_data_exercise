#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""
import sys
import os

seqfi1 = sys.argv[1]
seqfi2 = sys.argv[2]

file1_name = os.path.basename(seqfi1).split('/')[-1]
file2_name = os.path.basename(seqfi2).split('/')[-1]

def fasta_as_string(filename):
    fi = open(filename)
    seq = ''
    for lin in fi.readlines():
        if lin.startswith('>'):
            name = lin.strip()
        else:
            seq = seq+lin.strip()
    return name, seq


name1, seq1 = fasta_as_string(seqfi1)
name2, seq2 = fasta_as_string(seqfi2)


print("Sequence {f1} is {l1} bp".format(f1=sys.argv[1],l1=len(seq1)))
print("Sequence {f2} is {l2} bp".format(f2=sys.argv[2],l2=len(seq2)))

assert(len(seq1) == len(seq2))

diff_dict = {}
for i, char in enumerate(seq1):
    if char.lower() != seq2[i].lower():
        diff_dict[i] = (char.lower(), seq2[i].lower())


print("The sequences differ at {d} sites".format(d=len(diff_dict)))

bases=set(['a','t','g','c'])
not_gap_diff = 0

differences = open("differences.csv", "w")

keylist = list(diff_dict.keys())
keylist.sort()

differences.write("positions, " + file1_name + ", " + file2_name + "\n")

for i in keylist:
    diff = diff_dict[i]
    if set(diff).issubset(bases):
        not_gap_diff += 1
    differences.write("{i}, {b1}, {b2}\n".format(i=i, b1=diff[0], b2=diff[1]))

differences.close()

print("Of those {d} sites, {ng} are not a gap or an ambiguity code in one taxon".format(d=len(diff_dict), ng=not_gap_diff))
