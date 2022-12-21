from abc import ABC, abstractmethod
import sampling.SamplerStrategy as sample
import perturbing.PerturberStrategy as perturb

class Analyzer(ABC):

    FAILURE_PROBABILITY = 0.01

    def __init__(self, sampler_strategy, perturber_strategy, sample_size):
        self.SAMPLE_SIZE = sample_size
        self.sampler = sample.create_sampler(sampler_strategy)
        self.perturber = perturb.create_perturber(perturber_strategy)

    @abstractmethod
    def analyze(self):
        pass

    @abstractmethod
    def print_analyze(self):
        pass