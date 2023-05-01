
import copy

import streamlit as st

import numpy as np
from scipy.spatial.transform import Rotation as rot

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.set_page_config(layout="wide")

st.header("Cantilever Test")
D_half = st.slider("Dist. to move each end (m)", 0., 0.25, 0., step=0.0025)
phi_half = st.slider("Angle to rotate each end (deg)", 0, 3000, 0, step=10)
# n_turns = st.slider("Number of full rotations to turn each end", 0, 30, 0, step=1)
# phi_half = n_turns * 360
n_points = st.slider("Initial number of solution points (#)", 3, 100, 10, step=1)
show_poses = st.checkbox("Show poses", 1)

rod = Rod()

## Create boundary condition objects
R_base = rot.from_euler("xyz", [phi_half, 0, 0], degrees=True).as_quat()
base_bc = PoseBC(np.array([D_half, 0, 0]), R_base)    # Base situated at origin

R_tip = rot.from_euler("xyz", [-phi_half, 0, 0], degrees=True).as_quat()
tip_bc = PoseBC(np.array([rod.params.l - D_half, 0, 0]), R_tip)                                 # Tip loaded with specified strain and moments

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