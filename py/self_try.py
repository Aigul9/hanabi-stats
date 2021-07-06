class H:
    def __init__(self, s):
        self.stats = s

    def clear_2p(self):
        self.stats = [row for row in self.stats if int(row['options']['numPlayers']) != 2]
        return self

    def clear_speedruns(self):
        self.stats = [row for row in self.stats if not row['options']['speedrun']]
        return self
