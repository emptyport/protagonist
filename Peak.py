class Peak():

    def __init__(self, mz, intensity, hasCounterpart, rank):
        self.mz = mz
        self.intensity = intensity
        self.hasCounterpart = hasCounterpart
        self.rank = rank

    def __repr__(self):
        return str(self.mz) + '\t' + str(self.intensity) + '\t' + str(self.hasCounterpart) + '\t' + str(self.rank)
