import math
import pprint

from analyzing.FirstAnalyzer import FirstAnalyzer
from analyzing.SecondAnalyzer import SecondAnalyzer
from analyzing.ThirdAnalyzer import ThirdAnalyzer
from perturbing.PerturberStrategy import PerturberType
from sampling.SamplerStrategy import SamplerType
import utils.Utils as utils
import matplotlib as mplt
import matplotlib.pyplot as plt
import numpy as np

# analyzer1 = FirstAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.BINARY_PERTURBING, sample_size = 10000, fail_probability = 0.001)
# analyzer1.print_analyze()

# analyzer2 = SecondAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.QUALITY_SCORE_PERTURBING, sample_size = 10000, fail_probability = 0.001, bounds = [25, 30])
# analyzer2.print_analyze()

# analyzer3 = ThirdAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.DISTRIBUTED_QUALITY_SCORE, sample_size = 10000, goal = 0.001)
# analyzer3.print_analyze()

# Get the error percentages for the total and the repairable errors with theirstandard deviations as pairs 

# For analyzer 1
print("analyzer 1 started")
prob_standard_dev1 = np.zeros((2, 2, 41))
for i in range(41):
    analyzer1 = FirstAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.BINARY_PERTURBING, sample_size = 10000, fail_probability = math.pow(10,  -i / 10))
    results_analyzer1 = analyzer1.analyze()
    prob_standard_dev1[0][0][i] = results_analyzer1[0]
    prob_standard_dev1[0][1][i] = results_analyzer1[3]
    prob_standard_dev1[1][0][i] = results_analyzer1[1]
    prob_standard_dev1[1][1][i] = results_analyzer1[4]
    print("analyzer 1 has results up to ", i)

x_axis = [i for i in range(41)]

# For analyzer 2 we use the potential error values as the total error values are the same as analyzer 1
print("analyzer 2 started")
prob_standard_dev2 = np.zeros((2, 2, 41))
for i in range(41):
    analyzer2 = SecondAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.QUALITY_SCORE_PERTURBING, sample_size=10000, fail_probability = math.pow(10,  -i / 10), bounds = [25, 30])
    results_analyzer2 = analyzer2.analyze()
    prob_standard_dev2[0][0][i] = results_analyzer2[0]
    prob_standard_dev2[0][1][i] = results_analyzer2[6]
    prob_standard_dev2[1][0][i] = results_analyzer2[2]
    prob_standard_dev2[1][1][i] = results_analyzer2[7]
    print("analyzer 2 has results up to ", i)

print("analyzer 3 started")
prob_standard_dev3 = np.zeros((2, 2, 41))
for i in range(41):
    analyzer3 = ThirdAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.DISTRIBUTED_QUALITY_SCORE, sample_size = 10000, goal = math.pow(10,  -i / 10))
    results_analyzer3 = analyzer3.analyze()
    prob_standard_dev3[0][0][i] = results_analyzer3[5]
    prob_standard_dev3[0][1][i] = results_analyzer3[7]
    prob_standard_dev3[1][0][i] = results_analyzer3[6]
    prob_standard_dev3[1][1][i] = results_analyzer3[8]
    print("analyzer 3 has results up to ", i)

fig, axs = plt.subplots(3, sharex=True)

# plot results analyzer 1 in first plot together with the standard deviation
# normal error percentage:
axs[0].plot(x_axis, prob_standard_dev1[1][0], 'red')
axs[0].plot(x_axis, prob_standard_dev1[0][0] + prob_standard_dev1[0][1], 'blue')
axs[0].plot(x_axis, prob_standard_dev1[0][0] - prob_standard_dev1[0][1], 'blue')
# error percentage after repairs:
axs[0].plot(x_axis, prob_standard_dev1[1][0], 'purple', linestyle = 'dashed')
axs[0].plot(x_axis, prob_standard_dev1[1][0] + prob_standard_dev1[1][1], 'green', linestyle = 'dashed')
axs[0].plot(x_axis, prob_standard_dev1[1][0] - prob_standard_dev1[1][1], 'green', linestyle = 'dashed')

# plot results analyzer 2 in second plot together with the standard deviation
# normal error percentage:
axs[1].plot(x_axis, prob_standard_dev2[0][0], 'red')
axs[1].plot(x_axis, prob_standard_dev2[0][0] + prob_standard_dev2[0][1], 'blue')
axs[1].plot(x_axis, prob_standard_dev2[0][0] - prob_standard_dev2[0][1], 'blue')
# error percentage after repairs:
axs[1].plot(x_axis, prob_standard_dev2[1][0], 'purple', linestyle = 'dashed')
axs[1].plot(x_axis, prob_standard_dev2[1][0] + prob_standard_dev2[1][1], 'green', linestyle = 'dashed')
axs[1].plot(x_axis, prob_standard_dev2[1][0] - prob_standard_dev2[1][1], 'green', linestyle = 'dashed')

# plot results analyzer 3 in second plot together with the standard deviation
# minimal q score needed normally:
axs[2].plot(x_axis, prob_standard_dev3[0][0], 'red')
axs[2].plot(x_axis, prob_standard_dev3[0][0] + prob_standard_dev3[0][1], 'blue')
axs[2].plot(x_axis, prob_standard_dev3[0][0] - prob_standard_dev3[0][1], 'blue')
# minimal q score needed after repairs:
axs[2].plot(x_axis, prob_standard_dev3[1][0], 'purple', linestyle = 'dashed')
axs[2].plot(x_axis, prob_standard_dev3[1][0] + prob_standard_dev3[1][1], 'green', linestyle = 'dashed')
axs[2].plot(x_axis, prob_standard_dev3[1][0] - prob_standard_dev3[1][1], 'green', linestyle = 'dashed')

# Setting labels, comment these out to get plots with no text:
mplt.rcParams.update({'font.size': 10})
fig.suptitle("Percentage of errors in the result as a function of the \n probability that a nucleotide in the sequence is perturbed.")
axs[0].set(ylabel = "error percentage")
axs[0].set_title("analyzer 1")
# axs[0].set_title("Binary analyzer")

axs[1].set(ylabel = "error percentage")
axs[1].set_title("analyzer 2")
# axs[1].set_title("Q score analyzer")

axs[2].set(ylabel = "minimal Q score")
axs[2].set_title("analyzer 3")
# axs[2].set_title("Reverse Q score analyzer")

# Set x axis label for lowest plot
axs[2].set(xlabel = "Q score for error")

# Uncomment to make x axis not shared
for ax in axs:
    ax.label_outer()

plt.show()


# QUESTIONS TO ANSWER WITH PLOTS:
# - What is the probability that the correct amino acid can be recovered? I.e. what is the percentage of errors that are repairable?
# + SUGGESTION: Plot percentage of correct/correctable reads as function of error probability per sequencer.

# - What are the quality requirements for a machine in order to be able to recover the correct sequence of amino acids 99% of the time?
#   I.e. what is the maximal error percentage (for analyzers 1 & 2) or minimal Q score (for analyzer 3) needed to have get 99% accuracy for repairable? 
# + Can directly be answered from first graph with percentage of correct reads >= 99 I think

# - is this an extra research question?
# + SUGGESTION: if we have time:
# Given that there is a mistake that we could not correct how many less mistakes should we make to fix the RNA sequence 
# (including the repairable mistakes). Make a histogram for this per analyzer/error percentage