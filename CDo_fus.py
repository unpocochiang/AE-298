import numpy as np
import fcn

def calcRe(l_fus, true_airspeed, density, kinematic_viscosity):
    re = (l_fus*true_airspeed*density)/kinematic_viscosity #double check not sure if I am right
    return re

def calcRwf(mach, re):
    # Wing Fuselage Interference Factor: Rwf
    # curve fits for Roskam Figure 4.1, Rwf versus Fuselage Re

    # mach #s for curve fits
    m = np.array([0.25, 0.40, 0.60, 0.70, 0.80, 0.85, 0.90])
    rwfm = np.zeros(7)

    # mach 0.25 curve fit
    rwfm[0]=(0.98738954-0.22335005*np.log(re)+0.0189956*(np.log(re))**2-0.00071991301*(np.log(re))**3+1.0258411e-5*(np.log(re))**4)/(1.0-0.22716486*np.log(re)+0.019401223*(np.log(re))**2-0.0007383189*(np.log(re))**3+1.0563041e-5*(np.log(re))**4)
    #
    # mach 0.40 curve fit
    rwfm[1]=(1.0499334-0.12161303*np.log(re)+0.0035277416*(np.log(re))**2)/(1.0-0.112725*np.log(re)+0.0029917867*(np.log(re))**2+1.091304e-5*(np.log(re))**3)
    #
    # mach 0.60 curve fit
    rwfm[2]=(0.86828712685455-0.18845483203009*np.log(re)+0.0153254133318254*(np.log(re))**2-0.00055346095362923*(np.log(re))**3+7.49008313386838e-6*(np.log(re))**4)/(1.0-0.22438644552757*np.log(re)+0.0192423512899198*(np.log(re))**2-0.000766748565364264*(np.log(re))**3+1.329171731769246e-5*(np.log(re))**4-6.3067958874473e-8*(np.log(re))**5)
    #
    # mach 0.70 curve fit
    rwfm[3]=(0.90322124-0.10780675*np.log(re)+0.0032322543*(np.log(re))**2)/(1.0-0.12386001*np.log(re)+0.0041251962*(np.log(re))**2-1.668079e-5*(np.log(re))**3)
    #
    # mach 0.80 curve fit
    rwfm[4]=(0.81875278-0.094299175*np.log(re)+0.0027309697*(np.log(re))**2)/(1.0-0.12335048*np.log(re)+0.0042868258*(np.log(re))**2-2.7863927e-5*(np.log(re))**3)
    #
    # mach 0.85 curve fit
    rwfm[5]=(0.94758681-0.21700704*np.log(re)+0.018794158*(np.log(re))**2-0.00072928383*(np.log(re))**3+1.0693582e-5*(np.log(re))**4)/(1.0-0.22764419*np.log(re)+0.01959818*(np.log(re))**2-0.00075606298*(np.log(re))**3+1.1024387e-5*(np.log(re))**4)
    #
    # mach 0.90 curve fit
    rwfm[6]=(0.94027346-0.21838712*np.log(re)+0.019174732*(np.log(re))**2-0.00075384048*(np.log(re))**3+1.1189366e-5*(np.log(re))**4)/(1.0-0.2304395*np.log(re)+0.020080209*(np.log(re))**2-0.00078380017*(np.log(re))**3+1.1556739e-5*(np.log(re))**4)
    #
    # interpolate for final Rwf based on mach #
    rwf = np.interp(mach, m, rwfm)
    return rwf

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


    cfm=np.zeros(5)
    # Calculate Cf for a given Re, for the Mach number ranges with data
    for i in range(5):
        cfm[i]=a[i]+b[i]*np.log(re)+c[i]/np.log(re)+d[i]/(re**2)


    # interpolate from Mach number data to find Cf for given Mach 
    cf= np.interp(mach, m, cfm)
    return cf

def calcCDofus(cf, rwf, l_fus, df, S_fus_wet, S_wing):

    # Calculate CDo for the fuselage from Roskam Section 4.3.1.1
    CDofus=rwf*cf*(1+60/((l_fus/df)**3)+0.0025*(l_fus/df))*(S_fus_wet/S_wing)
    return CDofus

