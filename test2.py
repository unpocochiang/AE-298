import numpy as np

# Define the starting value and the increment
start_value = 0.1
end_value = 0.8
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

# Initialize CDo_wing as array of the same size as mach
cd_val = np.zeros_like(mach)
cl_val = np.zeros_like(mach)

# Define values independent of mach, as we will iteratively define CDo_wing w/ mach
altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(alt)

# Iteratively define CDo_wing w/ mach
for k, m in enumerate(mach):
    re = re_calc.re(density, m, c_bar, visc, temp) # float for each mach
    
    #span is b_wing
    #sweep is L_c_4_wing
    #vinf is true airspeed
    #sref and wref may be both s_wing
    vinf = m * speed_of_sound

    cd_val[k] = CD.total_cd_calc(takeoff_weight, m, alt, b_wing, s_wing, float(form_data["s_wet"]), c_bar, float(form_data["L_c_4_wing"]), 
                    float(form_data["tc_avg"]), float(form_data["tc_max_loc"]), float(form_data["tc_max"]), float(form_data["c_tip"]), 
                    float(form_data["c_root"]), float(form_data["c_l_alpha"]), float(form_data["c_l_0"]), float(form_data["rle"]), 
                    float(form_data["l_fus"]), float(form_data["S_fus_plan_top"]), float(form_data["d_fus"]), 
                    float(form_data["s_fus_maxfront"]), float(form_data["c_root_h"]), float(form_data["c_tip_h"]), float(form_data["b_h"]), 
                    float(form_data["L_c_4_h"]), float(form_data["tc_max_loc_v"]), float(form_data["tc_avg_v"]), float(form_data["tc_max_v"]),
                    float(form_data["tc_max_h"]), float(form_data["tc_avg_h"]), float(form_data["tc_max_loc_h"]), float(form_data["c_tip_v"]), 
                    float(form_data["c_root_v"]), float(form_data["b_v"]), float(form_data["L_c_4_v"]), float(form_data["l_gear_flatplate"]), 
                    float(form_data["s_lg_front"]), float(form_data["s_h"]), float(form_data["NumNac"]), float(form_data["l_nac"]), 
                    float(form_data["d_nac"]), float(form_data["S_nac_maxfront"]), float(form_data["t_nac"]), float(form_data["NumPyl"]), 
                    float(form_data["pylon_arrangement"]), float(form_data["w_py"]), float(form_data["l_pyl"]), float(form_data["c_bar_v"]), 
                    float(form_data["c_bar_h"]), float(form_data["S_v_wet"]), float(form_data["S_h_wet"]), float(form_data["S_fus_wet"]), 
                    float(form_data["S_fus_b"]), float(form_data["AR"]), float(form_data["taper"]), float(form_data["AR_h"]))
    
    #cl_val[k] = CL.total_cl_calc(L_c_4_wing, AR, re, airfoil_name)
    cl_val[k] = 2 * takeoff_weight / (density * vinf**2 * s_wing)

cl_val = np.nan_to_num(cl_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
cd_val = np.nan_to_num(cd_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()





