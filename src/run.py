

from insertWCS import insertWCS

def main( image ):

    insertWCS( fileName=image, lowarcsec=0.55, higharcsec=0.60, location_of_index_files='/dap/b_insert_wcs/cfg/astrometryGaia.cfg')

if __name__ == '__main__':


    image = '/dap_data/2023_DZ2/2023_03_21/working/012025_0013_2023_DZ2_REDUCED.fits'

    main( image )