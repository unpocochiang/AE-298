from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
import ast
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
from io import BytesIO
import base64
import matplotlib.colors as mcolors
import plotly.graph_objs as go
import json
from matplotlib.figure import Figure
import io
import base64
import sys
import os
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

sys.path.append(os.path.join(os.path.dirname(__file__), "avl"))
import avl_main
import airfoil
import erj_data
import re_calc
import atmosphere_function
import CDo_wing
import CDo_vtail
import CDo_htail
import CDo_fus
import CDi_wing
import CD_misc
import CD_lg
import CDo_nac
import CDo_ply
import range_endurace
import CD
import CL

from flask import Flask
from flask_session import Session

def graph_generator(mach, drag_data):
    # Create a line trace for each name
    traces = []
    for altitude, data in drag_data.items():
        coefficients =data['total_cd']
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

def max_ratio(cl_list, cd_list, mach_list):
    best_sqrtcl_cd = {'value': -np.inf, 'mach': None, 'cl': None, 'cd': None}
    best_cl_cd = {'value': -np.inf, 'mach': None, 'cl': None, 'cd': None}

    for cl, cd, mach in zip(cl_list, cd_list, mach_list):
        if cd == 0:
            continue  # Avoid division by zero

        cl_cd = cl / cd
        sqrtcl_cd = np.sqrt(cl) / cd if cl > 0 else -np.inf

        if cl_cd > best_cl_cd['value']:
            best_cl_cd = {
                'value': cl_cd,
                'mach': mach,
                'cl': cl,
                'cd': cd
            }

        if sqrtcl_cd > best_sqrtcl_cd['value']:
            best_sqrtcl_cd = {
                'value': sqrtcl_cd,
                'mach': mach,
                'cl': cl,
                'cd': cd
            }

    return best_sqrtcl_cd, best_cl_cd


app = Flask(__name__)
app.secret_key = 'super-secret'  # Still needed for session signing
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use 'redis', etc.

