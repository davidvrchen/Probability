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

sampleSize = 10000
failProb = 0.001

analyzer1 = FirstAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.BINARY_PERTURBING, sample_size = sampleSize, fail_probability = failProb)
analyzer1.print_analyze()

analyzer2 = SecondAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.QUALITY_SCORE_PERTURBING, sample_size = sampleSize, fail_probability = failProb, bounds = [25, 30])
analyzer2.print_analyze()

analyzer3 = ThirdAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.DISTRIBUTED_QUALITY_SCORE, sample_size = sampleSize, goal = failProb)
analyzer3.print_analyze()

mplt.rcParams.update({'font.size': 10})

# Get the error percentages for the total and the repairable errors with theirstandard deviations as pairs 
start = 0
end = 41
x_axis = [j for j in range(start, end)]
# The bounds for analyzer 2
boundsVar = [25, 30]

# Make the error % plots for all Q scores
# For analyzer 1
print("analyzer 1 started")
prob_standard_dev1 = np.zeros((2, 2, end - start))
for j in range(start, end):
    analyzer1 = FirstAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.BINARY_PERTURBING, sample_size = sampleSize, fail_probability = math.pow(10,  -j / 10))
    results_analyzer1 = analyzer1.analyze()
    i = j - start
    prob_standard_dev1[0][0][i] = results_analyzer1[0]
    prob_standard_dev1[0][1][i] = results_analyzer1[3]
    prob_standard_dev1[1][0][i] = results_analyzer1[1]
    prob_standard_dev1[1][1][i] = results_analyzer1[4]
    print("analyzer 1 has results up to ", j)

# For analyzer 2 we use the potential error values as the total error values are the same as analyzer 1
print("analyzer 2 started")
prob_standard_dev2 = np.zeros((2, 2, end - start))
for j in range(start, end):
    analyzer2 = SecondAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.QUALITY_SCORE_PERTURBING, sample_size = sampleSize, fail_probability = math.pow(10,  -j / 10), bounds = boundsVar)
    results_analyzer2 = analyzer2.analyze()
    i = j - start
    prob_standard_dev2[0][0][i] = results_analyzer2[0]
    prob_standard_dev2[0][1][i] = results_analyzer2[6]
    prob_standard_dev2[1][0][i] = results_analyzer2[2]
    prob_standard_dev2[1][1][i] = results_analyzer2[7]
    print("analyzer 2 has results up to ", j)

print("analyzer 3 started")
prob_standard_dev3 = np.zeros((2, 2, end - start))
for j in range(start, end):
    analyzer3 = ThirdAnalyzer(SamplerType.ACID_SAMPLING, PerturberType.DISTRIBUTED_QUALITY_SCORE, sample_size = sampleSize, goal = math.pow(10,  -j / 10))
    results_analyzer3 = analyzer3.analyze()
    i = j - start
    prob_standard_dev3[0][0][i] = results_analyzer3[5]
    prob_standard_dev3[0][1][i] = results_analyzer3[7]
    prob_standard_dev3[1][0][i] = results_analyzer3[6]
    prob_standard_dev3[1][1][i] = results_analyzer3[8]
    print("analyzer 3 has results up to ", j)


fig, axs = plt.subplots(3, sharex = True)

# plot results analyzer 1 in first plot together with the standard deviation
# normal error percentage:
axs[0].plot(x_axis, prob_standard_dev1[0][0], 'red', label = "error % without repairs")
axs[0].plot(x_axis, prob_standard_dev1[0][0] + prob_standard_dev1[0][1], 'blue', label = "std dev without repairs")
axs[0].plot(x_axis, prob_standard_dev1[0][0] - prob_standard_dev1[0][1], 'blue')
# error percentage after repairs:
axs[0].plot(x_axis, prob_standard_dev1[1][0], 'purple', linestyle = 'dashed', label = "error % with repairs")
axs[0].plot(x_axis, prob_standard_dev1[1][0] + prob_standard_dev1[1][1], 'green', linestyle = 'dashed', label = "std dev with repairs")
axs[0].plot(x_axis, prob_standard_dev1[1][0] - prob_standard_dev1[1][1], 'green', linestyle = 'dashed')

# plot results analyzer 2 in second plot together with the standard deviation
# normal error percentage:
axs[1].plot(x_axis, prob_standard_dev2[0][0], 'red', label = "error % without repairs")
axs[1].plot(x_axis, prob_standard_dev2[0][0] + prob_standard_dev2[0][1], 'blue', label = "std dev without repairs")
axs[1].plot(x_axis, prob_standard_dev2[0][0] - prob_standard_dev2[0][1], 'blue')
# error percentage after repairs:
axs[1].plot(x_axis, prob_standard_dev2[1][0], 'purple', linestyle = 'dashed', label = "error % with repairs")
axs[1].plot(x_axis, prob_standard_dev2[1][0] + prob_standard_dev2[1][1], 'green', linestyle = 'dashed', label = "std dev with repairs")
axs[1].plot(x_axis, prob_standard_dev2[1][0] - prob_standard_dev2[1][1], 'green', linestyle = 'dashed')

# plot results analyzer 3 in second plot together with the standard deviation
# minimal q score needed normally:
axs[2].plot(x_axis, prob_standard_dev3[0][0], 'red', label = "min Q score without repairs")
axs[2].plot(x_axis, prob_standard_dev3[0][0] + prob_standard_dev3[0][1], 'blue', label = "std dev without repairs")
axs[2].plot(x_axis, prob_standard_dev3[0][0] - prob_standard_dev3[0][1], 'blue')
# minimal q score needed after repairs:
axs[2].plot(x_axis, prob_standard_dev3[1][0], 'purple', linestyle = 'dashed', label = "min Q score with repairs")
axs[2].plot(x_axis, prob_standard_dev3[1][0] + prob_standard_dev3[1][1], 'green', linestyle = 'dashed', label = "std dev with repairs")
axs[2].plot(x_axis, prob_standard_dev3[1][0] - prob_standard_dev3[1][1], 'green', linestyle = 'dashed')

# Setting labels and grids, comment these out to get plots with no text or grid:

# fig.suptitle("Percentage of errors in the result as a function of the \n probability that a nucleotide in the sequence is perturbed.\n")
axs[0].set(ylabel = "error percentage")
axs[0].set_title("analyzer 1")
# axs[0].set_title("Binary analyzer")
axs[0].legend(loc = "upper right")
axs[0].grid()
axs[0].margins(0)

axs[1].set(ylabel = "error percentage")
axs[1].set_title("analyzer 2")
# axs[1].set_title("Q score analyzer")
axs[1].legend(loc = "upper right")
axs[1].grid()
axs[1].margins(0)

axs[2].set(ylabel = "minimal Q score")
axs[2].set_title("analyzer 3")
# axs[2].set_title("Reverse Q score analyzer")
axs[2].legend(loc = "upper left")
axs[2].grid()
axs[2].margins(0)

# Set x axis label for lowest plot
axs[2].set(xlabel = "Q score for error")

# Uncomment to make x axis not shared
for ax in axs:
    ax.label_outer()

plt.show()
