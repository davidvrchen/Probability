AMINO_ACIDS = [
    {'code': "A", 'bases': ["GCX"], 'p': 0.0777},
    {'code': "C", 'bases': ["TGT", "TGC"], 'p': 0.0157},
    {'code': "D", 'bases': ["GAT", "GAC"], 'p': 0.053},
    {'code': "E", 'bases': ["GAA", "GAG"], 'p': 0.0656},
    {'code': "F", 'bases': ["TTX"], 'p': 0.0405},
    {'code': "G", 'bases': ["GGX"], 'p': 0.0691},
    {'code': "H", 'bases': ["CAT", "CAC"], 'p': 0.0227},
    {'code': "I", 'bases': ["ATT", "ATC", "ATA"], 'p': 0.0591},
    {'code': "K", 'bases': ["AAA", "AAG"], 'p': 0.0595},
    {'code': "L", 'bases': ["CTX"], 'p': 0.096},
    {'code': "M", 'bases': ["ATG"], 'p': 0.0238},
    {'code': "N", 'bases': ["AAT", "AAC"], 'p': 0.0427},
    {'code': "P", 'bases': ["CCX"], 'p': 0.0469},
    {'code': "Q", 'bases': ["CAA", "CAG"], 'p': 0.0393},
    {'code': "R", 'bases': ["CGX", "AGA", "AGG"], 'p': 0.0526},
    {'code': "S", 'bases': ["TCX", "AGT", "AGC"], 'p': 0.0694},
    {'code': "T", 'bases': ["ACX"], 'p': 0.055},
    {'code': "V", 'bases': ["GTX"], 'p': 0.0667},
    {'code': "W", 'bases': ["TGG"], 'p': 0.0118},
    {'code': "Y", 'bases': ["TAT", "TAC"], 'p': 0.0311},
]

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
    for acid in AMINO_ACIDS:
        for code in acid['bases']:
            if code[2] == 'X':
                if base[0] == code[0] and base[1] == code[1]:
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