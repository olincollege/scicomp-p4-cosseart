from dataclasses import dataclass

import numpy as np
from scipy.spatial.transform import Rotation as rot
from scipy.integrate import solve_bvp

import plotly.graph_objects as go

from rod_rate_funcs import rate_func_bvp
from BoundaryConditions import RodBC, PoseBC, LoadBC
from visual_tools import plot_transforms

@dataclass
class RodParams:
    """ Dataclass for storing rod parameters
    """
    K_se: np.ndarray    = np.diag([0.1, 10., 10.])
    K_bt: np.ndarray    = 0.1 * np.diag([0.1, 1., 1.])
    l: float            = 1

class Rod:
    params: RodParams
    y: np.ndarray
    marker_style: dict  = dict(size=3)
    line_style: dict    = dict(width=5, color="black")

    def __init__(self, params=RodParams):
        ## Initialize all the variables needed for the boundary value problem that are worth storing
        self.params = params

    def solve_equillibrium(self, base_bc: RodBC, tip_bc: RodBC, n_points=10):
        if isinstance(base_bc, PoseBC) and isinstance(tip_bc, LoadBC):
            f_bound_conds = lambda ya, yb: np.concatenate([base_bc.residual(ya), tip_bc.residual(yb)])
        elif isinstance(base_bc, PoseBC) and isinstance(tip_bc, PoseBC):
            f_bound_conds = lambda ya, yb: np.concatenate([base_bc.residual(ya), tip_bc.residual(yb, rotvec=True)])
        elif isinstance(base_bc, LoadBC) and isinstance(tip_bc, LoadBC):
            f_bound_conds = lambda ya, yb: np.concatenate([base_bc.residual(ya), tip_bc.residual(yb), [np.dot(base_bc.residual(ya), tip_bc.residual(yb))]])

        # 2. Create the initial condition mesh
        ## Initialize solver
        # Create mesh point coordinates
        s_grid = np.linspace(0, 1, n_points)

        # Create initial conditions (along the rod)
        p_0 = np.array([0, 0, 0])
        R_0 = rot.from_euler("xyz", [0, 0, 0], degrees=True).as_quat() # X is up
        m_0 = np.array([0, 0, 0])
        n_0 = np.array([0, 0, 0])
        y_0 = np.concatenate([p_0, R_0, m_0, n_0])
        y_0_mesh = np.repeat(np.atleast_2d(y_0).T, n_points, axis=1)
        y_0_mesh[0, :] = s_grid

        bvp_soln = solve_bvp(rate_func_bvp, f_bound_conds, s_grid, y_0_mesh)
        self.y = bvp_soln.y

    def plot(self, fig=go.Figure(), marker=None, line=None, show_poses=False):
        if marker is not None:
            self.marker_style = marker

        if line is not None:
            self.line_style = line

        fig = plot_transforms(self.y[0:3, :], self.y[3:7, :], fig=fig, show=show_poses)

        fig.add_trace(go.Scatter3d(
            x = self.y[0, :],
            y = self.y[1, :],
            z = self.y[2, :],
            name="Rod",
            marker=self.marker_style,
            line=self.line_style
        ))

        mins = np.min(self.y[0:3, :], axis=1)
        maxs = np.max(self.y[0:3, :], axis=1)
        lims = np.array([mins, maxs]).T
        ranges = maxs - mins
        midpoints = np.atleast_2d(np.mean(lims, axis=1)).T
        max_range = np.max(ranges)

        new_ranges = midpoints + np.array([
            [-max_range, max_range],
            [-max_range, max_range],
            [-max_range, max_range]
        ])

        fig.update_layout(
            scene=dict(
                aspectmode='manual',
                xaxis=dict(range=new_ranges[0, :]),
                yaxis=dict(range=new_ranges[1, :]),
                zaxis=dict(range=new_ranges[2, :])
            ),
        )

        return fig