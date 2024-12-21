import numpy as np

#need to figure what is "interp1"


#Variables used

c_root_deg = 3 #deg #side view
Rootdeg = c_root_deg
c_tip_deg = -3 #deg #side view
Tipdeg = c_tip_deg



### Induced Drag

#given Mach Number, h

#V_true=Mach*acoustV
#RefArea
#CurrentWeight

def CL_calc(W, rho, V, sref):
    CL = W / rho / V / V /sref * 2
    return CL

def CL_w_eta_t(CL,Tipdeg,Rootdeg):
    # Routine to calculate Wing induced drag coefficient 
    # from Roskam section 4.2.1.2 CDLw
    # Calculate Lift Coefficient based on Weight and q
    CL_w=1.05*CL
    # Calculate Linear Twist Parameter Et
    eta_t=Tipdeg-Rootdeg
    return CL, CL_w, eta_t

def CL_alpha_w(mach,Span,ctip,croot,Cl_alpha,AR,Sweep):
    # Convert Cla from per/deg to per/rad
    Cl_alpha=Cl_alpha*180/np.pi
    # Calculate 1/2 chord sweep and Leading Edge Sweep
    Sweep_1_2=(180.0/np.pi)*np.arctan(((Span/2)*np.tan(Sweep*np.pi/180)+0.25*ctip-0.25*croot)/(Span/2))
    # Calculate Mach Correction Factor
    beta=np.sqrt((1-mach**2))
    # Calculate k factor
    k=(Cl_alpha/beta)/(2*np.pi/beta)
    # Calculate CLaw from equation 8.22
    CL_alpha_w=(2*np.pi*AR/(2+np.sqrt((AR**2*beta**2/k**2)*(1+(np.tan(Sweep_1_2*np.pi/180))**2/(beta**2))+4)))*np.pi/180
    return CL_alpha_w

def R_LE_suct_param(mach,rho,vinf,rle,mu,AR,Span,Sweep,ctip,croot):
    Sweep_LE=(180.0/np.pi)*np.arctan(((Span/2)*np.tan(Sweep*np.pi/180)-0.25*ctip+0.25*croot)/(Span/2))
    # Calculate Leading Edge Radius Suction Parameter (Roskam Fig. 4.7)
    Rele=(rho*vinf*rle/mu)*1/(np.tan(Sweep_LE*np.pi/180))*np.sqrt(1-mach**2*(np.cos(Sweep_LE*np.pi/180))**2) #cot doesn't work
    # Determine which Roskam fig. 4.7 to use based on Rele value
    # and then calculate Leanding Edge Suction Ratio parameter
    Rsucrat=0
    taper=ctip/croot
    ARLambda=AR*taper/np.cos(Sweep_LE*np.pi/180)
    R=np.zeros(5)
    if (Rele>=1.3e+5):
        Rsucrat=(0.8631975+0.65931724*ARLambda-0.015271903*ARLambda**2)/(1+0.66823168*ARLambda-0.016799564*ARLambda**2+0.00010212808*ARLambda**3)
    if (Rele<1.3e+5):
        a = np.array([2.7634696, 2.9327777, 2.9047627, 2.9589507, 2.9826368])
        b = np.array([-2.2982392e-6, -3.1016726e-6, -2.9207766e-6, -3.2819458e-6, -3.3531771e-6])
        c = np.array([1.068842e-14, 6.272409e-14, 5.6825808e-14, 8.4043421e-14, 8.7552799e-14])
        d = np.array([1.0830434e-17, -9.9684685e-17, -8.9818861e-17, -1.4874644e-16, -1.5513286e-16])
        e = np.array([-19.774724, -20.944706, -20.495264, -20.770602, -20.826379])
        for i in range(0,5):
            R[i]=a[i]+b[i]*Rele+c[i]*Rele**2.5+d[i]*Rele**3+e[i]/np.log(Rele)
        ARLam = np.array([0, 1, 2, 4, 10])
        Rsucrat=np.interp(ARLambda, ARLam, R)
    R_LE_suct_param=Rsucrat
    return R_LE_suct_param

