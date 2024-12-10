from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
from io import BytesIO
import base64
import matplotlib.colors as mcolors
import plotly.graph_objs as go
import json

import re_calc
import atmosphere_function
import CDo_wing
import CDo_vtail
import CDo_htail
import CDo_fus
import CDi_wing
import CD_misc
import CD_lg

def graph_generator(mach, drag_data):
    # Create a line trace for each name
    traces = []
    for altitude, coefficients in drag_data.items():
        # Create a line trace
        trace = go.Scatter(x=mach, y=coefficients, mode='lines+markers', name=f'{altitude} ft')
        traces.append(trace)
    
    # Define layout
    layout = dict(
        title='',
        xaxis=dict(title='Mach'),
        yaxis=dict(title='Drag Coefficient'),
    )
    
    # Create figure
    fig = dict(data=traces, layout=layout)

    # Convert the figure to an interactive HTML representation
    graph_html = pio.to_html(fig, include_plotlyjs=True, full_html=False)

    return graph_html

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/drag/calculate", methods=["POST"])
def calculate():
    Length = float(request.form["length"]) #ft
    height = float(request.form["height"]) #ft
    takeoff_weight = float(request.form["takeoff_weight"]) #lbs
    
    #Wing Data
    b_wing = float(request.form["b_wing"]) #ft
    S_wing = float(request.form["s_wing"]) #ft^2
    AR = (b_wing**2)/S_wing
    S_wet = float(request.form["s_wet"]) #ft^2
    c_bar =  float(request.form["c_bar"]) #ft
    L_c_4_wing = float(request.form["L_c_4_wing"]) #deg
    tc_avg =  float(request.form["tc_avg"]) #ratio #thickness to chord ratio
    tc_max_loc =  float(request.form["tc_max_loc"]) #percentage #from the leading edge
    tc_max =  float(request.form["tc_max"]) #ratio
    c_tip =  float(request.form["c_tip"]) #ft #chord at tip #
    c_root = float(request.form["c_root"]) #ft #chord at root
    taper = c_tip/c_root
    
    #Airfoil Data
    c_l_alpha = float(request.form["c_l_alpha"])
    c_l_0 = float(request.form["c_l_0"])
    rle = float(request.form["rle"])

    #Fuslage
    l_fus = float(request.form["l_fus"]) #ft this include the tip of the propeller
    S_fus_wet = float(request.form["s_fus_wet"]) #ft2
    d_fus = float(request.form["d_fus"]) #ft
    S_fus_maxfront = float(request.form["s_fus_maxfront"]) #ft2 #front view
    S_fus_plan = float(request.form["S_fus_plan"]) #ft2
    d_fus_b= float(request.form["d_fus_b"]) #diamter of the fuselage at end of the tail #Note the tail is not really circular #top down view
    S_fus_b = (d_fus_b**2)*(np.pi/4) #ft2 #equation written on Roskam Fig 4.17
    
    #H_Stab Data
    c_root_h = float(request.form["c_root_h"]) #ft #top view
    c_tip_h = float(request.form["c_tip_h"]) #ft #top view #not accurate
    b_h = float(request.form["b_h"]) #ft #APM
    L_c_4_h =  float(request.form["L_c_4_h"]) #c/4, deg #top view
    S_h = float(request.form["s_h"])  #ft2 #APM #!!!Have to double check
    AR_h = (b_h**2)/S_h 
    taper_h = c_tip_h/c_root_h
    tc_max_h = float(request.form["d_fus_b"]) #top view
    tc_avg_h = float(request.form["tc_avg_h"])
    S_h_expo = float(request.form["s_h_expo"]) # ft2
    S_h_wet = S_h_expo*(1.977+0.52*tc_avg_h)# #ft2 # Eq 7.12 Raymer 6th Ed. 
    tc_max_loc_h = float(request.form["tc_max_loc_h"]) #top view of Vtail
    
    #V_Stab Data
    V_stab_area = float(request.form["v_stab_area"]) #ft^2 # My calculation shows the reference area to be 12.5945867091379
    S_v_wet =  float(request.form["s_v_wet"]) #S_v_expo*(1.977+0.52*tc_avg_v)# #ft2 # Eq 7.12 Raymer 6th Ed.
    tc_max_v = float(request.form["tc_max_v"]) #top view #NACA0012
    tc_avg_v = float(request.form["tc_avg_v"])
    tc_max_loc_v = float(request.form["tc_max_loc_v"]) #top view
    L_c_4_v = float(request.form["L_c_4_v"]) #c/4, deg
    c_tip_v = float(request.form["c_tip_v"]) #ft #side view
    c_root_v = float(request.form["c_root_v"]) #ft #side view #note: the root cacluated is slanted
    b_v = float(request.form["b_v"]) #ft
    
    #Landing Gear Data
    L_gear_flatplate = float(request.form["l_gear_flatplate"])
    s_lg_front = float(request.form["s_lg_front"]) #ft2 #new val

    # Calculate drag coefficient over a range of Mach numbers
    mach_numbers = np.linspace(0.1, 1.0, 100)

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

    drag_data = {}

    for i, alt in enumerate(altitude):
        # Initialize CDo_wing as array of the same size as mach
        CDo_wing_val = np.zeros_like(mach)
        CDo_vtail_val = np.zeros_like(mach)
        CDo_htail_val = np.zeros_like(mach)
        CDo_fus_val = np.zeros_like(mach)
        CDi_wing_val = np.zeros_like(mach)
        CDi_htail_val = np.zeros_like(mach)
        CDi_fus_val = np.zeros_like(mach)
        CD_misc_val = np.zeros_like(mach)
        CD_lg_val = np.zeros_like(mach)
        total_CD_val = np.zeros_like(mach)
        
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
            CDo_wing_val[k] = CDo_wing.CDo_wing_calc(re, m, L_c_4_wing, tc_avg,S_wing,S_wet, tc_max_loc,
                                                    takeoff_weight,vinf,density,tc_max,c_tip,
                                                    c_root,S_wing,b_wing)
            CDo_vtail_val[k] = CDo_vtail.CDo_vtail(re, m, L_c_4_v, tc_max_loc_v, tc_avg_v, S_wing, S_v_wet, 
                                                takeoff_weight, vinf,density,tc_max_v, c_tip_v, c_root_v, 
                                                    S_wing #use S_wing now according to simulink, but I think it should be s_h 
                                                    , b_v)
            CDo_htail_val[k] = CDo_htail.CDo_htail(re,m, L_c_4_h, tc_max_loc_h, 
                                                tc_avg_h, S_wing, 
                                                S_h_wet, takeoff_weight, vinf, 
                                                c_tip_h, c_root_h, b_h, 
                                                S_wing, #use S_wing now according to simulink, but I think it should be s_h
                                                density, tc_max_h)      
            CDo_fus_val[k] = CDo_fus.CDo_fus(re,m, l_fus, d_fus, 
                                            S_fus_wet, S_wing,
                                            S_fus_maxfront)  
            CDi_wing_val[k] = CDi_wing.CDi_wing_calc(m, AR, L_c_4_wing, taper, 
                                                    density, vinf, rle, visc, b_wing, 
                                                    c_tip, c_root, c_l_alpha, 
                                                    takeoff_weight, S_wing)
            CDi_htail_val[k] = CDi_wing.induced_drag_htail(AR_h,S_h,S_wing,takeoff_weight,
                                                        density,vinf,S_wing)
            # might need to double check with ERJ-Data
            CDi_fus_val[k] = CDi_wing.fuse_induced_drag(c_l_0,l_fus,d_fus,m,S_wing,
                                                        S_fus_plan,S_fus_b,
                                                        takeoff_weight, density, vinf, S_wing, 
                                                        b_wing, c_tip,
                                                        c_root,c_l_alpha,
                                                        AR,L_c_4_wing)
            # might need to double check with ERJ-Data
            CD_misc_cons = 0.05
            CDo_pyl = 0
            CDo_nac = 0
            CD_misc_val[k] = CD_misc.CD_misc_calc(CDo_pyl,CDo_fus_val[k],CDo_wing_val[k],CDo_nac,CDo_vtail_val[k],CDo_htail_val[k],CD_misc_cons)
            #Missing Landing Gear Calculation
            CD_lg_val[k] = CD_lg.cd_lg(L_gear_flatplate, s_lg_front)
            total_CD_val[k] = CD_lg_val[k] + CD_misc_val[k] + CDi_fus_val[k] + CDi_htail_val[k] + CDi_wing_val[k] + CDo_fus_val[k] + CDo_htail_val[k] + CDo_vtail_val[k] + CDo_wing_val[k]
            
        total_CD_val = total_CD_val.tolist()
        drag_data[alt] = total_CD_val

    drag_html = graph_generator(mach, drag_data)
    return render_template("result.html", drag_html=drag_html)

if __name__ == "__main__":
    app.run

application = app