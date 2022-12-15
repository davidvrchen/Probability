# import random
# import utils.AminoAcids as acids
# import math

# FAILURE_PROBABILITY = 0.001

# def perturb_sequence(sequence):
#     errors = []
#     for i in range(len(sequence)):
#         p = random.uniform(0,1)
#         if p < FAILURE_PROBABILITY:
#             temp = NUCLEOTIDES.copy()
#             temp.remove(sequence[i])
#             sequence[i] = random.choice(temp)
#             errors += ['W']
#         else:
#             errors += ['R']

#     return [sequence, errors]

# def perturb_sequence2(sequence):
#     errors = []
#     for i in range(len(sequence)):
#         p = random.uniform(0,1)
#         if p < FAILURE_PROBABILITY:
#             temp = NUCLEOTIDES.copy()
#             temp.remove(sequence[i])
#             sequence[i] = random.choice(temp)
#             expected = random.uniform(math.pow(10, -2.9), 1) # gives a q score < 30 for perturbed ones

#         else:
#             expected = random.uniform(0, math.pow(10, -2.5)) # gives a q score >= 25 for correct ones
        
#         qScoreNr = round(-10 * math.log(expected, 10)) + 33
#         qScore = chr(qScoreNr)
#         errors += [qScore] 

#     return [sequence, errors]

# def analyze_failure():

#     total = 0
#     total_errors = 0
#     total_repairable = 0
#     for j in range(100000):
#         seq = random_sequence()
#         pert = perturb_sequence(seq)
        
#         for i in range(len(pert[0])):
#             total += 1
#             if pert[1][i] == 'W':
#                 total_errors += 1
#                 if i % 3 == 2:
#                     if acids.is_ambig(pert[0][i-2:i+1]):
#                         total_repairable += 1
    
#     error_perc = (total_errors / total) * 100
#     rep_perc = ((total_errors - total_repairable) / total) * 100
#     rep_perc2 = (total_repairable / total_errors) * 100
#     improv = error_perc - rep_perc
#     return (error_perc, rep_perc, rep_perc2, improv)

# def more_certain_than(qScore, checkValue):
#     return ord(qScore) > checkValue # if more certain than this we will assume it is correct

# def analyze_failure2():

#     total = 0
#     total_errors = 0
#     total_repairable = 0
#     uncertain_unchanged = 0
#     uncertain_changed = 0
#     correct_uncertainties = 0
#     guessed_uncertainties = 0
#     unfixed_errors = 0

#     for j in range(100000):
#         seq = random_sequence()
#         pert = perturb_sequence2(seq)
#         attempted_fix = [i for i in pert[1]]
#         for i in range(len(pert[0])):
#             total += 1
#             if ord(pert[1][i]) < 63: # if the qScoreNr was lower than 30, so there was an error (defined in code)
#                 total_errors += 1
#                 if i % 3 == 2:
#                     if acids.is_ambig(pert[0][i-2:i+1]):
#                         total_repairable += 1
#                     elif (ord(pert[1][i]) >  58): # qScore > 25 might be correct
#                         uncertain_unchanged += 1 
#                         if (attempted_fix[i] == seq[i]):
#                             correct_uncertainties += 1
#                         else: 
#                             unfixed_errors += 1
#                     else:
#                         temp = NUCLEOTIDES.copy()
#                         temp.remove(pert[0][i])
#                         attempted_fix[i] = random.choice(temp)
#                         uncertain_changed += 1
#                         if (attempted_fix[i] == seq[i]):
#                             guessed_uncertainties += 1
#                         else: 
#                             unfixed_errors += 1


#     error_perc = (total_errors / total) * 100
#     rep_perc = ((total_errors - total_repairable) / total) * 100
#     rep_perc2 = (total_repairable / total_errors) * 100
#     improv = error_perc - rep_perc
#     corrected_perc = ((total_errors - total_repairable - correct_uncertainties)/total_errors) * 100
#     unfixed_uncertainties = ((uncertain_unchanged + uncertain_changed - unfixed_errors) / (uncertain_unchanged + uncertain_changed)) * 100
#     # percentage of correct readings with 25 <= qScore < 30
#     high_qScore_correct_perc = ((uncertain_unchanged - correct_uncertainties) / uncertain_unchanged) * 100 
#     # percentage of readings that were correctly fixed by guessing 
#     # probably not interesting now as it should be 1/3 but interesting for more involved models
#     correct_guess_perc = ((uncertain_changed - (uncertain_changed - guessed_uncertainties)) / uncertain_changed) * 100 

#     return (error_perc, rep_perc, rep_perc2, improv, corrected_perc, unfixed_uncertainties, high_qScore_correct_perc, correct_guess_perc)