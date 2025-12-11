from .cellularAutomat import *


class FluidFlow(AutomatRule):
    #ALGORITMUS:
    # Vezměte hmotnost aktuální buňky a buňky pod ní a spočítejte, kolik vody by měla spodní buňka obsahovat.
    # Pokud má méně, odeberte odpovídající množství z aktuální buňky a přidejte jej do spodní buňky.
    # Zkontrolujte buňku vlevo od této buňky. Pokud obsahuje méně vody, přesuňte do ní tolik vody, aby obě buňky obsahovaly stejné množství.
    # Totéž proveďte pro sousední buňku vpravo.
    # Proveďte totéž jako v kroku 1, ale pro buňku nad aktuální buňkou.


    #Počáteční nastavení hmoty v oblasti podle toho, jestli v buňce je nebo není tekutina
    def massInit(self,initState):
        for x in range(self.Nx):
            for y in range(self.Ny):
                if(initState[x][y] == self.WATER):
                    self.mass[x][y] = self.MaxMass

    #Počáteční nastavení parametrů
    def __init__(self, iNx, iNy, params=None, initState=None):
        super().__init__(iNx, iNy)
        # Cell typy
        self.AIR = 0
        self.WALL = 1
        self.WATER = 2

        self.mass = np.zeros((self.Nx, self.Ny))
        self.newmass = np.zeros((self.Nx, self.Ny))

        # Vlastnosti vody 
        self.MaxMass = params['MaxMass']
        self.MaxCompress = params['MaxCompress']
        #self.MaxCompress = 0.1
        self.MinMass = params['MinMass']

        # Omezaní na proudění
        self.MaxSpeed = params['MaxSpeed']
        #self.MaxSpeed = 10.0
        self.MinFlow = params['MinFlow']
        #self.MinFlow = 0.5


        self.colors = {
            'wall':[239, 247, 5],
            'water' : [0, 0, 255],
            'air' : [0,0,0]
        }


        #massInitialization
        self.massInit(initState)

    #Funkce pro vrácení obrázku s řešením
    def returnBitmap(self, curState):
        bitmap = np.zeros((self.Nx,self.Ny,3))
        for x in range(self.Nx):
            for y in range(self.Ny):
                if(curState[x][y] == self.AIR):
                    bitmap[x][y] = self.colors['air']
                elif(curState[x][y] == self.WATER):
                    bitmap[x][y] = self.colors['water']
                    bitmap[x][y][2] = int(bitmap[x][y][2]*self.mass[x][y])
                else:
                    bitmap[x][y] = self.colors['wall']
        return np.clip(bitmap.swapaxes(0, 1), 0, 255).astype(np.uint8)

    # Funkce určující jak má voda proudit z mezi buňkami co jsou nad sebou
    def get_stable_state_b(self, total_mass):
        if ( total_mass <= 1 ):
            return 1
        elif( total_mass < 2*self.MaxMass + self.MaxCompress ):
            return (self.MaxMass*self.MaxMass + total_mass*self.MaxCompress)/(self.MaxMass + self.MaxCompress)

        else:
            return (total_mass + self.MaxCompress)/2
    
    #Omezení, tj. veličina musí být mezi lo a hi
    def constrain(self, v, lo, hi):
        if v < lo:
            return lo
        if v > hi:
            return hi
        return v

    def getNewState(self,curState):
        return self.applyRule(curState)


    #funkce aplikující dané pravidlo
    def applyRule(self, state):
        print("flow")
        self.newmass = self.mass.copy()
        for x in range(1,self.Nx-1):
            for y in range(1,self.Ny-1):
                #Pokud aktuální buňak je zeď, nedělej nic
                if ( state[x][y] == self.WALL):
                    continue

                #Na začátku nastavíme tok na 0
                Flow = 0
                #Zbylá hmota v buňce je na začátku rovna hmotě v buňce
                remaining_mass = self.mass[x][y]
                if ( remaining_mass <= 0 ):
                    continue
                #Pokud je podemnou zeď, nic podemne neteče, jinak:
                if(state[x][y-1] != self.WALL):
                    Flow = self.get_stable_state_b( remaining_mass + self.mass[x][y-1] ) - self.mass[x][y-1]
                    if ( Flow > self.MinFlow ):
                        Flow *= 0.5
                    #Omezím tok, tak aby nebyl záporný a nepřevýšil maximalní rychlost nebo hmotu, která je teď v buňce
                    Flow = self.constrain(Flow, 0, np.minimum(self.MaxSpeed, remaining_mass))
                    #Od aktuální buňky odečtu to z ní vyteklo
                    self.newmass[x][y] -= Flow
                    #K buňce podemnou přičtu co do ní přiteklo
                    self.newmass[x][y-1] += Flow   
                    #Snížím zbylou hmotu v buňce o to co z ní vyteklo
                    remaining_mass -= Flow


                if ( remaining_mass <= 0 ):
                    continue

                #Tok doleva
                if (state[x-1][y] != self.WALL):
                    #spočtu tok doleva jako rozdíl co mi v buňce zbylo mínus to co je v levo a vydělím 4
                    Flow = (remaining_mass - self.mass[x-1][y])/4
                    if ( Flow > self.MinFlow ):
                        Flow *= 0.5
                    #omezím tok, aby nebyl menší než 0 a vyšší než to co mi zbývá
                    Flow = self.constrain(Flow, 0, remaining_mass)
                    # od sebe odečtu co odteklo
                    self.newmass[x][y] -= Flow
                    # k sousedovi přidám co k němu přiteklo
                    self.newmass[x-1][y] += Flow
                    #upravím co zbývá
                    remaining_mass -= Flow
                
                if ( remaining_mass <= 0 ):
                    continue


                #Tok doprava
                if ( state[x+1][y] != self.WALL ):
                    #spočtu tok doprava jako rozdíl co mi v buňce zbylo mínus to co je v vpravo a vydělím 4
                    Flow = (remaining_mass - self.mass[x+1][y])/4
                    if ( Flow > self.MinFlow ):
                        Flow *= 0.5
                    #omezím tok, aby nebyl menší než 0 a vyšší než to co mi zbývá
                    Flow = self.constrain(Flow, 0, remaining_mass)
                    
                    self.newmass[x][y] -= Flow
                    self.newmass[x+1][y] += Flow
                    remaining_mass -= Flow

                if ( remaining_mass <= 0 ):
                    continue

                #V případě stlačení tekutiny může tekutina proudit i ve vertikálním směru
                if ( state[x][y+1] != self.WALL ):
                    #Určení toku k dosažení rovnováhy
                    Flow = remaining_mass - self.get_stable_state_b( remaining_mass + self.mass[x][y+1] )
                    if ( Flow > self.MinFlow ):
                        Flow *= 0.5
                    #omezení roku
                    Flow = self.constrain( Flow, 0, min(self.MaxSpeed, remaining_mass) )
                    
                    self.newmass[x][y] -= Flow
                    self.newmass[x][y+1] += Flow   
                    remaining_mass -= Flow

        #Novým polem přepíšeme staré
        self.mass = self.newmass.copy()

        #Zjistíme, do kterých buněk přitekla voda a naopak
        for x in range(1,self.Nx-1):
            for y in range(1,self.Ny-1):

                if(state[x][y] == self.WALL):
                     continue
                #Flag/unflag water blocks
                if (self.mass[x][y] > self.MinMass):
                    state[x][y] = self.WATER
                else:
                    state[x][y] = self.AIR

        #Na okraji není žádná hmota, pokud tam něco přiteklo, tak zmizí
        for x in range(0,self.Nx):
            self.mass[x][0] = 0
            self.mass[x][self.Ny-1] = 0
        for y in range(0,self.Ny):
            self.mass[0][y] = 0
            self.mass[self.Nx - 1][y] = 0

        


        return state, self.returnBitmap(state)

