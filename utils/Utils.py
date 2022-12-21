AMINO_ACIDS = [
    {'code': "A", 'bases': ["GCA","GCT","GCC","GCG"], 'p': 0.0777},
    {'code': "C", 'bases': ["TGT", "TGC"], 'p': 0.0157},
    {'code': "D", 'bases': ["GAT", "GAC"], 'p': 0.053},
    {'code': "E", 'bases': ["GAA", "GAG"], 'p': 0.0656},
    {'code': "F", 'bases': ["TTA","TTT","TTG","TTC"], 'p': 0.0405},
    {'code': "G", 'bases': ["GGT","GGA","GGG","GGC"], 'p': 0.0691},
    {'code': "H", 'bases': ["CAT", "CAC"], 'p': 0.0227},
    {'code': "I", 'bases': ["ATT", "ATC", "ATA"], 'p': 0.0591},
    {'code': "K", 'bases': ["AAA", "AAG"], 'p': 0.0595},
    {'code': "L", 'bases': ["CTA","CTT","CTG","CTC"], 'p': 0.096},
    {'code': "M", 'bases': ["ATG"], 'p': 0.0238},
    {'code': "N", 'bases': ["AAT", "AAC"], 'p': 0.0427},
    {'code': "P", 'bases': ["CCA","CCT","CCC","CCG"], 'p': 0.0469},
    {'code': "Q", 'bases': ["CAA", "CAG"], 'p': 0.0393},
    {'code': "R", 'bases': ["CGG","CGC","CGT","CGA", "AGA", "AGG"], 'p': 0.0526},
    {'code': "S", 'bases': ["TCG","TCC","TCA","TCT", "AGT", "AGC"], 'p': 0.0694},
    {'code': "T", 'bases': ["ACA","ACT","ACG","ACC"], 'p': 0.055},
    {'code': "V", 'bases': ["GTA","GTT","GTG","GTC"], 'p': 0.0667},
    {'code': "W", 'bases': ["TGG"], 'p': 0.0118},
    {'code': "Y", 'bases': ["TAT", "TAC"], 'p': 0.0311},
]

NUCLEOTIDES = ["A", "G", "C", "T"]

# Gets the acid from the bases
def get_acid(base):
    for acid in AMINO_ACIDS:
        for code in acid['bases']:
            if base == code:
                return acid['code']
            if code[2] == 'X':
                if base[0:2] == code[0:2]:
                    return acid['code']
    return None

# Returns whether the last base of an acid can be any value
def is_ambig(base):
    base = list(base)
    base1, base2, base3, base4 = base.copy(), base.copy(), base.copy(), base.copy()
    base1[2] = 'A'
    base2[2] = 'T'
    base3[2] = 'G'
    base4[2] = 'C'
    base1 = ''.join(base1)
    base2 = ''.join(base2)
    base3 = ''.join(base3)
    base4 = ''.join(base4)
    for acid in AMINO_ACIDS:
        if (base1 in acid['bases']) and (base2 in acid['bases']) and (base3 in acid['bases']) and (base4 in acid['bases']):
            return True
    return False

# Gets the probability of occuring for any acid
def get_probability(base):
    if len(base) > 1:
        base = get_acid(base)
    
    for acid in AMINO_ACIDS:
        if base == acid['code']:
            return acid['p']
    
    return None