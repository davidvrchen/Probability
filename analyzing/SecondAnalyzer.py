import math
from analyzing.Analyzer import Analyzer
from utils import Utils as utils
import random
import copy

class SecondAnalyzer(Analyzer):

    def __init__(self, sampler_strategy, perturber_strategy, sample_size=10000, fail_probability = 0.01, bounds = [25, 30]):
        super().__init__(sampler_strategy, perturber_strategy, sample_size, fail_probability)
        self.BOUNDS = bounds

    def print_analyze(self):
        print("Analyzing using SecondAnalyzer")
        analysis = self.analyze()
        print("Total potential error percentage: ", analysis[0]) # potential_error_percentage
        print("Total actual error percentage: ", analysis[1]) # actual_error_percentage
        print("Potential error percentage after repairs: ", analysis[2]) #rep_perc
        print("Percentage of potential errors that were repaired or correct: ", analysis[3]) #rep_perc2
        print("Actual error percentage after repairs: ", analysis[4]) #actual_rep_perc
        print("Percentage of actual errors that were repaired or correct: ", analysis[5]) #actual_rep_perc2
        
        print("Standard deviation for total potential errors: ", analysis[6])
        print("Standard deviation for potential errors after repairs: ", analysis[7])
        print("Standard deviation for total actual errors: ", analysis[8])
        print("Standard deviation for actual errors after repairs: ", analysis[9])

        print("Percentage of actual errors that were unrepairable and have Q score >=", self.BOUNDS[0], " : ", analysis[10])
        print("Percentage of correct readings with ", self.BOUNDS[0], " <= Q score < ", self.BOUNDS[1], ": ", analysis[11])
        print("Percentage of incorrect uncertainties: ", analysis[12])
        print("Percentage of readings fixed by guessing: ", analysis[13])
        print('\n')

    def analyze(self):
        total = 0
        actual_errors = 0
        potential_errors = 0
        total_repairable = 0
        actual_errors_repairable = 0

        uncertain_unchanged = 0
        uncertain_changed = 0
        correct_uncertainties = 0
        guessed_uncertainties = 0
        unfixed_errors = 0

        potential_deviations = [0 for i in range(self.SAMPLE_SIZE)]
        potential_repairable_deviations = [0 for i in range(self.SAMPLE_SIZE)]
        actual_deviations = [0 for i in range(self.SAMPLE_SIZE)]
        actual_repairable_deviations = [0 for i in range(self.SAMPLE_SIZE)]

        for j in range(self.SAMPLE_SIZE):
            seq = self.sampler.random_sequence()
            pert = self.perturber.perturb_sequence(seq, self.BOUNDS)
            attempted_fix = copy.deepcopy(pert[0])

            old_total = total
            old_potential_errors = potential_errors
            old_total_repairable = total_repairable
            old_correct_uncertainties = correct_uncertainties
            old_actual_errors = actual_errors
            old_actual_repairable = actual_errors_repairable

            for i in range(len(pert[0])):
                total += 1
                if ord(pert[1][i]) < self.BOUNDS[1] + 33: # if the q_score_nr was lower than the upper bound, so there could have been an error (defined in code)
                    potential_errors += 1
                    if(pert[0][i] != seq[i]):
                        actual_errors += 1
                        if (i % 3 == 2 and utils.is_ambig(pert[0][i-2:i+1])):
                            actual_errors_repairable += 1
                    
                    if (i % 3 == 2 and utils.is_ambig(pert[0][i-2:i+1])):
                        total_repairable += 1 # big overlap with this and correct_uncertainties  
                    elif (ord(pert[1][i]) >=  self.BOUNDS[0] + 33): # q_score_nr >= lower bound, so it might be correct
                        uncertain_unchanged += 1 
                        # need to change to fix acids not nucleotides
                        if (attempted_fix[i] == seq[i]): 
                            correct_uncertainties += 1
                        else: 
                            unfixed_errors += 1
                    else:
                        temp = utils.NUCLEOTIDES.copy()
                        temp.remove(pert[0][i])
                        attempted_fix[i] = random.choice(temp)
                        uncertain_changed += 1
                        
                        if (attempted_fix[i] == seq[i]): 
                            guessed_uncertainties += 1
                        else: 
                            unfixed_errors += 1

            potential_deviations[j] = (potential_errors - old_potential_errors) / (total - old_total) * 100
            # potential_repairable_deviations[j] = potential_errors - old_potential_errors - (total_repairable + correct_uncertainties - old_total_repairable - old_correct_uncertainties)
            potential_repairable_deviations[j] = potential_errors - old_potential_errors - (total_repairable - old_total_repairable)
            potential_repairable_deviations[j] = potential_repairable_deviations[j] / (total - old_total) * 100
            actual_deviations[j] = (actual_errors - old_actual_errors) / (total - old_total) * 100
            actual_repairable_deviations[j] = (actual_errors - old_actual_errors - (actual_errors_repairable - old_actual_repairable)) / (total - old_total) * 100

        potential_error_perc = (potential_errors / total) * 100
        actual_error_perc = (actual_errors / total) * 100 
        rep_perc = ((potential_errors - total_repairable) / total) * 100 
        actual_rep_perc = ((actual_errors - actual_errors_repairable) / total) * 100
        rep_perc2 = ((total_repairable + correct_uncertainties) / potential_errors) * 100 
        actual_rep_perc2 = ((actual_errors_repairable) / actual_errors) * 100 
        
        # calculate standard deviation 
        potential_standard_deviation = 0
        potential_standard_deviation_repairable = 0
        actual_standard_deviation = 0
        actual_standard_deviation_repairable = 0
        for k in range(self.SAMPLE_SIZE):
            potential_standard_deviation += math.pow(potential_deviations[k] - potential_error_perc, 2)
            potential_standard_deviation_repairable += math.pow(potential_repairable_deviations[k] - rep_perc, 2)
            actual_standard_deviation += math.pow(actual_deviations[k] - potential_error_perc, 2)
            actual_standard_deviation_repairable += math.pow(actual_repairable_deviations[k] - actual_rep_perc, 2)

        potential_standard_deviation = math.pow(potential_standard_deviation / self.SAMPLE_SIZE, 1/2)
        potential_standard_deviation_repairable = math.pow(potential_standard_deviation_repairable / self.SAMPLE_SIZE, 1/2)
        actual_standard_deviation = math.pow(actual_standard_deviation / self.SAMPLE_SIZE, 1/2)
        actual_standard_deviation_repairable = math.pow(actual_standard_deviation_repairable / self.SAMPLE_SIZE, 1/2)

        unrepairable_uncertain_perc = ((uncertain_unchanged - correct_uncertainties) / actual_errors) * 100 
        
        # return -1 if not possible (very low channce)
        high_q_score_correct_perc = -1
        unfixed_potential_errors = -1
        correct_guess_perc = -1

        if (uncertain_unchanged > 0):
            # percentage of correct readings with 25 <= q_score < 30
            high_q_score_correct_perc = ((correct_uncertainties) / uncertain_unchanged) * 100 
        
        if (uncertain_unchanged > 0 or uncertain_changed > 0):
            unfixed_potential_errors = ((unfixed_errors) / (uncertain_unchanged + uncertain_changed)) * 100
        
        if (uncertain_changed > 0): 
            # percentage of readings that were correctly fixed by guessing, could be interesting for some models
            correct_guess_perc = ((uncertain_changed - (uncertain_changed - guessed_uncertainties)) / uncertain_changed) * 100            

        return [potential_error_perc, actual_error_perc, rep_perc, rep_perc2, actual_rep_perc, actual_rep_perc2, 
                    potential_standard_deviation, potential_standard_deviation_repairable, actual_standard_deviation, 
                    actual_standard_deviation_repairable, unrepairable_uncertain_perc, high_q_score_correct_perc, 
                    unfixed_potential_errors, correct_guess_perc]
