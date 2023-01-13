from perturbing.Perturber import Perturber
import random
from utils import Utils as utils
import copy

# Perturbs a sequence with a predefined error rate an assigns 'W' or 'R' to indicate whether it is perturbed or not.
class BinaryPerturber(Perturber):

    def __init__(self, fail_probability):
        super().__init__(fail_probability)

    def perturb_sequence(self, sequence):
        errors = []
        pert_seq = copy.deepcopy(sequence)
        for i in range(len(sequence)):
            p = random.uniform(0,1)
            if p < self.FAILURE_PROBABILITY:
                temp = utils.NUCLEOTIDES.copy()
                temp.remove(sequence[i])
                pert_seq[i] = random.choice(temp)
                errors += ['W']
            else:
                errors += ['R']

        return [pert_seq, errors]