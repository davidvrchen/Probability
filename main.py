from utils.RNAsampler import random_nucleotide
import utils.AminoAcids as acids

# TESTING
print(random_nucleotide())
print(acids.get_acid("TCT")) # Expected: S
print(acids.is_ambig("TCT")) # Expected: True
print(acids.is_ambig("TGG")) # Expected: False
print(acids.get_probability("GCT")) # Expected: 0.0777
print(acids.get_probability("Q")) # Expected: 0.0393


import pandas as pd

df = pd.read_csv("RNA_seqs/seq1.csv")

print(df.head())
