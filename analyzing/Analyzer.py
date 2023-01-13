from abc import ABC, abstractmethod
import sampling.SamplerStrategy as sample
import perturbing.PerturberStrategy as perturb

class Analyzer(ABC):

    FAILURE_PROBABILITY = 0.01
    ERROR_GOAL = 0.01

    def __init__(self, sampler_strategy, perturber_strategy, sample_size, fail_probability):
        self.SAMPLE_SIZE = sample_size
        self.FAILURE_PROBABILITY = fail_probability
        self.sampler = sample.create_sampler(sampler_strategy)
        self.perturber = perturb.create_perturber(perturber_strategy, fail_probability)
        

    @abstractmethod
    def analyze(self):
        pass

    @abstractmethod
    def print_analyze(self):
        pass