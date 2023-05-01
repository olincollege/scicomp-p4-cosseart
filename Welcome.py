#!/usr/bin/env python3
import streamlit as st

import numpy as np
from scipy.integrate import solve_ivp, solve_bvp
from scipy.spatial.transform import Rotation as rot

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

# TODO: Make this a proper landing page!
# 1. Plot a bending rod simulation result, no sliders
# 2. Give a little introductory blurb: page navigation, sandbox, benchmarks, features included and not included
st.header("Elastic Beam Simulation")
load_mass = st.slider("Load (kg)", 0., 0.05, 0.01, step=0.001, format="%.3f")
load_torsion_moment = st.slider("Load torsion moment (Nm)", -1., 1., 0.0, step=0.025, format="%.3f")
load_y_moment = st.slider("Load y moment(Nm)", -0.1, 0.1, 0.0, step=0.005, format="%.3f")
load_z_moment = st.slider("Load z moment(Nm)", -0.1, 0.1, 0.0, step=0.005, format="%.3f")

show_poses = st.checkbox("Show poses", 1)

## Create boundary condition objects
stress = np.array([0, 0, -9.8 * load_mass])
moment = np.array([load_torsion_moment, load_y_moment, load_z_moment])

base_bc = PoseBC(np.array([0, 0, 0]), np.array([0, 0, 0, 1]))   # Base situated at origin
tip_bc = LoadBC(stress, moment)                                 # Tip loaded with specified strain and moments

rod = Rod()
rod.solve_equillibrium(base_bc, tip_bc)

## Plot the solution
fig = go.Figure()
fig = rod.plot(fig, show_poses=show_poses)
fig.update_layout(height = 800, width = 600, scene_camera=dict(eye=dict(x=0.5,y=1.1,z=0.4)))
st.plotly_chart(fig, use_container_width=True)