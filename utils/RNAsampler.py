import random
import utils.AminoAcids as acids

FAILURE_PROBABILITY = 0.001
NUCLEOTIDES = ["A", "G", "C", "U"]

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
    for j in range(100000):
        seq = random_sequence()
        pert = perturb_sequence(seq)
        
        for i in range(len(pert[0])):
            total += 1
            if pert[1][i] == 'W':
                total_errors += 1
                if i % 3 == 2:
                    if acids.is_ambig(pert[0][i-2:i+1]):
                        total_repairable += 1
    
    error_perc = (total_errors / total) * 100
    rep_perc = ((total_errors - total_repairable) / total) * 100
    rep_perc2 = (total_repairable / total_errors) * 100
    improv = error_perc - rep_perc
    return (error_perc, rep_perc, rep_perc2, improv)
