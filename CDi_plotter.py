# Plots CDi_Wing
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import erj_data 
import CDi_wing

def Re(rho, u, L, mu, T):
    '''
    Determines Reynold's Number
    ------------
    Inputs:
    - Air density: rho [sl/ft^3]
        + Varies with altitude, THIS is where altitude comes in for our first plot
    - Velocity: u [Mach]
        + Assuming SSL, convert Mach to ft/s for Imperical calculations
    - Characteristic Length: L [ft]
        + For the wing's plot, this is the chord length of the plane
    - Dynamic Fluid Viscocity: mu [slug/s*ft]
        + For air assuming, foolishly, SSL conditions
    ------------
    Outputs:
    - Reynold's Number: Re
    '''
    ### Can CF make a CDo_wing with RE = 5286, get 0.3186

    gamma = 1.4 # for air
    R = 1716.59 # for air in imperial
    a = np.sqrt(gamma * R * T) # ft/s
    V = a * u # also in ft/s

    Re = rho * L * V / mu
    return Re

def rho(h):
    '''Returns density as a function of altitude!
    -------------
    Input:
    - Altitude: h [ft]
    -------------
    Output:
    - Density: rho [lb/ft^3]
    '''
    p0 = 2116.224 # lb/ft^2
    M = 28.96 / 453.592 # Molar Mass, dividing SI units by their converstions to imperial
    R = 1716.59 # used in Reynold's Number equation
    T0 = 518.67 # Rankine
    L = 0.0065 * 1.8 / 3.28084 # In Rankine / ft, temperature lapse rate

    rho = p0 * M / (R * T0 * (1 - L*h/T0))
    return rho

def AtmosphereFunction(h_G):          #Atmosphere Function
    r_e=3959*5280                     #miles to feet
    R=1716.5                          #ft2/R-sec
    g0=32.174                         #ft/s^2
    T0=518.69                         #deg R
    g_hG=g0*(r_e/(r_e+h_G))**2        #gravity acceleration based on geopotential altitude
    h=(r_e/(r_e+h_G))*h_G             #altitude from geopotential altitude and earth radius
    if h<36000:                       # standard atmosphere maths up until tropopause
        h0=0                          # initial altitude of comparison is sea level
        T0=518.69                     #deg R
        P0=2116.22                    #psf
        rho0=2.3769e-3                #slugs/ft3
        a1=-3.57/1000                 #deg R/ft
        T= T0 + a1*(h-h0)             # calculate temperature from linear distribution
        P= P0*(T/T0)**(-g0/(R*a1))    #pressure from temperature
        rho = rho0*(T/T0)**(-((g0/(R*a1))+1))       #density from temperature
    else:
        h0=36000                      #tropopause altitude (ft)
        P0=4.760119191888137e+2       #from anderson appendix B
        rho0=7.103559955456123e-4     #from running code at 36000
        T=389.99                      # constant temperature
        P= P0*np.exp((-g0/(R*T)*(h-h0)))            #pressure from temperature
        rho = rho0*np.exp(-(g0/(R*T)*(h-h0)))       #density from temperature
    mu0=3.62e-7                       # viscosity at SL
    a=np.sqrt(1.4*P/rho)              # speed of sound
    mu=mu0*(T/T0)**(1.5)*((T0+198.72)/(T+198.72))   # viscosity from temperature
    return [h_G, h, T, P, rho,a,mu]

# from profile_drag import calCf, calcRls, CalcLparam, CalcCDow

# Now we initialize our values, and calculate!
#mach = np.linspace(0.01, 0.8, 100) # Mach Number
mach = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.7])
# altitude = np.arange(0., 55000., 5000.) # ft
altitude = np.array([0., 5000., 10000., 15000, 20000, 25000, 30000])
mach_size = np.size(mach)



colors_xkcd = mcolors.XKCD_COLORS
color_list = [colors_xkcd['xkcd:red'],   colors_xkcd['xkcd:orange'], colors_xkcd['xkcd:purple'],      colors_xkcd['xkcd:apple green'],
              colors_xkcd['xkcd:azure'], colors_xkcd['xkcd:plum'],   colors_xkcd['xkcd:lime yellow'], colors_xkcd['xkcd:tomato red'],
              colors_xkcd['xkcd:mango'], colors_xkcd['xkcd:dusk'],   colors_xkcd['xkcd:bright cyan']]

# CDo_wing_list = [] (might be necessary to make this list? Probably not tho)

for i, alt in enumerate(altitude):
    # Initialize CDo_wing as array of the same size as mach
    CDi_wing_val = np.zeros_like(mach)
    # Define values independent of mach, as we will iteratively define CDo_wing w/ mach
    altitude, geo_alt, temp, pressure, density, speed_of_sound, visc = AtmosphereFunction(alt)

    print(f'Altitude: {alt}')

    # Iteratively define CDo_wing w/ mach
    for k, m in enumerate(mach):
        print(k)
        print(f'm:{m}')
        #span is b_wing
        #sweep is L_c_4_wing
        #vinf is true airspeed
        #sref and wref may be both s_wing
        # visc is just mu #kinematic viscosity
        vinf = m * speed_of_sound
        CDi_wing_val[k] = CDi_wing.CDi_wing_calc(m, erj_data.AR, erj_data.L_c_4_wing, erj_data.taper, density, vinf, erj_data.rle, visc, erj_data.b_wing, erj_data.c_tip, 
                                                 erj_data.c_root, erj_data.cl_alpha, erj_data.weight, erj_data.S_wing)
        
        #print(f'Mach: {m}')
        print(f'CDo_wing: {CDi_wing_val[k]}')
        
    # Plot each CDo_wing now that it has finished construction
    plt.plot(mach, CDi_wing_val, label=f'{alt} ft', color=color_list[i])

#plt.plot(0.5*np.ones(100), np.linspace(0.005, 0.03, 100), 'k--')
plt.title('CDi_wing') # gonna do some LaTeX stuff with this in a bit, but this is a proof of concept lol
plt.xlabel('Mach Number')
plt.ylabel('CDo_wing')
plt.legend()
plt.show()