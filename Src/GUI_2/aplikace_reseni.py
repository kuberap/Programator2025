import sys
from pathlib import Path

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout, QMainWindow, \
    QGridLayout, QComboBox, QSizePolicy, QLineEdit
from canvas import CanvasWidget # moje vlastni trida pro kresleni

import yaml

class AutomataGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_file_path = Path("../../Config/registry.yaml") # kdyz to bude spatne, tak to spadne - prostor pro zlepšení
        self.setWindowTitle("Simulace celulárního automatu ")
        self.setGeometry(100, 100, 840, 480) # rozmery okna
        # ---- NOTE přidáno načtení registru modelů
        try:
            with open(self.config_file_path, "r") as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"YAML config file {self.config_file_path}\n error in : {e}")

        # tisk nacteneho konfigu
        print(self.config)
        self.left_layout_config_widgets = {} # zde jsou uloženy všechny konfigurační edity
        self.setup_gui()


    def setup_gui(self):
        central_widget = QWidget() # sem budu vsechno davat
        #--------------- nastaveni layoutu----------------
        vertical_layout_main = QVBoxLayout(central_widget)
        horizontal_layout_central = QHBoxLayout() # v leve casti konfigurace a vyber modelu, v prave kresleni
        horizontal_layout_bottom = QHBoxLayout() # spodni layout pro tlacitka start, stop atd.
        vertical_layout_left = QVBoxLayout() # leva cast centralniho layoutu - volba modelu, konfigurace modelu
        vertical_layout_right = QVBoxLayout() # komponenta pro kresleni
        left_layout_up = QVBoxLayout() # zde bude vyber modelu a  pripadne dalsi obecne ovladani
        self.left_layout_configs = QGridLayout() # zde bude ovladani jednotlivych voleb modelu - dopsano self
        # pridani do leveho panelu
        vertical_layout_left.addLayout(left_layout_up, stretch=1)
        vertical_layout_left.addLayout(self.left_layout_configs, stretch=8)
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
        self.combo_model = QComboBox()
        # upraveno na pridani modelu z registru - vytvořen seznam s modely
        self.combo_model.addItems(list(self.config.keys()))

        left_layout_up.addWidget(label_model)
        left_layout_up.addWidget(self.combo_model)
        #----------------pridani umeleho objektu do konfiguracni casti---------
        self.left_layout_configs.addWidget(QLabel(""))
        # TODO - přidejte přidání konfigurace modelu = upravte metodu model_changed()
        self.model_changed(self.combo_model.currentText())


        #---------------pridani ovladacich tlacitek do spodni casti---------------
        # udelej tlacitka
        self.start_button = QPushButton("Start")
        self.one_step_button = QPushButton("|>")
        self.pause_button = QPushButton("Pause")
        self.resume_button = QPushButton("Resume")
        self.stop_button = QPushButton("Stop")

        # nastav styl - nepovinné
        self.start_button.setStyleSheet("background-color: green; color: white; font-weight: bold; font-size: 14px;")
        self.one_step_button.setStyleSheet("background-color: blue; color: white; font-weight: bold; font-size: 14px;")
        self.pause_button.setStyleSheet("background-color: orange; color: white; font-weight: bold; font-size: 14px;")
        self.resume_button.setStyleSheet("background-color: purple; color: white; font-weight: bold; font-size: 14px;")
        self.stop_button.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 14px;")

        # nastav chovani pri zvetsovani - nepovinne
        for btn in [self.start_button, self.one_step_button, self.pause_button, self.resume_button, self.stop_button]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumHeight(30)  # volitelně pevná výška

        # pridej tlacitka do spodniho layoutu
        horizontal_layout_bottom.addWidget(self.start_button)
        horizontal_layout_bottom.addWidget(self.one_step_button)
        horizontal_layout_bottom.addWidget(self.pause_button)
        horizontal_layout_bottom.addWidget(self.resume_button)
        horizontal_layout_bottom.addWidget(self.stop_button)
        horizontal_layout_bottom.setSpacing(10)  # mezery mezi tlačítky

        # ---------------------registrace událostí na komponenty---------------------
        # tato metoda se vola pri zmene hodnoty comboboxu
        self.combo_model.currentTextChanged.connect(self.model_changed) # pozoro nepiste self.model_changed() - volani metody


    def model_changed(self, key):
        """metoda kontroluje udalost vyber modelu z komboboxu"""
        # odstran stare komponenenty z gui a smaz je
        self.left_layout_config_widgets.clear() # smaž registrované widgety
        while self.left_layout_configs.count()>1:
            item = self.left_layout_configs.takeAt(1)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # ------------------- RESENI-----------------------------
        row = 1 # pozice jedna
        # pridani kombo visualisatoru
        self.combo_visualisator = QComboBox()
        self.combo_visualisator.addItems(list(self.config[key]["visualizers"].keys()))
        self.left_layout_configs.addWidget(self.combo_visualisator,row,0, 1,2)
        row += 1
        for k,v in self.config[key]["params"].items():
            label = QLabel(str(k))
            edit = QLineEdit()
            value = float(v)
            edit.setValidator(QDoubleValidator(value/1000, 1000*value,6, self))
            edit.setText(str(value))
            self.left_layout_config_widgets[k]=edit # nutno si uložit referenci
            self.left_layout_configs.addWidget(label, row, 0)
            self.left_layout_configs.addWidget(edit, row, 1)
            row += 1

        #--------------------------------------------------------
        # test, ze jsem schopen nacitat hodnoty - pak z toho nekdy udelame metodu
        for k,w in self.left_layout_config_widgets.items():
            print(f"{k}: {w.text()}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomataGui()
    window.show()
    sys.exit(app.exec())