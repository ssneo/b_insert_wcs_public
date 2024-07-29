

from insertWCS import insertWCS
import glob

def main( image ):

    #insertWCS( fileName=image, lowarcsec=0.55, higharcsec=0.65, location_of_index_files='/dap/b_insert_wcs/cfg/astrometryGaia_dr2.cfg')
    #insertWCS( fileName=image, lowarcsec=1.15, higharcsec=1.25, location_of_index_files='/dap/b_insert_wcs/cfg/astrometryGaia_dr2.cfg')
    #insertWCS( fileName=image, lowarcsec=1.15, higharcsec=1.25, location_of_index_files='/dap/b_insert_wcs/cfg/astrometry2Mass.cfg')
    #insertWCS( fileName=image, lowarcsec=2.00, higharcsec=4.00, location_of_index_files='/dap/b_insert_wcs/cfg/astrometry2Mass.cfg')
    insertWCS( fileName=image, lowarcsec=0.55, higharcsec=0.65, location_of_index_files='/dap/b_insert_wcs/cfg/astrometryGaia_dr2.cfg')
    #insertWCS( fileName=image, lowarcsec=0.55, higharcsec=0.65, location_of_index_files='/dap/b_insert_wcs/cfg/astrometryGaia_dr2_small_field.cfg')

if __name__ == '__main__':


    #image = '/dap_data/2023_DZ2/2023_03_21/working/012025_0013_2023_DZ2_REDUCED.fits'

    #image = '/dap_data/Yerkes_Plate_Vault/10B-161.fits'
    #image = '/dap_data/V518Cyg_07_11-001_60s_light_B.fit'
    #image = '/dap_data/V518Cyg_07_11-001_60s_light_B_2.fit'
    #image = '/dap_data/Yerkes_Images/381677-002_60s_light_V_c-2.fits'

    #image = '/dap_data/7_11_Calibration/2012FN62_07_11-001_30s_light_V_c.fits'

    #image = '/dap_data/SA107/working/SA107_2024-04-17_clear_-10_4x4x60s_0000.fit'
    #image = '/dap_data/7_11_Calibration/2012FN62_07_11-001_30s_light_V_c.fits'
    image = '/dap_data/7_11_Calibration/39796_07_11-001_60s_light_V_c.fits'
    #image = '/dap_data/7_11_Calibration/2012FN62_07_11-001_30s_light_V_c.fits'
    #image = '/dap_data/7_11_Calibration/415029_07_11-001_30s_light_V_c.fits'
    #image = '/dap_data/7_11_Calibration/481032_07_11-001_60s_light_V_c.fits'

    #image = '/dap_data/V518Cyg_07_13-007_60s_light_B.fit'
    #image = '/dap_data/V518Cyg_07_13-007_60s_light_B.fit'

    image_folder = '/dap_data/michelle_asteroids/2024-07-17/415029/'

    images = glob.glob( image_folder + "*c.fits")
    
    for im in images:
        #print (im)
        #stop

        main( im )