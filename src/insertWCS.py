

import glob
from astropy.io import fits
import os
import shutil
import sys
from astropy.wcs import WCS
from astropy import units as u
import logging
import time
import socket
#import psycopg2
from datetime import datetime

from client_queue import client_queue

try:
    logging.basicConfig( filename = '/container_b_log.log', level=logging.DEBUG)
except:
    logging.basicConfig( filename = '/Users/linder/container_b_log.log', level=logging.DEBUG)


def readInformationFromDatabase(msg): #confirm the psql line is correct
    #image = "1120208_N1.fits"
    #file_location = "/dap_data/DECAM/2022_08_12/1120208/working/"

    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "SELECT file_location, image FROM dap WHERE id=%s"%( msg )
    #print ('psql line 72', psql)

    cur.execute(psql)
    output = cur.fetchall()
    folder_loc = output[0][0]
    image_file_name = output[0][1]
    con.close()
    #

    if os.path.basename( folder_loc  ) == 'working' or os.path.basename( folder_loc  ) == 'workin':
        fileName = os.path.join( folder_loc, image_file_name )
    else:
        fileName = os.path.join( folder_loc, 'working', image_file_name)

    return fileName

def updateDB( msg ):
    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "UPDATE dap SET insert_wcs_in_progress=false, insert_wcs_complete=true WHERE id=%s "%( msg )
    print ('psql update command is: ', psql )

    cur.execute(psql)

    con.commit()

    con.close()

def log(value):
    utcTime = datetime.utcnow()
    time = '%s-%s-%s %s:%s:%s'%( utcTime.strftime("%Y"), utcTime.strftime("%m"), utcTime.strftime("%d"), utcTime.strftime("%H"), utcTime.strftime("%m"), utcTime.strftime("%S"))
    logging.info("%s: %s"%(time, value))

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

                '''
                rah = int(ra)
                ra1 = (ra - rah)
                ram = int( ra1 * 60. )
                ra2 = (ra1 * 60.) - int( ra1 * 60. ) 
                ras = round ( ra2*60., 2)

                #print ('ra', ra)
                #print ('ra1', ra1)
                #print ('ram', ram)
                #print ('ra2', ra2)
                #print ('ras', ras)

                #print (rah, ram, ras)
                #stop
                

                ded = int(dec)
                if ded < 0:
                    de1 = abs( (dec - ded) )
                    dem = 60 - int( de1 * 60. )
                    de2 = (de1 * 60) - int( de1 * 60. )
                    des = 60. - round ( de2*60., 2)
                    #print (dec)
                    #print (ded)
                    #print ('de1',de1)
                    #print ('dem',dem)
                    #print ('de2',de2)
                    print ('des',des)
                else:
                    de1 = (dec - ded)
                    dem = int( de1 * 60. )
                    de2 = (de1 * 60) - int( de1 * 60. )
                    des = round ( de2*60., 2)
                #print (ded, dem, des)


                #print ('t1', f'{des:02}')
                rahms = f"{rah}:{ram:02}:{ras:05}"
                dedms = f"{ded}:{dem:02}:{des:05}"

                ra = rahms
                dec = dedms
                '''


            except:
                overRide = True
                if overRide == True: #gives me an option to manually insert and ra/dec value
                    #ra = "16:50:18.8"
                    #dec = "+12:01:32"
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


    if ra != None:
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --cpulimit 300 -d 100 --sigma 100 --no-plots  --config %s %s'%(lowarcsec, higharcsec, ra, dec, location_of_index_files, fileName)
        submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --cpulimit 300 -d 100 --no-plots  --config %s %s'%(lowarcsec, higharcsec, ra, dec, location_of_index_files, fileName)
        #submis1 = 'solve-field --overwrite  --ra %s --dec %s --radius 3 --cpulimit 300 -d 100 --no-plots  --config %s %s'%( ra, dec, location_of_index_files, fileName)
        #-d 20 means only look at the brightest 20 stars
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --cpulimit 300 -d 20 --no-plots  --config %s %s'%(lowarcsec, higharcsec, ra, dec, location_of_index_files, fileName)

    else:
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --cpulimit 300 --no-plots  -d 100 --sigma 100 --config %s %s'%(lowarcsec, higharcsec, location_of_index_files, fileName)
        
        #submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --cpulimit 300 --no-plots  -d 100 --config %s %s'%(lowarcsec, higharcsec, location_of_index_files, fileName)
        submis1 = 'solve-field --overwrite --scale-units arcsecperpix --scale-low %s --scale-high %s --cpulimit 300 --no-plots --config %s %s'%(lowarcsec, higharcsec, location_of_index_files, fileName)

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

        wcs_failed_path = os.path.join( par_name, 'wcs_failed')
        if os.path.exists( wcs_failed_path ) == False:
            os.mkdir( wcs_failed_path )

        shutil.move(fileName, newLoc)

        print ('')
        print ('')
        print(f'PLATE-SOLVE FAILED {fileName}')
        print ('')
        print ('')

