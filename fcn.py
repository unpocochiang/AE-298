def fcn(mach,CDo_sub,CDo_trans):
    Cdo=0
    if mach <=0.5:
        Cdo=CDo_sub
    elif mach >= 0.5 and mach <= 0.7:
        Wsub = -5*mach + 3.5
        Wtrans = 5*mach - 2.5
        Cdo = Wsub*CDo_sub + Wtrans*CDo_trans
    elif mach > 0.7:
        Cdo=CDo_trans
    CDo = Cdo
    return CDo