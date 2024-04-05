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