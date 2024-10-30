# zt_calc_workflow/dataset.py


# ---------
# Docstring
# ---------

""" Routines for building and working with datasets. """


# -------
# Imports
# -------

import numpy as np


from .amset import read_amset_csv
from .phono3py import read_phono3py_kappa_csv


# ----------------
# Dataset creation
# ----------------

def zt_dataset_from_data(elec_prop_data, kappa_latt_data):
    """ Combine electrical properties and lattice thermal conductivity data
    to create a new Pandas DataFrame with a ZT dataset. The new DataFrame
    has the same fields as elec_prop_data plus 'kappa_latt_*', 'kappa_tot_*'
    and 'zt_*' fields. """

    elec_t = elec_prop_data['t'].unique()
    kappa_latt_t = kappa_latt_data['t'].to_numpy()

    # Check temperatures in AMSET calculation are covered by the Phono3py
    # calculation.

    for t in elec_t:
        if t not in kappa_latt_t:
            raise Exception("Phono3py calculation must cover the temperature "
                            "range of the AMSET calculation.")

    zt_data = elec_prop_data.copy()

    # Append \kappa_latt columns to ZT data.

    kl_cols = [[] for _ in range(4)]

    for t in zt_data['t']:
        (loc, ), = np.where(kappa_latt_t == t)

        for i, k in enumerate(
                ['kappa_xx', 'kappa_yy', 'kappa_zz', 'kappa_ave']):
            kl_cols[i].append(kappa_latt_data.loc[loc, k])

    kl_keys = ['kappa_latt_xx', 'kappa_latt_yy', 'kappa_latt_zz', 'kappa_latt_ave']

    for k, col in zip(kl_keys, kl_cols):
        zt_data[k] = col

    # Calculate and append \kappa_tot columns to AMSET data.

    key_sets = [('kappa_el_xx', 'kappa_latt_xx', 'kappa_tot_xx'),
                ('kappa_el_yy', 'kappa_latt_yy', 'kappa_tot_yy'),
                ('kappa_el_zz', 'kappa_latt_zz', 'kappa_tot_zz'),
                ('kappa_el_ave', 'kappa_latt_ave', 'kappa_tot_ave')]

    for k_el, k_latt, k_tot in key_sets:
        zt_data[k_tot] = zt_data[k_el] + zt_data[k_latt]

    # Calculate and append ZT columns to AMSET data.

    key_sets = [('pf_xx', 'kappa_tot_xx', 'zt_xx'),
                ('pf_yy', 'kappa_tot_yy', 'zt_yy'),
                ('pf_zz', 'kappa_tot_zz', 'zt_zz'),
                ('pf_ave', 'kappa_tot_ave', 'zt_ave')]

    for k_pf, k_kappa, k_zt in key_sets:
        zt_data[k_zt] = (
            ((1.0e-3 * zt_data[k_pf]) / zt_data[k_kappa]) * zt_data['t'])

    return zt_data

def zt_dataset_from_amset_phono3py_csvs(amset_file, phono3py_kappa_file):
    """ Reads an AMSET CSV and Phono3py kappa CSV file and return a ZT dataset
    from zt_dataset_from_data(). """

    elec_prop_data = read_amset_csv(amset_file, convert_sigma_s_cm=True,
                                    calculate_pf_mw_m_k2=True)

    kappa_latt_data = read_phono3py_kappa_csv(phono3py_kappa_file)

    return zt_dataset_from_data(elec_prop_data, kappa_latt_data)


# -------------------
# 1D -> 2D conversion
# -------------------

def dataset_to_2d(data):
    """ Convert a dataset as a Pandas DataFrame to a set of n and T values and
    a dictionary of 2D NumPy arrays for each data column.
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
