import streamlit as st

import numpy as np

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.header("Cantilever Test")
load_mass = st.slider("Load (kg)", 0., 0.05, 0.01, step=0.001, format="%.3f")

## Create boundary condition objects
stress = np.array([0, 0, -9.8 * load_mass])
moment = np.array([0, 0, 0])

base_bc = PoseBC(np.array([0, 0, 0]), np.array([0, 0, 0, 1]))   # Base situated at origin
tip_bc = LoadBC(stress, moment)                                 # Tip loaded with specified strain and moments

rod = Rod()
rod.solve_equillibrium(base_bc, tip_bc)

## Plot the solution
fig = go.Figure()
fig = rod.plot(fig)
fig.update_layout(height = 800, width = 600, scene_camera=dict(eye=dict(x=0.5,y=1.1,z=0.4)))
st.plotly_chart(fig, use_container_width=True)

# TODO!!! Implement the analytic timoshenko beam solution from Gazzola et al 2018.