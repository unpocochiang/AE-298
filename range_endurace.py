import numpy as np

def prop_range_calc(v, ld, takeoff_weight, fuel_weight, sfc):
    prop_eff = 0.8
    sfc = sfc / 3600
    R = prop_eff / sfc * ld * np.log(takeoff_weight / fuel_weight)
    return R

#possible usage
# def prop_aircraft_range():
#     R = v / c * ld * np.log(takeoff_weight / fuel_weight)

def jet_endurance_calc(ld, takeoff_weight, fuel_weight, sfc):
    TSFC = sfc/3600
    E = ld/TSFC*np.log(takeoff_weight/(takeoff_weight-fuel_weight))
    return E
 
def jet_range_calc(CL, CD, rho, S, takeoff_weight, fuel_weight, sfc):
    TSFC = sfc/3600
    R = 2*np.sqrt(2/rho/S) / TSFC * np.sqrt(CL) / CD * (np.sqrt(takeoff_weight) - np.sqrt(takeoff_weight-fuel_weight))
    return R

def prop_endurance_calc(v, rho, S, CL, CD, takeoff_weight, fuel_weight, sfc):
    prop_eff = 0.8
    sfc = sfc / 3600
    E = prop_eff / sfc * CL**(3/2) / CD * np.sqrt(rho*S*2) * ((takeoff_weight-fuel_weight)**(-0.5) - (takeoff_weight)**(-0.5))
    return E