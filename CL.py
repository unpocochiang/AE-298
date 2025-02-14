import numpy as np
import pandas as pd

def cl_calc (cl_2d,sweep,AR,re,airfoil_name):
    if sweep == 0:
        e = (1.78(1-0.045*AR**0.68))/AR**0.64
    else:
        e = (4.61(1-0.045*AR**0.68))/AR**0.84
    sweep_rad = sweep * np.pi / 180

    filename = f'{airfoil_name}_{re}.csv'
    df = pd.read_csv(filename)
    cl_2d = df.loc[df['Alpha'] == 0, 'Cl'].values

    cl = cl_2d*np.cos(sweep_rad)/(1+(cl_2d*np.cos(sweep_rad))/(np.pi*e*AR))
    return cl