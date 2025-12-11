from .cellularAutomat import *

# třída Game of Life
class GameOfLife(AutomatRule):

    #Počáteční nastavení parametrů a proměnných
    def __init__(self, iNx, iNy, params=None, initState=None):
        super().__init__(iNx, iNy)

        #Definice barev pro výstupní obrázek
        self.colors = {
            'alive':[255,255,0],
            'dead' : [0,0,0]
        }

    #funkce vracející obrázek systému
    def returnBitmap(self,curState):
        bitmap = np.zeros((self.Nx,self.Ny,3))
        for x in range(self.Nx):
            for y in range(self.Ny):
                if(curState[x][y] == 1):
                    bitmap[x][y] = self.colors['alive']
                else:
                    bitmap[x][y] = self.colors['dead']
        return np.clip(bitmap.swapaxes(0, 1), 0, 255).astype(np.uint8)

    #funkce vracející další stav
    def getNewState(self,curState):
        print("game")
        #vytvořím si místo kam uložit nový stav
        newState = np.zeros((self.Nx, self.Ny))
        for x in range(1,self.Nx-1):
            for y in range(1,self.Ny-1):
                #udělám si okénko, které použiji pro zisk nového řešení
                box = curState[x-1:x+2,y-1:y+2]
                #aplikuji pravidlo
                newState[x][y] = self.applyRule(box)
        # vracím nový stav
        return newState, self.returnBitmap(newState)

    #funkce provádějící dané pravidlo algoritmu
    def applyRule(self, box):

        #bod, pro který provádím pravidlo
        me = box[1][1]
        #součtem (sumou) zjistím počet "žijících" sousedů
        num_alive = np.sum(box) - me

        #buňka zemre
        if me == 1 and num_alive < 2 or num_alive > 3:
            return 0
        #buňka zůstane žít nebo se narodi
        elif (me == 1 and 2 <= num_alive <= 3) or (me == 0 and num_alive==3):
            return 1
        #buňka zůstane mrtva
        else:
            return 0