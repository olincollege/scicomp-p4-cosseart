from abc import ABC

import numpy as np

from scipy.spatial.transform import Rotation as rot

class RodBC(ABC):
    """Boundary condition defining configuration of one side of the rod
    """
    position: np.ndarray    = np.zeros((3, 1))
    orientation: np.ndarray = np.zeros((4, 1))
    stress: np.ndarray      = np.zeros((3, 1))
    moment: np.ndarray      = np.zeros((3, 1))

    def __init__(self):
        return

    def residual(self, y):
        pass

class PoseBC(RodBC):
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

    def residual(self, y: np.ndarray, rotvec=False):
        if rotvec:
            orientation_residual = rot.from_quat(y[3:7]).as_rotvec() - rot.fromr_quat(self.orientation).as_rotvec()
            return np.concatenate([y[0:3] - self.position, orientation_residual])
        else:
            return np.concatenate([y[0:3] - self.position, y[3:7] - self.orientation])

class LoadBC(RodBC):
    def __init__(self, stress, moment):
        self.stress = stress
        self.moment = moment

    def residual(self, y: np.ndarray):
        return np.concatenate([y[7:10] - self.stress, y[10:13] - self.moment])