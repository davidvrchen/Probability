from abc import ABC, abstractmethod

class Perturber(ABC):

    FAILURE_PROBABILITY = 0.01

    @abstractmethod
    def perturb_sequence(self):
        pass