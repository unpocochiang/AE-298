from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
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
    S_fus_wet = float(request.form["S_fus_wet"]) #ft2
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
    drag_coefficients = drag_coefficient_0 + (1 / (np.pi * aspect_ratio * efficiency_factor)) * mach_numbers ** 2

    # Generate an interactive plot
    fig, ax = plt.subplots()
    ax.plot(mach_numbers, drag_coefficients)
    ax.set_title("Drag Coefficient vs. Mach Number")
    ax.set_xlabel("Mach Number")
    ax.set_ylabel("Drag Coefficient")
    ax.grid()

    # Save the plot to a string
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return render_template("result.html", plot_url=f"data:image/png;base64,{plot_data}")

if __name__ == "__main__":
    app.run(debug=True)
