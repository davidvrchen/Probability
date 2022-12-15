from sampling.Sampler import Sampler
import random
import utils

class UniformSampler(Sampler):

    def random_sequence(self):
        sequence = []
        for i in range(self.sequence_length):
            sequence += [self.__random_nucleotide()]
        return sequence

    def __random_nucleotide(self):
        return random.choice(utils.NUCLEOTIDES)