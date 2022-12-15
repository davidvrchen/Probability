from enum import Enum
from perturbing.BinaryPerturber import BinaryPerturber
from perturbing.QualityScorePerturber import QualityScorePerturber

class PerturberType(Enum):
    BINARY_PERTURBING = 0
    QUALITY_SCORE_PERTURBING = 1

def create_perturber(type):
    if type == PerturberType.BINARY_PERTURBING:
        return BinaryPerturber()
    elif type == PerturberType.QUALITY_SCORE_PERTURBING:
        return QualityScorePerturber()