# Plots CDi_Wing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import Piper_Archer_III_data 
import re_calc
import atmosphere_function

import CDo_wing

# Define the starting value and the increment
start_value = 0.01
end_value = 0.5
increment = 0.01

# Calculate the number of elements needed
num_elements = int((end_value - start_value) / increment) + 1

# Create the matrix
mach = []

# Fill the matrix with the desired values
current_value = start_value
for i in range(num_elements):
    mach.append(current_value) 
    current_value += increment
# altitude = np.arange(0., 55000., 5000.) # ft
altitude = np.array([0., 5000., 10000., 15000, 20000, 25000, 30000])
mach_size = np.size(mach)



colors_xkcd = mcolors.XKCD_COLORS
color_list = [colors_xkcd['xkcd:red'],   colors_xkcd['xkcd:orange'], colors_xkcd['xkcd:purple'],      colors_xkcd['xkcd:apple green'],
              colors_xkcd['xkcd:azure'], colors_xkcd['xkcd:plum'],   colors_xkcd['xkcd:lime yellow'], colors_xkcd['xkcd:tomato red'],
              colors_xkcd['xkcd:mango'], colors_xkcd['xkcd:dusk'],   colors_xkcd['xkcd:bright cyan']]

# CDo_wing_list = [] (might be necessary to make this list? Probably not tho)

for i, alt in enumerate(altitude):
    # Initialize CDo_wing as array of the same size as mach
    CDo_wing_val = np.zeros_like(mach)

    # Define values independent of mach, as we will iteratively define CDo_wing w/ mach
    altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(alt)
    

    print(f'Altitude: {alt}')

    # Iteratively define CDo_wing w/ mach
    for k, m in enumerate(mach):
        print(k)
        print(f'm:{m}')
        re = re_calc.re(density, m, Piper_Archer_III_data.c_bar, visc, temp) # float for each mach
        
        #span is b_wing
        #sweep is L_c_4_wing
        #vinf is true airspeed
        #sref and wref may be both s_wing
        vinf = m * speed_of_sound
        CDo_wing_val[k] = CDo_wing.CDo_wing_calc(re, m, Piper_Archer_III_data.L_c_4_wing, Piper_Archer_III_data.tc_avg,Piper_Archer_III_data.S_wing,Piper_Archer_III_data.S_wet, Piper_Archer_III_data.tc_max_loc,
                                                Piper_Archer_III_data.takeoff_weight,vinf,density,Piper_Archer_III_data.tc_max,Piper_Archer_III_data.c_tip,
                                                Piper_Archer_III_data.c_root,Piper_Archer_III_data.S_wing,Piper_Archer_III_data.Wing_span)
        
        #print(f'Mach: {m}')
        print(f'reynold: {re} | CDo_wing: {CDo_wing_val[k]}')
        
    # Plot each CDo_wing now that it has finished construction
    plt.plot(mach, CDo_wing_val, label=f'{alt} ft', color=color_list[i])

#plt.plot(0.5*np.ones(100), np.linspace(0.005, 0.03, 100), 'k--')
plt.title('CDo of wing') # gonna do some LaTeX stuff with this in a bit, but this is a proof of concept lol
plt.xlabel('Mach Number')
plt.ylabel('CDo_wing')
plt.legend()
plt.show()
m=0.4
altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(0) 
re = re_calc.re(density, 0.4, Piper_Archer_III_data.c_bar, visc, temp) # float for each mach
        
#span is b_wing
#sweep is L_c_4_wing
        #vinf is true airspeed
        #sref and wref may be both s_wing
vinf = m * speed_of_sound
CDo_wing_val_2 = CDo_wing.CDo_wing_calc(re, m, Piper_Archer_III_data.L_c_4_wing, Piper_Archer_III_data.tc_avg,Piper_Archer_III_data.S_wing,
                                         Piper_Archer_III_data.S_wet, Piper_Archer_III_data.tc_max_loc,
                                         Piper_Archer_III_data.takeoff_weight,vinf,density,Piper_Archer_III_data.tc_max,Piper_Archer_III_data.c_tip,
                                         Piper_Archer_III_data.c_root,Piper_Archer_III_data.S_wing,Piper_Archer_III_data.Wing_span)
        
print(f'Mach: {m}')
print(f'reynold: {re} | CDo_wing: {CDo_wing_val_2}')
D=0.008359041155112665/2*density*vinf**2*Piper_Archer_III_data.S_wing
print(D)
t=134225/vinf
print(t)