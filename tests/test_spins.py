import unittest
import numpy as np
import floq.systems.spins as spins
import assertions


def single_hf(controls, omega):
    a1 = controls[0]
    b1 = controls[1]
    a2 = controls[2]
    b2 = controls[3]
    return np.array([[[0, 0.25*(1j*a2 + b2)],
                      [0.25*1j*(a2 + 1j*b2), 0]],
                     [[0, 0.25*(1j*a1 + b1)],
                      [0.25*1j*(a1 + 1j*b1), 0]],
                     [[omega/2.0, 0],
                      [0, -(omega/2.0)]],
                     [[0, -0.25j*(a1 - 1j*b1)],
                      [0.25*(-1j*a1 + b1), 0]],
                     [[0, -0.25j*(a2 - 1j*b2)],
                     [0.25*(-1j*a2 + b2), 0]]])


class TestSpinSystem(unittest.TestCase, assertions.CustomAssertions):

    def test_build_single_hf(self):
        controls = np.array([1.2, 2.3, 3.4, 5.4])
        amps = np.array([0.9, 1.1])
        freqs = np.array([3.5, 6.0])
        amp = 1.0
        freq = 2.5
        target = single_hf(amp*controls, freq)

        ss = spins.SpinSystem(1, 1, 1, 1, 1)
        result = ss._build_single_hf(2, freq, amp, controls)
        self.assertArrayEqual(target, result)
