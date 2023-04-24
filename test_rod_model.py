#!/bin/usr/env python3
from rod_rate_funcs import mat_skew_sym_4

import numpy as np

def test_mat_skew_sym_4():
    # Integrate angular velocity for a quaternion state over unit time
    from scipy.integrate import solve_ivp
    from scipy.spatial.transform import Rotation as rot

    # Create example ang-vel integration problem
    # Integrating an angular velocity over unit time is equivalent to treating it as an axis-angle
    # representation of a rotation, and finding the corresponding quaternion.
    omega = np.array([1, 2, 3])
    q_0 = rot.from_euler("xyz", [0, 0, 0])
    q_end = q_0 * rot.from_rotvec(omega)

    q_0 = q_0.as_quat()
    q_end = q_end.as_quat()

    # Now numerically integrate it quaternion-style
    Omega = mat_skew_sym_4(omega)
    def rate_func(t, q):
        # Joan Sola's work does not have the 0.5 scale factor...
        qdot = 0.5 * Omega @ q

        # In theory this should work too? It should be equivalent to our computation here.
        # qdot = rot.from_quat(q) * rot.from_quat(np.concatenate([omega, [0]]))
        # qdot = qdot.as_quat()
        return qdot

    t = [0, 1]
    ivp_soln = solve_ivp(rate_func, t, q_0, reltol=1-10, abstol=1-10)

    assert np.allclose(ivp_soln.y[:, -1], q_end, atol=1e-3)

def test_batch_matmul():
    assert True