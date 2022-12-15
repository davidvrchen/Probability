from abc import ABC, abstractmethod

class Sampler(ABC):

    sequence_length = 252

    @abstractmethod
    def random_sequence(self):
        pass