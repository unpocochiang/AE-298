import numpy as np

#Piper Archer 3 Geo Data
#Data received from https://www.aopa.org/news-and-media/all-news/1994/november/pilot/piper-archer-iii
#Data received from chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://longislandaviators.com/wp-content/uploads/2018/08/PA-28-181-POH-Archer-III.pdf

#Basic parameters

Length = 24.0 #ft
height = 7 +(1/3) #ft
takeoff_weight = 2550 #lbs

#Wing Data
b_wing = 35.5 #ft #verified
S_wing = 170 #ft^2 #verified

S_wet = 362.34 #ft^2

c_bar = 4.829 #ft
L_c_4_wing = 5.25 #ft
tc_avg = 0.124 #ratio
tc_max_loc = 0.141 #percentage #from the leading edge
tc_max = 0.104 #ratio

c_tip = 3.5 #ft #chord at tip #
c_root = 6 + (1/6) #ft #chord at root




#Fuslage + Engine Data

l_fus = 16.8 #ft
#H_fus_max = 3.75 #ft
#H_fus_min =
#W_fus = 3.5 #ft
S_fus_wet = (14427.8139+48.3790)/12/12*2
d_fus = 3.761694981/2+4.267672038/2 #ft
S_fus_maxfront = 7.24534170483938*2 #ft2 #front view
S_fus_plan = 31.2239431980914*2 #
d_fus_b= 1.25 #diamter of the fuselage at end of the tail #Note the tail is not really circular 
S_fus_b = (d_fus_b**2)*(np.pi/4) #ft2 #equation written on Roskam Fig 4.17

#L_Engine = 3.69230769 #ft
#W_Engine = W_fus

#H_Stab Data

#H_Stab_Span = 11 + (21/24) #ft
#H_Stab_chord_max =
#H_Stab_chord_min =

c_root_h = 16.858332177318598 - 14.28583225600806 #ft #top view
c_tip_h = 16.858332177318598 - 14.28583225600806  #ft #top view #not accurate
b_h = 12.9791667 #ft #APM
L_c_4_h = 0 #c/4, deg #top view
S_h = (16.858332177318598 - 14.28583225600806)*12.9791667 #ft2 #APM
AR_h = (b_h**2)/S_h 
taper_h = 1
tc_max_h = 0.06530633636363636  #top view
tc_avg_h = 0.1200344
S_h_wet = 68.08541736959069 #S_h_expo*(1.977+0.52*tc_avg_h)# #ft2 # Eq 7.12 Raymer 6th Ed. 
tc_max_loc_h = 0.3003177 #top view of Vtail

#c_bar_h  = c_root_h * (2/3)*(1 + taper_h + taper_h**2)/(1+taper_h) #ft 


#V_Stab Data

#V_Stab_height =
#V_stab_width =
V_stab_area = 11.08438 #ft^2 # My calculation shows the reference area to be 12.5945867091379
S_v_wet = 25.682414101748073 #S_v_expo*(1.977+0.52*tc_avg_v)# #ft2 # Eq 7.12 Raymer 6th Ed.
tc_max_v = 0.06530633636363636 #top view
tc_avg_v = 0.1200344
tc_max_loc_v = 0.3003177 #top view

#b_v = 18.166 #ft
 
#S_v = 174+55/144 #ft2 #APM
 
#L_c_4_v =  38.762 #c/4, deg
 
#c_root_v = 20.457 #ft #side view
 
#c_tip_v = 4.48 #ft #side view

#taper_v = c_tip_v/c_root_v
#S_v_expo= 195.088 #only one side, same as htail.
#tc_max_loc_v = 0.3003177 #top view

#c_bar_v  = c_root_v * (2/3)*(1 + taper_v + taper_v**2)/(1+taper_v) #ft


#L_gear data use page 423 for drag calculations
L_gear_flatplate = 1.161678

#Propeller data use thrust calculations
#Data received from https://www.sensenich.com/wp-content/uploads/2019/10/P4EA_R13-1.pdf
#Model: Sensenich 76EM8S14-0-62

Prop_dia = 6 + (1/3) #ft
Prop_thickness = (7/24) #ft
Prop_pitch = 5 + (1/6) #ft at 0.75 of the length from the center to the tip I recomend this site for the calculation in case data is inaccurate (https://vansairforce.net/threads/calculating-propeller-pitch.202266/)

Prop_hub_dia = 0.5 #ft
Prop_hub_thickness = 0.25 #ft


