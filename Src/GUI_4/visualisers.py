import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QColor, QPainter
import matplotlib.pyplot as plt

from matplotlib import cm

from PyQt6.QtGui import QImage
import numpy as np

class BitmapVisualizer:
    """
    vizualisator s peti stavy
    """

    def __init__(self, max_state=4):
        self.max_state = max_state
        # definujeme vlastní kontrastní barvy pro stavy 0..4
        # např. černá, červená, zelená, modrá, žlutá
        self.palette = np.array([
            [0, 0, 0],       # stav 0 - černá
            [255, 0, 0],     # stav 1 - červená
            [0, 255, 0],     # stav 2 - zelená
            [0, 0, 255],     # stav 3 - modrá
            [255, 255, 0],   # stav 4 - žlutá
        ], dtype=np.uint8)

    def visualize(self, state_array: np.ndarray) -> QImage:
        """
        state_array: 2D numpy array s celými stavy 0..max_state
        vrací QImage pro vykreslení
        """
        h, w = state_array.shape
        img = np.zeros((h, w, 3), dtype=np.uint8)

        print(f"min state: {np.min(state_array)} max state: {np.max(state_array)}")
        # omezíme stavy do 0..max_state a převedeme na integer
        clipped = np.clip(state_array, 0, self.max_state).astype(int)

        # přiřadíme barvy podle stavu
        img[:, :, 0] = self.palette[clipped, 0]  # R
        img[:, :, 1] = self.palette[clipped, 1]  # G
        img[:, :, 2] = self.palette[clipped, 2]  # B

        # převedeme na QImage
        qimg = QImage(img.data, w, h, 3 * w, QImage.Format.Format_RGB888)
        return qimg


class GameOfLifeVisualizer:
    """
    Jednoduchý vizualizátor Game of Life:
    černé buňky (živé) na bílém pozadí.
    """

    def __init__(self):
        pass  # žádné parametry potřeba

    def visualize(self, state_array: np.ndarray) -> QImage:
        """
        state_array: 2D numpy array s hodnotami 0 (mrtvá) / 1 (živá)
        vrací QImage pro vykreslení
        """
        h, w = state_array.shape
        img = np.zeros((h, w, 3), dtype=np.uint8)
        img[:] = 255  # bílé pozadí
        img[state_array == 1] = [0, 0, 0]  # černé živé buňky

        # převod na QImage
        qimg = QImage(img.data, w, h, 3 * w, QImage.Format.Format_RGB888)
        return qimg


class FluidFlowVisualizer():
    def __init__(self, max_state=10):
        pass

    def visualize(self, state_array: np.ndarray) -> QImage:
        pass

