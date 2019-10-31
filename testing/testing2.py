import os
import sys
import time
import random
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import glob
import ntpath
import math


def _loadFormation(path: str):
    """Loads the formation file at the specified path and returns a list containing its name and the drone positions as a numpy array"""
    name = ntpath.basename(path)
    name = os.path.splitext(name)[0]
    drones = _getRowCount(path)
    arr = np.loadtxt(path, delimiter=",")
    arr = arr.reshape((drones, 3))
    return arr


def _getRowCount(path):
    """Counts the lines of a plain text file. No idea how it works, I copied it from stackoverflow."""
    with open(path) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


def printAsCSV(mat):
    for i in range(0, np.size(mat, 0)):
        print(f"{mat[i, 0]}, {mat[i, 1]}, {mat[i, 2]}")



def get9Grid(dist):
    print(f"{dist}, {dist}, {.3}")
    print(f"{dist}, {0}, {.3}")
    print(f"{dist}, {-dist}, {.3}")
    print(f"{0}, {dist}, {.3}")
    print(f"{0}, {0}, {.3}")
    print(f"{0}, {-dist}, {.3}")
    print(f"{-dist}, {dist}, {.3}")
    print(f"{-dist}, {0}, {.3}")
    print(f"{-dist}, {-dist}, {.3}")


# grid = get9Grid(.45)
mat = _loadFormation(os.path.join(sys.path[0], "8grid1.csv"))
printAsCSV(mat + [0, 0, .7])