import numpy as np
from scipy.signal import detrend


def find_peaks_ampd(x, scale=None, debug=False):
    """Find peaks in quasi-periodic noisy signals using AMPD algorithm
    Automati Multi-Scale Peak Detection originally proposed in
    "An Efficient Algorithm for Automatic Peak Detection in
    Noisy Periodic and Quasi-Periodic Signals", Algorithms 2012, 5, 588-603
    https://doi.org/10.1109/ICRERA.2016.7884365

    Optimized implementation by Igor Gotlibovych, 2018


    Parameters
    ----------
    x : ndarray
        1-D array on which to find peaks
    scale : int, optional
        specify maximum scale window size of (2 * scale + 1)
    debug : bool, optional
        if set to True, the Local Scalogram Matrix, `LSM`, and scale with most local maxima, `l`,
        are returned together with peak locations

    Returns
    -------
    pks: ndarray
        The ordered array of peak indices found in `x`
    """
    x = detrend(x)
    N = len(x)
    L = N // 2
    if scale:
        L = min(scale, L)

    # create LSM matix
    LSM = np.zeros((L, N), dtype=bool)
    for k in np.arange(1, L):
        LSM[k-1, k:N-k] = (x[0:N-2*k] < x[k:N-k]) & (x[k:N-k] > x[2*k:N])

    # Find scale with most maxima
    G = LSM.sum(axis=1)
    l = np.argmax(G)

    # find peaks that persist on all scales up to l
    pks_logical = np.min(LSM[0:l, :], axis=0)
    pks = np.nonzero(pks_logical)
    if debug:
        return pks, LSM, l
    return pks
