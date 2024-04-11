def rho_calc(h):
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