from abc import ABC, abstractmethod

class Perturber(ABC):

    FAILURE_PROBABILITY = 0.01

    def __init__(self, fail_probability):
        self.FAILURE_PROBABILITY = fail_probability

    @abstractmethod
    def perturb_sequence(self):
        pass