def find_local_folder_to_process():

    
    config = {
        "host": "host.docker.internal",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "SELECT obsid FROM dap WHERE insert_wcs=False order by id limit 1"
    
    cur.execute(psql)

    obsid = cur.fetchall()

    con.close()

    try:
        obsid = obsid[0][0] #if the response is empty this will error out

    except:
        obsid = 'None'

    return obsid

def update_local_folder_processed(obsid):

    config = {
        "host": "host.docker.internal",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()


    psql = "UPDATE dap SET insert_wcs=True where id=%s"%(obsid)
    
    cur.execute(psql)

    con.commit()

    con.close()

if __name__ == "__main__":

    #testImage = '/dap_data/DECAM/2022_08_12/1120208/working/1120208_N1.fits'
    testImage = '/mnt/truenas/linder/decam//2022_08_12/1120208/working/1120208_N1.fits'
    #testFolder = "/dap_data/2023_DZ2/2023_03_20/working/"
    #testFolder = "/dap_data/DECAM/2022_08_12/1120241/working/"
    #testFolder = "/dap_data/ARI/14/working/"

    #testFolder = "/dap_data/Apophis_Data/2020_12_18/working"
    #testFolder = "/dap_data/Apophis_Data/2021_03_06_CTIO/working"
    #testFolder = "/dap_data/Apophis_Data/2021_03_06_UoA/working"

    testFolder = "/dap_data/SA107/working"

    #testFolders = "/dap_data/Apophis_Data/2020_12_18/working" #this is the base directory

    runLocalFolders = False #run multiple folders of data
    runLocalFolder = True
    runLocalImage = False


    #lowarcsec = 1.00
    #higharcsec = 1.10
    lowarcsec = 0.7
    higharcsec = 0.8
    
    #if runLocalFolders == True:
    #    while(1):
    #        obsid = find_local_folder_to_process()

    #        if obsid != 'None':
                

    #            folder_loc = os.path.join( testFolders, str(obsid) )
    #            if folder_loc[-1] != "/":
    #                folder_loc += "/"

                #print ('folder_loc', folder_loc)
                #folders = glob.glob('%s*'%(folder_loc) )
                #print ('len(folders)', len(folders))
                #for folder in folders:

    #            images = glob.glob( "%s/working/*.fits"%(folder_loc) )
    #            images += glob.glob( "%s/working/*.FIT"%(folder_loc) )
    #            images += glob.glob( "%s/working/*.fit"%(folder_loc) )
                #print ('len(images)', len(images))
    #            for im in images:
                    #print (im)
    #                insertWCS( im, lowarcsec, higharcsec )
                    #stop

    #            update_local_folder_processed( obsid )
                #stop
                
    #        else:
    #            print ('Obsid returned none, obsid=%s'%(obsid))
    #            break


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
    
    stop


    while(1):
        
        sleepTime = 1
        msg = client_queue('192.168.1.21', 62892)
        if msg == 'NO_DATA':
            log('Got a message of None therefore going to sleep and doing nothing')
            time.sleep( sleepTime )
        else:
            #msg = msg.split('=')[1]
            #print ('msg', msg)
            #stop
            log('Got a message: ' + msg)
            print ('Got Message of: ', msg)
            fileName = readInformationFromDatabase( msg )
            #print ('file_location', file_location)
            #stop
            log('fileName: ' + fileName)
            print ('Got fileName of: ', fileName)
            

            lowarcsec = 0.23
            higharcsec = 0.29
            #lowarcsec = 1.00
            #higharcsec = 1.10

            #if runLocalFolder == True:
            #    for im in images:
            #        insertWCS( im, lowarcsec, higharcsec )
            #elif runLocalImage == True:
            #        insertWCS( testImage, lowarcsec, higharcsec )
            #    #stop
            #else:

            location_of_index_files = '/mnt/raid/k8s_files/sex/astrometryGaia.cfg'
            insertWCS( fileName=fileName, lowarcsec=lowarcsec, higharcsec=higharcsec, runLocalFolder=runLocalFolder, location_of_index_files=location_of_index_files )
            
            updateDB( msg ) #say the work has been done
            log('updateDB function complete')
            print ('updateDB is complete for ', msg )

            time.sleep( sleepTime )

