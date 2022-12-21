from abc import ABC, abstractmethod

class Sampler(ABC):

    sequence_length = 252

    def __init__(self):
        super().__init__()

    @abstractmethod
    def random_sequence(self):
        pass