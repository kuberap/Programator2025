import numpy as np

# obecná třída buněčný automat
class AutomatRule:
    def __init__(self, iNx, iNy, params=None):
        self.Nx = iNx
        self.Ny = iNy
        self.params = params