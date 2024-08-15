

import glob
from astropy.io import fits
import os
import shutil
import sys
from astropy.wcs import WCS
from astropy import units as u
import time
from datetime import datetime



def insertWCS( fileName=None, lowarcsec=None, higharcsec=None, location_of_index_files=None ):
    #fileNameWithoutEnding is the filename without the 4 or 5 digits of FIT, fit, FITS, or fits including the period before

    print (fileName)

    fileNameWithoutEnding = fileName.replace('.fits', '')
    fileNameWithoutEnding = fileNameWithoutEnding.replace('.fit', '')
    fileNameWithoutEnding = fileNameWithoutEnding.replace('.FIT', '')


    d1=fits.open('%s'%(fileName), ignore_missing_end=True)
    d1.close()
    h1=d1[0].header


    #w = WCS(h1)
    #sky = w.pixel_to_world(2048, 1024)
    #ra = sky.ra.hour
    #dec = sky.dec.deg
    #print (sky)
    #print (ra, dec)
    #stop

    #print h1
    #stop
    try:
        ra=h1['RA']
        dec=h1['DEC']
        
    except KeyError:

        try:
            ra=h1['OBJCTRA']
            dec=h1['OBJCTDEC']

        except KeyError: #it is possilbe that DECAM images will need these values to be extracted
            try:
                w = WCS(h1)
                sky = w.pixel_to_world(2048, 1024)
                ra = sky.ra.hour
                dec = sky.dec.deg

                ra = ra * 15.0 #the ra value is ra-hours not ra-deg

                ra = round(ra, 5)
                dec = round(dec, 5)

            except:
                overRide = True
                if overRide == True: #gives me an option to manually insert and ra/dec value
                    #ra = "20:50:51.0"
                    #dec = "+48:27:36"
                    ra = None
                    dec = None
                else:
                    print ('Cannot locate RA/DEC values in the header')
                    sys.exit()


    
        

    if type(ra) is str:
        ra=ra.replace(" ",":")
        dec=dec.replace(" ",":")


        

    #print (ra, dec)
    #print (rahms, dedms)
    #print (filename)
    #print (lowarcsec, higharcsec)
    #stop
    #not used, but an example incase you need a different cfg file.
    #os.system('solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 0.5 --cpulimit 10 --no-plots  --config /usr/local/astrometry/etc/backend.cfg %s'%(lowarcsec, higharcsec, ra, dec, filename)) #backend.cfg is the Gaia database

    #the gaia database is the only database loaded.
    #submis = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 0.1 --cpulimit 5 --no-plots --skip-solved %s'%(lowarcsec, higharcsec, ra, dec, filename)

    #submis = 'solve-field  --scale-units arcsecperpix --scale-low %s --scale-high %s --cpulimit 5 --no-plots  --skip-solved %s'%(lowarcsec, higharcsec, filename)

    #there is a lot of diffent solve-field configurations I have tried in the past
    if ra != None:
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --cpulimit 300 -d 100 --sigma 100 --no-plots  --config %s %s'%(lowarcsec, higharcsec, ra, dec, location_of_index_files, fileName)
        submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --nsigma 3 --cpulimit 300 -d 100 --no-plots  --config %s %s'%(lowarcsec, higharcsec, ra, dec, location_of_index_files, fileName)
        #submis1 = 'solve-field --overwrite  --ra %s --dec %s --radius 3 --cpulimit 300 -d 100 --no-plots  --config %s %s'%( ra, dec, location_of_index_files, fileName)
        #-d 20 means only look at the brightest 20 stars
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --cpulimit 300 -d 20 --no-plots  --config %s %s'%(lowarcsec, higharcsec, ra, dec, location_of_index_files, fileName)

    else:
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --cpulimit 300 --no-plots  -d 100 --sigma 100 --config %s %s'%(lowarcsec, higharcsec, location_of_index_files, fileName)
        
        submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --nsigma 3 --cpulimit 300 --no-plots  -d 100 --config %s %s'%(lowarcsec, higharcsec, location_of_index_files, fileName)
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --cpulimit 300 --no-plots --config %s %s'%(lowarcsec, higharcsec, location_of_index_files, fileName)

    #submis2 = 'solve-field --overwrite --skip-solved --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --cpulimit 30 --no-plots  --config /dap/b_insert_wcs/sex/astrometry2Mass.cfg %s'%(lowarcsec, higharcsec, ra, dec, fileName)

    #submis2 = 'solve-field --overwrite --skip-solved --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --cpulimit 30 --no-plots  --config /dap/b_insert_wcs/sex/astrometryGaia.cfg %s'%(lowarcsec, higharcsec, ra, dec, fileName)

    #submis = 'solve-field --overwrite --scale-units arcsecperpix --ra %s --dec %s --radius .25 --no-plots  --config /dap/sex/astrometryGaia.cfg %s'%( ra, dec, filename)
    
    print ('submis1', submis1)
    os.system(submis1)
    #if runLocalFolder == True:
    #    os.system(submis2)
    #else:
    #    os.system(submis1)
    
    
    #try:
    #    os.system(submis1) #this also skips solved fields
    #    print (submis1)
    #except:
    #    os.system(submis2)
    #    print (submis2)
    #else:
    #    print ('submis1', submis1)
    #    print ('submis2', submis2)
    #    print ('**Unable to have either command run')



    '''        
    os.system("find . -name '*.xyls' -delete;")
    os.system("find . -name '*.axy' -delete;")
    os.system("find . -name '*.corr' -delete;")
    os.system("find . -name '*.match' -delete;")
    os.system("find . -name '*.rdls' -delete;")
    os.system("find . -name '*.solved' -delete;")
    os.system("find . -name '*.wcs' -delete;")
    os.system("find . -name '*.png' -delete;")
    '''


    #this deletes all of the external files but the new_fits image because I don't need them.


    if os.path.exists('%s.new' %(fileNameWithoutEnding)) == True:
        os.system("cp %s.new %s" %( fileNameWithoutEnding , fileName))
        os.remove('%s.new'%( fileNameWithoutEnding ))

    if os.path.exists('%s-indx.xyls' %(fileNameWithoutEnding)) == True:
        os.remove('%s-indx.xyls'%( fileNameWithoutEnding ))

    if os.path.exists('%s.axy' %(fileNameWithoutEnding)) == True:
        os.remove('%s.axy'%( fileNameWithoutEnding ))

    if os.path.exists('%s.corr' %(fileNameWithoutEnding)) == True:
        os.remove('%s.corr'%( fileNameWithoutEnding ))

    if os.path.exists('%s.match' %(fileNameWithoutEnding)) == True:
        os.remove('%s.match'%( fileNameWithoutEnding ))

    if os.path.exists('%s.rdls' %(fileNameWithoutEnding)) == True:
        os.remove('%s.rdls'%( fileNameWithoutEnding ))

    if os.path.exists('%s.solved' %(fileNameWithoutEnding)) == True:
        os.remove('%s.solved'%( fileNameWithoutEnding ))

    if os.path.exists('%s.wcs' %(fileNameWithoutEnding)) == True:
        os.remove('%s.wcs'%( fileNameWithoutEnding ))


    #stop
    #confirm that WCS is readable. If not, move the .fits file into the wcs_failed folder
    f = fits.open(fileName)
    h = f[0].header
    f.close()

    ax1 = h['NAXIS1']
    ax2 = h['NAXIS2']
    w = WCS(h)
    sky00 = w.pixel_to_world (0, 0)
    sky10 = w.pixel_to_world (ax1, 0)
    sky01 = w.pixel_to_world (0, ax2)
    sky11 = w.pixel_to_world (ax1, ax2)
    wcsRA_DEC 	=  w.pixel_to_world ( int(ax1/2), int(ax2/2) )
    #print (i, wcsRA_DEC)
    try: #if WCS solve was unsuccessful, move the file to failed_WCS folder
        wcsRA = (wcsRA_DEC.ra * u.degree).value
        wcsDEC = (wcsRA_DEC.dec * u.degree).value
    except:
        par_name = os.path.dirname( fileName )
        base_name = os.path.basename( fileName )
        par_name = par_name.replace( 'working', 'misc')

        newLoc = os.path.join( par_name, 'wcs_failed', base_name)

        #wcs_failed_path = os.path.join( par_name, 'wcs_failed')
        #if os.path.exists( wcs_failed_path ) == False:
        #    os.mkdir( wcs_failed_path )

        #shutil.move(fileName, newLoc)

        print ('')
        print ('')
        print(f'PLATE-SOLVE FAILED {fileName}')
        print ('')
        print ('')



