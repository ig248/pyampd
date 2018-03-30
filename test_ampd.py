import pytest
import numpy as np
import numpy.testing as npt
from ampd import find_peaks_ampd, find_peaks_ass_ampd


def _gen_gaussian_peaks(len=100, locs=[50], sigma=1):
    """timeseries with `len` samples and peaks of width `sigma` at `locs`"""
    t = np.arange(len)
    x = np.zeros((len,))
    for loc in locs:
        peak = np.exp(-(t-loc)**2/(2*sigma**2))
        x += peak
    return x


def test_ampd():
    len = 101
    delta = 10
    locs = np.arange(delta, len, delta)
    sigma = 2
    t = np.arange(len)
    x = _gen_gaussian_peaks(len, locs, sigma)
    peaks = find_peaks_ampd(x)
    peak_locs = t[peaks]
    npt.assert_array_equal(locs, peak_locs)


def test_ampd_endpoints():
    """include cut-off peaks at endpoints"""
    len = 101
    delta = 10
    locs = np.arange(0, len+1, delta)
    sigma = 2
    t = np.arange(len)
    x = _gen_gaussian_peaks(len, locs, sigma)
    peaks = find_peaks_ampd(x)
    peak_locs = t[peaks]
    npt.assert_array_equal(locs, peak_locs)


def test_ass_ampd():
    locs = np.hstack([
        np.arange(0, 100, 10),
        np.arange(100, 400, 30),
    ])
    len = locs[-1] + 1
    t = np.arange(len)
    x = _gen_gaussian_peaks(len, locs, sigma=2)
    peaks = find_peaks_ass_ampd(x, window=100)
    peak_locs = t[peaks]
    npt.assert_array_equal(locs, peak_locs)


if __name__ == '__main__':
    pytest.main()
