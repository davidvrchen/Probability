from analyzing.Analyzer import Analyzer
from utils import Utils as utils
import random
import copy

class ThirdAnalyzer(Analyzer):

    def __init__(self, sampler_strategy, perturber_strategy, sample_size=10000):
        super().__init__(sampler_strategy, perturber_strategy, sample_size)

    def print_analyze(self):
        print("Analyzing using ThirdAnalyzer")
        analysis = self.analyze()
        print("Total error percentage: ", analysis[0])
        print("Error percentage after repairs: ", analysis[1])
        print("Percentage of errors repaired: ", analysis[2])
        print("Minimal Q score to ensure error probability in all calls with this score or higher is less than the goal: ", analysis[3])
        print('\n')

    def analyze(self):
        total = 0
        total_errors = 0
        total_repairable = 0

        q_scores = [0] * 41
        
        for j in range(self.SAMPLE_SIZE):
            seq = self.sampler.random_sequence()
            pert = self.perturber.perturb_sequence(seq)

            for i in range(len(pert[0])):
                total += 1
                if (pert[0][i] != seq[i]):
                    total_errors += 1
                    q_score_nr = ord(pert[1][i]) - 33
                    q_scores[q_score_nr] += 1
                    if i % 3 == 2:
                        if utils.is_ambig(pert[0][i-2:i+1]):
                            total_repairable += 1

        error_perc = (total_errors / total) * 100
        rep_perc = ((total_errors - total_repairable) / total) * 100
        rep_perc2 = (total_repairable / total_errors) * 100

        achieve_goal = 41 # we decrement it instantly so we start a bit higher
        q_score_error_count = q_scores[40]
        while (((q_score_error_count / total_errors) < self.ERROR_GOAL) and achieve_goal > 0):
            achieve_goal -= 1
            q_score_error_count += q_scores[achieve_goal - 1] # add the values for the next highest Q score


        return [error_perc, rep_perc, rep_perc2, achieve_goal]
