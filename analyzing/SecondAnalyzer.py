from analyzing.Analyzer import Analyzer
from utils import Utils as utils
import random
import copy

class SecondAnalyzer(Analyzer):

    def __init__(self, sampler_strategy, perturber_strategy, sample_size=10000):
        super().__init__(sampler_strategy, perturber_strategy, sample_size)

    def print_analyze(self):
        print("Analyzing using SecondAnalyzer")
        analysis = self.analyze()
        print("Total error percentage: ", analysis[0])
        print("Error percentage after repairs: ", analysis[1])
        print("Percentage of errors repaired: ", analysis[2])
        print("Percentage of corrected base pairs: ", analysis[3])
        print("Percentage of unfixed uncertainties: ", analysis[4])
        print("Percentage of correct readings with 25 <= qScore < 30: ", analysis[5])
        print("Percentage of readings fixed by guessing: ", analysis[6])
        print('\n')

    def analyze(self):
        total = 0
        total_errors = 0
        total_repairable = 0
        uncertain_unchanged = 0
        uncertain_changed = 0
        correct_uncertainties = 0
        guessed_uncertainties = 0
        unfixed_errors = 0

        for j in range(self.SAMPLE_SIZE):
            seq = self.sampler.random_sequence()
            pert = self.perturber.perturb_sequence(seq)
            attempted_fix = copy.deepcopy(pert[0])

            for i in range(len(pert[0])):
                total += 1
                if ord(pert[1][i]) < 63: # if the qScoreNr was lower than 30, so there could have been an error (defined in code)
                    total_errors += 1
                    if i % 3 == 2:
                        if utils.is_ambig(pert[0][i-2:i+1]):
                            total_repairable += 1
                        elif (ord(pert[1][i]) >=  58): # qScore >= 25 = 58 - 33 might be correct 
                            uncertain_unchanged += 1 
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

        error_perc = (total_errors / total) * 100
        rep_perc = ((total_errors - total_repairable) / total) * 100
        rep_perc2 = (total_repairable / total_errors) * 100
        corrected_perc = ((total_errors - total_repairable - correct_uncertainties) / total_errors) * 100

        # return -1 if not possible (very low channce)
        unfixed_uncertainties = -1
        high_qScore_correct_perc = -1
        correct_guess_perc = -1

        if (uncertain_unchanged > 0 or uncertain_changed > 0):
            unfixed_uncertainties = ((unfixed_errors) / (uncertain_unchanged + uncertain_changed)) * 100

        if (uncertain_unchanged > 0):
            # percentage of correct readings with 25 <= qScore < 30
            high_qScore_correct_perc = ((correct_uncertainties) / uncertain_unchanged) * 100 
        
        if (uncertain_changed > 0): 
            # percentage of readings that were correctly fixed by guessing, could be interesting for some models
            correct_guess_perc = ((uncertain_changed - (uncertain_changed - guessed_uncertainties)) / uncertain_changed) * 100 
           

        return [error_perc, rep_perc, rep_perc2, corrected_perc, unfixed_uncertainties, high_qScore_correct_perc, correct_guess_perc]

    # def analyze_failure(self):
    #     total = 0
    #     total_errors = 0
    #     total_repairable = 0
    #     uncertain_unchanged = 0
    #     uncertain_changed = 0
    #     correct_uncertainties = 0
    #     guessed_uncertainties = 0
    #     unfixed_errors = 0

    #     for j in range(self.SAMPLE_SIZE):
    #         seq = self.sampler.random_sequence()
    #         pert = self.perturber.perturb_sequence(seq)
    #         attempted_fix = [i for i in pert[1]]
    #         for i in range(len(pert[0])):
    #             total += 1
    #             if ord(pert[1][i]) < 63: # if the qScoreNr was lower than 30, so there was an error (defined in code)
    #                 total_errors += 1
    #                 if i % 3 == 2:
    #                     if utils.is_ambig(pert[0][i-2:i+1]):
    #                         total_repairable += 1
    #                     elif (ord(pert[1][i]) >  58): # qScore > 25 might be correct
    #                         uncertain_unchanged += 1 
    #                         if (attempted_fix[i] == seq[i]):
    #                             correct_uncertainties += 1
    #                         else: 
    #                             unfixed_errors += 1
    #                     else:
    #                         temp = utils.NUCLEOTIDES.copy()
    #                         temp.remove(pert[0][i])
    #                         attempted_fix[i] = random.choice(temp)
    #                         uncertain_changed += 1
    #                         if (attempted_fix[i] == seq[i]):
    #                             guessed_uncertainties += 1
    #                         else: 
    #                             unfixed_errors += 1
    #     return [total,total_errors,total_repairable,uncertain_unchanged,uncertain_changed,correct_uncertainties,guessed_uncertainties,unfixed_errors]
