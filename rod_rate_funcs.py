import numpy as np
from scipy.spatial.transform import Rotation as rot

# Helper functions for the rod rate functions
def mat_skew_sym_3(omega):
    # Create 2x3 skew-symmetric matrix given a 3-vector
    # Aka create the corresponding matrix to a cross-product
    # For converting an angular velocity vector to its matrix form
    # 
    # TODO: take a list of omega vectors?
    
    x, y, z = omega
    
    Omega = np.array([
        [0, -x, y],
        [x, 0, -z],
        [-y, z, 0]
    ])
    
    return Omega

def mat_skew_sym_4(omega):
    # Skew symmetric matrix for converting body frame angular velocities to the dq/dt quaternion rate of change
    # See https://math.stackexchange.com/q/1797542 
    x, y, z = omega
    
    # See https://arxiv.org/pdf/1711.02508.pdf  pg 7, eq 17 and 18.
    # Take the Right multiplication and substitute in qw=0, qx=omega_x, qy=omega_y, qz=omega_z
    # Motivation: See pg 21 eq 93. To integrat a body-frame angular velocity in the world frame we must multiply from the right
    # the orientation by the angular velocity. This is the corresponding matrix to that operation.
    Omega = np.array([
        [0, z, -y, x],
        [-z, 0, x, y],
        [y, -x, 0, z],
        [-x, -y, -z, 0]
    ])
    return Omega

def rate_func_bvp(s, y):
    ## Define constants
    f = np.array([0., 0., 0.])
    l = np.array([0., 0., 0.])
    K_se = np.diag([0.1, 10., 10.]) # Stiffnesses: [stretch, x_shear, y_shear]
    K_bt = 0.1 * np.diag([0.1, 1., 1.]) # Stiffnesses: [torsion, bending_y, bending_z]

    # TODO: You shouldn't need to define both v_star and vdot_star
    # Could numerically differentiate one to get the other..?
    # Also TODO: This is not equipped to handle varying v_star or vdot_star
    # Which is rare for these rods but still possible.
    v_star = np.array([[1, 0, 0]]).T
    u_star = np.array([[0, 0, 0]]).T
    vdot_star = np.array([[0, 0, 0]]).T
    udot_star = np.array([[0, 0, 0]]).T
    
    p = y[0:3, :]
    R_q = y[3:7, :]
    n = y[7:10, :]
    m = y[10:13, :]
    
    # Apply conversions between matrix-vecor forms
    # !!!!! REMEMBER: SCIPY QUATERNIONS HAVE W LAST !!!!!
    R = rot.from_quat(R_q.T).as_matrix() # We store the rotation as quaternion in state for compactness; now convert to mat
    
    # u, v from m, n
    u = K_se @ np.einsum('ijk,ki->ji', np.transpose(R, [0, 2, 1]), m) + u_star
    v = K_bt @ np.einsum('ijk,ki->ji', np.transpose(R, [0, 2, 1]), n) + v_star
    
    # u_hat = mat_skew_sym_3(u)
    # v_hat = mat_skew_sym_3(v)
    
    ## System of ODEs from Rucker
    # Rate of change of position is the body-frame velocity rotated to world frame:
    pdot = np.einsum('ijk,ki->ji', R, v)
    
    # Rate of change of orinetation quaternion in wordl frame is the skew-symmetric form of angular vel
    # converted to an angular velocity in world frame by multiplying with current orientation quaternion
    qdot = np.zeros(R_q.shape)
    for i, u_i in enumerate(u.T):
        R_qdot_i = 0.5 * mat_skew_sym_4(u_i) @ R_q[:, i]
        qdot[:, i] = R_qdot_i
           
    # Rate of change for m and n!
    ndot = np.zeros(n.shape)
    mdot = np.cross(-pdot, n, axis=0) - np.atleast_2d(l).T
    
    dy = np.vstack([pdot, qdot, ndot, mdot])    
    return dy    

