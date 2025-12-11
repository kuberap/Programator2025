from PyQt6.QtCore import QThread, pyqtSignal



class AdapterAutomata(QThread):

    progress_updated = pyqtSignal(int)          # aktuální krok
    state_updated = pyqtSignal(object)         # pole pro vykreslení
    finished = pyqtSignal()                     # simulace dokončena

    def __init__(self, automaton, max_step=5000):
        super().__init__()
        self.automaton = automaton
        self.max_step = max_step
        self.current_step = 0

        self._is_paused = False
        self._is_stopped = False
        self._step_requested = False
    # --------------- ovladaci metody----------------
    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def stop(self):
        self._is_stopped = True
        self.wait() # pockej na ukonceni vlakna - mozny zdroj problemu

    def step(self):
        self._step_requested = True

    def run(self):
        self._is_stopped = False

        self.current_step = 0

        while self.current_step < self.max_step: # delej dokud neni maximalni pocet iteraci
            if self._is_stopped:
                self.finished.emit()
                return

            if self._is_paused and not self._step_requested: # udelej jeden krok, ale vlakno musi byt jiz spustene
                QThread.msleep(50)
                continue

            # provedení kroku automatu
            self.automaton.nextStep()
            self.current_step += 1

            # získání aktuálního stavu (2D numpy array)
            state = self.automaton.getCurrentState()


            # emit signálů do GUI
            self.state_updated.emit(state)
            self.progress_updated.emit(self.current_step)

            # reset po flagu pro one step jednom kroku
            self._step_requested = False

            QThread.msleep(500) # počkej - toto je možné dát jako volba parametru s GUI, podobně jako max počet iterací

        self.finished.emit()