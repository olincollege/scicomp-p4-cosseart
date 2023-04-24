import plotly.graph_objects as go
import numpy as np
from scipy.spatial.transform import Rotation as rot
import matplotlib.pyplot as plt

# TODO: Just take in a soln. object rather than posns and quats
def plot_transforms(posns, quats, axis_length=0.1, marker_size = 3, fig=go.Figure()):
    # 3D matrix which stores the list of individual points to plot for each body-axis (x, y, z)
    # For each pose: store start point (at the center of pose), end point of the body-axis, and then insert 'None' to separate lines.
    # Note there will be a trailing 'None'.
    numels = 3*len(posns.T)
    body_points_xyz = np.zeros((3, 3, numels))
    
    R = rot.from_quat(quats.T).as_matrix()
    
    idx = 0
    for i, posn in enumerate(posns.T):
        for i_axis, body_points_axis in enumerate(body_points_xyz):
            body_points_axis[:, idx] = posn
            body_points_axis[:, idx+1] = posn + R[i, :, i_axis] * axis_length
            body_points_axis[:, idx+2] = np.array([None, None, None])
        
        idx += 3
        
    axis_names = ["x", "y", "z"]
    axis_colors = ["red", "green", "blue"]
    for i, axis in enumerate(body_points_xyz):
        fig.add_trace(go.Scatter3d(
            x=axis[0, :],
            y=axis[1, :],
            z=axis[2, :],
            name=axis_names[i],
            mode="lines+markers",
            legendgroup="poses",
            showlegend=False,
            marker=dict(color=axis_colors[i], size=marker_size)
        ))
    
    fig.add_trace(go.Scatter3d(
        x=posns[0, :],
        y=posns[1, :],
        z=posns[2, :],
        mode="markers",
        name="Poses",
        legendgroup="poses",
        marker=dict(color="black", size=marker_size)
    ))
    
    return fig

def plot_rod_plotly(soln):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x = soln.y[0, :],
        y = soln.y[1, :],
        z = soln.y[2, :],
        marker=dict(size=2)
    ))

    mins = np.min(soln.y[0:3, :], axis=1)
    maxs = np.max(soln.y[0:3, :], axis=1)
    lims = np.array([mins, maxs]).T
    ranges = maxs - mins
    midpoints = np.atleast_2d(np.mean(lims, axis=1)).T
    max_range = np.max(ranges)

    new_ranges = midpoints + np.array([
        [-max_range, max_range],
        [-max_range, max_range],
        [-max_range, max_range]
    ])

    fig.update_layout(
        scene=dict(
            aspectmode='manual',
            xaxis=dict(range=new_ranges[0, :]),
            yaxis=dict(range=new_ranges[1, :]),
            zaxis=dict(range=new_ranges[2, :])
        ),
        height=600,
        width=800,
    )
    fig.show()

def plot_rod_mpl(soln):
    # Using matplotlib for now as plotly is being annoying about rods
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot(soln.y[0, :], soln.y[1, :], soln.y[2, :], marker='o')
    ax.stem(soln.y[0, :], soln.y[1, :], soln.y[2, :])
    # ax.axis("equal")
    plt.show()
    