if __name__ == "__main__":

    #testImage = '/dap_data/DECAM/2022_08_12/1120208/working/1120208_N1.fits'
    testImage = '/mnt/truenas/linder/decam//2022_08_12/1120208/working/1120208_N1.fits'

    testFolder = "/dap_data/SA107/working"

    #testFolders = "/dap_data/Apophis_Data/2020_12_18/working" #this is the base directory

    runLocalFolders = False #run multiple folders of data
    runLocalFolder = True
    runLocalImage = False

    #set the image scale of the image. 

    #lowarcsec = 1.00
    #higharcsec = 1.10
    lowarcsec = 0.7
    higharcsec = 0.8
    

    if runLocalFolder == True:
        images = glob.glob( "%s/*.fits"%(testFolder) )
        images += glob.glob( "%s/*.FIT"%(testFolder) )
        images += glob.glob( "%s/*.fit"%(testFolder) )

        #print (images)

        for im in images:
            print (im)
            insertWCS( im, lowarcsec, higharcsec, runLocalFolder )

    if runLocalImage == True:
            #insertWCS( testImage, lowarcsec, higharcsec, runLocalFolder )
            location_of_index_files = '/dap/b_insert_wcs/sex/astrometryGaia.cfg'
            insertWCS( fileName=testImage, lowarcsec=lowarcsec, higharcsec=higharcsec, location_of_index_files=location_of_index_files )
    
    



