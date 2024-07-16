# zt_calc_workflow/phono3py.py


# ---------
# Docstring
# ---------

""" Routines for working with Phono(3)py calculations. """


# -------
# Imports
# -------

from .io import read_validate_csv


# ---------
# CSV files
# ---------

_READ_PHONO3PY_KAPPA_HEADER_MAP = {
    'T [K]': 't', 'k_xx [W/m.K]': 'kappa_xx', 'k_yy [W/m.K]': 'kappa_yy',
    'k_zz [W/m.K]': 'kappa_zz', 'k_yz [W/m.K]': 'kappa_yz',
    'k_xz [W/m.K]': 'kappa_xz', 'k_xy [W/m.K]': 'kappa_xy',
    'k_iso [W/m.K]': 'kappa_ave'}

_READ_PHONO3PY_KAPPA_KNOWN_HEADERS = list(
    _READ_PHONO3PY_KAPPA_HEADER_MAP.values())

def read_phono3py_kappa_csv(file_path):
    """ Read a CSV file generated with the phono3py-get-kappa script. """

    return read_validate_csv(
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

    return read_validate_csv(
        file_path, header_map=_READ_PHONO3PY_CRTA_HEADER_MAP,
        known_headers=_READ_PHONO3PY_CRTA_KNOWN_HEADERS,
        known_headers_required=True)
