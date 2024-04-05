import numpy as np

#need Re

def calcCf(re,mach):
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


    cfm=np.array([0, 0, 0, 0, 0])
    # Calculate Cf for a given Re, for the Mach number ranges with data
    for i in range(5):
        cfm[i]=a[i]+b[i]*np.log(re)+c[i]/np.log(re)+d[i]/(re**2)


    # interpolate from Mach number data to find Cf for given Mach 
    cf= np.interp(mach, m, cfm, left=None, right=None, period=None)
    return cf

def calcRls(mach,sweep):
    # Lifting Surface Correction Factor
    coswp=np.cos(sweep*np.pi/180.0)
    # Calculate Rls based on sweep and Mach #
    # From Roskam (Fig. 4.2) && DATCOM (Fig 4.1.5.1-28b)

    # Curve Fit Coeffs for Mach=0.0, 0.25, 0.6, 0.8, and 0.9
    # from http://arohatgi.info/WebPlotDigitizer/app/
    m = np.array([0.25, 0.6, 0.8, 0.9])
    a = np.array([-4.4363748875679, -1.3980668095706, -3.7024275413330, -2.5098065762271])
    b = np.array([37.4515358769251, 16.6308626837892, 32.6444107064539, 24.1862175399295])
    c = np.array([-108.6958023553826, -51.6354467265998, -92.5961436816895, -66.8522534839584])
    d = np.array([157.8327607721516, 81.3412404781636, 132.1057774251434, 93.4885564152735])
    e = np.array([-111.9494230798703, -61.6248216450456, -92.2697362481424, -63.8412329193048])
    f = np.array([30.8640121878326, 17.8367311969906, 25.0753189387920, 16.8857580964143])

    rlsm=np.array([0, 0, 0, 0])
    # loop through Mach #s and calculate Cf for a given Re
    for i in range(0,3):
        rlsm[i]=a[i]+b[i]*(coswp)+c[i]*(coswp**2)+d[i]*(coswp**3)+e[i]*(coswp**4)+f[i]*(coswp**5)

    # interpolate for final Cf based on mach #
    rls = np.interp(mach, m, rlsm, left=np.nan, right=np.nan)
    return rls

def CalcLparam(maxtcloc):
    #
    # routine to determine L_param DATCOM page 4.1.5.1-2
    #
    param=0
    if(maxtcloc >= 0.30):
        param=1.2

    if(maxtcloc < 0.30):
        param=2.0
    

    L_param=param
    return L_param

def CalcCDow(cf,rls,L_param,tc_avg,sref,swet):

    # calculate CDow: Subsonic DATCOM 4.1.5.1-a
    CDo_vtail = cf*(1 + L_param*tc_avg + 100*(tc_avg)**4)*rls*(swet/sref)
    return CDo_vtail

