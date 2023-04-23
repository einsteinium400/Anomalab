import math

class Calc:
    def __init__(self):
        self.sum = 0
        self.n = 0
        self.var = 0
        self.avg = 0
        self.min = 0
        self.max = 0
    
    def __str__(self):
        return f'sum is: {self.sum} squaresum: {self.squareSum} number: {self.n}'

    def add(self, value):
        if (self.n == 0):
            self.max = value
            self.min = value
        else:
            if (value > self.max):
                self.max = value
            if (value < self.min):
                self.min = value
        
        self.n = self.n + 1
        self.var =(self.n-1/self.n)*(self.var+((self.avg-value)**2)/(self.nroot))
        self.sum = self.sum + value
        self.avg = self.sum / self.n
    
    def clean(self):
        self.sum = 0
        self.n = 0
        self.var = 0
        self.avg = 0
        self.min = 0
        self.max = 0
    
    def getStdDev(self):
        return math.sqrt(self.var)
    
    def getRange(self):
        return self.max - self.min