from PyQt6.QtGui import QPainter, QPalette, QColor
from PyQt6.QtWidgets import QWidget



class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buffer = None     # obrázek pro vykreslení
        self.setMinimumSize(400, 400)
        self.setAutoFillBackground(True)

        # nastavení tmavého pozadí
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(80, 10, 10))
        self.setPalette(palette)

    def set_buffer(self, image):
        """Sem ti bude vizualizátor dávat QImage/QPixmap"""
        self.buffer = image
        self.update()  # překreslit

    def paintEvent(self, event):
        # metoda je volana pri zneplatneni okna/update/min/max/zmena velikosti - kresli obsah bufferu
        painter = QPainter(self)
        # sem je mozne implementovat ruzne serepeticky
        if self.buffer:
            if self.buffer:
                painter.drawImage(self.rect(), self.buffer)

    # dodelam nekdy v budoucnu
    def wheelEvent(self, event):
        # zoom in/out
        print("wheel TODO")
        pass