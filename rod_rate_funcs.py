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

# Implement Rucker's equation
# y:= [p, R, v, u]
# 
# We store R not as its full rotation matrix but instead in quaternion form, giving a final expanded state:
# [x, y, z, q1, q2, q3, q4, v1, v2, v3, u1, u2, u3]
def rate_func_ivp(s, y, f, l, v_star, u_star, vdot_star, udot_star, K_se, K_bt):    
    p = y[0:3]
    R_q = y[3:7]
    v = y[7:10]
    u = y[10:13]
    
    # Apply conversions between matrix-vecor forms
    # !!!!! REMEMBER: SCIPY QUATERNIONS HAVE W LAST !!!!!
    R = rot.from_quat(R_q).as_matrix() # We store the rotation as quaternion in state for compactness; now convert to mat
    u_hat = mat_skew_sym_3(u)
    v_hat = mat_skew_sym_3(v)
    
    ## System of ODEs from Rucker
    # Rate of change of position is the body-frame velocity rotated to world frame:
    pdot = R @ v
    
    # Rate of change of orinetation quaternion in wordl frame is the skew-symmetric form of angular vel
    # converted to an angular velocity in world frame by multiplying with current orientation quaternion
    R_qdot = 0.5 * mat_skew_sym_4(u) @ R_q
    
    # Calculate forces and moments at the current point along the rod:
    # force per unit of s: N/m = kg m /s^2 m = kg/s^2
    # g / (rho*A) = m/s^2 * (kg/m^3 * m^2) = m/s^2 * kg/m = kg/s^2 :)
    rho_g_cm3 = 1.1 # g/cm^3
    rho = rho_g_cm3 * 100**2 / 1000 # kg/m^3
    A = (0.0254/4)**2 * np.pi # m^2
    f_g_world = np.array([0, 0, -9.8 * (rho*A)])
    f += f_g_world
    
    # Beam bending equlibrium constituitive equations
    vdot = vdot_star - np.linalg.inv(K_se) @ (u_hat @ K_se @ (v - v_star) + R.T @ f)
    udot = udot_star - np.linalg.inv(K_bt) @ (u_hat @ K_bt @ (u - u_star) + K_se @ v_hat @ (v - v_star) + R.T @ l)
    
    # import pdb; pdb.set_trace()
    
    dy = np.concatenate([pdot, R_qdot, vdot, udot])
    
    return dy

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

