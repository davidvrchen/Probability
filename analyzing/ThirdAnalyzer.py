import math
from analyzing.Analyzer import Analyzer
from utils import Utils as utils
import random
import copy

class ThirdAnalyzer(Analyzer):

    def __init__(self, sampler_strategy, perturber_strategy, sample_size=10000, goal = 0.01):
        super().__init__(sampler_strategy, perturber_strategy, sample_size, goal)
        self.ERROR_GOAL = goal

    def print_analyze(self):
        print("Analyzing using ThirdAnalyzer")
        analysis = self.analyze()
        print("Total error percentage: ", analysis[0])
        print("Error percentage after repairs: ", analysis[1])
        print("Percentage of errors repaired: ", analysis[2])
        print("Standard deviation for total errors: ", analysis[3])
        print("Standard deviation for errors after repairs: ", analysis[4])
        print("Minimal Q score to ensure error probability without repairsthis score or higher is less than the goal: ", analysis[5])
        print("Minimal Q score to ensure error probability with repairsthis score or higher is less than the goal: ", analysis[6])
        print("Standard deviation for the minimal Q score without repairs: ", analysis[7])
        print("Standard deviation for the minimal Q score with repairs: ", analysis[8])
        # print("Percentage of readings with a Q score above 30 that are incorrect: ", analysis[6])
        
        print('\n')

    def analyze(self):
        total = 0
        total_errors = 0
        total_repairable = 0

        q_scores_error = [0 for i in range(41)]
        q_scores_total = [0 for i in range(41)]
        q_scores_repaired = [0 for i in range(41)] 

        no_rep_min_qscores = 0
        rep_min_qscores = 0

        deviations = [0 for i in range(self.SAMPLE_SIZE)]
        repairable_deviations = [0 for i in range(self.SAMPLE_SIZE)]
        no_reps_min_qscore_deviation = [0 for i in range(self.SAMPLE_SIZE)]
        rep_min_qscore_deviation = [0 for i in range(self.SAMPLE_SIZE)]

        for j in range(self.SAMPLE_SIZE):
            seq = self.sampler.random_sequence()
            pert = self.perturber.perturb_sequence(seq)

            old_total = total
            old_total_repairable = total_repairable
            old_total_errors = total_errors
            old_no_rep_min_qscores = no_rep_min_qscores
            old_rep_min_qscores = rep_min_qscores
            old_q_scores_error = copy.deepcopy(q_scores_error)
            old_q_scores_total = copy.deepcopy(q_scores_total)

            for i in range(len(pert[0])):
                total += 1
                q_score_nr = ord(pert[1][i]) - 33
                q_scores_total[q_score_nr] += 1
                if (pert[0][i] != seq[i]):
                    total_errors += 1
                    q_scores_error[q_score_nr] += 1
                    if i % 3 == 2:
                        if utils.is_ambig(pert[0][i-2:i+1]):
                            total_repairable += 1
                            q_scores_repaired[q_score_nr] +=1
            
            deviations[j] = (total_errors - old_total_errors) / (total - old_total) * 100
            repairable_deviations[j] = (total_errors - old_total_errors - (total_repairable - old_total_repairable)) / (total - old_total) * 100

            # The rest of the loop calculates the minimally required Q-score to have an error percentage lower than the goal

            achieve_goal = 41 # we decrement it instantly so we start a bit higher
            q_score_error_count = q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1]
            reading_count = q_scores_total[achieve_goal - 1] - old_q_scores_total[achieve_goal - 1]
            rep_q_score_error_count = q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1] - q_scores_repaired[achieve_goal - 1]

            if (reading_count == 0):
                achieve_goal -= 1
                q_score_error_count += q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1] # add the values for the next highest Q score
                reading_count += q_scores_total[achieve_goal - 1] - old_q_scores_total[achieve_goal - 1]
                rep_q_score_error_count += q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1] - q_scores_repaired[achieve_goal - 1]
                # TODO: Fix the geq_set_wrong_perc and add one for repairable and maybe make geq_30_wrong_perc geq_set_wrong_perc which uses a variable
                if(achieve_goal == 30):
                    geq_30_wrong_perc = q_score_error_count / reading_count   

            while (((q_score_error_count / reading_count) < self.ERROR_GOAL) and achieve_goal > 0):
                achieve_goal -= 1
                q_score_error_count += q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1] # add the values for the next highest Q score
                reading_count += q_scores_total[achieve_goal - 1] - old_q_scores_total[achieve_goal - 1]
                rep_q_score_error_count += q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1] - q_scores_repaired[achieve_goal - 1]
                # TODO: Fix the geq_set_wrong_perc and add one for repairable and maybe make geq_30_wrong_perc geq_set_wrong_perc which uses a variable
                if(achieve_goal == 30):
                    geq_30_wrong_perc = q_score_error_count / reading_count                
            
            # set here and continue with repairable
            no_rep_min_qscores += achieve_goal

            while (((rep_q_score_error_count / reading_count) < self.ERROR_GOAL) and achieve_goal > 0):
                achieve_goal -= 1
                rep_q_score_error_count += q_scores_error[achieve_goal - 1] - old_q_scores_error[achieve_goal - 1] - q_scores_repaired[achieve_goal - 1]
                # TODO: Fix the geq_30_wrong_perc and add one for repairable and maybe make geq_30_wrong_perc geq_set_wrong_perc which uses a variable
                if(achieve_goal == 30):
                    geq_30_wrong_perc = q_score_error_count / reading_count 

            # TODO: Implement the deviation calculation
            rep_min_qscores += achieve_goal

            no_reps_min_qscore_deviation[j] = no_rep_min_qscores - old_no_rep_min_qscores
            rep_min_qscore_deviation[j] = rep_min_qscores - old_rep_min_qscores

        error_perc = (total_errors / total) * 100
        rep_perc = ((total_errors - total_repairable) / total) * 100
        rep_perc2 = (total_repairable / total_errors) * 100

        # TODO: use this in output to replace achieve_goal
        no_rep_avg_qscore_error = round(no_rep_min_qscores / self.SAMPLE_SIZE)
        rep_avg_qscore_error = round(rep_min_qscores / self.SAMPLE_SIZE)

        # calculate sample standard deviation as we clearly only have a sample
        standard_deviation = 0
        standard_deviation_repairable = 0
        std_dev_no_rep_qscores = 0
        std_dev_rep_qscores = 0
        for k in range(self.SAMPLE_SIZE):
            standard_deviation += math.pow(deviations[k] - error_perc, 2)
            standard_deviation_repairable += math.pow(repairable_deviations[k] - rep_perc, 2)

            std_dev_no_rep_qscores += math.pow(no_reps_min_qscore_deviation[k] - no_rep_avg_qscore_error, 2)
            std_dev_rep_qscores += math.pow(rep_min_qscore_deviation[k] - rep_avg_qscore_error, 2)

        standard_deviation = math.pow(standard_deviation / (self.SAMPLE_SIZE - 1), 1/2)
        standard_deviation_repairable = math.pow(standard_deviation_repairable / (self.SAMPLE_SIZE - 1), 1/2)        

        # TODO: Use standard deviation in output
        std_dev_no_rep_qscores = math.pow(std_dev_no_rep_qscores / (self.SAMPLE_SIZE - 1), 1/ 2)
        std_dev_rep_qscores = math.pow(std_dev_rep_qscores / (self.SAMPLE_SIZE - 1), 1 / 2)
        return [error_perc, rep_perc, rep_perc2, standard_deviation, standard_deviation_repairable, no_rep_avg_qscore_error, rep_avg_qscore_error, standard_deviation, standard_deviation_repairable]