def CD_fus_wave(mach,lfus,dfus,Sfus_maxfront,Wsref):

    finenessratio=lfus/dfus
    M1=np.array([[5.8451853,     0.11528099],
                [6.080223,      0.10606428],
                [6.503668,      0.09151056],
                [6.9751782,     0.08083471],
                [7.446778,      0.07064371],
                [7.871478,      0.06287787],
                [8.532561,      0.053168043],
                [9.241172,      0.044426996],
                [10.375737,     0.03470799],
                [11.652886,     0.027895316],
                [13.40325,      0.019618917],
                [15.391162,     0.01570156],
                [17.331726,     0.011785124],
                [18.893951,     0.010300276],
                [20.92957,      0.008321396],
                [22.965279,     0.0068273647],
                [24.90647,      0.0063048666]])

    M1_025=np.array([[5.803666,      0.14679706],
                    [6.0858727,     0.13660973],
                    [6.4620585,     0.12254178],
                    [6.9328513,     0.10798714],
                    [7.54542,       0.091975205],
                    [8.253134,      0.07838567],
                    [9.292465,      0.06575941],
                    [10.237101,     0.053134985],
                    [11.2773285,    0.04535721],
                    [12.459512,     0.03709183],
                    [13.73684,      0.031248853],
                    [15.818911,     0.024420569],
                    [17.61752,      0.020991735],
                    [19.084957,     0.019023875],
                    [20.599655,     0.016570248],
                    [22.304016,     0.015567493],
                    [24.102983,     0.014078054],
                    [24.954983,     0.012606978]])

    M1_05=np.array([[5.806984,      0.16473645],
                    [6.1827216,     0.14824426],
                    [6.5114694,     0.13369238],
                    [6.887476,      0.11865473],
                    [7.5469446,     0.10021763],
                    [8.349086,      0.085171714],
                    [9.293542,      0.07157759],
                    [10.049411,     0.06235078],
                    [10.852898,     0.054577593],
                    [11.798608,     0.04777135],
                    [13.3594885,    0.039013773],
                    [15.062683,     0.031707987],
                    [16.861021,     0.02682461],
                    [19.180193,     0.021931129],
                    [21.215542,     0.018497704],
                    [22.72997,      0.014589531],
                    [24.954983,     0.012606978]])

    M1_1=np.array([[5.763402,      0.18510102],
                    [6.044712,      0.1700652],
                    [6.4677978,     0.15357208],
                    [6.843625,      0.13756473],
                    [7.3142385,     0.122040406],
                    [7.926897,      0.106513314],
                    [8.303801,      0.09632415],
                    [8.964793,      0.08612948],
                    [9.8619,        0.072536275],
                    [10.901681,     0.06233425],
                    [12.698405,     0.0487236],
                    [13.928027,     0.040942147],
                    [15.0634,       0.035586778],
                    [16.672077,     0.029252525],
                    [17.997112,     0.025348026],
                    [19.653585,     0.021437097],
                    [21.168104,     0.018013773],
                    [22.256668,     0.015568411],
                    [23.866152,     0.013597796],
                    [25.00233,      0.012606061]])

    M1_2=np.array([[5.8133507,     0.1991607],
                    [6.235988,      0.18024334],
                    [6.658267,      0.15938659],
                    [7.1280737,     0.13949862],
                    [7.7872734,     0.11960698],
                    [8.588518,      0.09971258],
                    [9.626504,      0.07981359],
                    [10.760263,     0.065730944],
                    [11.658536,     0.05844077],
                    [12.887979,     0.049689624],
                    [14.259555,     0.041420568],
                    [15.678749,     0.03460514],
                    [17.098122,     0.028759412],
                    [19.038326,     0.022903582],
                    [21.073498,     0.018500458],
                    [22.682713,     0.015075298],
                    [24.907724,     0.013092746]])


    x=np.array([1, 1.025, 1.05, 1.1, 1.2])

    CD_wave_x1 = np.interp(finenessratio, M1[:, 0], M1[:, 1])
    
    CD_wave_x2 = np.interp(finenessratio, M1_025[:, 0], M1_025[:, 1])

    CD_wave_x3 = np.interp(finenessratio, M1_05[:, 0], M1_05[:, 1])

    CD_wave_x4 = np.interp(finenessratio, M1_1[:, 0], M1_1[:, 1])

    CD_wave_x5 = np.interp(finenessratio, M1_2[:, 0], M1_2[:, 1])

    CD_wave_x=np.array([CD_wave_x1, CD_wave_x2, CD_wave_x3, CD_wave_x4, CD_wave_x5])
    
    CD_fus_wave_test = np.interp(mach, x, CD_wave_x)
    print(f'CD_fus_wave_test={CD_fus_wave_test}')
    CD_fus_wave=max(CD_fus_wave_test,0)*Sfus_maxfront/Wsref
    return CD_fus_wave

def CDo_fus(re,mach,l_fus, df, S_fus_wet, S_wing,Sfus_maxfront):
    #Sfus_maxfront = Fuselage max frontal area
    cf = calcCf(re,mach)
    rwf = calcRwf(mach,re)
    sub_CDo = calcCDofus(cf, rwf, l_fus, df, S_fus_wet, S_wing)
    CDw = CD_fus_wave(mach,l_fus,df,Sfus_maxfront,S_wing)
    trans_CDo = CDw + sub_CDo
    CDo_fus_val = fcn.fcn(mach, sub_CDo, trans_CDo)
    return CDo_fus_val