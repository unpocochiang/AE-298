import numpy as np
import fcn

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
    cf= np.interp(mach, m, cfm, left=None, right=None, period=None)
    return cf

def CalcCDonac(numnac,cfnac,ln,dn,Wsref):

    # nac_param = (dn - .75*dn)/(2*ln)
    # Swet_nac = pi*ln*dn
    # CDonac= numnac*cfnac*(1 + 1.2*nac_param)*(Swet_nac/Wsref)
    Swet_nac = np.pi*ln*dn
    fr=ln/dn

    # FF= 1 + 1.5/fr**(1.5) + 7/fr**3 #Hoerner
    FF= 1 + 2.2/fr**(1.5) + 3.8/fr**3 # Torenbeak
    # FF= 1 + 0.0025*fr + 60/fr**3 # Raymer
    # FF= 1 + 2.8/fr**(1.5) + 3.8/fr**3 # Shevell

    CDonac= numnac*cfnac*FF*(Swet_nac/Wsref)
    return CDonac

def cdn_int(NoNac,Snac_maxfront,Wsref,t_nac,dnac):
    # Calculate CDn' from Roskam Fig 4.42
    # Assume CL=0 

    a = -1.1322525448425
    b = -1.1885419773080
    c = 56.6769678820883
    d = -227.5790146927701
    e = 391.9418006311096
    f = -318.5924478305004
    g = 100.3233768196473

    x=t_nac/dnac

    CDn_= a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5 + g*x**6
    CDn_=max(.06,CDn_)
    Fa2=0.5 #with local area ruling, assume true for transport aircraft
    # Fa2=1.0 #without local area ruling, asume false for transport aircraft

    cdn_int = NoNac*Fa2*(CDn_ - 0.05)*(Snac_maxfront/Wsref)
    return cdn_int

def CD_nac_wave(numnac,mach,ln,dn,Snac_maxfront,Wsref):


    # finenessratio=ln/dn
    # M1=[5.8451853	0.11528099
    # 6.080223	0.10606428
    # 6.503668	0.09151056
    # 6.9751782	0.08083471
    # 7.446778	0.07064371
    # 7.871478	0.06287787
    # 8.532561	0.053168043
    # 9.241172	0.044426996
    # 10.375737	0.03470799
    # 11.652886	0.027895316
    # 13.40325	0.019618917
    # 15.391162	0.01570156
    # 17.331726	0.011785124
    # 18.893951	0.010300276
    # 20.92957	0.008321396
    # 22.965279	0.0068273647
    # 24.90647	0.0063048666]
    # 
    # M1_025=[5.803666	0.14679706
    # 6.0858727	0.13660973
    # 6.4620585	0.12254178
    # 6.9328513	0.10798714
    # 7.54542	0.091975205
    # 8.253134	0.07838567
    # 9.292465	0.06575941
    # 10.237101	0.053134985
    # 11.2773285	0.04535721
    # 12.459512	0.03709183
    # 13.73684	0.031248853
    # 15.818911	0.024420569
    # 17.61752	0.020991735
    # 19.084957	0.019023875
    # 20.599655	0.016570248
    # 22.304016	0.015567493
    # 24.102983	0.014078054
    # 24.954983	0.012606978]
    # 
    # M1_05=[5.806984	0.16473645
    # 6.1827216	0.14824426
    # 6.5114694	0.13369238
    # 6.887476	0.11865473
    # 7.5469446	0.10021763
    # 8.349086	0.085171714
    # 9.293542	0.07157759
    # 10.049411	0.06235078
    # 10.852898	0.054577593
    # 11.798608	0.04777135
    # 13.3594885	0.039013773
    # 15.062683	0.031707987
    # 16.861021	0.02682461
    # 19.180193	0.021931129
    # 21.215542	0.018497704
    # 22.72997	0.014589531
    # 24.954983	0.012606978]
    # 
    # M1_1=[5.763402	0.18510102
    # 6.044712	0.1700652
    # 6.4677978	0.15357208
    # 6.843625	0.13756473
    # 7.3142385	0.122040406
    # 7.926897	0.106513314
    # 8.303801	0.09632415
    # 8.964793	0.08612948
    # 9.8619	0.072536275
    # 10.901681	0.06233425
    # 12.698405	0.0487236
    # 13.928027	0.040942147
    # 15.0634	0.035586778
    # 16.672077	0.029252525
    # 17.997112	0.025348026
    # 19.653585	0.021437097
    # 21.168104	0.018013773
    # 22.256668	0.015568411
    # 23.866152	0.013597796
    # 25.00233	0.012606061]
    # 
    # M1_2=[5.8133507	0.1991607
    # 6.235988	0.18024334
    # 6.658267	0.15938659
    # 7.1280737	0.13949862
    # 7.7872734	0.11960698
    # 8.588518	0.09971258
    # 9.626504	0.07981359
    # 10.760263	0.065730944
    # 11.658536	0.05844077
    # 12.887979	0.049689624
    # 14.259555	0.041420568
    # 15.678749	0.03460514
    # 17.098122	0.028759412
    # 19.038326	0.022903582
    # 21.073498	0.018500458
    # 22.682713	0.015075298
    # 24.907724	0.013092746]
    # 
    # 
    # x=[1 1.025 1.05 1.1 1.2]
    # 
    # CD_wave_x1 = interp1(M1(:,1),M1(:,2),finenessratio,'linear','extrap')
    # 
    # CD_wave_x2 = interp1(M1_025(:,1),M1_025(:,2),finenessratio,'linear','extrap')
    # 
    # CD_wave_x3 = interp1(M1_05(:,1),M1_05(:,2),finenessratio,'linear','extrap')
    # 
    # CD_wave_x4 = interp1(M1_1(:,1),M1_1(:,2),finenessratio,'linear','extrap')
    # 
    # CD_wave_x5 = interp1(M1_2(:,1),M1_2(:,2),finenessratio,'linear','extrap')
    # CD_wave_x=[CD_wave_x1 CD_wave_x2 CD_wave_x3 CD_wave_x4 CD_wave_x5]
    # 
    # CD_fus_wave_test = interp1(x,CD_wave_x,mach,'linear','extrap')
    # CD_nac_wave=numnac*max(CD_fus_wave_test,0)*Snac_maxfront/Wsref


    Mcr=0.7
    # Calculate CDwave
    CDwave=0
    if (mach <= Mcr):
        CDwave=0
    
    if (mach > Mcr):
        CDwave=20*((mach-Mcr)**4)*Snac_maxfront/Wsref
    CD_nac_wave=CDwave
    return CD_nac_wave

def CDo_nac(re,mach,numnac,ln,dn,Wsref,Snac_maxfront,t_nac):
    cf = calcCf(re,mach)
    CDonac_val = CalcCDonac(numnac,cf,ln,dn,Wsref)
    cdn_int_val = cdn_int(numnac,Snac_maxfront,Wsref,t_nac,dn)
    CDw_nac_val = CD_nac_wave(numnac,mach,ln,dn,Snac_maxfront,Wsref)

    CDo_sub = cdn_int_val + CDonac_val
    CDo_trans = cdn_int_val + CDonac_val + CDw_nac_val
    CDo_nac_val = fcn.fcn(mach,CDo_sub,CDo_trans)
    return CDo_nac_val