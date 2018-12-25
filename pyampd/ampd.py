import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import detrend


def find_peaks_original(x, scale=None, debug=False):
    """Find peaks in quasi-periodic noisy signals using AMPD algorithm.

    Automatic Multi-Scale Peak Detection originally proposed in
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
        if set to True, return the Local Scalogram Matrix, `LSM`,
        and scale with most local maxima, `l`,
        together with peak locations

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
        LSM[k - 1, k:N - k] = (
            (x[0:N - 2 * k] < x[k:N - k]) & (x[k:N - k] > x[2 * k:N])
        )

    # Find scale with most maxima
    G = LSM.sum(axis=1)
    l_scale = np.argmax(G)

    # find peaks that persist on all scales up to l
    pks_logical = np.min(LSM[0:l_scale, :], axis=0)
    pks = np.flatnonzero(pks_logical)
    if debug:
        return pks, LSM, l_scale
    return pks


def find_peaks(x, scale=None, debug=False):
    """Find peaks in quasi-periodic noisy signals using AMPD algorithm.

    Extended implementation handles peaks near start/end of the signal.

    Optimized implementation by Igor Gotlibovych, 2018


    Parameters
    ----------
    x : ndarray
        1-D array on which to find peaks
    scale : int, optional
        specify maximum scale window size of (2 * scale + 1)
    debug : bool, optional
        if set to True, return the Local Scalogram Matrix, `LSM`,
        weigted number of maxima, 'G',
        and scale at which G is maximized, `l`,
        together with peak locations

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
    LSM = np.ones((L, N), dtype=bool)
    for k in np.arange(1, L + 1):
        LSM[k - 1, 0:N - k] &= (x[0:N - k] > x[k:N]
                                )  # compare to right neighbours
        LSM[k - 1, k:N] &= (x[k:N] > x[0:N - k])  # compare to left neighbours

    # Find scale with most maxima
    G = LSM.sum(axis=1)
    G = G * np.arange(
        N // 2, N // 2 - L, -1
    )  # normalize to adjust for new edge regions
    l_scale = np.argmax(G)

    # find peaks that persist on all scales up to l
    pks_logical = np.min(LSM[0:l_scale, :], axis=0)
    pks = np.flatnonzero(pks_logical)
    if debug:
        return pks, LSM, G, l_scale
    return pks


def find_peaks_adaptive(x, window=None, debug=False):
    """Find peaks in quasi-periodic noisy signals using ASS-AMPD algorithm.

    Adaptive Scale Selection Automatic Multi-Scale Peak Detection,
    an extension of AMPD -
    "An Efficient Algorithm for Automatic Peak Detection in
    Noisy Periodic and Quasi-Periodic Signals", Algorithms 2012, 5, 588-603
    https://doi.org/10.1109/ICRERA.2016.7884365

    Optimized implementation by Igor Gotlibovych, 2018


    Parameters
    ----------
    x : ndarray
        1-D array on which to find peaks
    window : int, optional
        sliding window size for adaptive scale selection
    debug : bool, optional
        if set to True, return the Local Scalogram Matrix, `LSM`,
        and `adaptive_scale`,
        together with peak locations

    Returns
    -------
    pks: ndarray
        The ordered array of peak indices found in `x`

    """
    x = detrend(x)
    N = len(x)
    if not window:
        window = N
    if window > N:
        window = N
    L = window // 2

    # create LSM matix
    LSM = np.ones((L, N), dtype=bool)
    for k in np.arange(1, L + 1):
        LSM[k - 1, 0:N - k] &= (x[0:N - k] > x[k:N]
                                )  # compare to right neighbours
        LSM[k - 1, k:N] &= (x[k:N] > x[0:N - k])  # compare to left neighbours

    # Create continuos adaptive LSM
    ass_LSM = uniform_filter1d(LSM * window, window, axis=1, mode='nearest')
    normalization = np.arange(L, 0, -1)  # scale normalization weight
    ass_LSM = ass_LSM * normalization.reshape(-1, 1)

    # Find adaptive scale at each point
    adaptive_scale = ass_LSM.argmax(axis=0)

    # construct reduced LSM
    LSM_reduced = LSM[:adaptive_scale.max(), :]
    mask = (np.indices(LSM_reduced.shape)[0] > adaptive_scale
            )  # these elements are outside scale of interest
    LSM_reduced[mask] = 1

    # find peaks that persist on all scales up to l
    pks_logical = np.min(LSM_reduced, axis=0)
    pks = np.flatnonzero(pks_logical)
    if debug:
        return pks, ass_LSM, adaptive_scale
    return pks
