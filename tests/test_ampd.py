import numpy as np
import numpy.testing as npt
import pytest

from pyampd.ampd import find_peaks, find_peaks_adaptive


def _gen_gaussian_peaks(len=100, locs=[50], sigma=1):
    """timeseries with `len` samples and peaks of width `sigma` at `locs`"""
    t = np.arange(len)
    x = np.zeros((len, ))
    for loc in locs:
        peak = np.exp(-(t - loc) ** 2 / (2 * sigma ** 2))
        x += peak
    return x


def signal_simple():
    len = 101
    delta = 10
    sigma = 2
    locs = np.arange(delta, len - 1, delta)
    x = _gen_gaussian_peaks(len, locs, sigma)
    peaks = locs
    return x, peaks


def signal_with_endpoints():
    len = 101
    delta = 10
    sigma = 2
    locs = np.arange(0, len + 1, delta)
    x = _gen_gaussian_peaks(len, locs, sigma)
    peaks = locs
    return x, peaks


def signal_multiscale():
    locs = np.hstack([
        np.arange(0, 100, 10),
        np.arange(100, 400, 30),
    ])
    len = locs[-1] + 1
    x = _gen_gaussian_peaks(len, locs, sigma=2)
    peaks = locs
    return x, peaks


@pytest.mark.parametrize('scale', [None, 100])
@pytest.mark.parametrize('signal', [signal_simple, signal_with_endpoints])
def test_ampd(signal, scale):
    x, known_peaks = signal()
    peaks = find_peaks(x, scale=scale)
    npt.assert_array_equal(peaks, known_peaks)


@pytest.mark.parametrize(
    'signal, window', [
        (signal_simple, None), (signal_with_endpoints, None),
        (signal_simple, 100), (signal_with_endpoints, 100),
        (signal_multiscale, 100)
    ]
)
def test_ass_ampd(signal, window):
    x, known_peaks = signal()
    peaks = find_peaks_adaptive(x, window=window)
    npt.assert_array_equal(peaks, known_peaks)


if __name__ == '__main__':
    pytest.main()
