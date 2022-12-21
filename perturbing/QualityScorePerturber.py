from perturbing.Perturber import Perturber
import random
from utils import Utils as utils
import math
import copy

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
                expected = random.uniform(math.pow(10, -2.9), 1) # gives a q score < 30 for perturbed ones

            else:
                expected = random.uniform(0, math.pow(10, -2.5)) # gives a q score >= 25 for correct ones
            
            qScoreNr = min(round(-10 * math.log(expected, 10)), 40) # max q score is 40
            qScoreAscii = chr(qScoreNr + 33)
            errors += [qScoreAscii] 

        return [pert_seq, errors]