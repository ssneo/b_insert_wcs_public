

import socket

headerSize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect ( ('192.168.1.21', 1234) )

#s.connect ( ( socket.gethostname(), 1234) )


full_msg = ''
new_msg = True

#while True: 


for i in range(0, 5):
    msg = s.recv(1024)

    if new_msg:
        print (f"new message length {msg[:headerSize] }" )
        msglen = int(msg[:headerSize] )
        new_msg = False

    full_msg += msg.decode("utf-8")

    if len(full_msg) - headerSize == msglen:
        print (full_msg[headerSize:] )

        new_msg = True
        full_msg = ''

        break
