import numpy as np
import benchmark.museum_of_forks.p0.core.fixed_system as fs
import benchmark.museum_of_forks.p0.evolution as ev
import benchmark.museum_of_forks.p0.errors as er


class ParametricSystemBase(object):
    """
    Specifies a physical system that still has open parameters,
    such as the control amplitudes, the control duration, or other arbitrary
    parameters in the Hamiltonian.

    The base class provides two functions:
    - u(controls, t)
    - du(controls, t),
    which implement basic caching and automatically update self.nz.

    To function, this needs to be sub-classed, and a subclass should provide:
    - _hf(controls),
    - _dhf(controls)
    as well as __init__, which has to set self.nz, self.omega and self.t, and needs to call
    this class' __init__.

    """
    def __init__(self):
        self._last_controls = None
        self._last_t = None


    def _hf(self, controls):
        raise NotImplementedError


    def _dhf(self, controls):
        raise NotImplementedError


    def u(self, controls, t):
        if self._is_cached(controls, t):
            return self._fixed_system.u
        else:
            self._set_cached(controls, t)

            u = self._fixed_system.u
            self.nz = self._fixed_system.params.nz
            return u


    def du(self, controls, t):
        if self._is_cached(controls, t):
            return self._fixed_system.du
        else:
            self._set_cached(controls, t)

            du = self._fixed_system.du
            self.nz = self._fixed_system.params.nz
            return du


    def _is_cached(self, controls, t):
        if not isinstance(controls, np.ndarray):
            return False
        elif self._last_t != t:
            return False
        else:
            return np.array_equal(self._last_controls, controls)


    def _set_cached(self, controls, t):
        self._last_controls = controls
        self._last_t = t

        hf = self._hf(controls)
        dhf = self._dhf(controls)
        self._fixed_system = fs.FixedSystem(hf, dhf, self.nz, self.omega, t)


class ParametricSystemWithFunctions(ParametricSystemBase):
    """
    A ParametricSystem that wraps callables hf and dhf.
    """

    def __init__(self, hf, dhf, nz, omega, parameters):
        """
        hf: callable hf(controls,parameters,omega)
        dhf: callable dhf(controls,parameters,omega)
        omega: 2 pi/T, the period of the Hamiltonian
        nz: number of Fourier modes to be considered during evolution
        parameters: a data structure that holds parameters for hf and dhf
        (dictionary is probably the best idea)
        """
        self.hf = hf
        self.dhf = dhf
        self.omega = omega
        self.nz = nz
        self.parameters = parameters

    def _hf(self, controls):
        return self.hf(controls, self.parameters, self.omega)


    def _dhf(self, controls):
        return self.dhf(controls, self.parameters, self.omega)
