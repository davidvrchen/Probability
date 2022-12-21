from enum import Enum
from analyzing.FirstAnalyzer import FirstAnalyzer
from analyzing.SecondAnalyzer import SecondAnalyzer

class AnalyzerType(Enum):
    FIRST_ANALYSE = 0
    SECOND_ANALYSE = 1

def create_analyzer(type):
    if type == AnalyzerType.FIRST_ANALYSE:
        return FirstAnalyzer()
    elif type == AnalyzerType.SECOND_ANALYSE:
        return SecondAnalyzer()