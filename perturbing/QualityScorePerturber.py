from perturbing.Perturber import Perturber
import random
from utils import Utils as utils
import math

class QualityScorePerturber(Perturber):

    def perturb_sequence(self, sequence):
        errors = []
        for i in range(len(sequence)):
            p = random.uniform(0,1)
            if p < self.FAILURE_PROBABILITY:
                temp = utils.NUCLEOTIDES.copy()
                temp.remove(sequence[i])
                sequence[i] = random.choice(temp)
                expected = random.uniform(math.pow(10, -2.9), 1) # gives a q score < 30 for perturbed ones

            else:
                expected = random.uniform(0, math.pow(10, -2.5)) # gives a q score >= 25 for correct ones
            
            qScoreNr = round(-10 * math.log(expected, 10)) + 33
            qScore = chr(qScoreNr)
            errors += [qScore] 

        return [sequence, errors]