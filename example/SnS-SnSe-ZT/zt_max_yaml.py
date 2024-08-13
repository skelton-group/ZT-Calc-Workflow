# zt_max_yaml.py


""" In this example, we determine the ZT_max from ZT calculations on p- and
n-type Pnma SnS and SnSe at temperatures around the Pnma -> Cmcm transition T
and write the data to a YAML file.

The calculation combines data from multiple papers:

    Approximate models for the lattice thermal conductivity of alloy
        thermoelectrics
    J. M. Skelton
    J. Mater. Chem. C 9 (35), 11772 (2021), DOI: 10.1039/D1TC02026A

    Thermoelectric Properties of Pnma and Rocksalt SnS and SnSe
    J. M. Flitcroft, I. Pallikara and J. M. Skelton
    Solids 3 (1), 155-176 (2022), DOI: 10.3390/solids3010011
    
    Thermoelectric properties of Pnma and R3m GeS and GeSe
    M. Zhang, J. Flictroft, S. Guillemot and J. Skelton
    J. Mater. Chem. C 11, 14833 (2023, DOI: 10.1039/D3TC02938G
"""


from zt_calc_workflow.amset import read_amset_csv
from zt_calc_workflow.analysis import get_zt_max
from zt_calc_workflow.dataset import zt_dataset_from_data
from zt_calc_workflow.phono3py import read_phono3py_kappa_csv



if __name__ == "__main__":
    # Load AMSET and Phono3py calculations and create ZT datasets.
    
    input_files = {'SnS': (r"SnS-Pnma-AMSET-p.csv", r"SnS-Pnma-AMSET-n.csv",
                          r"SnS-kappa-m16816.Prim.csv"),
                   'SnSe': (r"SnSe-Pnma-AMSET-p.csv", r"SnSe-Pnma-AMSET-n.csv",
                            r"SnSe-kappa-m16816.Prim.csv")}
    
    zt_data = {}
    
    for k, (amset_p, amset_n, kappa) in input_files.items():
        kappa_data = read_phono3py_kappa_csv(kappa)
        
        # The Phono3py calculations were performed on structures with the axes
        # oriented differently to those in the AMSET calculations. We deal with
        # this by dropping the off-diagonal elements and relabelling the
        # diagonal elements in kappa_data.
        
        kappa_data.drop(columns=['kappa_yz', 'kappa_xz', 'kappa_xy'],
                        inplace=True)
        
        kappa_data.columns = ['t', 'kappa_yy', 'kappa_zz', 'kappa_xx',
                              'kappa_ave']
        
        amset_data_p = read_amset_csv(amset_p)
        amset_data_n = read_amset_csv(amset_n)
        
        zt_data[k] = (zt_dataset_from_data(amset_data_p, kappa_data),
                      zt_dataset_from_data(amset_data_n, kappa_data))
    
    # Get ZT_max for each system and n/p-type doping and write to a YAML file.
    
    with open(r"zt_max.yaml", 'w') as f:
        for system, t_max in ('SnS', 880.), ('SnSe', 800.):
            p_data, n_data = zt_data[system]
            
            for doping_type, data in ('p', p_data), ('n', n_data):
                rec = get_zt_max(data, t_max=t_max)
                
                f.write("- system: {0}\n".format("{0}-Pnma".format(system)))
                f.write("  carrier_type: {0}\n".format(doping_type))
                
                f.write("  carrier_conc: {0}\n".format(rec['n']))
                f.write("  temp: {0}\n".format(rec['t']))
                
                data_k = []
                
                for k in rec.index:
                    if k.endswith('ave'):
                        data_k.append(k.replace('_ave', ''))

                for k in data_k:
                    f.write("  {0}:\n".format(k))

                    for suffix in 'xx', 'yy', 'zz', 'ave':
                        f.write("    {0}: {1}\n".format(
                                    suffix, rec['{0}_{1}'.format(k, suffix)]))
