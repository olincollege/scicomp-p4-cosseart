import copy

import streamlit as st

import numpy as np

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.header("Cantilever Test")
load_mass = st.slider("Load (kg)", 0., 0.05, 0.01, step=0.001, format="%.3f")

## Create boundary condition objects
stress = np.array([0, 0, -9.8*load_mass])
moment = np.array([0, 0, 0])

base_bc = PoseBC(np.array([0, 0, 0]), np.array([0, 0, 0, 1]))   # Base situated at origin
tip_bc = LoadBC(stress, moment)                                 # Tip loaded with specified strain and moments

rod = Rod()
rod.solve_equillibrium(base_bc, tip_bc)

# Now calculate the Timoshenko beam solution from Gazzola et al 2018
# TODO: should this get moved somewhere else so that streamlit is just UI?
F = np.linalg.norm(stress)
alpha_AG = rod.params.K_se[1, 1]
EI = rod.params.K_bt[1, 1]
L = rod.params.l
s = rod.y[0, :]
disp = (-F)/(alpha_AG)*s - (F*L)/(2*EI)*(s**2) + F/(6*EI)*(s**3)

## Plot the solution
st.subheader("Visual Comparsion")
fig_scene = go.Figure()
fig_scene = rod.plot(fig_scene)
fig_scene.update_layout(height = 800, width = 600, scene_camera=dict(eye=dict(x=0.5,y=1.1,z=0.4)))

analytic_linestyle = copy.deepcopy(rod.line_style)
analytic_linestyle["color"] = "darkkhaki"
fig_scene.add_trace(go.Scatter3d(
    x=s,
    y=np.zeros(s.shape),
    z=disp,
    name=("Rod (analytic)"),
    line=analytic_linestyle,
    marker=rod.marker_style
))

st.plotly_chart(fig_scene, use_container_width=True)

st.subheader("Displacement Comparison")
fig_displacement = go.Figure()
fig_displacement.add_trace(go.Scatter(
    x=rod.y[0, :],
    y=rod.y[2, :],
    name="Displacement (ours)"
))

fig_displacement.add_trace(go.Scatter(
    x=s,
    y=disp,
    name="Displacement (analytic)"
))

fig_displacement.update_xaxes(title="Length along rod (m)")
fig_displacement.update_yaxes(title="Vertical displacement (m)")
st.plotly_chart(fig_displacement)