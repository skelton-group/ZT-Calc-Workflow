# zt_calc_workflow/io.py

# ---------
# Docstring
# ---------

""" Routines for general I/O. """


# -------
# Imports
# -------

import pandas as pd


# ---------
# CSV files
# ---------

def read_validate_csv(file_path, header_map=None, known_headers=None,
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
