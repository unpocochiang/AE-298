import numpy as np
import CDo_htail
import CDo_vtail
import fcn

tc_average = 0.6

def check_pylon_arrangement(pylon_arrangement):
    horiz=1
    vert=0

    if pylon_arrangement == 1:
        horiz=1
        vert=0
    else:
        horiz=0
        vert=1
    return horiz, vert

def Est_pylon_wet_area(t_nac, dn,l_py):
    w_py = abs((t_nac - .5*dn))

    S_wet_pylon = 2*l_py*w_py
    return S_wet_pylon, w_py

def sub_htail_Cdo(re, mach, sref, swet, tc_avg, sweep):
    cf = CDo_htail.calcCf(re,mach)
    rls = CDo_htail.calcRls(mach,sweep)
    L_param = 1.2
    CDo_htail_val = CDo_htail.CalcCDow(cf,rls,L_param,tc_avg,sref,swet)
    return CDo_htail_val

def trans_htail_Cdo_Cdw(re, tc_avg, sref, swet, mach, weight, vinf, rho, htail_sweep, tcmax, ctip, croot, span):
    cf = CDo_htail.trans_calcCf(re,mach)
    rls = CDo_htail.calcRls(mach, htail_sweep)
    
    tc_max_loc_h = 0.4 # this will make L_param be 1.2 (based on 0018)(<--- not sure what this meant)
    CDo_htail_val = CDo_htail.CalcCDow(cf,rls,tc_max_loc_h,tc_avg,sref,swet)
    
    CDw_htail = CDo_htail.CalcCDwave(mach,weight,vinf,rho,htail_sweep,tcmax,ctip,croot,sref,span)    
    CDo_trans = CDo_htail_val + CDw_htail
    return CDo_trans

def sub_vtail_Cdo(re, mach, sref, swet, tc_avg, sweep):
    cf = CDo_vtail.calcCf(re, mach)
    rls = CDo_vtail.calcRls(mach,sweep)
    L_param = 1.2
    CDo_vtail_val = CDo_vtail.CalcCDow(cf,rls,L_param,tc_avg,sref,swet)
    return CDo_vtail_val

def trans_vtail_Cdo_cdw(re, tc_avg, sref, swet, mach, weight, vinf, rho, sweep, tcmax, ctip, croot, span):
    cf = CDo_vtail.calcCf(re, mach)
    maxtcloc = 0.4
    CDo_vtail_trans_val = CDo_vtail.CalcCDow_transonic(cf,maxtcloc,tc_avg,sref,swet)
    CDw_vtail = CDo_vtail.CalcCDwave(mach,weight,vinf,rho,sweep,tcmax,ctip,croot,sref,span)
    return CDo_vtail_trans_val + CDw_vtail

def CDo_ply(num_ply, pylon_arrangement,t_nac, dn,l_py,re, mach, sref, tc_avg,weight,vinf, rho,ctip, croot):
    tc_avg = 0.06 #set value by Dr.Elle. Im not sure where it came from
    htail_sweep = 50
    vtail_sweep = 50
    tcmax = 0.15
    horiz, vert = check_pylon_arrangement(pylon_arrangement)
    swet, w_py= Est_pylon_wet_area(t_nac, dn,l_py)
    sub_htail_Cdo_val = sub_htail_Cdo(re, mach, sref, swet, tc_avg, htail_sweep)
    trans_htail_Cdo_Cdw_val = trans_htail_Cdo_Cdw(re, tc_avg, sref, swet, mach, weight, vinf, rho, htail_sweep, tcmax, ctip, croot, w_py)
    sub_vtail_Cdo_val = sub_vtail_Cdo(re, mach, sref, swet, tc_avg, vtail_sweep)
    trans_vtail_Cdo_cdw_val = trans_vtail_Cdo_cdw(re, tc_avg, sref, swet, mach, weight, vinf, rho, vtail_sweep, tcmax, ctip, croot, w_py)
    
    CDo_sub = (horiz*sub_htail_Cdo_val + vert*sub_vtail_Cdo_val) * num_ply
    CDo_trans = (horiz*trans_htail_Cdo_Cdw_val + vert*trans_vtail_Cdo_cdw_val) * num_ply
    CDo_ply = fcn.fcn(mach, CDo_sub, CDo_trans)
    return CDo_ply