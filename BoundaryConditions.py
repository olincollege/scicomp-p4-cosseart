from abc import ABC

import numpy as np

class RodBC(ABC):
    """Boundary condition defining configuration of one side of the rod
    """
    position: np.ndarray    = np.zeros((3, 1))
    orientation: np.ndarray = np.zeros((4, 1))
    stress: np.ndarray      = np.zeros((3, 1))
    moment: np.ndarray      = np.zeros((3, 1))

    def __init__(self):
        return

class PoseBC(RodBC):
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

class LoadBC(RodBC):
    def __init__(self, stress, moment):
        self.stress = stress
        self.moment = moment