from perturbing.Perturber import Perturber
import random
from utils import Utils as utils

class BinaryPerturber(Perturber):

    def perturb_sequence(self, sequence):
        errors = []
        for i in range(len(sequence)):
            p = random.uniform(0,1)
            if p < self.FAILURE_PROBABILITY:
                temp = utils.NUCLEOTIDES.copy()
                temp.remove(sequence[i])
                sequence[i] = random.choice(temp)
                errors += ['W']
            else:
                errors += ['R']

        return [sequence, errors]