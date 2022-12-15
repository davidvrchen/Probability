import utils.RNAsampler as sampler
import utils.AminoAcids as acids

# # TESTING
# print(sampler.random_nucleotide())
# print(acids.get_acid("TCT")) # Expected: S
# print(acids.is_ambig("TCT")) # Expected: True
# print(acids.is_ambig("TGG")) # Expected: False
# print(acids.get_probability("GCT")) # Expected: 0.0777
# print(acids.get_probability("Q")) # Expected: 0.0393
# seq = sampler.random_sequence()
# print(seq)
# print(sampler.perturb_sequence(seq))

print(sampler.analyze_failure())
print(sampler.analyze_failure2())