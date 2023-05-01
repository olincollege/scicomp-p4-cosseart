import plotly.graph_objects as go
import numpy as np
from scipy.spatial.transform import Rotation as rot

# TODO: Just take in a soln. object rather than posns and quats
def plot_transforms(posns, quats, axis_length=0.1, marker_size = 3, show=True, fig=go.Figure()):
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
            visible= True if show else "legendonly",
            marker=dict(color=axis_colors[i], size=marker_size)
        ))
    
    fig.add_trace(go.Scatter3d(
        x=posns[0, :],
        y=posns[1, :],
        z=posns[2, :],
        mode="markers",
        name="Poses",
        legendgroup="poses",
        visible= True if show else "legendonly",
        marker=dict(color="black", size=marker_size)
    ))
    
    return fig