Session(app)  # <-- This swaps in the server-side backend

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    
    form_data = request.form.to_dict()
    session['form_data'] = form_data  # Save to session 



    takeoff_weight = float(request.form["takeoff_weight"]) #lbs
    mach_min = float(request.form["mach_min"])
    mach_max = float(request.form["mach_max"])
    altitude_min = float(request.form["altitude_min"])
    altitude_max = float(request.form["altitude_max"])

    # Engine and Airfoil Data
    engine_type = request.form["engine_type"]  # value from dropdown like 'turboprop', 'piston', etc.
    airfoil_name = request.form["airfoil_name"]  # string input like 'NACA 2412'
    
    #Wing Data
    b_wing = float(request.form["b_wing"]) #ft
    S_wing = float(request.form["s_wing"]) #ft^2
    AR = (b_wing**2)/S_wing
    form_data['AR'] = AR
    S_wet = float(request.form["s_wet"]) #ft^2
    c_bar =  float(request.form["c_bar"]) #ft
    L_c_4_wing = float(request.form["L_c_4_wing"]) #deg
    tc_avg =  float(request.form["tc_avg"]) #ratio #thickness to chord ratio
    tc_max_loc =  float(request.form["tc_max_loc"]) #percentage #from the leading edge
    tc_max =  float(request.form["tc_max"]) #ratio
    c_tip =  float(request.form["c_tip"]) #ft #chord at tip #
    c_root = float(request.form["c_root"]) #ft #chord at root
    taper = c_tip/c_root
    form_data['taper'] = taper

    #Airfoil Data
    c_l_alpha = float(request.form["c_l_alpha"])
    c_l_0 = float(request.form["c_l_0"])
    rle = float(request.form["rle"])

    #Fuslage
    l_fus = float(request.form["l_fus"]) #ft this include the tip of the propeller
    S_fus_plan_side = float(request.form["S_fus_plan_side"]) #ft2 #fuselag side planform view
    S_fus_plan_top = float(request.form["S_fus_plan_top"]) #ft2 #fuselag top planform view
    S_fus_wet = 3.4*(S_fus_plan_top+S_fus_plan_side)/2
    form_data['S_fus_wet'] = S_fus_wet
    d_fus = float(request.form["d_fus"]) #ft
    S_fus_maxfront = float(request.form["s_fus_maxfront"]) #ft2 #front view
    d_fus_b= float(request.form["d_fus_b"]) #diamter of the fuselage at end of the tail #Note the tail is not really circular #top down view
    S_fus_b = (d_fus_b**2)*(np.pi/4) #ft2 #equation written on Roskam Fig 4.17
    form_data['S_fus_b'] = S_fus_b
    
    #H_Stab Data
    c_root_h = float(request.form["c_root_h"]) #ft #top view
    c_tip_h = float(request.form["c_tip_h"]) #ft #top view #not accurate
    b_h = float(request.form["b_h"]) #ft #APM
    L_c_4_h =  float(request.form["L_c_4_h"]) #c/4, deg #top view
    S_h = float(request.form["s_h"])  #ft2 #APM #!!!Have to double check
    AR_h = (b_h**2)/S_h 
    form_data['AR_h'] = AR_h
    tc_max_h = float(request.form["tc_max_h"]) #top view
    tc_avg_h = float(request.form["tc_avg_h"])
    S_h_expo = float(request.form["s_h_expo"]) # ft2
    if tc_avg_h > 0.05:
        S_h_wet =  S_h_expo*(1.977+0.52*tc_avg_h)# #ft2 # Eq 7.12 Raymer 6th Ed. 
        form_data['S_h_wet'] = S_h_wet
    else:
        S_h_wet =  S_h_expo*2.003# #ft2 # Eq 7.12 Raymer 6th Ed.
        form_data['S_h_wet'] = S_h_wet
    tc_max_loc_h = float(request.form["tc_max_loc_h"]) #top view of Vtail
    taper_h = c_tip_h/c_root_h 
    form_data['taper_h'] = taper_h
    c_bar_h  = c_root_h * (2/3)*(1 + taper_h + taper_h**2)/(1+taper_h) #ft 
    form_data['c_bar_h'] = c_bar_h

    #V_Stab Data
    tc_avg_v = float(request.form["tc_avg_v"])
    S_v_expo = float(request.form['S_v_expo'])
    if tc_avg_v > 0.05:
        S_v_wet =  S_v_expo*(1.977+0.52*tc_avg_v)# #ft2 # Eq 7.12 Raymer 6th Ed.
        form_data['S_v_wet'] = S_v_wet
    else:
        S_v_wet =  S_v_expo*2.003# #ft2 # Eq 7.12 Raymer 6th Ed.
        form_data['S_v_wet'] = S_v_wet
    tc_max_v = float(request.form["tc_max_v"]) #top view #NACA0012
    tc_max_loc_v = float(request.form["tc_max_loc_v"]) #top view
    L_c_4_v = float(request.form["L_c_4_v"]) #c/4, deg
    c_tip_v = float(request.form["c_tip_v"]) #ft #side view
    c_root_v = float(request.form["c_root_v"]) #ft #side view #note: the root cacluated is slanted
    b_v = float(request.form["b_v"]) #ft
    taper_v = c_tip_v/c_root_v
    form_data['taper_v'] = taper_v
    c_bar_v  = c_root_v * (2/3)*(1 + taper_v + taper_v**2)/(1+taper_v) #ft
    form_data['c_bar_v'] = c_bar_v

    # Handle landing gear data
    has_landing_gear = 'has_landing_gear' in request.form
    if has_landing_gear:
        form_data['has_landing_gear'] = True
        L_gear_flatplate = float(request.form["l_gear_flatplate"])
        s_lg_front = float(request.form["s_lg_front"])
    else:
        form_data['has_landing_gear'] = False
        L_gear_flatplate = 0 
        s_lg_front = 10 
        form_data['l_gear_flatplate'] = L_gear_flatplate
        form_data['s_lg_front'] = s_lg_front
    
    # Handle landing gear data
    has_nac = 'has_nac' in request.form
    if has_nac:
        form_data['has_nac'] = True
        NumNac = float(request.form["NumNac"])
        l_nac = float(request.form["l_nac"])
        d_nac = float(request.form["d_nac"])
        S_nac_maxfront = float(request.form["S_nac_maxfront"])
        t_nac = float(request.form["t_nac"])
        w_py = float(request.form["w_py"])
        NumPyl = float(request.form["NumPyl"])
        pylon_arrangement = float(request.form["pylon_arrangement"])
        l_pyl = float(request.form["l_pyl"])
    else:
        form_data['has_nac'] = False
        NumNac = 0
        form_data['NumNac'] = NumNac
        NumPyl = 0
        form_data['NumPyl'] = NumPyl
        S_nac_maxfront = 0
        form_data['S_nac_maxfront'] = S_nac_maxfront
        l_nac = 1
        form_data['l_nac'] = l_nac
        d_nac = 1
        form_data['d_nac'] = d_nac
        pylon_arrangement = 1
        form_data['pylon_arrangement'] = pylon_arrangement
        l_pyl = 1
        form_data['l_pyl'] = l_pyl
        t_nac = 1
        form_data['t_nac'] = t_nac
        w_py = 0
        form_data['w_py'] = w_py

    # Define the starting value and the increment
    start_value = mach_min
    end_value = mach_max
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
    altitude = np.linspace(altitude_min, altitude_max, 7)

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
        CDo_nac_val = np.zeros_like(mach)
        CDo_ply_val = np.zeros_like(mach)
        total_CD_val = np.zeros_like(mach)
        cl_val = np.zeros_like(mach)
        cl_force_val = np.zeros_like(mach)
        avl_cdi_val = np.zeros_like(mach)
        
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
            CDo_wing_val[k] = CDo_wing.CDo_wing_calc(re, m, L_c_4_wing, tc_avg,S_wing,S_wet, tc_max_loc, takeoff_weight,
                                                    vinf,density,tc_max,c_tip, c_root,S_wing,b_wing)
            re_v = re_calc.re(density, m, c_bar_v, visc, temp)                          
            CDo_vtail_val[k] = CDo_vtail.CDo_vtail(re_v, m, L_c_4_v, tc_max_loc_v, tc_avg_v, S_wing, S_v_wet, takeoff_weight, 
                                                vinf,density,tc_max_v, c_tip_v, c_root_v, S_wing , b_v)
                                                #use S_wing now according to simulink, but I think it should be s_h 
            re_h = re_calc.re(density, m, c_bar_h, visc, temp)                               
            CDo_htail_val[k] = CDo_htail.CDo_htail(re_h , m, L_c_4_h, tc_max_loc_h, tc_avg_h, S_wing, S_h_wet, takeoff_weight, vinf, 
                                                c_tip_h, c_root_h, b_h, S_wing, density, tc_max_h)      
                                                #use S_wing now according to simulink, but I think it should be s_h
                     
            CDo_fus_val[k] = CDo_fus.CDo_fus(re,m, l_fus, d_fus, S_fus_wet, S_wing, S_fus_maxfront)  

            CDi_wing_val[k] = CDi_wing.CDi_wing_calc(m, AR, L_c_4_wing, taper, density, vinf, rle, visc, b_wing, c_tip, 
                                                    c_root, c_l_alpha, takeoff_weight, S_wing)
        
            CDi_htail_val[k] = CDi_wing.induced_drag_htail(AR_h,S_h,S_wing,takeoff_weight, density,vinf)

            CDi_fus_val[k] = CDi_wing.fuse_induced_drag(c_l_0,l_fus,d_fus,m,S_wing, S_fus_plan_top,S_fus_b, takeoff_weight, 
                                                        density, vinf, b_wing, c_tip, c_root,c_l_alpha, AR,L_c_4_wing)
            
            CDo_nac_val[k] = CDo_nac.CDo_nac(re,m,NumNac,l_nac, d_nac, S_wing, S_nac_maxfront, t_nac)
            
            CDo_ply_val[k] = CDo_ply.CDo_ply(NumPyl, pylon_arrangement, w_py, l_pyl,re, m, S_wing, takeoff_weight, vinf, density, l_pyl, l_pyl)

            # might need to double check with ERJ-Data
            CD_misc_cons = 0.05
            CD_misc_val[k] = CD_misc.CD_misc_calc(CDo_ply_val[k],CDo_fus_val[k],CDo_wing_val[k], CDo_nac_val[k] ,CDo_vtail_val[k],CDo_htail_val[k],CD_misc_cons)
            #Missing Landing Gear Calculation
            CD_lg_val[k] = CD_lg.cd_lg(L_gear_flatplate, s_lg_front)
            
            total_CD_val[k] = CD_lg_val[k] + CD_misc_val[k] + CDi_fus_val[k] + CDi_htail_val[k] + CDi_wing_val[k] + CDo_fus_val[k] + CDo_htail_val[k] + CDo_vtail_val[k] + CDo_wing_val[k] + CDo_nac_val[k] + CDo_ply_val[k]
            
            cl_val[k] = CL.total_cl_calc(L_c_4_wing, AR, re, airfoil_name)
            
            cl_force_val[k] = 2 * takeoff_weight / (density * vinf**2 * S_wing)
            

            # uncomment in the future # change
            # wing_sections = session["wing_sections"]
            # alpha, avl_cdi_val[k], e = avl_main.solve_alpha_for_cl(cl_force_val[k], m, wing_sections, density * 515.3788, 9.81) #input for rho and gravity needs to be SI unit 
            
            # if alpha is None:
            #     alpha, avl_cdi_val[k], e = avl_main.solve_alpha_for_cl(cl_val[k], m, wing_sections, density * 515.3788, 9.81) #input for rho and gravity needs to be SI unit 
            
        total_CD_val = np.nan_to_num(total_CD_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDo_wing_val = np.nan_to_num(CDo_wing_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CD_lg_val = np.nan_to_num(CD_lg_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CD_misc_val = np.nan_to_num(CD_misc_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDi_fus_val = np.nan_to_num(CDi_fus_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDi_htail_val = np.nan_to_num(CDi_htail_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDi_wing_val = np.nan_to_num(CDi_wing_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDo_fus_val = np.nan_to_num(CDo_fus_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDo_htail_val = np.nan_to_num(CDo_htail_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDo_vtail_val = np.nan_to_num(CDo_vtail_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDo_nac_val = np.nan_to_num(CDo_nac_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        CDo_ply_val = np.nan_to_num(CDo_ply_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        cl_val = np.nan_to_num(cl_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        cl_force_val = np.nan_to_num(cl_force_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
        avl_cdi_val = np.nan_to_num(avl_cdi_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()

        drag_data[alt] = {
            "mach": mach,
            "wing_cd": CDo_wing_val,
            "lg_cd": CD_lg_val,
            "misc_cd": CD_misc_val,
            "fus_cdi": CDi_fus_val,
            "htail_cdi": CDi_htail_val,
            "wing_cdi": CDi_wing_val,
            "fus_cd": CDo_fus_val,
            "htail_cd": CDo_htail_val,
            "vtail_cd": CDo_vtail_val,
            "nac_cd": CDo_nac_val,
            "ply_cd": CDo_ply_val,
            "total_cd": total_CD_val,
            "cl_calc" : cl_val,
            "avl_cl" : cl_force_val,
            "avl_cdi": avl_cdi_val
        }
    
    drag_html = graph_generator(mach, drag_data)
    session['drag_data'] = drag_data
    return render_template("result.html", drag_html=drag_html, drag_data=drag_data, mach=mach)

@app.route("/upload_input", methods=["POST"])
def upload_input():
    file = request.files["input_file"]
    if not file:
        return "No file uploaded", 400

    content = file.read().decode("utf-8")
    parsed = {}

    # Parse Python assignments using ast
    try:
        tree = ast.parse(content)
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                key = node.targets[0].id
                val = ast.literal_eval(node.value)
                parsed[key] = val
    except Exception as e:
        return f"Failed to parse file: {e}", 400

    # Store values in session
    from flask import session
    session["form_prefill"] = parsed
    if "wing_sections" in parsed:
        session["wing_sections"] = parsed["wing_sections"]

    # Redirect to a form page that uses session["form_prefill"]
    return redirect(url_for("prefill_form"))

@app.route("/prefill")
def prefill_form():
    return render_template("index.html", prefill=session.get("form_prefill", {}), wing_sections=session.get("wing_sections", []))

@app.route("/download_input", methods=["POST"])
def download_input():
    # Extract form data
    form_data = request.form.to_dict()

    # Convert form values into Python assignments
    lines = []
    for key, value in form_data.items():
        try:
            val = float(value)
            val_str = f"{val:.4f}" if '.' in value else f"{int(val)}"
        except ValueError:
            val_str = f'"{value}"'
        lines.append(f"{key} = {val_str}")

    # Retrieve wing sections from session
    wing_sections = session.get("wing_sections", [])
    lines.append("\n# Wing sections")
    lines.append("wing_sections = [")
    for sec in wing_sections:
        sec_str = f'    {{"x": {sec["x"]}, "y": {sec["y"]}, "z": {sec["z"]}, "chord": {sec["chord"]}, "airfoil": "{sec["airfoil"]}"}},'
        lines.append(sec_str)
    lines.append("]")

    # Generate the file content
    py_content = "\n".join(lines)

    # Create downloadable response
    response = make_response(py_content)
    response.headers["Content-Disposition"] = "attachment; filename=aircraft_input.py"
    response.headers["Content-Type"] = "text/x-python"
    return response

from flask import request, jsonify

@app.route("/estimate-range", methods=["POST"])
def estimate_range():
    data = request.get_json()
    velocity = float(data["velocity"])
    fuel_weight = float(data["fuel_weight"])
    alt = float(data["altitude"])
    drag_data = session.get('drag_data', {})

    form_data = session.get('form_data', {})
    takeoff_weight = float(form_data["takeoff_weight"])
    plane_type = form_data["engine_category"]
    engine_type = form_data["engine_type"]
    altitude, geo_alt, temp, pressure, rho, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(alt)
    s_wing = float(form_data["s_wing"])
    b_wing = float(form_data["b_wing"])
    c_bar = float(form_data["c_bar"])
    AR = (b_wing**2)/s_wing
    m = velocity / speed_of_sound
    airfoil_name = form_data["airfoil_name"]
    sweep = float(form_data["L_c_4_wing"])
    re = re_calc.re(rho, m, c_bar, visc, temp) # float for each mach
    cd = CD.total_cd_calc(takeoff_weight, m, alt, b_wing, s_wing, float(form_data["s_wet"]), c_bar, float(form_data["L_c_4_wing"]), 
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

    wing_sections = session.get('wing_sections', [])
    # solve for alpha in steady flight
    cl = CL.total_cl_calc(sweep, AR, re, airfoil_name)
    #cl = 2 * takeoff_weight / (rho * velocity**2 * s_wing)

    cl_0, cdi, e = avl_main.main(m, wing_sections, 0, rho * 515.3788, 9.81) #input for rho and gravity needs to be SI unit 
    print(f'cl_0: {cl_0}')
    ld = cl/cd


    # Define the starting value and the increment
    start_value = 0.1
    end_value = 0.8
    increment = 0.01
    num_elements = int((end_value - start_value) / increment) + 1
    mach = []
    current_value = start_value
    for i in range(num_elements):
        mach.append(current_value) 
        current_value += increment
    cd_val = np.zeros_like(mach)
    cl_val = np.zeros_like(mach)

    # Iteratively define CDo_wing w/ mach
    for k, m in enumerate(mach):
        re = re_calc.re(rho, m, c_bar, visc, temp) # float for each mach
        
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
        
        cl_val[k] = CL.total_cl_calc(float(form_data["L_c_4_wing"]), AR, re, airfoil_name)
        #cl_val[k] = 2 * takeoff_weight / (rho * vinf**2 * s_wing)

    cl_val = np.nan_to_num(cl_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()
    cd_val = np.nan_to_num(cd_val, nan=0.0, posinf=1.0, neginf=-1.0).tolist()

    best_sqrtcl_cd, best_cl_cd = max_ratio(cl_val,cd_val, mach)
    print(best_sqrtcl_cd)
    print(best_cl_cd)

    if plane_type == "jet":
        aircraft_range_optimal = range_endurace.jet_range_calc(best_sqrtcl_cd['cl'], best_sqrtcl_cd['cd'], rho, s_wing, takeoff_weight, fuel_weight, engine_type)
        aircraft_endurance_optimal = range_endurace.jet_endurance_calc(best_cl_cd['value'], takeoff_weight, fuel_weight, engine_type)
    elif plane_type == "prop":
        aircraft_range = range_endurace.prop_range_calc(velocity, ld, takeoff_weight, fuel_weight, engine_type)
        aircraft_endurance = range_endurace.prop_endurance_calc(velocity, rho, s_wing, cl, cd, takeoff_weight, fuel_weight, engine_type)
    print(f'optimal range: {aircraft_range_optimal}')
    print(f'optimal endurance: {aircraft_endurance_optimal}')
    
    if plane_type == "jet":
        aircraft_range = range_endurace.jet_range_calc(cl, cd, rho, s_wing, takeoff_weight, fuel_weight, engine_type)
        aircraft_endurance = range_endurace.jet_endurance_calc(ld, takeoff_weight, fuel_weight, engine_type)
    elif plane_type == "prop":
        aircraft_range = range_endurace.prop_range_calc(velocity, ld, takeoff_weight, fuel_weight, engine_type)
        aircraft_endurance = range_endurace.prop_endurance_calc(velocity, rho, s_wing, cl, cd, takeoff_weight, fuel_weight, engine_type)
    print(aircraft_range)
    print(aircraft_endurance)
    return jsonify({
        "range": aircraft_range/5280,
        "endurance": aircraft_endurance/60/60,
    })

@app.route("/populate_wing", methods=["POST"])
def populate_wing():
    from matplotlib.figure import Figure
    import io
    import base64

    data = request.get_json()
    sections = data.get("sections", [])

    if not sections:
        return jsonify({"error": "No section data provided"}), 400

    # Save to session
    session["wing_sections"] = sections

    # Plot
    fig = Figure()
    ax = fig.subplots()

    x_le = [s["x"] for s in sections]
    y_le = [s["y"] for s in sections]
    x_te = [s["x"] + s["chord"] for s in sections]
    y_te = y_le

    # Apply 90-degree clockwise rotation: (x, y) → (y, -x)
    rot_x_le = y_le
    rot_y_le = [-x for x in x_le]
    rot_x_te = y_te
    rot_y_te = [-x for x in x_te]

    x_outline = rot_x_le + rot_x_te[::-1] + [rot_x_le[0]]
    y_outline = rot_y_le + rot_y_te[::-1] + [rot_y_le[0]]

    ax.fill(x_outline, y_outline, color="skyblue", edgecolor="black", alpha=0.6)
    ax.plot(x_outline, y_outline, "k-")
    ax.set_title("Wing Geometry (Right side)")
    ax.set_xlabel("Y (ft)")
    ax.set_ylabel("X (ft)")

    ax.set_aspect("equal")
    ax.grid(True)

    # Encode to base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return jsonify({"image": f"data:image/png;base64,{img_base64}"})



# uncomment before pushing #change
if __name__ == "__main__":
    app.run
application = app

# comment before pushing
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)