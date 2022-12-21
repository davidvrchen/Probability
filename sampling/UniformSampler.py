from sampling.Sampler import Sampler
import random
from utils import Utils as utils

class UniformSampler(Sampler):

    def __init__(self):
        super().__init__()

    def random_sequence(self):
        sequence = []
        for i in range(self.sequence_length):
            sequence += [self.__random_nucleotide()]
        return sequence

    def __random_nucleotide(self):
        return random.choice(utils.NUCLEOTIDES)