import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

from .gameOfLife import *
from .forestFire import *
from .fluidFlow import *

from .forestFireAdvanced import *



class automat:

    def __init__(self, iName, irule = GameOfLife, params=None):
        self.state = self.load(iName) #přečti počáteční stav
        self.Nx = self.state.shape[0] #nastav rozměr v x-ovém směru
        self.Ny = self.state.shape[1] #nastav rozměr v y-ovém směru
        self.rule = irule(self.Nx, self.Ny, params, self.state) #nastav pravidlo pro danou úlohu
        self.bitmap = np.zeros((self.Nx, self.Ny, 3)) #vytvoř základní obrázek řešení
        print('Načten počáteční stav s rozměry ', self.state.shape)


    #načti csv soubor s počátečním stavem
    def load(self, iname):
        df = pd.read_csv(iname, header=None)
        return df.to_numpy().T

    # proveď další krok 
    def nextStep(self):
        print("Automaton next state")
        self.state, self.bitmap = self.rule.getNewState(self.state)

    #vrať aktuální stav 
    def getCurrentState(self):
        return self.state

    #vrať obrázek aktuálního stavu
    def getCurrentBitmap(self):
        return self.bitmap

    #nech systém vyvíjet a kresli
    def iterateAndPlot(self):
        fig, ax = plt.subplots()
        #smyčka udávající, že systém poběží daný počet iterací
        for it in range(5000):
            ax.clear()  
            #nakresli obrázek s řešením
            plt.imshow(self.bitmap, origin='lower')
            plt.draw()
            plt.pause(0.001)
            print(it)
            self.nextStep()


if __name__ == '__main__':
    aut = automat('../../Csv/initGame.csv', irule=GameOfLife)

    # aut = automat('../../Csv/forestFire.csv', irule=ForestFire2, params={'f':0.00002, 'p':0.002})
    aut = automat('../../Csv/initFluid.csv', irule=FluidFlow, params={'MaxMass':1.0, 'MaxCompress': 0.02, 'MinMass':0.0001,
    'MaxSpeed':1.0, 'MinFlow':0.01})
    aut.iterateAndPlot()
