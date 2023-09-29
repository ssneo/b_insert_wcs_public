

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
#the command above prevents install applications from asking questions using a GUI interface

RUN apt-get update

RUN apt-get install -y apt-utils
RUN apt-get install dialog apt-utils -y

RUN apt-get upgrade -y

RUN apt-get update
RUN apt-get install -y vim
#RUN apt-get update
RUN apt-get install -y python3.8
RUN apt-get update
RUN apt-get install -y python3-pip 
#RUN apt-get update
RUN apt-get install -y iputils-ping
#RUN apt-get update
RUN apt-get install -y astrometry.net

RUN echo 'alias python="/usr/bin/python3.8"' >> /root/.bashrc


RUN pip3 install psycopg2-binary
RUN pip3 install astropy

#we are going to make the dir DAP here then make that the workingDir. This need to occur now because not until after the DockerFile is build are the volumne connected
RUN mkdir /dap
RUN mkdir /dap/b_insert_wcs
RUN mkdir /dap/b_insert_wcs/src
WORKDIR /dap/b_insert_wcs/src 


COPY /src/insertWCS.py /dap/b_insert_wcs/src/insertWCS.py
COPY /src/keepRunning.py /dap/b_insert_wcs/src/keepRunning.py
COPY /src/client_queue.py /dap/b_insert_wcs/src/client_queue.py
COPY /src/log.py /dap/b_insert_wcs/src/log.py


#RUN chmod +x /bashFile.sh
RUN chmod +x /dap/b_insert_wcs/src/insertWCS.py
RUN chmod +x /dap/b_insert_wcs/src/keepRunning.py

#CMD ["python3.8", "/dap/b_insert_wcs/src/insertWCS.py"]
CMD ["python3.8", "/dap/b_insert_wcs/src/keepRunning.py"]


