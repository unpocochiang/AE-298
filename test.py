import atmosphere_function
import erj_data
import CDi_wing

h_G, h, T, P, rho, speed_of_sound,mu = atmosphere_function.AtmosphereFunction(40000)
mach = 0.6
vinf = mach * speed_of_sound

cdi_fus = CDi_wing.fuse_induced_drag(erj_data.cl_o,erj_data.l_fus,erj_data.d_fus,mach,erj_data.S_wing,erj_data.S_fus_plan,
                                     erj_data.S_fus_b,erj_data.weight, 
                                     rho, vinf, erj_data.b_wing,erj_data.c_tip, erj_data.c_root,erj_data.cl_alpha,
                                     erj_data.AR, erj_data.L_c_4_wing)
cdi_htail = CDi_wing.induced_drag_htail(erj_data.AR_h,erj_data.S_h, erj_data.S_wing,erj_data.weight,rho,vinf,)
cdi_wing = CDi_wing.CDi_wing_calc(mach, erj_data.AR, erj_data.L_c_4_wing, erj_data.taper, rho, vinf, erj_data.rle, mu, 
                                  erj_data.b_wing, erj_data.c_tip, erj_data.c_root, erj_data.cl_alpha, erj_data.weight, erj_data.S_wing)
cdi = cdi_htail + cdi_fus + cdi_wing
print(cdi)