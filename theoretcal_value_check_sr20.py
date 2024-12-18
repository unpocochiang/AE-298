import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol
import CDi_wing
import SR_20_data
import atmosphere_function
import SR_20_data
import CDo_wing
import CDo_vtail
import CDo_htail
import CDo_fus
import CDi_wing
import CD_misc
import CD_lg
import re_calc

def real_Cd_calc(alt, mach):
    weight = 2600 #lb
    h_G, h, T, P, rho, speed_of_sound,mu = atmosphere_function.AtmosphereFunction(alt)
    sref = SR_20_data.S_wing
    x = sp.symbols('x')
    cd = 0
    if alt == 2000:
        eq = 1.61 + -0.0347*x + 4.72E-04*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 127 and vel <= 160:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    if alt == 4000:
        eq = 4.26 + -0.103*x + 8.98e-4*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 131 and vel <= 159:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    if alt == 6000:
        eq = 10.9 - 0.284*x + 2.13e-3*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 134 and vel <= 159:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    if alt == 8000:
        eq = 6.35 -0.164*x + 1.32e-3*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 131 and vel <= 157:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    if alt == 10000:
        eq = -0.393 + 0.0201*x + 5.13e-5*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 134 and vel <= 155:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    if alt == 12000:
        eq = -1.39 + 0.0495*x + -1.74e-4*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 136 and vel <= 153:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    if alt == 14000:
        eq = -87.1 + 2.31*x + -0.015*x**2
        vel = mach * speed_of_sound
        vel = vel / 1.68780986 #change unit to knts
        if vel >= 142 and vel <= 151:
            vel_ms = vel * 0.5144
            thurst = eq.subs(x,vel_ms)
            thurst = thurst * 0.2248089431
            vel = mach * speed_of_sound
            cd = thurst*2/rho/vel/vel/sref
    return cd

def theoretical_Cd_calc(m,alt):
    altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(alt) 
    re = re_calc.re(density, 0.4, SR_20_data.c_bar, visc, temp) # float for each mach
            
    #span is b_wing
    #sweep is L_c_4_wing
            #vinf is true airspeed
            #sref and wref may be both s_wing
    vinf = m * speed_of_sound
    CDo_wing_val = CDo_wing.CDo_wing_calc(re, m, SR_20_data.L_c_4_wing, SR_20_data.tc_avg,SR_20_data.S_wing,SR_20_data.S_wet, SR_20_data.tc_max_loc,
                                                    SR_20_data.takeoff_weight,vinf,density,SR_20_data.tc_max,SR_20_data.c_tip,
                                                    SR_20_data.c_root,SR_20_data.S_wing,SR_20_data.b_wing)
    CDo_vtail_val = CDo_vtail.CDo_vtail(re, m, SR_20_data.L_c_4_v, SR_20_data.tc_max_loc_v, SR_20_data.tc_avg_v, SR_20_data.S_wing, SR_20_data.S_v_wet, 
                                                SR_20_data.takeoff_weight, vinf,density,SR_20_data.tc_max_v, SR_20_data.c_tip_v, SR_20_data.c_root_v, 
                                                    SR_20_data.S_wing #use S_wing now according to simulink, but I think it should be s_h 
                                                    , SR_20_data.b_v)
    CDo_htail_val = CDo_htail.CDo_htail(re,m, SR_20_data.L_c_4_h, SR_20_data.tc_max_loc_h, 
                                                SR_20_data.tc_avg_h, SR_20_data.S_wing, 
                                                SR_20_data.S_h_wet, SR_20_data.takeoff_weight, vinf, 
                                                SR_20_data.c_tip_h, SR_20_data.c_root_h, SR_20_data.b_h, 
                                                SR_20_data.S_wing, #use S_wing now according to simulink, but I think it should be s_h
                                                density, SR_20_data.tc_max_h)      
    CDo_fus_val = CDo_fus.CDo_fus(re,m, SR_20_data.l_fus, SR_20_data.d_fus, 
                                            SR_20_data.S_fus_wet, SR_20_data.S_wing,
                                            SR_20_data.S_fus_maxfront)  
    CDi_wing_val = CDi_wing.CDi_wing_calc(m, SR_20_data.AR, SR_20_data.L_c_4_wing, SR_20_data.taper, 
                                                    density, vinf, SR_20_data.rle, visc, SR_20_data.b_wing, 
                                                    SR_20_data.c_tip, SR_20_data.c_root, SR_20_data.c_l_alpha, 
                                                    SR_20_data.takeoff_weight, SR_20_data.S_wing)
    CDi_htail_val = CDi_wing.induced_drag_htail(SR_20_data.AR_h,SR_20_data.S_h,SR_20_data.S_wing,SR_20_data.takeoff_weight,
                                                        density,vinf,SR_20_data.S_wing)
    # might need to double check with ERJ-Data
    CDi_fus_val = CDi_wing.fuse_induced_drag(SR_20_data.c_l_0,SR_20_data.l_fus,SR_20_data.d_fus,m,SR_20_data.S_wing,
                                                        SR_20_data.S_fus_plan,SR_20_data.S_fus_b,
                                                        SR_20_data.takeoff_weight, density, vinf, SR_20_data.S_wing, 
                                                        SR_20_data.b_wing, SR_20_data.c_tip,
                                                        SR_20_data.c_root,SR_20_data.c_l_alpha,
                                                        SR_20_data.AR,SR_20_data.L_c_4_wing)
    # might need to double check with ERJ-Data
    CD_misc_cons = 0.05
    CDo_pyl = 0
    CDo_nac = 0
    CD_misc_val = CD_misc.CD_misc_calc(CDo_pyl,CDo_fus_val,CDo_wing_val,CDo_nac,CDo_vtail_val,CDo_htail_val,CD_misc_cons)
    #Missing Landing Gear Calculation
    flat_plate_area = CD_lg.flat_plate_area_calc(SR_20_data.takeoff_weight,1)
    flat_plate_area = SR_20_data.L_gear_flatplate
    CD_lg_val = CD_lg.cd_lg(flat_plate_area, SR_20_data.s_lg_front) 
    CD_lg_val = 0
    total_CD_val = CD_lg_val + CD_misc_val + CDi_fus_val + CDi_htail_val + CDi_wing_val + CDo_fus_val + CDo_htail_val + CDo_vtail_val + CDo_wing_val
    
    '''
    print(f'CD_lg_val: {CD_lg_val/total_CD_val}')
    print(f'CD_misc_val: {CD_misc_val/total_CD_val}')
    print(f'CDi_fus_val: {CDi_fus_val/total_CD_val}')
    print(f'CDi_htail_val: {CDi_htail_val/total_CD_val}')
    print(f'CDi_wing_val: {CDi_wing_val/total_CD_val}')
    print(f'CDo_fus_val: {CDo_fus_val/total_CD_val}')
    print(f'CDo_htail_val: {CDo_htail_val/total_CD_val}')
    print(f'CDo_vtail_val: {CDo_vtail_val/total_CD_val}')
    print(f'CDo_wing_val: {CDo_wing_val/total_CD_val}')
    '''
    return total_CD_val