def v_w_factor(AR,mach,Sweep,taper):
    ##  Generate lift induced drag factor (v) due to linear twist
    # from Roskam Fig. 4.9a
    import numpy as np

    a = np.array([[-0.00015409894, -0.00052920937, -0.0003708111, 0.00067802995],
                [-0.00027946484, -0.00078653643, -0.00116592, 9.4498124e-5],
                [-0.00034347775, -0.001017145, -0.0014012178, -7.7679156e-5],
                [-0.00024511592, -0.0012403199, -0.0015560798, -0.0005724915],
                [-0.00040770148, -0.001489559, -0.0019631434, -0.00011651238],
                [-0.00054376314, -0.0018406751, -0.0021800671, -0.00040414573],
                [-0.0007896756, -0.0018327209, -0.0024538711, -0.0004099083]])

    b = np.array([[-0.0011687925, -0.00019529117, 6.1443652e-5, -0.00017405715],
                [-0.00067178771, 0.00026424644, 0.0010038484, 0.00089581566],
                [-0.00036864528, 0.00065134647, 0.0014582919, 0.0015197275],
                [-0.00024880431, 0.001085384, 0.0018078866, 0.0022752518],
                [5.9598833e-7, 0.0013202793, 0.0022891063, 0.0025416537],
                [0.00036797738, 0.0019352653, 0.0028492321, 0.0034065521],
                [0.00076774237, 0.0021744023, 0.0035522759, 0.0038933402]])

    c = np.array([[0.00015018746, -2.8267732e-6, -4.3337941e-5, -2.0595988e-5],
                [7.8671093e-5, -3.3885884e-5, -0.00018213742, -0.00019089179],
                [4.8119138e-5, -7.6207415e-5, -0.00022821202, -0.00028221837],
                [4.9615497e-5, -0.00014095739, -0.00026758263, -0.00040481804],
                [2.8778295e-5, -0.00015418689, -0.00033095354, -0.00046180673],
                [5.9835483e-7, -0.00023631398, -0.00038943384, -0.00058314743],
                [-4.2725339e-5, -0.00024181392, -0.00051956829, -0.00064249741]])

    d = np.array([[-8.4877088e-6, 1.2995414e-6, 3.6839881e-6, 3.2030845e-6],
                [-3.8944128e-6, 9.6660988e-7, 1.2614469e-5, 1.4041685e-5],
                [-2.5425681e-6, 3.4100476e-6, 1.4359855e-5, 1.9628038e-5],
                [-3.1613828e-6, 7.8361163e-6, 1.6710025e-5, 2.7786664e-5],
                [-2.8178978e-6, 7.9819761e-6, 2.0315118e-5, 3.31166e-5],
                [-1.8335434e-6, 1.3212051e-5, 2.2814589e-5, 3.9699562e-5],
                [2.705878e-7, 1.1998513e-5, 3.3145485e-5, 4.2005172e-5]])

    e = np.array([[1.8202834e-7, -4.0359432e-8, -8.7697084e-8, -1.0202601e-7],
                [7.2457911e-8, 1.4659888e-8, -3.0501117e-7, -3.5335013e-7],
                [5.1282743e-8, -4.9264645e-8, -3.2357149e-7, -4.7781215e-7],
                [6.4316753e-8, -1.6134406e-7, -3.9013751e-7, -6.7465838e-7],
                [8.2071491e-8, -1.5913253e-7, -4.6597284e-7, -8.5349599e-7],
                [6.4554576e-8, -2.8601178e-7, -5.0211002e-7, -9.7071311e-7],
                [2.9625062e-8, -2.2881023e-7, -7.9260142e-7, -9.7820984e-7]])

    _lambda = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]) #vars name is orginally "lambda" but that is not allow in python

    sweepparam=np.array([0, 30, 45, 60])
    beta=np.sqrt((1-mach**2))
    betaAR=beta*AR
    sweeptan=np.arctan(np.tan(Sweep*np.pi/180)/beta)*180/np.pi
    # loop through all taper ratios and sweep paraemters to generate v's
    vbase = np.zeros((7,4))
    
    for i in range(7):
        for j in range(4):
            vbase[i][j]=a[i][j]+b[i][j]*betaAR+c[i][j]*betaAR**2+d[i][j]*betaAR**3+e[i][j]*betaAR**4

    # interpolate based on sweep parameter for each taper ratio
    vmid=np.zeros(7)
    vmid = np.array([np.interp(sweeptan, sweepparam, vbase[i, :]) for i in range(vbase.shape[0])]) # chatgpt translation

    #print(vmid)    
    # do final interpolation for v (induced drag factor due to linear twist)
    v = np.interp(taper, _lambda, vmid)

    ##  Generate zero lift drag factor (w) due to linear twist
    # from Roskam Fig. 4.10
    #
    a = np.array([[-2.537141e-5, -7.1542796e-5, 2.4625866e-6, 0.00026429692],
                [-0.00014747191, -0.00018090834, -0.00012117113, 0.00018095563],
                [-0.00014042165, -0.00021950903, -0.00015070721, 0.00013025583],
                [-0.00012668309, -0.00011892872, -0.00012609671, 0.00019915061],
                [-0.00014510163, -0.0001657092, -0.00013051248, 0.00017515605],
                [-0.00014027909, -0.00025252253, -0.00013318089, 0.00022161007],
                [-4.1709909e-5, -8.7557317e-5, -9.8642076e-5, 0.00016456666]])

    b = np.array([[0.00054887716, 0.00059687263, 0.0005759761, 0.00038570995],
                [0.00062647913, 0.00065387389, 0.00065242907, 0.00048253976],
                [0.00061936789, 0.00069114272, 0.00068422952, 0.00051628353],
                [0.00062545607, 0.00063232826, 0.00068051276, 0.00048891332],
                [0.00064077013, 0.0006670118, 0.00067937604, 0.00052060705],
                [0.00061634954, 0.00072146042, 0.0006677402, 0.00046853966],
                [0.00056127727, 0.0006140573, 0.00066374085, 0.00051659595]])

    c = np.array([[-6.3441527e-5, -7.7000618e-5, -8.5105971e-5, -6.5538693e-5],
                [-7.1355722e-5, -7.6610529e-5, -8.9761814e-5, -8.1662302e-5],
                [-6.4528149e-5, -8.3478762e-5, -9.4151096e-5, -8.4600917e-5],
                [-6.5298492e-5, -6.903935e-5, -9.2883175e-5, -7.7259995e-5],
                [-6.8106098e-5, -7.5923398e-5, -9.0567672e-5, -8.4769936e-5],
                [-5.9385364e-5, -8.8793102e-5, -8.7002311e-5, -7.0391041e-5],
                [-5.0242003e-5, -6.6287268e-5, -9.0548495e-5, -8.3760511e-5]])

    d = np.array([[3.3902937e-6, 4.2357828e-6, 5.1356194e-6, 4.2055035e-6],
                [3.8050778e-6, 3.7494115e-6, 5.0733782e-6, 5.3282878e-6],
                [3.1147461e-6, 4.5109558e-6, 5.4752810e-6, 5.4681650e-6],
                [3.2480764e-6, 3.2683384e-6, 5.4850477e-6, 4.7970985e-6],
                [3.5174380e-6, 3.8797967e-6, 5.2079653e-6, 5.5546683e-6],
                [2.5929761e-6, 5.0998832e-6, 4.9614312e-6, 4.1595920e-6],
                [1.9725061e-6, 3.1464996e-6, 5.4654796e-6, 5.5161038e-6]])

    e = np.array([[-7.3215757e-8, -8.6591196e-8, -1.1240819e-7, -9.5364761e-8],
                [-8.0749688e-8, -6.6538864e-8, -1.0402373e-7, -1.2369681e-7],
                [-6.1297374e-8, -9.5231372e-8, -1.1793121e-7, -1.2641296e-7],
                [-6.7097016e-8, -5.9019688e-8, -1.2368361e-7, -1.0739950e-7],
                [-7.5421788e-8, -7.7730343e-8, -1.1402626e-7, -1.3327333e-7],
                [-4.4795515e-8, -1.1573128e-7, -1.0944079e-7, -8.7899251e-8],
                [-2.9473417e-8, -5.6522676e-8, -1.2603950e-7, -1.3206249e-7]])


    # loop through all taper ratios and sweep paraemters to generate w's

    bwbase = np.zeros((7,4))

    for i in range(0,6):
        for j in range(0,3):
            bwbase[i][j]=a[i][j]+b[i][j]*betaAR+c[i][j]*betaAR**2+d[i][j]*betaAR**3+e[i][j]*betaAR**4

    # interpolate based on sweep parameter for each taper ratio

    bwmid=np.zeros(7)
    bwmid = np.array([np.interp(sweeptan, sweepparam, bwbase[i, :]) for i in range(bwbase.shape[0])]) # chatgpt translation

    # do final interpolation for w (zero lift drag factor due to linear twist)

    bw = np.interp(taper, _lambda, bwmid) # chatgpt translation
    w=bw/beta
    return v,w

