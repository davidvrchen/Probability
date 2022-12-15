from analyzing.Analyzer import Analyzer
import utils

class FirstAnalyzer(Analyzer):
    
    def __init__(self, sampler_strategy, perturber_strategy):
        super().__init__(sampler_strategy, perturber_strategy)

    def analyze(self):
        total = 0
        total_errors = 0
        total_repairable = 0
        for j in range(self.SAMPLE_SIZE):
            self.analyze_failure()

        error_perc = (total_errors / total) * 100
        rep_perc = ((total_errors - total_repairable) / total) * 100
        rep_perc2 = (total_repairable / total_errors) * 100
        improv = error_perc - rep_perc
        return (error_perc, rep_perc, rep_perc2, improv)

    def analyze_failure(self):
        seq = self.sampler.random_sequence()
        pert = self.perturber.perturb_sequence(seq)
        
        for i in range(len(pert[0])):
            total += 1
            if pert[1][i] == 'W':
                total_errors += 1
                if i % 3 == 2:
                    if utils.acids.is_ambig(pert[0][i-2:i+1]):
                        total_repairable += 1
        