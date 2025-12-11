import sys
import os
# trochu jsem si musel pohrát s importy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # pridej cestu o uroven vyse

from Backend.gameOfLife import GameOfLife
from Backend.forestFire import ForestFire
from Backend.fluidFlow import FluidFlow


RULES_DICT = {
    "GameOfLife": GameOfLife,
    "ForestFire": ForestFire,
    "FluidFlow": FluidFlow,
}