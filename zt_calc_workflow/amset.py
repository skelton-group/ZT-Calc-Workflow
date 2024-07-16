# zt_calc_workflow/io.py


# ---------
# Docstring
# ---------

""" Routines for working with AMSET calculations. """


# -------
# Imports
# -------

import warnings

import numpy as np

from .io import read_validate_csv


# ------------------
# Internal functions
# ------------------

def _check_update_amset_dataset(
        df, check_uniform=True, convert_sigma_s_cm=True,
        calculate_pf_mw_m_k2=True):
    """ Check and an AMSET dataset in the form of a Pandas DataFrame:
    
    * sort the dataset by carrier concentration and then by temperature;
    * check the dataset has a uniform set of n and T;
    * convert the electrical conductivity from S m^-1 to S cm^-1; and
    * (re)calculate the power factors in mW m^-1 K^-2.
    """
    
    # Sort by n, then T.

    df.sort_values(by=['n', 't'], inplace=True)

    # Check for uniform n and temperatures.

    if check_uniform:
        t_vals = sorted(df['t'].unique())
        n_vals = sorted(df['n'].unique())
    
        for n in n_vals:
            t_check = df[df['n'] == n]['t'].unique()
    
            if len(t_check) != len(t_vals):
                raise Exception("Incomplete set of temperatures for n = "
                                "{1:.3e}".format(n))
    
            if not np.allclose(t_vals, sorted(t_check)):
                raise Exception("Inconsistent set of temperatures for n = "
                                "{1:.3e}".format(n))
    else:
        warnings.warn("check_uniform is set to False - other functions may "
                      "not work as expected on non-uniform data.", UserWarning)

    # If requested, recalculate PFs in mW/m.K^2.

    has_pf = ('pf_xx' in df.columns and 'pf_yy' in df.columns
              and 'pf_zz' in df.columns and 'pf_ave' in df.columns)

    if calculate_pf_mw_m_k2 or not has_pf:
        key_sets = [
            ('s_xx', 'sigma_xx', 'pf_xx'), ('s_yy', 'sigma_yy', 'pf_yy'),
            ('s_zz', 'sigma_zz', 'pf_zz'), ('s_ave', 'sigma_ave', 'pf_ave')]

        for k_s, k_sigma, k_pf in key_sets:
            df.loc[:, k_pf] = 1.0e3 * ((1.0e-6 * df[k_s].to_numpy()) ** 2
                                       * df[k_sigma].to_numpy())
    else:
        warnings.warn(
            "calculate_pf_mw_m_k2 is set to False - other functions may not "
            "work as expected if data is in different units.", UserWarning)

    # If requested, convert \sigma from S/m -> S/cm.

    if convert_sigma_s_cm:
        for k in 'sigma_xx', 'sigma_yy', 'sigma_zz', 'sigma_ave':
            df.loc[:, k] = df[k].to_numpy() / 100.0
    else:
        warnings.warn(
            "convert_sigma_s_cm is set to False - other functions may not "
            "work as expected if data is in different units.", UserWarning)
    
    return df


# ---------
# CSV files
# ---------

_READ_AMSET_HEADER_MAP = {
    'Carrier Concentration': 'n', 'Temperature': 't',
    'Conducitivty x': 'sigma_xx', 'Conducitivty y': 'sigma_yy',
    'Conducitivty z': 'sigma_zz', 'Conducitivty ave': 'sigma_ave',
    'Seebeck x': 's_xx', 'Seebeck y': 's_yy', 'Seebeck z': 's_zz',
    'Seebeck ave': 's_ave', 'Kele x': 'kappa_el_xx', 'Kele y': 'kappa_el_yy',
    'Kele z': 'kappa_el_zz', 'Kele ave': 'kappa_el_ave', 'Mobility x': 'mu_xx',
    'Mobility y': 'mu_yy', 'Mobility z': 'mu_zz', 'Mobility ave': 'mu_ave',
    'PF x': 'pf_xx', 'PF y': 'pf_yy', 'PF z': 'pf_zz', 'PF ave': 'pf_ave',
    'ADP': 'mu_adp_xx', 'ADP.1': 'mu_adp_yy', 'ADP.2': 'mu_adp_zz',
    'ADP.3': 'mu_adp_ave', 'IMP': 'mu_imp_xx', 'IMP.1': 'mu_imp_yy',
    'IMP.2': 'mu_imp_zz', 'IMP.3': 'mu_imp_ave', 'PIE': 'mu_pie_xx',
    'PIE.1': 'mu_pie_yy', 'PIE.2': 'mu_pie_zz', 'PIE.3': 'mu_pie_ave',
    'POP': 'mu_pop_xx', 'POP.1': 'mu_pop_yy', 'POP.2': 'mu_pop_zz',
    'POP.3': 'mu_pop_ave'}

_READ_AMSET_KNOWN_HEADERS = list(_READ_AMSET_HEADER_MAP.values())

def read_amset_csv(file_path, **kwargs):
    """ Read a CSV file generated with Joe's AMSET code and, by default,
    perform some checks and unit conversions. kwargs are passed to
    _check_update_amset_dataset(). """

    df = read_validate_csv(file_path, header_map=_READ_AMSET_HEADER_MAP,
                           known_headers=_READ_AMSET_KNOWN_HEADERS,
                           known_headers_required=False)
    
    return _check_update_amset_dataset(df, **kwargs)
