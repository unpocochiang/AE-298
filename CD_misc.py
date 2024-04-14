def CD_misc_calc(CDo_pyl,CDo_fus,CDo_w,CDo_nac,CDo_vtail,CDo_htail,CD_misc_cons):
    CDo = CDo_pyl + CDo_fus + CDo_w + CDo_nac + CDo_vtail + CDo_htail

    CD_misc_a=CD_misc_cons*CDo
    # if mission ==7065 || 7070
    #     CDo_flaps=0.0074*1.1*0.8*(20*pi/180)
    #     CDi_flaps=0.14^2*(DCL_flaps)^2*cosd(Sweep)
    #     CD_LG=0.015
    #     CD_misc_a=CD_misc*CDo+CDo_flaps+CDi_flaps+CD_LG
    # end
    # 
    # if mission ==6738
    #     if h<1000
    #     CDo_flaps=0.0074*1.1*0.8*(20*pi/180)
    #     CDi_flaps=0.14^2*(DCL_flaps)^2*cosd(Sweep)
    #     CD_LG=0.015
    #     CD_misc_a=CD_misc*CDo+CDo_flaps+CDi_flaps+CD_LG
    #     else
    #         CD_misc_a=CD_misc*CDo
    #     end
    # end
    # 
    # if mission ==7465 || 7446
    #     CDo_flaps=0.0074*1.1*0.8*(30*pi/180)
    #     CDi_flaps=0.14^2*(DCL_flaps)^2*cosd(Sweep)
    #     CD_LG=0.015
    #     CD_misc_a=CD_misc*CDo+CDo_flaps+CDi_flaps+CD_LG
    # end

    CD_misc_actual=CD_misc_a
    return CD_misc_actual
