from perturbing.Perturber import Perturber
import random
from utils import Utils as utils
import math
import copy

# Perturbs with a predefined error rate and generates a Q score dependent on a pass or fail.
class QualityScorePerturber(Perturber):

    def perturb_sequence(self, sequence):
        errors = []
        pert_seq = copy.deepcopy(sequence)
        for i in range(len(sequence)):
            p = random.uniform(0,1)
            if p < self.FAILURE_PROBABILITY:
                temp = utils.NUCLEOTIDES.copy()
                temp.remove(sequence[i])
                pert_seq[i] = random.choice(temp)
                q_score_nr = random.randrange(0, 30) # gives a q score < 30 for perturbed ones

            else:
                q_score_nr = random.randrange(25, 41) # gives a q score >= 25 for correct ones
            
            q_score_ascii = chr(q_score_nr + 33)
            errors += [q_score_ascii] 

        return [pert_seq, errors]