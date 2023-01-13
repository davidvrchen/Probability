from enum import Enum
from perturbing.BinaryPerturber import BinaryPerturber
from perturbing.QualityScorePerturber import QualityScorePerturber
from perturbing.SecondQualityScorePerturber import SecondQualityScorePerturber

class PerturberType(Enum):
    BINARY_PERTURBING = 0
    QUALITY_SCORE_PERTURBING = 1
    DISTRIBUTED_QUALITY_SCORE = 2

def create_perturber(type, fail_probability):
    if type == PerturberType.BINARY_PERTURBING:
        return BinaryPerturber(fail_probability)
    elif type == PerturberType.QUALITY_SCORE_PERTURBING:
        return QualityScorePerturber(fail_probability)
    elif type == PerturberType.DISTRIBUTED_QUALITY_SCORE:
        return SecondQualityScorePerturber(fail_probability)