def comparison(mach,altitude):
    real_cd = real_Cd_calc(altitude, mach)
    real_cd = real_cd * 1000
    theoretical_cd = theoretical_Cd_calc(mach,altitude)
    error = (theoretical_cd - real_cd) / real_cd * 100
    return real_cd, theoretical_cd, error

'''
mach = 0.01
real_cd, theoretical_cd, error = comparison(mach)
print(f'real CD value: {real_cd}')
print(f'theoretica CD value: {theoretical_cd}')
print(f'percent error: {error}')
'''

import numpy as np
import matplotlib.pyplot as plt

# Generate Mach speeds from 0 to 0.4
mach_values = np.linspace(0.18, 0.25, 1000)
altitudes = [2000, 4000, 6000, 8000, 10000, 12000, 14000]

# Initialize a dictionary to store errors for each altitude
altitude_errors = {}

# Calculate percentage errors for each Mach speed at different altitudes
for altitude in altitudes:
    errors = []  # Store errors for current altitude
    for mach in mach_values:
        real_cd, theo_cd, error = comparison(mach,altitude)  # Replace with your function
        # if real_cd != 0:
        #     print(f'altiude: {altitude}, real_cd: {real_cd}, theo_cd: {theo_cd}')
        if real_cd == 0:  # Avoid invalid divisions
            error = 0
        errors.append(error)
    altitude_errors[altitude] = errors  # Store errors for the current altitude

# Plotting
plt.figure(figsize=(10, 6))
for altitude in altitudes:
    plt.plot(mach_values, altitude_errors[altitude], label=f'Altitude: {altitude} ft')

# Adding labels and customization
plt.title('Percentage Error of CD vs. Mach Speed for Different Altitudes')
plt.xlabel('Mach Speed')
plt.ylabel('Percentage Error (%)')
plt.axhline(0, color='r', linestyle='--', label='Zero Error')  # Reference line at y=0
plt.ylim(-10, 10)  # Restrict y-axis from -10 to 10
plt.grid(True)
plt.legend()
plt.show()



#percent error increases almost exponentially.
# value 0.1 for landing gear
#landing gear .02