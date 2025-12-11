import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout, QMainWindow, \
    QGridLayout, QComboBox, QSizePolicy
from canvas import CanvasWidget # moje vlastni trida pro kresleni

class AutomataGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulace celulárního automatu ")
        self.setGeometry(100, 100, 840, 480) # rozmery okna
        self.setup_gui()

    # !!! tady jeste bude zmena ve vstupnim parametru - nekopirujte ten kod do dalsiho
    def setup_gui(self):
        # +--------------------------------------------------------------+
        # |                     Main Window (QMainWindow)                |
        # |                                                              |
        # |  +--------------------------------------------------------+  |
        # |  |                central_widget (QWidget)                |  |
        # |  |                                                        |  |
        # |  |  +--------------------------------------------------+  |  |
        # |  |  |         vertical_layout_main (QVBoxLayout)        |  |  |
        # |  |  |                                                  |  |  |
        # |  |  |  +--------------------------------------------+  |  |  |
        # |  |  |  |    horizontal_layout_central               |  |  |  |
        # |  |  |  |    (hlavní pracovní prostor)               |  |  |  |
        # |  |  |  |                                            |  |  |  |
        # |  |  |  |  +-------------------+   +----------------+ |  |  |  |
        # |  |  |  |  | vertical_layout   |   | vertical_layout| |  |  |  |
        # |  |  |  |  | _left             |   | _right         | |  |  |  |
        # |  |  |  |  | (panel vlevo)     |   | (kreslení)     | |  |  |  |
        # |  |  |  |  |                   |   |                | |  |  |  |
        # |  |  |  |  | +--------------+  |   |     Canvas     | |  |  |  |
        # |  |  |  |  | |left_layout_up|  |   |   / Drawing    | |  |  |  |
        # |  |  |  |  | |(výběr modelu,|  |   |      area      | |  |  |  |
        # |  |  |  |  | | obecné volby)|  |   |                | |  |  |  |
        # |  |  |  |  | +--------------+  |   |                | |  |  |  |
        # |  |  |  |  | +--------------+  |   +----------------+ |  |  |  |
        # |  |  |  |  | |left_layout_   |  |                    |  |  |  |
        # |  |  |  |  | |configs (Grid) |  |                    |  |  |  |
        # |  |  |  |  | | parametry     |  |                    |  |  |  |
        # |  |  |  |  | | modelu        |  |                    |  |  |  |
        # |  |  |  |  | +--------------+  |                    |  |  |  |
        # |  |  |  |  +-------------------+                    |  |  |  |
        # |  |  |  +--------------------------------------------+  |  |  |
        # |  |  |                                                  |  |  |
        # |  |  |  +--------------------------------------------+  |  |  |
        # |  |  |  |    horizontal_layout_bottom                |  |  |  |
        # |  |  |  |    (Start, Stop, Reset, Step…)             |  |  |  |
        # |  |  |  +--------------------------------------------+  |  |  |
        # |  |  +--------------------------------------------------+  |  |
        # |  +--------------------------------------------------------+  |
        # |                                                              |
        # +--------------------------------------------------------------+

        central_widget = QWidget() # sem budu vsechno davat
        #--------------- nastaveni layoutu----------------
        vertical_layout_main = QVBoxLayout(central_widget)
        horizontal_layout_central = QHBoxLayout() # v leve casti konfigurace a vyber modelu, v prave kresleni
        horizontal_layout_bottom = QHBoxLayout() # spodni layout pro tlacitka start, stop atd.
        vertical_layout_left = QVBoxLayout() # leva cast centralniho layoutu - volba modelu, konfigurace modelu
        vertical_layout_right = QVBoxLayout() # komponenta pro kresleni
        left_layout_up = QVBoxLayout() # zde bude vyber modelu a  pripadne dalsi obecne ovladani
        left_layout_configs = QGridLayout() # zde bude ovladani jednotlivych voleb modelu
        # pridani do leveho panelu
        vertical_layout_left.addLayout(left_layout_up)
        vertical_layout_left.addLayout(left_layout_configs)
        # pridani leveho a praveho panelu do centralniho
        horizontal_layout_central.addLayout(vertical_layout_left,1) #20% šířky
        horizontal_layout_central.addLayout(vertical_layout_right,4) #80% šířky
        # pridani centralniho a spodniho panelu do hlavniho layoutu
        vertical_layout_main.addLayout(horizontal_layout_central)
        vertical_layout_main.addLayout(horizontal_layout_bottom)
        central_widget.setLayout(vertical_layout_main)
        self.setCentralWidget(central_widget)

        # ------------------pridani kresliciho platna----------------------
        self.canvas = CanvasWidget()
        vertical_layout_right.addWidget(self.canvas)

        #------------------- pridani vyberu modelu do leveho honiho------------------
        label_model = QLabel("Zvolte model:")
        combo_model = QComboBox()
        # bude v budoucnu upraveno - jen aby tam ted neco bylo
        combo_model.addItems([
            "Zivot",
            "Les",
            "Voda"
        ])
        left_layout_up.addWidget(label_model)
        left_layout_up.addWidget(combo_model)
        #----------------pridani umeleho objektu do konfiguracni casti---------
        left_layout_configs.addWidget(QLabel("TADY BUDE KONFIGURACE"))

        #---------------pridani ovladacich tlacitek do spodni casti---------------
        # udelej tlacitka
        # TODO pridej ovladaci tlacitka start, stop, resume, pause, onestep






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomataGui()
    window.show()
    sys.exit(app.exec())