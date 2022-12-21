from sampling.Sampler import Sampler
import random
from utils import Utils as utils

class AcidSampler(Sampler):

    def random_sequence(self):
        sequence = []
        for i in range(self.sequence_length // 3):
            sequence += list(self.__translate_acid(self.__random_acid()))
        return sequence
    
    def __translate_acid(self, acid):
        for a in utils.AMINO_ACIDS:
            if acid == a['code']:
                return random.choice(a['bases'])

        print("ERROR: Invalid acid.")
        return None
    
    def __random_acid(self):
        probability = random.uniform(0, 0.9982) # Acids probabilities didn't sum to 1
        p_sum = 0
        for acid in utils.AMINO_ACIDS:
            if p_sum >= probability:
                return acid['code']

            p_sum += acid['p']

            if p_sum >= probability:
                return acid['code']

        print("ERROR: No acid chosen.")
        return None     # Not possible