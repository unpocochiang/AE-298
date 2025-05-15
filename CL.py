import numpy as np
import pandas as pd
import airfoil
import os

def total_cl_calc (sweep,AR,re,airfoil_name):
    e = 0
    if sweep == 0:
        e = (1.78 * (1-0.045*AR**0.68))/AR**0.64
    else:
        e = (4.61 * (1-0.045*AR**0.68))/AR**0.84
    sweep_rad = sweep * np.pi / 180
    
    re_list = [50000, 100000, 200000, 500000, 1000000]
    closest = min(re_list, key=lambda x: abs(x - re))
    
    filename = os.path.join('airfoils', f'{airfoil_name}_{closest}.csv')
    if not os.path.exists(filename):
        airfoil.airfoil_data(airfoil_name, re)  # make sure this generates the correct file

    df = pd.read_csv(filename)
    exact_match = df[df["Alpha"] == 0]
    if not exact_match.empty:
        cl_2d = float(exact_match["Cl"].values[0])
    else :
        lower = df[df["Alpha"] < 0].iloc[-1] if not df[df["Alpha"] < 0].empty else None
        upper = df[df["Alpha"] > 0].iloc[0] if not df[df["Alpha"] > 0].empty else None
        # Linear interpolation
        alpha1, cl1 = lower["Alpha"], lower["Cl"]
        alpha2, cl2 = upper["Alpha"], upper["Cl"]

        cl_2d = cl1 + (0 - alpha1) * (cl2 - cl1) / (alpha2 - alpha1)
        
    #print(f'cl_2d: {cl_2d}')
    cl = cl_2d*np.cos(sweep_rad)/(1+(cl_2d*np.cos(sweep_rad))/(np.pi*e*AR))
    #print(f'cl: {cl}')
    return cl