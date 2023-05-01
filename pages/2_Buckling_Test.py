
import copy

import streamlit as st

import numpy as np
from scipy.spatial.transform import Rotation as rot

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.set_page_config(layout="wide")

st.header("Cantilever Test")
st.subheader("Test Description")
st.markdown("""
    **Expected outcome:** When you both compress and twist the beam, at some point it should buckle!

    **Actual outcome:** When you compress the beam it doubles in on itself / inverts so that the length becomes negative. Like it just goes backwards. Thus no amount of twisting can make it buckle.
""")

f_compression = st.slider("Stretch(+) / Compression(-) force on tip (N)", -1000, 1000, 0, step=10)
m_torsion = st.slider("Twisting moment on tip (Nm)", int(-1e6), int(1e6), 0, step=100)
n_points = st.slider("Initial number of solution points (#)", 3, 100, 10, step=1)
show_poses = st.checkbox("Show poses", 1)

rod = Rod()

## Create boundary condition object
stress = np.array([f_compression, 0, 0])
moment = np.array([m_torsion, 0, 0])

base_bc = PoseBC(np.array([0, 0, 0]), np.array([0, 0, 0, 1]))   # Base situated at origin
tip_bc = LoadBC(stress, moment)                                 # Tip loaded with specified strain and moments

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

    st.plotly_chart(fig_scene, use_container_width=True)

with col_2:
    st.subheader("Curvature Comparison")
    st.error("Currently does not work :(")