import numpy as np
import CalcLparam

def trans_calcCf(re,mach):
    # Calculate Skin Friction Coefficient: Cf based on Re and Mach #
    # From Roskam (Fig. 4.3 Turbulent Mean Skin Friction Coefficient)
    # Copied From DATCOM report

    # Curve Fit Coeffs for Mach=0.0, 0.3, 0.7, 0.9, and 1.0 
    # data extracted from plot (Mach 1.5-3.0 ignored)

    #smooth surface, ignore effects of k

    m = np.array([0.0, 0.3, 0.7, 0.9, 1.0])
    a = np.array([-0.0149707777, -0.015459984, -0.014293646, -0.013678702, -0.01352922])
    b = np.array([0.00031324979, 0.0003275811, 0.00029737175, 0.00028215683, 0.00027862711])
    c = np.array([0.20871616, 0.21209476, 0.19996085, 0.19313828, 0.19090034])
    d = np.array([8511410.2, 3123020.6, 6835568.1, 7239508.8, 6777808.5])

    cfm = np.zeros(5)
    # Calculate Cf for a given Re, for the Mach number ranges with data
    for i in range(5):
        cfm[i]=a[i]+b[i]*np.log(re)+c[i]/np.log(re)+d[i]/(re^2)

    # interpolate from Mach number data to find Cf for given Mach 
    cf= np.interp(mach, m, cfm, left=None, right=None, period=None)
    return cf

def CalcCDow_transonic(cf,tc_max_loc_v,tc_avg,sref,swet):
    L_param = CalcLparam.CalcLparam(tc_max_loc_v)
    # calculate CDow: Subsonic DATCOM 4.1.5.1-a

    CDo_vtail = cf*(1 + L_param*tc_avg)*(swet/sref)
    return CDo_vtail

def CalcCDwave(mach,Weight,vinf,rho,Sweep,tcmax,ctip,croot,Wsref,Span):
    #
    # Calculate Wing Wave Drag 
    # from Gur, Mason, and Schetz
    # "Full-Configuration Drag Estimation" Journal of Aircraft Vol. 47, No. 4
    # July-August 2010
    #
    #
    # ka=0.95 for supercritical  sections, 0.87 for conventional 
    #
    ka=0.95
    #
    # Calculate Lift Coefficient based on Weight and q
    CL=Weight/(0.5*rho*vinf*vinf*Wsref)
    #
    #
    # Calculate 1/2 chord sweep and Leading Edge Sweep
    #
    Sweep2=(180.0/np.pi)*np.arctan(((Span/2)*np.tan(Sweep*np.pi/180)+0.25*ctip-0.25*croot)/(Span/2))
    #
    # Calculate Mdd
    #
    Mdd=(ka-CL/(10*(np.cos(Sweep2*np.pi/180))^2)-tcmax/(np.cos(Sweep2*np.pi/180)))/(np.cos(Sweep2*np.pi/180))
    #
    # Calculate Mcr
    #
    Mcr=Mdd-(0.1/80)^(1/3)
    #
    # Calculate CDwave
    #
    CDwave=0
    if (mach <= Mcr):
        CDwave=0
    if (mach > Mcr):
        CDwave=20*((mach-Mcr)^4)
    CDw_vtail = CDwave
    return CDw_vtail

def CDo_trans(CDw_vtail, CDo_vtail):
    CDo_trans = CDw_vtail + CDo_vtail
    return CDo_trans