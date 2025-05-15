import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol
import CDi_wing
import atmosphere_function
import Piper_Archer_III_data
import CDo_wing
import CDo_vtail
import CDo_htail
import CDo_fus
import CDi_wing
import CD_misc
import CD_lg
import re_calc
import CDo_nac
import CDo_ply

def real_Cd_calc(mach):
    # altitude is 3500ft
    # aircraft weight is 924 kg
    weight = 2037.0713026 #lb #924 kg
    alt = 3500
    h_G, h, T, P, rho, speed_of_sound,mu = atmosphere_function.AtmosphereFunction(alt)
    sref = Piper_Archer_III_data.S_wing
    x = sp.symbols('x')
    eq = -14.2 + 0.664*x - (4.61*10**-3)*x**2
    # x is velocity
    vel = mach * speed_of_sound
    vel = vel / 1.68780986 #change unit to knts
    # calc Cl
    cl = CDi_wing.CL_calc(weight, rho, vel, sref)
    cd = 0
    if vel >= 28.451 and vel <= 248.732:
        # find 
        glide_ratio = eq.subs(x,vel)
        cd = cl / glide_ratio
    return cd

def theoretical_Cd_calc(m):
    altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(3500) 
    re = re_calc.re(density, 0.4, Piper_Archer_III_data.c_bar, visc, temp) # float for each mach
            
    #span is b_wing
    #sweep is L_c_4_wing
            #vinf is true airspeed
            #sref and wref may be both s_wing
    vinf = m * speed_of_sound
    CDo_wing_val = CDo_wing.CDo_wing_calc(re, m, Piper_Archer_III_data.L_c_4_wing, Piper_Archer_III_data.tc_avg,Piper_Archer_III_data.S_wing,Piper_Archer_III_data.S_wet, Piper_Archer_III_data.tc_max_loc,
                                                    Piper_Archer_III_data.takeoff_weight,vinf,density,Piper_Archer_III_data.tc_max,Piper_Archer_III_data.c_tip,
                                                    Piper_Archer_III_data.c_root,Piper_Archer_III_data.S_wing,Piper_Archer_III_data.b_wing)
    CDo_vtail_val = CDo_vtail.CDo_vtail(re, m, Piper_Archer_III_data.L_c_4_v, Piper_Archer_III_data.tc_max_loc_v, Piper_Archer_III_data.tc_avg_v, Piper_Archer_III_data.S_wing, Piper_Archer_III_data.S_v_wet, 
                                                Piper_Archer_III_data.takeoff_weight, vinf,density,Piper_Archer_III_data.tc_max_v, Piper_Archer_III_data.c_tip_v, Piper_Archer_III_data.c_root_v, 
                                                    Piper_Archer_III_data.S_wing #use S_wing now according to simulink, but I think it should be s_h 
                                                    , Piper_Archer_III_data.b_v)
    CDo_htail_val = CDo_htail.CDo_htail(re,m, Piper_Archer_III_data.L_c_4_h, Piper_Archer_III_data.tc_max_loc_h, 
                                                Piper_Archer_III_data.tc_avg_h, Piper_Archer_III_data.S_wing, 
                                                Piper_Archer_III_data.S_h_wet, Piper_Archer_III_data.takeoff_weight, vinf, 
                                                Piper_Archer_III_data.c_tip_h, Piper_Archer_III_data.c_root_h, Piper_Archer_III_data.b_h, 
                                                Piper_Archer_III_data.S_wing, #use S_wing now according to simulink, but I think it should be s_h
                                                density, Piper_Archer_III_data.tc_max_h)      
    CDo_fus_val = CDo_fus.CDo_fus(re,m, Piper_Archer_III_data.l_fus, Piper_Archer_III_data.d_fus, 
                                            Piper_Archer_III_data.S_fus_wet, Piper_Archer_III_data.S_wing,
                                            Piper_Archer_III_data.S_fus_maxfront)  
    CDi_wing_val = CDi_wing.CDi_wing_calc(m, Piper_Archer_III_data.AR, Piper_Archer_III_data.L_c_4_wing, Piper_Archer_III_data.taper, 
                                                    density, vinf, Piper_Archer_III_data.rle, visc, Piper_Archer_III_data.b_wing, 
                                                    Piper_Archer_III_data.c_tip, Piper_Archer_III_data.c_root, Piper_Archer_III_data.c_l_alpha, 
                                                    Piper_Archer_III_data.takeoff_weight, Piper_Archer_III_data.S_wing)
    CDi_htail_val = CDi_wing.induced_drag_htail(Piper_Archer_III_data.AR_h,Piper_Archer_III_data.S_h,Piper_Archer_III_data.S_wing,Piper_Archer_III_data.takeoff_weight,
                                                        density,vinf)
    # might need to double check with ERJ-Data
    CDi_fus_val = CDi_wing.fuse_induced_drag(Piper_Archer_III_data.c_l_0,Piper_Archer_III_data.l_fus,Piper_Archer_III_data.d_fus,m,Piper_Archer_III_data.S_wing,
                                                        Piper_Archer_III_data.S_fus_plan,Piper_Archer_III_data.S_fus_b,
                                                        Piper_Archer_III_data.takeoff_weight, density, vinf, 
                                                        Piper_Archer_III_data.b_wing, Piper_Archer_III_data.c_tip,
                                                        Piper_Archer_III_data.c_root,Piper_Archer_III_data.c_l_alpha,
                                                        Piper_Archer_III_data.AR,Piper_Archer_III_data.L_c_4_wing)
    # might need to double check with ERJ-Data
    CD_misc_cons = 0.05
    CDo_pyl = 0
    CDo_nac_val = 0
    CD_misc_val = CD_misc.CD_misc_calc(CDo_pyl,CDo_fus_val,CDo_wing_val,CDo_nac_val,CDo_vtail_val,CDo_htail_val,CD_misc_cons)
    #Missing Landing Gear Calculation
    flat_plate_area = CD_lg.flat_plate_area_calc(Piper_Archer_III_data.takeoff_weight,1)
    flat_plate_area = Piper_Archer_III_data.L_gear_flatplate
    # For landing gear drag
    cd_lg_back = CDo_nac.CDo_nac(re,m,Piper_Archer_III_data.lg_back_num,
                                Piper_Archer_III_data.lg_back_l, Piper_Archer_III_data.lg_back_dia,
                                Piper_Archer_III_data.S_wing,Piper_Archer_III_data.lg_back_maxfront,
                                Piper_Archer_III_data.lg_back_tnac)
    
    cd_lg_front = CDo_nac.CDo_nac(re,m,Piper_Archer_III_data.lg_front_num,
                                Piper_Archer_III_data.lg_front_l, Piper_Archer_III_data.lg_front_dia,
                                Piper_Archer_III_data.S_wing,Piper_Archer_III_data.lg_front_maxfront,
                                Piper_Archer_III_data.lg_front_tnac)
    
    cd_lg_bpyl = CDo_ply.CDo_ply(Piper_Archer_III_data.back_numpyl, Piper_Archer_III_data.back_pylon_arrangement,
                                Piper_Archer_III_data.back_wpyl, Piper_Archer_III_data.back_lpyl,re, mach, 
                                Piper_Archer_III_data.S_wing,Piper_Archer_III_data.takeoff_weight,vinf, density,
                                Piper_Archer_III_data.back_lpyl, Piper_Archer_III_data.back_lpyl)
    
    cd_lg_fpyl = CDo_ply.CDo_ply(Piper_Archer_III_data.front_numpyl, Piper_Archer_III_data.front_pylon_arrangement,
                                Piper_Archer_III_data.back_wpyl, Piper_Archer_III_data.front_lpyl,re, mach, 
                                Piper_Archer_III_data.S_wing, Piper_Archer_III_data.takeoff_weight,vinf, density, 
                                Piper_Archer_III_data.front_lpyl, Piper_Archer_III_data.front_lpyl)
    
    CD_lg_val = cd_lg_back + cd_lg_front + cd_lg_bpyl + cd_lg_fpyl
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

