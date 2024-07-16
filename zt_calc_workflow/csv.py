# zt_calc_workflow/csv.py


# -------
# Imports
# -------

import warnings

import numpy as np
import pandas as pd


# -------
# Generic
# -------

def _read_validate_csv(file_path, header_map=None, known_headers=None,
                       known_headers_required=False):
    """ Read a CSV file into a Pandas DataFrame and optionally update headers
    with header_map and check headers against known_headers. """

    df = pd.read_csv(file_path)

    # Rename columns.

    if header_map is not None:
        df.rename(columns=header_map, inplace=True)

    # Check for unexpected column headers.

    if known_headers is not None:
        for h in df.columns:
            if h not in known_headers:
                raise Exception("Unknown column header '{0}'.".format(h))

        if known_headers_required:
            for h in known_headers:
                if h not in df.columns:
                    raise Exception("Required column '{0}' missing.".format(h))

    return df


# ----------
# Phono(3)py
# ----------

_READ_PHONO3PY_KAPPA_HEADER_MAP = {
    'T [K]': 't', 'k_xx [W/m.K]': 'kappa_xx', 'k_yy [W/m.K]': 'kappa_yy',
    'k_zz [W/m.K]': 'kappa_zz', 'k_yz [W/m.K]': 'kappa_yz',
    'k_xz [W/m.K]': 'kappa_xz', 'k_xy [W/m.K]': 'kappa_xy',
    'k_iso [W/m.K]': 'kappa_ave'}

_READ_PHONO3PY_KAPPA_KNOWN_HEADERS = list(
    _READ_PHONO3PY_KAPPA_HEADER_MAP.values())

def read_phono3py_kappa_csv(file_path):
    """ Read a CSV file generated with the phono3py-get-kappa script. """

    return _read_validate_csv(
        file_path, header_map=_READ_PHONO3PY_KAPPA_HEADER_MAP,
        known_headers=_READ_PHONO3PY_KAPPA_KNOWN_HEADERS,
        known_headers_required=True)

_READ_PHONO3PY_CRTA_HEADER_MAP = dict(_READ_PHONO3PY_KAPPA_HEADER_MAP, **{
    "(k/t)_xx [W/m.K.ps]": 'kappa_tau_crta_xx',
    "(k/t)_yy [W/m.K.ps]": 'kappa_tau_crta_yy',
    "(k/t)_zz [W/m.K.ps]": 'kappa_tau_crta_zz',
    "(k/t)_yz [W/m.K.ps]": 'kappa_tau_crta_yz',
    "(k/t)_xz [W/m.K.ps]": 'kappa_tau_crta_xz',
    "(k/t)_xy [W/m.K.ps]": 'kappa_tau_crta_xy',
    "(k/t)_iso [W/m.K.ps]": 'kappa_tau_crta_ave',
    "(t^CRTA)_xx [ps]": 'tau_crta_xx', "(t^CRTA)_yy [ps]": 'tau_crta_yy',
    "(t^CRTA)_zz [ps]": 'tau_crta_zz', "(t^CRTA)_yz [ps]": 'tau_crta_yz',
    "(t^CRTA)_xz [ps]": 'tau_crta_xz', "(t^CRTA)_xy [ps]": 'tau_crta_xy',
    "(t^CRTA)_iso [ps]": 'tau_crta_ave'})

_READ_PHONO3PY_CRTA_KNOWN_HEADERS = list(
    _READ_PHONO3PY_CRTA_HEADER_MAP.values())

def read_phono3py_crta_csv(file_path):
    """ Read a CSV file generated with the CRTA.py script. """

    return _read_validate_csv(
        file_path, header_map=_READ_PHONO3PY_CRTA_HEADER_MAP,
        known_headers=_READ_PHONO3PY_CRTA_KNOWN_HEADERS,
        known_headers_required=True)


# -----
# AMSET
# -----

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

def read_amset_csv(file_path, check_uniform=True, convert_sigma_s_cm=True,
                   recalculate_pf_mw_m_k2=True):
    """ Read a CSV file generated with Joe's AMSET code and, by default,
    perform some unit conversions. """

    df = _read_validate_csv(
        file_path, header_map=_READ_AMSET_HEADER_MAP,
        known_headers=_READ_AMSET_KNOWN_HEADERS, known_headers_required=False)

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

    if recalculate_pf_mw_m_k2:
        key_sets = [
            ('s_xx', 'sigma_xx', 'pf_xx'), ('s_yy', 'sigma_yy', 'pf_yy'),
            ('s_zz', 'sigma_zz', 'pf_zz'), ('s_ave', 'sigma_ave', 'pf_ave')]

        for k_s, k_sigma, k_pf in key_sets:
            df.loc[:, k_pf] = 1.0e3 * ((1.0e-6 * df[k_s].to_numpy()) ** 2
                                       * df[k_sigma].to_numpy())
    else:
        warnings.warn(
            "recalculate_pf_mw_m_k2 is set to False - other functions not "
            "work as expected if data is in different units.", UserWarning)

    # If requested, convert \sigma from S/m -> S/cm.

    if convert_sigma_s_cm:
        for k in 'sigma_xx', 'sigma_yy', 'sigma_zz', 'sigma_ave':
            df.loc[:, k] = df[k].to_numpy() / 100.0
    else:
        warnings.warn(
            "convert_sigma_s_cm is set to False - other functions not work as "
            "expected if data is in different units.", UserWarning)

    return df


# --------
# Combined
# --------

def zt_dataset_from_data(amset_data, phono3py_kappa_data):
    """ Combine electrical properties from amset and lattice thermal
    conductivity from Phono3py to create a new Pandas DataFrame with the AMSET
    data plus additional 'kappa_latt_*', 'kappa_tot_*' and 'zt_*' fields. """

    amset_t = amset_data['t'].unique()
    phono3py_t = phono3py_kappa_data['t'].to_numpy()

    # Check temperatures in AMSET calculation are covered by the Phono3py
    # calculation.

    for t in amset_t:
        if t not in phono3py_t:
            raise Exception("Phono3py calculation must cover the temperature "
                            "range of the AMSET calculation.")

    zt_data = amset_data.copy()

    # Append \kappa_latt columns to ZT data.

    kl_cols = [[] for _ in range(4)]

    for t in zt_data['t']:
        (loc, ), = np.where(phono3py_t == t)

        for i, k in enumerate(
                ['kappa_xx', 'kappa_yy', 'kappa_zz', 'kappa_ave']):
            kl_cols[i].append(phono3py_kappa_data.loc[loc, k])

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

def zt_dataset_from_files(amset_file, phono3py_kappa_file):
    """ Reads an AMSET and Phono3py file and return a ZT dataset from
    zt_dataset_from_data(). """

    amset_data = read_amset_csv(amset_file, convert_sigma_s_cm=True,
                                recalculate_pf_mw_m_k2=True)

    phono3py_kappa_data = read_phono3py_kappa_csv(phono3py_kappa_file)

    return zt_dataset_from_data(amset_data, phono3py_kappa_data)
