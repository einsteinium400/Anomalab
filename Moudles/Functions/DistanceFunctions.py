class mixed_distance():

    def __init__(self, u, v, type_values):
        self.distance = 0
        self.u=u
        self.v=v
        self.type_values=type_values

    def calc(self):
        self.distance = 0
        for i in range(len(self.u)):
            # if type is categorical
            if self.type_values[i]:
                if self.v[i] != self.u[i]:
                    self.distance += 1
            # if type is numeric
            else:
                self.distance += abs(self.u[i] - self.v[i])

        return self.distance



