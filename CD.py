import atmosphere_function
import numpy as np
import re_calc
import CDo_wing
import CDo_vtail
import CDo_htail
import CDo_fus
import CDo_nac
import CDo_ply
import CDi_wing
import CD_misc
import CD_lg

def total_cd_calc(takeoff_weight, m, alt, b_wing, S_wing, S_wet, c_bar, L_c_4_wing, tc_avg, tc_max_loc, tc_max, c_tip, c_root, c_l_alpha, 
            c_l_0, rle, l_fus, S_fus_plan_top, d_fus, S_fus_maxfront,
            c_root_h, c_tip_h, b_h, L_c_4_h, tc_max_loc_v, tc_avg_v, tc_max_v, tc_max_h, tc_avg_h,
            tc_max_loc_h, c_tip_v,c_root_v,b_v,L_c_4_v, L_gear_flatplate,s_lg_front, S_h, NumNac, 
            l_nac, d_nac, S_nac_maxfront, t_nac, NumPyl, pylon_arrangement, w_py, l_pyl,c_bar_v, c_bar_h,
            S_v_wet, S_h_wet, S_fus_wet, S_fus_b, AR, taper, AR_h):
    
    # Define values independent of mach, as we will iteratively define CDo_wing w/ mach
    altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = atmosphere_function.AtmosphereFunction(alt)
    re = re_calc.re(density, m, c_bar, visc, temp) # float for each mach
    vinf = m * speed_of_sound

    CDo_wing_val = CDo_wing.CDo_wing_calc(re, m, L_c_4_wing, tc_avg,S_wing,S_wet, tc_max_loc, takeoff_weight,
                                            vinf,density,tc_max,c_tip, c_root,S_wing,b_wing)
    re_v = re_calc.re(density, m, c_bar_v, visc, temp)                          
    CDo_vtail_val = CDo_vtail.CDo_vtail(re_v, m, L_c_4_v, tc_max_loc_v, tc_avg_v, S_wing, S_v_wet, takeoff_weight, 
                                        vinf,density,tc_max_v, c_tip_v, c_root_v, S_wing , b_v)
                                        #use S_wing now according to simulink, but I think it should be s_h 
    re_h = re_calc.re(density, m, c_bar_h, visc, temp)                               
    CDo_htail_val = CDo_htail.CDo_htail(re_h , m, L_c_4_h, tc_max_loc_h, tc_avg_h, S_wing, S_h_wet, takeoff_weight, vinf, 
                                        c_tip_h, c_root_h, b_h, S_wing, density, tc_max_h)      
                                        #use S_wing now according to simulink, but I think it should be s_h
                
    CDo_fus_val = CDo_fus.CDo_fus(re,m, l_fus, d_fus, S_fus_wet, S_wing, S_fus_maxfront)  

    CDi_wing_val = CDi_wing.CDi_wing_calc(m, AR, L_c_4_wing, taper, density, vinf, rle, visc, b_wing, c_tip, 
                                            c_root, c_l_alpha, takeoff_weight, S_wing)

    CDi_htail_val = CDi_wing.induced_drag_htail(AR_h,S_h,S_wing,takeoff_weight, density,vinf)

    CDi_fus_val = CDi_wing.fuse_induced_drag(c_l_0,l_fus,d_fus,m,S_wing, S_fus_plan_top,S_fus_b, takeoff_weight, 
                                                density, vinf, b_wing, c_tip, c_root,c_l_alpha, AR,L_c_4_wing)
    
    CDo_nac_val = CDo_nac.CDo_nac(re,m,NumNac,l_nac, d_nac, S_wing, S_nac_maxfront, t_nac)
    
    CDo_ply_val = CDo_ply.CDo_ply(NumPyl, pylon_arrangement, w_py, l_pyl,re, m, S_wing, takeoff_weight, vinf, density, l_pyl, l_pyl)

    # might need to double check with ERJ-Data
    CD_misc_cons = 0.05
    CD_misc_val = CD_misc.CD_misc_calc(CDo_ply_val, CDo_fus_val, CDo_wing_val, CDo_nac_val, CDo_vtail_val, CDo_htail_val, CD_misc_cons)
    #Missing Landing Gear Calculation
    CD_lg_val = CD_lg.cd_lg(L_gear_flatplate, s_lg_front)
    
    total_CD_val = CD_lg_val + CD_misc_val + CDi_fus_val + CDi_htail_val + CDi_wing_val + CDo_fus_val + CDo_htail_val + CDo_vtail_val + CDo_wing_val + CDo_nac_val + CDo_ply_val
    return total_CD_val
    