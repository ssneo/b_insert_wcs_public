

import socket
from datetime import datetime
import time
from log import log

#this function has a test function built and has passed
def client_queue(ip, port, timeOutAfterSeconds=60):

    headerSize = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    waitTime = 10 #seconds
    maxLoopCounts = 3
    loopCounts = 0
    while True:
        try:
            s.connect ( ( ip, port ) )
            #s.connect ( ('192.168.1.21', 62890) )
            #s.connect ( ('0.0.0.0', 62891) )
            break
        except ConnectionRefusedError:
            log(f'Connection_Refused_Error for ip= {ip}, port= {port}')
            print (f'Connection_Refused_Error for ip= {ip}, port= {port}')
            loopCounts += 1
            if loopCounts == maxLoopCounts:
                return 'Unable to Connect to Server'
            time.sleep( waitTime )


    full_msg = ''
    new_msg = True

    startTime = datetime.utcnow()
    while True: #we are going to wait for a successful message and then break the loop with a return statement. Otherwise we reset after 60 seconds.

    #for i in range(0, 5): #this needs to be turned off for final system
        msg = s.recv(1024)

        #print ('msg that is coming from queue', msg)
        if new_msg:
            #print (f"new message length {msg[:headerSize] }" )
            msglen = int(msg[:headerSize] )
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - headerSize == msglen:
            #print (full_msg[headerSize:] )
            s.close()
            return full_msg[headerSize:]
        
        endTime = datetime.utcnow()

        lapseTime = endTime - startTime
        if lapseTime.total_seconds() > timeOutAfterSeconds: #this break does not have a test assoicate with it. It is unclear what will happen to the main code when this occurs.
            s.close()
            break

