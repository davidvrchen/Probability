import math
from analyzing.Analyzer import Analyzer
from utils import Utils as utils

class FirstAnalyzer(Analyzer):
    
    def __init__(self, sampler_strategy, perturber_strategy, sample_size=10000, fail_probability = 0.01):
        super().__init__(sampler_strategy, perturber_strategy, sample_size, fail_probability)

    def print_analyze(self):
        print("Analyzing using FirstAnalyzer")
        analysis = self.analyze()
        print("Total error percentage: ", analysis[0])
        print("Error percentage after repairs: ", analysis[1])
        print("Percentage of errors repaired: ", analysis[2])
        print("Standard deviation for total errors: ", analysis[3])
        print("Standard deviation for errors after repairs: ", analysis[4])
        print('\n')

    def analyze(self):
        total = 0
        total_errors = 0
        total_repairable = 0

        deviations = [0 for i in range(self.SAMPLE_SIZE)]
        repairable_deviations = [0 for i in range(self.SAMPLE_SIZE)]
        totals = [total, total_errors, total_repairable]

        for j in range(self.SAMPLE_SIZE):
            seq = self.sampler.random_sequence()
            pert = self.perturber.perturb_sequence(seq)
            old_total = total
            old_total_repairable = total_repairable
            old_total_errors = total_errors

            for i in range(len(pert[0])):
                total += 1
                if pert[1][i] == 'W':
                    total_errors += 1
                    if i % 3 == 2:
                        if utils.is_ambig(pert[0][i-2:i+1]):
                            total_repairable += 1

            deviations[j] = (total_errors - old_total_errors) / (total - old_total) * 100
            repairable_deviations[j] = (total_errors - old_total_errors - (total_repairable - old_total_repairable)) / (total - old_total) * 100

        error_perc = (total_errors / total) * 100
        rep_perc = ((total_errors - total_repairable) / total) * 100
        rep_perc2 = (total_repairable / total_errors) * 100

        # calculate standard deviation
        standard_deviation = 0
        standard_deviation_repairable = 0
        for k in range(self.SAMPLE_SIZE):
            standard_deviation += math.pow(deviations[k] - error_perc, 2)
            standard_deviation_repairable += math.pow(repairable_deviations[k] - rep_perc, 2)

        standard_deviation = math.pow(standard_deviation / self.SAMPLE_SIZE, 1/2)
        standard_deviation_repairable = math.pow(standard_deviation_repairable / self.SAMPLE_SIZE, 1/2)

        return [error_perc, rep_perc, rep_perc2, standard_deviation, standard_deviation_repairable]
