from .cellularAutomat import *
import random

class ForestFire2(AutomatRule):

    def __init__(self, iNx, iNy, params, initState=None):
        super().__init__(iNx, iNy, params)
        self.f = 0.00002 # pravděpodobnost, že blesk zasáhne strom
        self.p = 0.002;  # pravděpodobnost, že vyroste strom

        #buňky nabívají různých hodnot podle svých stavů
        self.nicID = 0  #nic tam nehoří ani neroste
        self.stromID = 1 #strom
        self.pozarID = 2 #požár

        self.treeAge = np.zeros((self.Nx, self.Ny))
        self.fireLevels = 10
        self.growLevels = 20

        self.colors = {
            'tree':[0,255,0],
            'newTree' : [155, 237, 140],
            'newfire' : [239, 247, 5],
            'oldfire' : [138, 83, 36],
            'empty' : [0,0,0]
        }

    def treeLevel(self, age):
        if age < self.growLevels:
            return age
        else:
            return self.growLevels

    #vrať obrázek s řešením (aktuálním stavem)
    def returnBitmap(self,curState):
        bitmap = np.zeros((self.Nx,self.Ny,3))
        for x in range(self.Nx):
            for y in range(self.Ny):
                if(curState[x][y] == self.stromID):
                    if self.treeAge[x][y] < self.growLevels:
                        bitmap[x][y] = self.colors['newTree']
                    else:
                        bitmap[x][y] = self.colors['tree']
                elif(curState[x][y] == self.pozarID):
                    if self.treeAge[x][y] > -self.fireLevels:
                        bitmap[x][y] = self.colors['oldfire']
                    else:
                        bitmap[x][y] = self.colors['newfire']
                else:
                    bitmap[x][y] = self.colors['empty']
        return np.clip(bitmap.swapaxes(0, 1), 0, 255).astype(np.uint8)

    #vypočti nový stav
    def getNewState(self,curState):
        #vytvořím si místo kam nový stav uložit
        newState = np.zeros((self.Nx, self.Ny))
        for x in range(1,self.Nx-1):
            for y in range(1,self.Ny-1):
                #vytvořím okénko, které použijeme pro výpočet nového stavu
                box = curState[x-1:x+2,y-1:y+2]
                #vypočteme nový stav
                currAge = self.treeAge[x][y]
                newState[x][y], self.treeAge[x][y] = self.applyRule(box, currAge)
        return newState, self.returnBitmap(newState)

    #funkce říkající, zda daná buňka (strom) hoří
    def hori(self, cell):
        #aplikace if podmínky
        if cell == self.pozarID:
            return True
        else:
            return False

    #funkce aplikující dané pravidlo
    def applyRule(self, box, currAge):
        #aktuální bod (buňka), kde pravidlo aplikuji
        me = box[1,1]
        #do burningNeighbour uložím Pravda(True) nebo Nepravda(False) pokud hoří aspoň jeden soused
        burningNeighbour = False
        for x in range(len(box)):
            for y in range(len(box[0])):
                if x != 1 and y!= 1:
                    if self.hori(box[x,y]):
                        burningNeighbour = True

        if me == self.stromID:
            #chytne od souseda
            if burningNeighbour:
                return self.pozarID, -self.fireLevels
            #zapálí blesk
            else:
                prop = random.random()*currAge/self.growLevels
                if(prop <=  self.params['f']):
                    return self.pozarID, -self.fireLevels
                else:
                    return self.stromID, self.treeLevel(currAge)
        elif me == self.pozarID:
            currAge = currAge + 1
            if(currAge < 0):
                return self.pozarID, currAge
            else:
                return self.nicID, currAge
        else:
            #vyroste strom
            prop = random.random()
            if (prop <= self.params['p']):
                return self.stromID, 1
            else:
                return self.nicID, 0
