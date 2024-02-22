import numpy as np
import scipy.special


def bernstein_poly(i, n, t):
    return scipy.special.comb(n, i) * t ** i * (1 - t) ** (n - i)


def bezier_curve(points, t):
    n = len(points) - 1
    curve = np.zeros(2)
    for i in range(n + 1):
        curve += points[i] * bernstein_poly(i, n, t)
    return curve

