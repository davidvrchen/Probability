from abc import ABC, abstractmethod
import sampling.SamplerStrategy as sample
import perturbing.PerturberStrategy as perturb

class Analyzer(ABC):

    FAILURE_PROBABILITY = 0.01
    SAMPLE_SIZE = 10000

    def __init__(self, sampler_strategy, perturber_strategy):
        self.sampler = sample.create_sampler(sampler_strategy)
        self.perturber = perturb.create_perturber(perturber_strategy)

    @abstractmethod
    def analyze(self):
        pass