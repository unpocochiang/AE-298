import sympy as sp
from sympy import Symbol

def flat_plate_area_calc(takeoff_weight,config):
    #tricycle config is 1
    #conventional config is 2 
    #Bicyle and outrigger config is 3
    x = sp.symbols('x')
    tricycle_eq = 4.47+0.393*x-(6.91*(10**-4))*x**2
    convetional_eq = 2.31+0.328*x-(4.59*(10**-4))*x**2
    outrigger_eq = 10.7+0.27*x-(1.12*(10**-3))*x**2+(2.95*(10**-6))*x**3-(3.14*(10**-4))*x**4
    flate_plate_area = 0
    if config == 1:
        #if takeoff_weight >= 28.451 and takeoff_weight <= 248.732:
        flate_plate_area = tricycle_eq.subs(x,takeoff_weight)
    if config == 2:
        #if takeoff_weight >= 34.648 and takeoff_weight <= 247.606:
        flate_plate_area = convetional_eq.subs(x,takeoff_weight)
    if config == 3:
        #if takeoff_weight >= 152.394 and takeoff_weight <= 395.775:
        flate_plate_area = outrigger_eq.subs(x,takeoff_weight)
    return flate_plate_area

def cd_lg(flat_plate_area, front_surface_area):
    cd_lg_val = flat_plate_area/front_surface_area
    return cd_lg_val