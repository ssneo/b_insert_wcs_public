

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
import psycopg2
from datetime import datetime

try:
    logging.basicConfig( filename = '/container_b_log.log', level=logging.DEBUG)
except:
    logging.basicConfig( filename = '/Users/linder/container_b_log.log', level=logging.DEBUG)

def client_queue():

    headerSize = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect ( ('192.168.1.21', 62892) )
    #s.connect ( ('0.0.0.0', 62891) )

    #s.connect ( ( socket.gethostname(), 1234) )


    full_msg = ''
    new_msg = True

    #while True: 

    for i in range(0, 5): #this needs to be turned off for final system
        msg = s.recv(1024)

        print ('msg that is coming from queue', msg)
        if new_msg:
            print (f"new message length {msg[:headerSize] }" )
            msglen = int(msg[:headerSize] )
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - headerSize == msglen:
            print (full_msg[headerSize:] )

            #new_msg = True
            #full_msg = ''

            return full_msg[headerSize:]

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

    psql = "SELECT image,file_location FROM dap WHERE id=%s"%( msg )
    print ('psql line 72', psql)

    cur.execute(psql)
    output = cur.fetchall()
    image = output[0][0]
    file_location = output[0][1]
    con.close()
    #

    if os.path.basename( file_location  ) == 'working':
        fileName = os.path.join( file_location, image )
    else:
        fileName = os.path.join( file_location, 'working', image)

    return fileName

def updateDB( msg, id ):
    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "UPDATE dap SET insert_wcs_in_progress=false, insert_wcs_complete=true WHERE id=%s "%( id )
    print ('psql update command is: ', psql )

    cur.execute(psql)

    con.commit()

    con.close()

def log(value):
    utcTime = datetime.utcnow()
    time = '%s-%s-%s %s:%s:%s'%( utcTime.strftime("%Y"), utcTime.strftime("%m"), utcTime.strftime("%d"), utcTime.strftime("%H"), utcTime.strftime("%m"), utcTime.strftime("%S"))
    logging.info("%s: %s"%(time, value))

def insertWCS( fileName, lowarcsec, higharcsec ):
    #fileNameWithoutEnding is the filename without the 4 or 5 digits of FIT, fit, FITS, or fits including the period before



    fileNameWithoutEnding = fileName.replace('.fits', '')
    fileNameWithoutEnding = fileNameWithoutEnding.replace('.fit', '')


    d1=fits.open('%s'%(fileName))
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


    submis = 'solve-field --overwrite --skip-solved --scale-units arcsecperpix --scale-low %s --scale-high %s --ra %s --dec %s --radius 3 --cpulimit 30 --no-plots  --config /dap/sex/astrometryGaia.cfg %s'%(lowarcsec, higharcsec, ra, dec, fileName)

    #submis = 'solve-field --overwrite --scale-units arcsecperpix --ra %s --dec %s --radius .25 --no-plots  --config /dap/sex/astrometryGaia.cfg %s'%( ra, dec, filename)
    
    print (submis)
    os.system(submis) #this also skips solved fields



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
        newLoc = fileName.replace('working', 'wcs_failed')
        shutil.move(fileName, newLoc)


if __name__ == "__main__":

    while(1):
        sleepTime = 1
        msg = client_queue()
        if msg == 'None':
            log('Got a message of None therefore going to sleep and doing nothing')
            time.sleep( sleepTime )
        else:
            msg = msg.split('=')[1]
            #print ('msg', msg)
            #stop
            log('Got a message: ' + msg)
            print ('Got Message of: ', msg)
            fileName = readInformationFromDatabase( msg )
            #print ('file_location', file_location)
            #stop
            log('fileName: ' + fileName)
            print ('Got fileName of: ', fileName)
            #startUp("/dap_data/DECAM/2022_08_12/1120208/working/")

            lowarcsec = 0.23
            higharcsec = 0.29

            insertWCS( fileName, lowarcsec, higharcsec )
            
            #updateDB( msg, msg ) #say the work has been done
            log('updateDB function complete')
            print ('updateDB is complete for ', msg )

            time.sleep( sleepTime )

