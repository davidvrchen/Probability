from perturbing.Perturber import Perturber
import random
from utils import Utils as utils
import math
import copy

# Perturbs with a predefined error rate and generates a Q score dependent on a pass or fail.
class QualityScorePerturber(Perturber):

    def __init__(self, fail_probability):
        super().__init__(fail_probability)

    def perturb_sequence(self, sequence, bounds):
        errors = []
        pert_seq = copy.deepcopy(sequence)
        for i in range(len(sequence)):
            p = random.uniform(0,1)
            if p < self.FAILURE_PROBABILITY:
                temp = utils.NUCLEOTIDES.copy()
                temp.remove(sequence[i])
                pert_seq[i] = random.choice(temp)
                q_score_nr = random.randrange(0, bounds[1]) # gives a q score < upper bound for perturbed ones

            else:
                q_score_nr = random.randrange(bounds[0], 41) # gives a q score >= lowe bound for correct ones
            
            q_score_ascii = chr(q_score_nr + 33)
            errors += [q_score_ascii] 

        return [pert_seq, errors]