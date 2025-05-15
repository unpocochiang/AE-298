import numpy as np

def prop_range_calc(v, ld, takeoff_weight, fuel_weight, engine_type):
    prop_eff = 0.8
    
    if engine_type.lower() == "turboprop":
        cbhp = 0.5
    elif engine_type.lower() == "piston prop":
        cbhp = 0.4
    else:
        raise ValueError("Unknown engine type. Use 'turboprop' or 'piston prop'.")
    
    c = cbhp * v / (550 * prop_eff) #ft/(ft*lb/s)(s) 
    R = v / c * ld * np.log(takeoff_weight / fuel_weight) * 3600
    return R

#possible usage
# def prop_aircraft_range():
#     R = v / c * ld * np.log(takeoff_weight / fuel_weight)

def jet_endurance_calc(ld, takeoff_weight, fuel_weight, engine_type):
    
    if engine_type.lower() == "turboprop":
        TSFC = 0.14/60/60 #hr
    elif engine_type.lower() == "high-bypass-turbofan":
        TSFC = 0.6/60/60
    elif engine_type.lower() == "Afterburning-turbofan":
        TSFC = 0.4/60/60
    else:
        raise ValueError("Unknown engine type. Use 'turboprop' or 'piston prop'.") 
    E = ld/TSFC*np.log(takeoff_weight/(takeoff_weight-fuel_weight))
    return E
 
def jet_range_calc(CL, CD, rho, S, takeoff_weight, fuel_weight, engine_type):
    if engine_type.lower() == "turboprop":
        TSFC = 0.14/60/60
    elif engine_type.lower() == "high-bypass-turbofan":
        TSFC = 0.6/60/60
    elif engine_type.lower() == "afterburning-turbofan":
        TSFC = 0.4/60/60
    elif engine_type.lower() == "piston":
        TSFC = 0.5/60/60
    else:
        raise ValueError("Unknown engine type. Use 'turboprop', 'high-bypass-turbofan', 'afterburning-turbofan', or 'piston'.") 
    
    R = 2*np.sqrt(2/rho/S) / TSFC * np.sqrt(CL) / CD * (np.sqrt(takeoff_weight) - np.sqrt(takeoff_weight-fuel_weight))
    return R

def prop_endurance_calc(v, rho, S, CL, CD, takeoff_weight, fuel_weight, engine_type):
    prop_eff = 0.8

    if engine_type.lower() == "turboprop":
        cbhp = 0.5
    elif engine_type.lower() == "piston":
        cbhp = 0.4
    else:
        raise ValueError("Unknown engine type. Use 'turboprop' or 'piston prop'.")
    
    c = cbhp * v / (550 * prop_eff) #ft/(ft*lb/s)(s) 
    E = prop_eff / c * CL**(3/2) / CD * np.sqrt(rho*S/2) * (np.sqrt(takeoff_weight-fuel_weight) - np.sqrt(takeoff_weight))
    return E