def spaneff_factor(CL_alpha_w,AR,R_LE_suct_param):
    spaneff=1.1*((CL_alpha_w*180/np.pi)/AR)/(R_LE_suct_param*((CL_alpha_w*180/np.pi)/AR)+(1-R_LE_suct_param)*np.pi)
    return spaneff

def CDi_wing_calc(mach, AR, Sweep, taper, rho, vinf, rle, mu, Span, ctip, croot, Cl_alpha, W, sref):
    v, w = v_w_factor(AR,mach,Sweep,taper)
    CL = CL_calc(W, rho, vinf, sref)
    CL, CL_w, eta_t = CL_w_eta_t(CL,Tipdeg,Rootdeg)
    R_LE_suct_param_val = R_LE_suct_param(mach,rho,vinf,rle,mu,AR,Span,Sweep,ctip,croot)
    CL_alpha_w_val = CL_alpha_w(mach,Span,ctip,croot,Cl_alpha,AR,Sweep)
    spaneff = spaneff_factor(CL_alpha_w_val,AR,R_LE_suct_param_val)
    
    CDiw=(CL_w**2)/(np.pi*AR*spaneff)+2*np.pi*CL_w*(eta_t*np.pi/180)*v + 4*np.pi*np.pi*(eta_t*np.pi/180)**2*w
    return CDiw

