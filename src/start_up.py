#!/usr/bin/python3.8
import os
import socket
import psycopg2
from datetime import datetime
import glob
import shutil
import logging
import time

logging.basicConfig( filename = '/container_a_log.log', level=logging.DEBUG)

def client_queue():

    headerSize = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect ( ('192.168.1.21', 62891) )
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

    psql = "SELECT file_location FROM dap WHERE id=%s"%( msg )
    #print (psql)

    cur.execute(psql)
    output = cur.fetchall()[0][0]

    con.close()

    return output

def startUp(file_location):

    #check if the last line of the file_location is a slash

    if file_location[-1] == '/': #for the logic to work for basename, the last value cannot be a slash
        file_location = file_location[:-1]

    if os.path.basename( file_location ) == 'working': #if the file_location already has the fits image in the working directory then the below actions should be perform a level higher.
        file_location = os.path.dirname( file_location )

    if os.path.exists( os.path.join( file_location, 'working' ) ) == False: #if the working folder does not exists, I create one
        os.mkdir( os.path.join( file_location, 'working' ) )

    if os.path.exists( os.path.join( file_location, 'source' ) ) == False: #if the source folder does not exists, I create one
        os.path.join( file_location, 'source' )

    if os.path.exists( os.path.join( file_location, 'calibrated' ) ) == False: #if the source folder does not exists, I create one
        os.mkdir(  os.path.join( file_location, 'calibrated' ) )

    if os.path.exists( os.path.join( file_location, 'compressed' ) ) == False: #if the source folder does not exists, I create one
        os.mkdir( os.path.join( file_location, 'compressed' ) )

    if os.path.exists( os.path.join( file_location, 'wcs_failed' ) ) == False: #if the source folder does not exists, I create one
        os.mkdir( os.path.join( file_location, 'wcs_failed' ) )

    if os.path.exists( os.path.join( file_location, 'plots' ) ) == False: #if the source folder does not exists, I create one
        os.mkdir( os.path.join( file_location, 'plots' ) )

    if os.path.exists( os.path.join( file_location, 'panstarrs' ) ) == False: #if the source folder does not exists, I create one
        os.mkdir( os.path.join( file_location, 'panstarrs' ) )

def confirmAllDataIsInWorkingFolderAndUncomprssed(  file_location ):

    #print ('1', file_location)
    if file_location[:1] == '/':
        test_file_location = file_location[:-1]
    else:
        test_file_location = file_location

    #print ( os.path.basename(test_file_location) )
    if os.path.basename(test_file_location) == 'working':
        file_location = os.path.dirname( test_file_location )

    if file_location[:-1] != '/':
        print ('yes')
        file_location += '/'
        

    #print ('2', file_location)

    
    #stop
    #if os.path.basename

    start = datetime.utcnow()
    #check if there are any compressed data in the main folder, if so, move them to the compressed folder
    images = glob.glob( file_location + '*.bz2')
    images += glob.glob( file_location + '*.zip')
    for i in images:


        newLoc = file_location + 'compressed/' + os.path.basename(i)
        newLoc = newLoc.replace(' ', '_') #remove spaces in the file names

        shutil.move(i, newLoc )

    #check if there are any .fits data in the main folder, if so, move them to the working folder
    images = glob.glob( file_location + '*.fit')
    images += glob.glob( file_location + '*.fits')
    for i in images:

        newLoc = file_location + 'working/' + os.path.basename(i) 
        newLoc = newLoc.replace(' ', '_') # remove spaces in the file names

        shutil.move(i, newLoc )


    #confirm every file in the compressed folder has been uncompressed and in the working folder
    images = glob.glob( file_location + 'compressed/' + '*.bz2')
    images += glob.glob( file_location + 'compressed/' + '*.zip')
    for j in images:
        
        newLoc = j.replace('compressed', 'working')
        

        if os.path.exists( newLoc[:-4] ) == False: #the file is not in the working directory
            #copy the file over
            print ('j', j)
            shutil.copy(j, newLoc)
            #os.system("bzip2 -d %s"%(newLoc))
            #print ('hello')

        #make sure all images are uncompressed in the working folder
        images = glob.glob( file_location + 'working/' + '*.bz2')
        for i in images:
            os.system("bzip2 -d %s"%(i))
        #make sure all images are uncompressed in the working folder
        images = glob.glob( file_location + 'working/' + '*.zip')
        for i in images:
            command = "unzip  -o %s  -d %s"%(i, file_location + 'working/'  )
            #print (command)
            
            os.system(command)
            os.remove(i)

def updateDB( msg, file_location ):
    config = {
        "host": "192.168.1.21",
        "user": "linder",
        "password": "flyhigh34",
        "database": "dap",
    }

    con=psycopg2.connect(**config)
    cur=con.cursor()

    psql = "UPDATE dap SET start_up_in_progress=false, start_up_complete=true WHERE file_location='%s' "%( file_location )
    print ('psql update command is: ', psql )

    cur.execute(psql)

    con.commit()

    con.close()

def log(value):
    utcTime = datetime.utcnow()
    time = '%s-%s-%s %s:%s:%s'%( utcTime.strftime("%Y"), utcTime.strftime("%m"), utcTime.strftime("%d"), utcTime.strftime("%H"), utcTime.strftime("%m"), utcTime.strftime("%S"))
    logging.info("%s: %s"%(time, value))

if __name__ == "__main__":

    #this single code is the primary operations of the container.
    #It will talk to the queue system via client_queue()
    #It will then pull the information need from the data via readInformationFromDatabase
    #It will then perform the start_up operations on the data.
    while(1):
        sleepTime = 1
    #for i in range(2):
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
            file_location = readInformationFromDatabase( msg )
            #print ('file_location', file_location)
            #stop
            log('File Location: ' + file_location)
            print ('Got File Location of: ', file_location)
            #startUp("/dap_data/DECAM/2022_08_12/1120208/working/")
            startUp( file_location )
            log('startUp function complete')
            print ('Start Up Complete for: ', msg)
            
            confirmAllDataIsInWorkingFolderAndUncomprssed( file_location )
            log('confirmAllDataIsInWorkingFolderAndUncompressed function complete')
            print ('Confirm All Data Is Working Foler and Uncompressed is complete for: ', msg)
            
            updateDB( msg, file_location ) #say the work has been done
            log('updateDB function complete')
            print ('updateDB is complete for ', msg )

            time.sleep( sleepTime )