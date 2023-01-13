from perturbing.Perturber import Perturber
import random
from utils import Utils as utils
import math
import copy

# Takes uniformly distributed Q scores and perturbs with an error rate based on the Q score.
class SecondQualityScorePerturber(Perturber):

    def __init__(self, fail_probability):
        super().__init__(fail_probability)

    def perturb_sequence(self, sequence):
        errors = []
        pert_seq = copy.deepcopy(sequence)
        for i in range(len(sequence)):
            q_score_nr = random.randrange(41)
            failure_probability = math.pow(10, -q_score_nr / 10)
            p = random.uniform(0, 1)
            if p < failure_probability:
                temp = utils.NUCLEOTIDES.copy()
                temp.remove(sequence[i])
                pert_seq[i] = random.choice(temp)
            
            q_score_ascii = chr(q_score_nr + 33)
            errors += [q_score_ascii] 

        return [pert_seq, errors]