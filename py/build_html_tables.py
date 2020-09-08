""" Methods to generate the FRB and Host galaxy HTML tables"""

import pandas
import os
import numpy as np

from frb import frb
from frb.galaxies import frbgalaxy


def build_frbs(out_path='./html_tables'):
    # Load
    frbs_tbl, tbl_units = frb.build_table_of_frbs()

    # Properties for the Table
    frb_properties = dict(DM='DM_FRB', DMISM='DM_ISM', RM='RM_FRB')
    frb_prop = [item for key, item in frb_properties.items()]

    # Formatting
    frb_formats = dict(DM='.1f', DMISM='.1f', RM='.1f')

    # Loop me
    for frb_idx in range(len(frbs_tbl)):
        # Quantity to get us started
        frb_tbl = pandas.DataFrame(dict(Quantity=frb_prop))

        # The rest
        values, errors, units = [], [], []
        for key in frb_properties.keys():
            value = frbs_tbl.iloc[frb_idx][key]
            if key in frb_formats.keys():
                values.append(format(value, frb_formats[key]))
            else:
                raise IOError("You must add a format for {}!".format(key))
            # Error?
            if hasattr(frbs_tbl.iloc[frb_idx], key + '_err'):
                error = frbs_tbl.iloc[frb_idx][key + '_err']
                errors.append(format(error, frb_formats[key]))
            else:
                errors.append('--')
            # Unit
            units.append(tbl_units[key])

        # Add em in
        frb_tbl['Measured Value'] = values
        frb_tbl['Measured Error'] = errors
        frb_tbl['Units'] = units

        # To HTML and disk
        filename = os.path.join(out_path, frbs_tbl.iloc[frb_idx].FRB+'.html')
        frb_tbl.to_html(open(filename, 'w'))


def main(inflg='all', options=None):

    if inflg == 'all':
        flg = np.sum(np.array( [2**ii for ii in range(25)]))
    else:
        flg = int(inflg)

    # FRBs
    if flg & (2**0):
        build_frbs()

# Command line execution
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        flg = 0
        flg += 2**0   # FRB tables
        #flg_fig += 2**1   # FRB 190102
        #flg_fig += 2**16   # Check impacts
    else:
        flg = sys.argv[1]

    main(inflg=flg)
