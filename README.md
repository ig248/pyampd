[![PyPI version](https://badge.fury.io/py/pyampd.svg)](https://badge.fury.io/py/pyampd)
[![Build Status](https://travis-ci.com/ig248/pyampd.svg?branch=master)](https://travis-ci.com/ig248/pyampd)
[![Coverage Status](https://codecov.io/gh/ig248/pyampd/branch/master/graph/badge.svg)](https://codecov.io/gh/ig248/pyampd)

# AMPD algorithm in Python
Implements a function `find_peaks` based on the Automatic Multi-scale
Peak Detection algorithm proposed by Felix Scholkmann et al. in
"An Efficient Algorithm for Automatic Peak Detection in
Noisy Periodic and Quasi-Periodic Signals", Algorithms 2012,
 5, 588-603

![Peak finding](https://raw.githubusercontent.com/ig248/pyampd/master/ass_ampd.png)

## Usage
Install from PyPI:

```
pip install pyampd
```

Or install from source:

```
pip install git+https://github.com/ig248/pyampd
```

Import function:

```python
from pyampd.ampd import find_peaks
```

See `notebooks/ampd.ipynb` for usage examples.

### Specifying maximum scale
To improve run-time on large time-series, it is possible to specify the maximum scale to consider:
```python
peaks = find_peaks(x, scale=100)
```
will only consider windows up to +-100 point either side of peak candidates.

### Adaptive Scale Selection
If the characteristic scale of the signal changes over time, a new algorithm called
Adaptive Scale Selection can track the changes in optimal scales and detect peaks accordingly:
```python
peaks = find_peaks_adaptive(x, window=200)
```
will select the optimal scale at each point using a 200-point running window.


### Original implementation
`find_peaks` is not identical to the algorithm proposed in the original paper (especially near start and end of time series).
 A performance-optimized version of the original implementation is provided in `find_peaks_original`.


## Tests
Run
```bash
pytest
```

## Other implementations
- R: https://cran.r-project.org/web/packages/ampd/index.html
- MATLAB: https://github.com/mathouse/AMPD-algorithm
- Python: https://github.com/LucaCerina/ampdLib

## Improvements
This Python implementation provides significant speed-ups in two areas:
1. Efficient tracking of local minima without using random numbers
2. Introduction of maximum window size, reducing algorithm run-time from
quadratic to linear in the number of samples.
3. Better handling of peaks near start/end of the series
4. Addition of new Adaptive Scale Selection 

## ToDo
- It may be possible to avoid repeated comparisons, and reduce worst-case
runtime from `O(n^2)` to `O(n log(n))`.
- `find_peaks_adaptive` could benefit from specifying both `window` and `max_scale`

## References
Original paper: https://doi.org/10.1109/ICRERA.2016.7884365
