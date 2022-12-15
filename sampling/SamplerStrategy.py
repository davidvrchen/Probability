from enum import Enum
from sampling.UniformSampler import UniformSampler
from sampling.AcidSampler import AcidSampler

class SamplerType(Enum):
    UNIFORM_SAMPLING = 0
    ACID_SAMPLING = 1

def create_sampler(type):
    if type == SamplerType.UNIFORM_SAMPLING:
        return UniformSampler()
    elif type == SamplerType.ACID_SAMPLING:
        return AcidSampler()