def induced_drag_htail(AR_H,Sref_H,Wsref,W,rho,vinf):
    #eH=0.7 #mounted on vertical tail
    eH=0.5 #mounted on body
    CL = CL_calc(W, rho, vinf, Wsref)
    CL_h  = -CL*0.05*(Sref_H/Wsref)
    CDi_h=(CL_h**2)/(np.pi*AR_H*eH)
    return CDi_h

def fuse_induced_drag(Clo,lfus,dfus,mach,Wsref,Sfplan,Sb_fuse,W, rho, vinf,Span,ctip,croot,Cl_alpha,AR,Sweep):
    # Calculate CDi for the fuselage
    # From Roskam Section 4.3.1.2
    # make a guess at fuselage alpha
    CL = CL_calc(W, rho, vinf, Wsref)
    CL_alpha_w_val = CL_alpha_w(mach,Span,ctip,croot,Cl_alpha,AR,Sweep)
    alpha=((CL - Clo)/CL_alpha_w_val)
    #
    # Calculate eta factor from Roskam fig. 4.19 based on body fineness ratio
    finrat=lfus/dfus
    eta=(0.499143362+0.065895723*finrat)/(1+0.067781450*finrat+8.41117e-5*finrat**2)
    #
    # Calculate Cdc from Roskam Fig. 4.20 based on cross flow Mach #
    Mc=mach*np.sin(alpha)
    Cdc=(1.203614020-3.00344153*Mc+2.519748833*Mc**2)/(1-2.45791587*Mc+1.936359670*Mc**2-0.07623664*Mc**3)
    #
    # Finally calculate fuselage induced drag: CDLfus

    if mach >= 0.8:
        CDi_fus= (alpha*np.pi/180)**2*(Sb_fuse/Wsref)
    else:
        CDi_fus=2*(alpha*np.pi/180)**2*(Sb_fuse/Wsref) + eta*Cdc*(abs(alpha*np.pi/180))**3*(Sfplan/Wsref)
    return CDi_fus

    