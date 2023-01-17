from abc import ABC, abstractmethod

class Sampler(ABC):

    sequence_length = 300

    def __init__(self):
        super().__init__()

    @abstractmethod
    def random_sequence(self):
        pass