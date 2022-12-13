import random
import utils.AminoAcids as acids

FAILURE_PROBABILITY = 0.001
NUCLEOTIDES = ["A", "G", "C", "U"]

AMINO_ACIDS = []

def random_nucleotide():
    return random.choice(NUCLEOTIDES)

def random_sequence():
    sequence = []
    for i in range(252):
        sequence += [random_nucleotide()]
    return sequence

def perturb_sequence(sequence):
    errors = []
    for i in range(len(sequence)):
        p = random.uniform(0,1)
        if p < FAILURE_PROBABILITY:
            temp = NUCLEOTIDES.copy()
            temp.remove(sequence[i])
            sequence[i] = random.choice(temp)
            errors += ['W']
        else:
            errors += ['R']

    return [sequence, errors]

def analyze_failure():

    total = 0
    total_errors = 0
    total_repairable = 0
    for j in range(10000):
        seq = random_sequence()
        pert = perturb_sequence(seq)
        
        for i in range(len(pert[0])):
            total += 1
            if pert[1][i] == 'W':
                total_errors += 1
                if i % 3 == 2:
                    if acids.is_ambig(pert[0][i-2:i+1]):
                        total_repairable += 1
    
    print(total_repairable)
    return (total_errors / total, (total_errors - total_repairable) / total)
