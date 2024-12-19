# Plots CDi_Wing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import erj_data 
import re_calc
import atmosphere_function

import CDo_htail

# from profile_drag import calCf, calcRls, CalcLparam, CalcCDow

# Now we initialize our values, and calculate!
#mach = np.linspace(0.01, 0.8, 100) # Mach Number
# Define the starting value and the increment
start_value = 0.01
end_value = 0.7
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
altitude = np.array([0., 6666., 13333., 20000, 26666, 33333,40000])
mach_size = np.size(mach)

colors_xkcd = mcolors.XKCD_COLORS
color_list = [colors_xkcd['xkcd:red'],   colors_xkcd['xkcd:orange'], colors_xkcd['xkcd:purple'],      colors_xkcd['xkcd:apple green'],
              colors_xkcd['xkcd:azure'], colors_xkcd['xkcd:plum'],   colors_xkcd['xkcd:lime yellow'], colors_xkcd['xkcd:tomato red'],
              colors_xkcd['xkcd:mango'], colors_xkcd['xkcd:dusk'],   colors_xkcd['xkcd:bright cyan']]

# CDo_wing_list = [] (might be necessary to make this list? Probably not tho)

for i, alt in enumerate(altitude):
    # Initialize CDo_wing as array of the same size as mach
    CDo_val = np.zeros_like(mach)

    # Define values independent of mach, as we will iteratively define CDo_wing w/ mach
    altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(alt)
    

    print(f'Altitude: {alt}')

    # Iteratively define CDo_wing w/ mach
    for k, m in enumerate(mach):
        print(k)
        print(f'm:{m}')
        re = re_calc.re(density, m, erj_data.c_bar_h, visc, temp) # float for each mach
        
        #l_fus is just l_fus
        #df is d_fus
        #vinf is true airspeed
        #
        vinf = m * speed_of_sound
        CDo_val[k] = CDo_htail.CDo_htail(re,m, erj_data.L_c_4_h,  
                                             erj_data.tc_max_loc_h,
                                             erj_data.tc_avg_h,
                                             erj_data.S_wing,
                                             erj_data.S_h_wet, erj_data.weight,
                                             vinf, erj_data.c_tip_h, 
                                             erj_data.c_root_h, erj_data.b_h, 
                                             erj_data.S_wing #use S_wing now according to simulink, but I think it should be s_h
                                             ,density, 
                                             erj_data.tc_max_h)        
        #print(f'Mach: {m}')
        print(f'reynold: {re} | CDo_wing: {CDo_val[k]}')
        
    # Plot each CDo_wing now that it has finished construction
    plt.plot(mach, CDo_val, label=f'{alt} ft', color=color_list[i])

#plt.plot(0.5*np.ones(100), np.linspace(0.005, 0.03, 100), 'k--')
plt.title('CDo of Horizontal Stabilizer') # gonna do some LaTeX stuff with this in a bit, but this is a proof of concept lol
plt.xlabel('Mach Number')
plt.ylabel('CDo_htail')
plt.legend()
plt.show()