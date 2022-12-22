from analyzing.FirstAnalyzer import FirstAnalyzer
from analyzing.SecondAnalyzer import SecondAnalyzer
from analyzing.ThirdAnalyzer import ThirdAnalyzer
from perturbing.PerturberStrategy import PerturberType
from sampling.SamplerStrategy import SamplerType
import utils.Utils as utils

# # TESTING
# print(sampler.random_nucleotide())
# print(acids.get_acid("TCT")) # Expected: S
# print(utils.is_ambig("TCT")) # Expected: True
# print(utils.is_ambig("TGG")) # Expected: False
# print(acids.get_probability("GCT")) # Expected: 0.0777
# print(acids.get_probability("Q")) # Expected: 0.0393
# seq = sampler.random_sequence()
# print(seq)
# print(sampler.perturb_sequence(seq))

#print(sampler.analyze_failure())
#print(sampler.analyze_failure2())

# analyzer1 = FirstAnalyzer(SamplerType.UNIFORM_SAMPLING, PerturberType.BINARY_PERTURBING)
# analyzer1.print_analyze()
analyzer2 = SecondAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.QUALITY_SCORE_PERTURBING, sample_size = 1000)
analyzer2.print_analyze()
# analyzer3 = ThirdAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.DISTRIBUTED_QUALITY_SCORE, sample_size = 1000)
# analyzer3.print_analyze()