def comparison(mach):
    real_cd = real_Cd_calc(mach)
    theoretical_cd = theoretical_Cd_calc(mach)
    error = (theoretical_cd - real_cd) / real_cd * 100
    return real_cd, theoretical_cd, error

'''
mach = 0.01
real_cd, theoretical_cd, error = comparison(mach)
print(f'real CD value: {real_cd}')
print(f'theoretica CD value: {theoretical_cd}')
print(f'percent error: {error}')
'''

# Generate Mach speeds from 0 to 0.6
mach_values = np.linspace(0, 0.1, 1000)
errors = []

# Calculate percentage error for each Mach speed
for mach in mach_values:
    real_cd, _, error = comparison(mach)
    if real_cd == 0:
        error = 0
    errors.append(error)
print(errors)
# Plotting
plt.figure(figsize=(10, 6))
plt.plot(mach_values, errors, label='Percentage Error', color='b')
plt.title('Percentage Error of CD vs. Mach Speed')
plt.xlabel('Mach Speed')
plt.ylabel('Percentage Error (%)')
plt.grid(True)
plt.axhline(0, color='r', linestyle='--')  # Add a line at y=0 for reference
plt.ylim(-100, 100) 
plt.legend()
plt.show()


#percent error increases almost exponentially.
# value 0.1 for landing gear
#landing gear .02