import numpy as np
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
# Test push