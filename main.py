#!/usr/bin/env python3
import streamlit as st
from rod_rate_funcs import rate_func_bvp
from visual_tools import plot_rod_plotly

import numpy as np
from scipy.integrate import solve_bvp
from scipy.spatial.transform import Rotation as rot

st.subheader("Cantilevered Beam Example")
load_mass = st.slider("Load (kg)", 0., 0.05, 0.01, step=0.001, format="%.3f")
load_torsion_moment = st.slider("Load torsion moment (Nm)", -20., 20., 0.0, step=0.5, format="%.3f")
load_y_moment = st.slider("Load y moment(Nm)", -0.1, 0.1, 0.0, step=0.005, format="%.3f")
load_z_moment = st.slider("Load z moment(Nm)", -0.1, 0.1, 0.0, step=0.005, format="%.3f")

## Define our boundary conditions
# TODO: Move this into the RodBC class
# Wall end: fix position and orientation
p_0 = np.array([0, 0, 0])
R_q_0 = rot.from_euler("xyz", [0, 0, 0], degrees=True).as_quat() # X is up

# Loaded end: gravity load
n_end = np.array([0, 0, -9.8*load_mass])
m_end = np.array([load_torsion_moment, load_y_moment, load_z_moment])

# Pack the boundry conditions into an evaluation function
# TODO: Move this into Rod.solve_equilibrium()
boundary_conditions = np.concatenate([p_0, R_q_0, n_end, m_end])
f_bound_conds = lambda ya, yb: np.concatenate([ya[0:7], yb[7:13]]) - boundary_conditions

## Initialize solver
# TODO: Move this to Rod.solve_equilibrium()
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
# TODO: Move this into Rod.plot()
fig = plot_rod_plotly(bvp_soln)
fig.update_layout(width=600, height=800, scene_camera=dict(eye=dict(x=0.5,y=1.1,z=0.4)))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Cantilievered Beam Validation")
st.text("TODO")