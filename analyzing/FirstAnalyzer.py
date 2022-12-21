from analyzing.Analyzer import Analyzer
from utils import Utils as utils

class FirstAnalyzer(Analyzer):
    
    def __init__(self, sampler_strategy, perturber_strategy, sample_size=10000):
        super().__init__(sampler_strategy, perturber_strategy, sample_size)

    def print_analyze(self):
        print("Analyzing using FirstAnalyzer")
        analysis = self.analyze()
        print("Total error percentage: ", analysis[0])
        print("Error percentage after repairs: ", analysis[1])
        print("Percentage of errors repaired: ", analysis[2])
        print('\n')

    def analyze(self):
        total = 0
        total_errors = 0
        total_repairable = 0

        totals = [total, total_errors, total_repairable]
        for j in range(self.SAMPLE_SIZE):
            seq = self.sampler.random_sequence()
            pert = self.perturber.perturb_sequence(seq)

            for i in range(len(pert[0])):
                total += 1
                if pert[1][i] == 'W':
                    total_errors += 1
                    if i % 3 == 2:
                        if utils.is_ambig(pert[0][i-2:i+1]):
                            total_repairable += 1

        error_perc = (total_errors / total) * 100
        rep_perc = ((total_errors - total_repairable) / total) * 100
        rep_perc2 = (total_repairable / total_errors) * 100
        return [error_perc, rep_perc, rep_perc2]

    # def analyze_failure(self):
    #     seq = self.sampler.random_sequence()
    #     pert = self.perturber.perturb_sequence(seq)

    #     total = 0
    #     total_errors = 0
    #     total_repairable = 0
        
    #     for i in range(len(pert[0])):
    #         total += 1
    #         if pert[1][i] == 'W':
    #             total_errors += 1
    #             if i % 3 == 2:
    #                 if utils.is_ambig(pert[0][i-2:i+1]):
    #                     total_repairable += 1
        
    #     return [total, total_errors, total_repairable]