import numpy as np

# m file to read in aircraft input data for performance analysis
#
## ERJ-175
# Flight Condition Data
weight = 85517 #lbf
rle = 0.21 #leading edge radius #ft
#  Wing Data

b_wing = 93+11/12 #ft #APM 

S_wing = 783 #ft^2 #APM #Span
S_wingtip=65 #ft^2 # side view
S_wing_expo = 2*345.278 #ft^2

s_wet = 1313.9 # ft^2
L_c_4_wing = 22.86 #deg #c/4 - top view

c_root = 16.242 #ft #top view

c_tip = 4.314 #ft #top view

c_tip_winglet= 1.65 #ft #top view

taper = c_tip/c_root
taper_winglet=c_tip_winglet/c_root

d_r_2_t= 36.31# ft distance from root to tip #top view
d_r_2_wt=42.12 # ft distance from root to wingtip tip #top view

c_joint= 10.405 #ft #chord at joint #top view

c_joint_y_joint= 10.405 #ft #y at joint  #top view

m1 = (c_joint-c_root)/c_joint_y_joint
m2=(c_tip-c_joint)/d_r_2_t

#c_bar = (2/S_wing)*((c_joint_y_joint**3*m1**3/3 + c_joint_y_joint**2*c_root*m1 + c_joint_y_joint*c_root^2 + ((c_joint + m2*d_r_2_t)**3-(c_joint+m2*c_joint_y_joint)**3)/(3*m2))) #ft
c_bar = (2/S_wing)*((c_joint_y_joint**3*m1**3/3 + c_joint_y_joint**2*c_root*m1 + c_joint_y_joint*c_root**2 + ((c_joint + m2*d_r_2_t)**3-(c_joint+m2*c_joint_y_joint)**3)/(3*m2))) #ft

#Cmac_2 = c_root * (2/3)*(1 + taper + taper^2)/(1+taper)

tc_max = .14 #Reported

tc_avg = (2/3)*tc_max #Estimated

tc_max_loc = 0.4 #Estimated

cl_alpha=0.11 #Estimated from similar supercritical airfoil data

cl_o=0.50 #Estimated from similar supercritical airfoil data
 
c_root_deg = 3 #deg #side view
 
c_tip_deg = -3 #deg #side view

LE_radius = (10/343.5)*c_bar #ft from airfoil image view #Brazilian Papers
 
h_wing = 10.286/2+6.349/2 #ft #front view
 
AR = 11.2648 #n.d #APM

tc_max_tip=0.09 #estimated from side view

tau=tc_max/tc_max_tip



# Fuselage Data

l_fus = 103 +11/12 #ft #APM

d_fus_top=10.024 #ft #top view
d_fus_side= 11.354 #ft #side view
d_fus = d_fus_top/2 + d_fus_side/2 #ft

#dfus_tail =  #fuse diameter at tail

#wing wetted area needs dfus
S_wing_wet = 2*(S_wing - c_root*d_fus)*(1+0.25*(tc_max)*((1+tau+taper)/(1+taper)))#ft2
#S_wing_wet=S_wing_expo*(1.977+0.52*tc_avg)
S_fus_plan_top= 805.643 #ft^2 #top view
S_fus_plan = S_fus_plan_top #ft2
S_fus_plan_side=973.547#ft^2 #side view

#S_fus_wet = pi*d_fus*l_fus*((1-(2/(l_fus/d_fus))^2/3)*(1+(1/(l_fus/d_fus)^2))) #ft2 https://www.scribd.com/document/27851579/Class-II-Methodology-for-Drag-Estimation
S_fus_wet=3.4*(S_fus_plan_top+S_fus_plan_side)/2
d_fus_b_side=1.298 #ft #side view
d_fus_b_top=1.261 #ft #side view
d_fus_b=d_fus_b_side/2+d_fus_b_top/2
S_fus_b = (d_fus_b**2)*(np.pi/4) #ft2 #equation written on Roskam Fig 4.17

S_fus_maxfront = 106.421 #ft2 #front view


# Horizontal Stab Data

b_h = 32 +9/12 #ft #APM
 
S_h = 250+37/144 #ft2 #APM

L_c_4_h = 30.5 #c/4, deg #top view
 
c_root_h = 10 #ft #top view
 
c_tip_h =3.8  #ft #top view
 
tc_max_h = 0.08  #top view

tc_avg_h = (2/3)*tc_max_h 

taper_h = c_tip_h/c_root_h 
 
S_h_expo = 2*106.071 #ft^2 #top view only

S_h_wet = S_h_expo*(1.977+0.52*tc_avg_h)# #ft2 # Eq 7.12 Raymer 6th Ed.

c_bar_h  = c_root_h * (2/3)*(1 + taper_h + taper_h**2)/(1+taper_h) #ft 

tc_max_loc_h = .35 #top view of Vtail

AR_h = (b_h**2)/S_h 

# Vertical Stab Data

b_v = 18.166 #ft
 
S_v = 174+55/144 #ft2 #APM
 
L_c_4_v =  38.762 #c/4, deg
 
c_root_v = 20.457 #ft #side view
 
c_tip_v = 4.48 #ft #side view

taper_v = c_tip_v/c_root_v
 
tc_max_v = 0.08 #top view

tc_avg_v = (2/3)*tc_max_v 

S_v_expo= 195.088 #only one side, same as htail.

S_v_wet = S_v_expo*(1.977+0.52*tc_avg_v)# #ft2 # Eq 7.12 Raymer 6th Ed.

tc_max_loc_v =0.35 #top view

c_bar_v  = c_root_v * (2/3)*(1 + taper_v + taper_v**2)/(1+taper_v) #ft

# Nacelle Data

NumNac = 2
 
l_nac = 13.105 #ft #side view

d_nac_top= 5.456 #ft #top view
d_nac_side=5.417 #ft #side view
d_nac = d_nac_top/2+d_nac_side/2 #ft

S_nac_plan = 50.08 #ft2 #side view

S_nac_maxfront = 22.639 #ft2 #front view
t_nac = 3.381 #ft #front view

# Pylon Data

pylon_arrangement = 0 # 1: horiz pylon, 0: vert pylon

NumPyl = 2
 
l_pyl = 4.6 #ft #estimated from side view
 
S_pyl_expo=24.632 #ft^2 #side view
t_pyl=.4 #ft #Estimated Average
c_pyl=8 #ft #Estimated Average

S_pyl_wet = S_pyl_expo*(1.977+0.52*(t_pyl/c_pyl)) #ft2

LGf= 32.86312072#Landing Gear Eq. Flat Plate Area (ft^2)
#Flaps
S_flap=2*(36.715+9.020+30.193) #flap, inboard slat, outboard slats
cf_c=(1.514+2.901)/14.694 # at one chord location: c=14.694, c_f=2.901, c_slat=1.514

