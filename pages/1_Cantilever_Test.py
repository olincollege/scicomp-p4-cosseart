import copy

import streamlit as st

import numpy as np

import plotly.graph_objects as go

from Rod import Rod
from BoundaryConditions import PoseBC, LoadBC

st.set_page_config(layout="wide")

st.header("Cantilever Test")
st.subheader("Test Description")
st.markdown("""
    **Expected outcome:** We know the analytic solution of applying a point load to the free end of a beam fixed at the other end. Our simulation should match the expected solution

    **Actual outcome:** Our simulation comes close to the analytic solution, but has errors at higher loads. It is unclear why this is - increasing the resolution of the BVP solution does not seem to change the error.
    
    The test scenario and analytic solution is taken from page 12 of [Gazzola et al 2018](https://mattia-lab.com/wp-content/uploads/2018/06/Gazzola_RSOS_2018.pdf)
""")

load_mass = st.slider("Load (kg)", 0., 0.05, 0.01, step=0.001, format="%.3f")
n_points = st.slider("Initial number of solution points (#)", 3, 100, 10, step=1)
show_poses = st.checkbox("Show poses", 1)

## Create boundary condition objects
stress = np.array([0, 0, -9.8*load_mass])
moment = np.array([0, 0, 0])

base_bc = PoseBC(np.array([0, 0, 0]), np.array([0, 0, 0, 1]))   # Base situated at origin
tip_bc = LoadBC(stress, moment)                                 # Tip loaded with specified strain and moments

rod = Rod()
rod.solve_equillibrium(base_bc, tip_bc, n_points = n_points)

# Now calculate the Timoshenko beam solution from Gazzola et al 2018
# TODO: should this get moved somewhere else so that streamlit is just UI?
F = np.linalg.norm(stress)
alpha_AG = rod.params.K_se[1, 1]
EI = rod.params.K_bt[1, 1]
L = rod.params.l
s = rod.y[0, :]
disp = (-F)/(alpha_AG)*s - (F*L)/(2*EI)*(s**2) + F/(6*EI)*(s**3)

## Plot the solution
col_1, col_2 = st.columns(2)
with col_1:
    st.subheader("Visual Comparsion")
    fig_scene = go.Figure()
    fig_scene = rod.plot(fig_scene, show_poses=show_poses)
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

with col_2:
    st.subheader("Displacement Comparison")
    fig_displacement = go.Figure()
    fig_displacement.add_trace(go.Scatter(
        x=rod.y[0, :],
        y=rod.y[2, :],
        name="Displacement (ours)",
        mode="markers+lines"
    ))

    fig_displacement.add_trace(go.Scatter(
        x=s,
        y=disp,
        name="Displacement (analytic)",
        mode="markers+lines"
    ))

    fig_displacement.update_xaxes(title="Length along rod (m)")
    fig_displacement.update_yaxes(title="Vertical displacement (m)")
    fig_displacement.update_layout(height=800, width=600)

    st.plotly_chart(fig_displacement, use_container_width=True)