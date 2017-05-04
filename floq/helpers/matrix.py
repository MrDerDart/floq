import numpy as np


def is_unitary(u, tolerance=1e-10):
    unitary = np.eye(u.shape[0])
    umat = np.mat(u)
    product = umat.H * umat
    return np.allclose(product, unitary, atol=tolerance)


def adjoint(m):
    return np.transpose(np.conj(m))


def gram_schmidt(vecs):
    """Computes an orthonormal basis for the given set of (complex) vectors.

    Vectors are expected to be supplied as the rows of an array,
    i.e. the first vector should be vecs[0] etc.

    An array of the same form is returned.

    The orthonormalisation is done with respect to the inner product
    used in QM: <a | b> = a^dagger b, i.e. including a complex conjugation.

    The algorithm implemented is the modified Gram-Schmidt procedure,
    given in Numerical Methods for Large Eigenvalue Problems: Revised Edition, algorithm 1.2.
    """

    result = np.zeros_like(vecs)
    n = vecs.shape[0]

    r = norm(vecs[0])
    if r == 0.0:
        raise ArithmeticError("Vector with norm 0 occured.")
    else:
        result[0] = vecs[0]/r

    for j in xrange(1, n):
        q = vecs[j]

        for i in xrange(j):
            rij = product(result[i], q)

            q = q-rij*result[i]

        rjj = norm(q)

        if rjj == 0.0:
            raise ArithmeticError("Vector with norm 0 occured.")
        else:
            result[j] = q/rjj

    return result


def product(a, b):
    """Compute <a | b>.

    Includes complex conjugation!"""

    return np.conj(a).dot(b)


def norm(a):
    """Compute sqrt(<a|b>)."""

    return np.sqrt(product(a, a))
