
import copy

import streamlit as st

import numpy as np
from scipy.spatial.transform import Rotation as rot

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.set_page_config(layout="wide")

st.header("Cantilever Test")
f_in = st.slider("Compressive force on each side (N)", 0., 0.1, 0., step=0.001)
m = st.slider("Twisting moment on each side (Nm)", 0., 1., 0., step=0.01)
n_points = st.slider("Initial number of solution points (#)", 3, 100, 10, step=1)
show_poses = st.checkbox("Show poses", 1)

rod = Rod()

## Create boundary condition objects
stress_base = np.array([f_in, 0, 0])
moment_base = np.array([m, 0, 0])
base_bc = LoadBC(stress_base, moment_base)

stress_tip = np.array([-f_in, 0, 0])
moment_tip = np.array([-m, 0, 0])
tip_bc = LoadBC(stress_tip, moment_tip)

rod.solve_equillibrium(base_bc, tip_bc, n_points = n_points)
# TODO: Calculate phi along the rod

# Now calculate the Coiling beam analytical solution from Gazzola 2018

## Plot the solution
col_1, col_2 = st.columns(2)
with col_1:
    st.subheader("Visual Comparsion")
    fig_scene = go.Figure()
    fig_scene = rod.plot(fig_scene, show_poses=True)
    fig_scene.update_layout(height = 800, width = 600, scene_camera=dict(eye=dict(x=0.5,y=1.1,z=0.4)))

    analytic_linestyle = copy.deepcopy(rod.line_style)
    analytic_linestyle["color"] = "darkkhaki"

    st.plotly_chart(fig_scene, use_container_width=True)

with col_2:
    st.subheader("Curvature Comparison")