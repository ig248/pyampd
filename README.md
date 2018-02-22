# AMPD algorithm in Python
Implements a function `find_peaks_ampd` based on the Automatic Multi-scale
Peak Detection algorithm proposed by Felix Scholkmann et al. in
"An Efficient Algorithm for Automatic Peak Detection in
Noisy Periodic and Quasi-Periodic Signals", Algorithms 2012,
 5, 588-603

## Usage
Copy `ampd.py` to your folder, and add it to your imports:
```python
from ampd import find_peaks_ampd
```

See `ampd.ipynb` for usage examples.

## Previous implementations
- R: https://cran.r-project.org/web/packages/ampd/index.html
- MATLAB: https://github.com/mathouse/AMPD-algorithm
- Python: https://github.com/LucaCerina/ampdLib

## Improvements
This Python implementation provides significant speed-ups in two areas:
1. Efficient tracking of local minima without using random numbers
2. Introduction of maximum window size, reducing algorithm run-time from
quadratic to linear in the number of samples.

## ToDo
It may be possible to avoid repeated comparisons, and reduce worst-case
runtime from `O(n^2)` to `O(n log(n))`.

## References
Original paper: https://doi.org/10.1109/ICRERA.2016.7884365
