#!/usr/bin/env python3

from rod_rate_funcs import rate_func_bvp
from visual_tools import plot_rod_plotly

import numpy as np
from scipy.integrate import solve_ivp, solve_bvp
from scipy.spatial.transform import Rotation as rot

## Define our boundary conditions
# Wall end: fix position and orientation
p_0 = np.array([0, 0, 0])
R_q_0 = rot.from_euler("xyz", [0, 0, 0], degrees=True).as_quat() # X is up

# Loaded end: gravity load
n_end = np.array([0, 0, -9.8*0.001])
m_end = np.array([0, 0, 0])

# Pack the boundry conditions into an evaluation function
boundary_conditions = np.concatenate([p_0, R_q_0, n_end, m_end])
f_bound_conds = lambda ya, yb: np.concatenate([ya[0:7], yb[7:13]]) - boundary_conditions

## Initialize solver
# Create mesh point coordinates
s_grid = np.linspace(0, 1, 10)

# Create initial conditions (along the rod)
p_0 = np.array([0, 0, 0])
R_q_0 = rot.from_euler("xyz", [0, 0, 0], degrees=True).as_quat() # X is up
m_0 = np.array([0, 0, 0])
n_0 = np.array([0, 0, 0])
y_0 = np.concatenate([p_0, R_q_0, m_0, n_0])
y_0_mesh = np.repeat(np.atleast_2d(y_0).T, 10, axis=1)
y_0_mesh[0, :] = s_grid

bvp_soln = solve_bvp(rate_func_bvp, f_bound_conds, s_grid, y_0_mesh)

## Plot the solution
fig = plot_rod_plotly(bvp_soln)
fig.show()