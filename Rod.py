from dataclasses import dataclass

import numpy as np

from rod_rate_funcs import rate_func_bvp

@dataclass
class RodParams:
    """ Dataclass for storing rod parameters
    """
    K_se: np.ndarray    = np.eye(3)
    K_bt: np.ndarray    = np.eye(3)
    l: float            = 1

class RodBC:
    """Boundary condition defining configuration of one side of the rod
    """
    position: np.ndarray    = np.zeros((3, 1))
    orientation: np.ndarray = np.zeros((4, 1))
    stress: np.ndarray      = np.zeros((3, 1))
    moment: np.ndarray      = np.zeros((3, 1))

    def __init__(self):
        return

    @staticmethod
    def default_pose_cond():
        pass

    @staticmethod
    def default_strain_cond():
        pass

class Rod:
    base_bc: RodBC
    tip_bc: RodBC
    params: RodParams

    def __init__(self, base_bc: RodBC, tip_bc: RodBC, params=RodParams):
        ## Initialize all the variables needed for the boundary value problem that are worth storing
        self.base_bc = base_bc
        self.tip_bc = tip_bc
        self.params = params

    def solve_equillibrium():
        # Initialize helper variables and solve the problem
        # 1. Create the boundary value callable
        # 2. Create the initial condition mesh
        pass

    def plot():
        pass