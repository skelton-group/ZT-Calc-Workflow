# zt_calc_workflow/utility.py


# -------
# Imports
# -------

import numpy as np


# ---------
# Functions
# ---------

def amset_or_zt_to_2d(data):
    """ Convert an AMSET or ZT dataset as a Pandas DataFrame to a set of n and
    T values and a dictionary containing a 2D NumPy array for each data column.
    """

    # Make sure data has 'n' (carrier concentration) and 't' (temperature) keys.

    assert 'n' in data.columns and 't' in data.columns

    # Make sure data is sorted.

    data = data.sort_values(by=['n', 't'])

    # Get n/T values.

    n_vals = data['n'].unique()
    t_vals = data['t'].unique()

    # Cast remaining columns into 2D arrays indexed by n (x) and T (y).

    shape = (len(n_vals), len(t_vals))

    data_2d = {}

    for k in data.columns:
        if k != 'n' and k != 't':
            arr = np.zeros(shape, dtype=np.float64)

            for i, n in enumerate(n_vals):
                arr[i, :] = data[data['n'] == n][k]

            data_2d[k] = arr

    return (n_vals, t_vals, data_2d)
