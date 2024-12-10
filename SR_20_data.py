import numpy as np
import CD_lg 

#Piper Archer 3 Geo Data
#Data received from https://www.aopa.org/news-and-media/all-news/1994/november/pilot/piper-archer-iii
#Data received from chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://longislandaviators.com/wp-content/uploads/2018/08/PA-28-181-POH-Archer-III.pdf

#Basic parameters

Length = 26.0 #ft
height = 8.9 #ft
takeoff_weight = 3150 #lbs

#Wing Data
b_wing = 38.3 #ft #verified
S_wing = 124.77473761335753 #ft^2 #verified
AR = (b_wing**2)/S_wing
S_wet = 258.5186025646079 #ft^2

c_bar =  3.6724345746649703 #ft
L_c_4_wing = 0.09024400112100135 #deg
tc_avg =  0.0655825 #ratio #thickness to chord ratio
tc_max_loc =  0.4276856 #percentage #from the leading edge
tc_max =  0.120477 #ratio

c_tip =  2.5745334204 #ft #chord at tip #
c_root = 4.7571242886 #ft #chord at root
taper = c_tip/c_root

#Airfoil Data
c_l_alpha = 0.0979866
c_l_0 = 0.194
rle = 0.0146

#Fuslage + Engine Data
l_fus = 26 #ft this include the tip of the propeller
#H_fus_max = 3.75 #ft
#H_fus_min =
#W_fus = 3.5 #ft
S_fus_wet = 162.31670670624257
d_fus = 4.1753667708 #ft
S_fus_maxfront = 11.943114360359544 #ft2 #front view
S_fus_plan = 61.332470212206374 #ft2
d_fus_b= 0.6490229538 #diamter of the fuselage at end of the tail #Note the tail is not really circular #top down view
S_fus_b = (d_fus_b**2)*(np.pi/4) #ft2 #equation written on Roskam Fig 4.17

#L_Engine = 3.69230769 #ft
#W_Engine = W_fus

#H_Stab Data

#H_Stab_Span = 11 + (21/24) #ft
#H_Stab_chord_max =
#H_Stab_chord_min =

#NACA 0012
c_root_h = 2.667578183 #ft #top view
c_tip_h = 1.7202031685  #ft #top view #not accurate
b_h = 6.2109188577#ft #APM
L_c_4_h =  4.335436975396782 #c/4, deg #top view
S_h = 26.67867873674511  #ft2 #APM #!!!Have to double check
AR_h = (b_h**2)/S_h 
taper_h = c_tip_h/c_root_h
tc_max_h = 0.09 #top view
tc_avg_h = 0.065
S_h_expo = 25.369405866633162
S_h_wet = S_h_expo*(1.977+0.52*tc_avg_h)# #ft2 # Eq 7.12 Raymer 6th Ed. 
tc_max_loc_h = 0.3 #top view of Vtail

#c_bar_h  = c_root_h * (2/3)*(1 + taper_h + taper_h**2)/(1+taper_h) #ft 


#V_Stab Data

#V_Stab_height =
#V_stab_width =
V_stab_area = 18.140359029204298 #ft^2
tc_max_v = 0.09 #top view #NACA0012
tc_avg_v = 0.065
tc_max_loc_v = 0.3 #top view
S_v_expo = 18.1207072743835
if tc_avg_v > 0.05:
    S_v_wet =  S_v_expo*(1.977+0.52*tc_avg_v)# #ft2 # Eq 7.12 Raymer 6th Ed.
else:
    S_v_wet =  S_v_expo*2.003# #ft2 # Eq 7.12 Raymer 6th Ed.

L_c_4_v = 29.93283736772014 #c/4, deg
c_tip_v = 1.3751525578 #ft #side view
c_root_v = 5.918554982795 #ft #side view #note: the root cacluated is slanted
b_v = 5.4809069029 #ft


#L_gear data use page 423 for drag calculations
L_gear_flatplate = CD_lg.flat_plate_area_calc(takeoff_weight,1)
#L_gear_flatplate=2.23 #Test value
#L_gear_flatplate = 8.40670836000000 #new landing gear flate plate area

#Landing Gear Geometry
#s_lg_front = 2.5432 #ft2
s_lg_front = 3.44245730403703 #ft2 #new val