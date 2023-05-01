#!/usr/bin/env python3
import streamlit as st

import numpy as np
from scipy.integrate import solve_ivp, solve_bvp
from scipy.spatial.transform import Rotation as rot

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.set_page_config(layout="wide")

# TODO: Make this a proper landing page!
# 1. Plot a bending rod simulation result, no sliders
# 2. Give a little introductory blurb: page navigation, sandbox, benchmarks, features included and not included
st.header("Elastic Beam Simulation")
st.text("TODO: Write a little blurb here!")

col_1, col_2 = st.columns(2)

with col_2:
    col_linear, col_angular = st.columns(2)
    with col_linear:
        x_force = st.slider("X force on tip (N)", -10., 10., 0., step=0.1)
        y_force = st.slider("Y force on tip (N)", -0.5, 0.5, 0., step=0.005, format="%.3f")
        z_force = st.slider("Z force on tip (N)", -0.5, 0.5, 0., step=0.005, format="%.3f")
        
    with col_angular:
        load_torsion_moment = st.slider("Torsion on tip (Nm)", -2., 2., 0.0, step=0.025, format="%.3f")
        load_y_moment = st.slider("Y bending moment on tip (Nm)", -0.1, 0.1, 0.0, step=0.005, format="%.3f")
        load_z_moment = st.slider("Z bending moment on tip (Nm)", -0.1, 0.1, 0.0, step=0.005, format="%.3f")

    show_poses = st.checkbox("Show poses", 1)

with col_1:
    ## Create boundary condition objects
    stress = np.array([x_force, y_force, z_force])
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