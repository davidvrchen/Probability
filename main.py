from analyzing.FirstAnalyzer import FirstAnalyzer
from analyzing.SecondAnalyzer import SecondAnalyzer
from analyzing.ThirdAnalyzer import ThirdAnalyzer
from perturbing.PerturberStrategy import PerturberType
from sampling.SamplerStrategy import SamplerType
import utils.Utils as utils
import matplotlib.pyplot as plt

analyzer1 = FirstAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.BINARY_PERTURBING, sample_size = 10000, fail_probability = 0.001)
analyzer1.print_analyze()

analyzer2 = SecondAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.QUALITY_SCORE_PERTURBING, sample_size=10000, fail_probability = 0.001, bounds=[29, 30])
analyzer2.print_analyze()

analyzer3 = ThirdAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.DISTRIBUTED_QUALITY_SCORE, sample_size=10000, fail_probability = 0.001)
analyzer3.print_analyze()

# FOR ALL PLOTS ADD STANDARD DEVIATION

# QUESTIONS TO ANSWER WITH PLOTS:
# - What is the probability that the correct amino acid can be recovered? I.e. what is the percentage of errors that are repairable?
# + SUGGESTION: Plot percentage of correct/correctable reads as function of error percentage per sequencer.

# - What are the quality requirements for a machine in order to be able to recover the correct sequence of amino acids 99% of the time?
#   I.e. what is the maximal error percentage (for analyzers 1 & 2) or minimal Q score (for analyzer 3) needed to h
# + Also do this with plots like the first one.

# - is this an extra research question?
# + SUGGESTION: if we have time:
# Given that there is a mistake that we could not correct how many less mistakes should we make to fix the RNA sequence 
# (including the repairable mistakes). Make a histogram for this per analyzer/error percentage