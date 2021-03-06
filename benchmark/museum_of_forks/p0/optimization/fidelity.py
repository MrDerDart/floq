# Provide templates and implementations for FidelityComputer class,
# which wraps a ParametricSystem and computes F and dF for given controls
from benchmark.museum_of_forks.p0.core.fidelities import d_operator_distance, operator_distance
import numpy as np


class FidelityBase(object):
    """
    Define how to calculate a fidelity and its gradient from a
    ParametricSystem. Keeps track of iterations, counting up every
    time a new controls_and_t array is encountered.

    This is a base class and needs to be sub-classed. Sub-classes
    should implement _f(controls_and_t) and _df(controls_and_t), where
    controls_and_t is an array of control amplitudes and possibly
    the duration of the pulse as last entry.

    Optionally, a sub-class can implement a function penalty(controls_and_t) and
    d_penalty(controls_and_t) that represent a penalty function that is added
    to f and df, respectively.

    Also optionally, a function _iteterate can be implemented, which gets called
    on each iteration.

    The __init__ should take the form __init__(self, system, **kwargs)
    for compatibility with EnsembleFidelity.
    """

    def __init__(self, system):
        self.system = system
        self._last_controls_and_t = None
        self.iterations = 0


    def f(self, controls_and_t):
        return self._f(controls_and_t) + self.penalty(controls_and_t)


    def df(self, controls_and_t):
        return self._df(controls_and_t) + self.d_penalty(controls_and_t)


    def iterate(self, controls_and_t):
        """
        Gets called by the Optimizer after each iteration. Increases
        the iteration count self.iterations, and calls the (optional)
        _iterate method.
        """
        self.iterations += 1
        self._iterate(controls_and_t)
        f = self.f(controls_and_t)


    def reset_iterations(self):
        self.iterations = 0


    def _f(self, controls_and_t):
        raise NotImplementedError


    def _df(self, controls_and_t):
        raise NotImplementedError


    def _iterate(self, controls_and_t):
        pass


    def penalty(self, controls_and_t):
        return 0.0


    def d_penalty(self, controls_and_t):
        return 0.0



class EnsembleFidelity(FidelityBase):
    """
    With a given Ensemble, and a FidelityComputer,
    calculate the average fidelity over the whole ensemble.
    """

    def __init__(self, ensemble, fidelity, **params):
        super(EnsembleFidelity, self).__init__(ensemble)
        self.fidelities = [fidelity(sys, **params) for sys in ensemble.systems]

    def _f(self, controls_and_t):
        f = np.mean([fid.f(controls_and_t) for fid in self.fidelities])
        return f


    def _df(self, controls_and_t):
        df = np.mean([fid.df(controls_and_t) for fid in self.fidelities], axis=0)
        return df




class OperatorDistance(FidelityBase):
    """
    Calculate the operator distance (see core.fidelities for details)
    for a given ParametricSystem and a fixed pulse duration t.
    """

    def __init__(self, system, t, target):
        super(OperatorDistance, self).__init__(system)

        self.t = t
        self.target = target


    def f(self, controls):
        u = self.system.u(controls, self.t)
        return operator_distance(u, self.target)


    def df(self, controls):
        u = self.system.u(controls, self.t)
        du = self.system.du(controls, self.t)
        return d_operator_distance(u, du, self.target)
