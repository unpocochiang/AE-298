import numpy as np
def re(rho, u, L, mu, T):
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