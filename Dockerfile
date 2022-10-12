

FROM ubuntu:20.04


RUN apt-get update
#RUN apt-get install dialog apt-utils -y
#RUN apt-get install -y apt-utils
#RUN apt-get upgrade -y

#RUN apt-get update
RUN apt-get install -y vim
#RUN apt-get update
RUN apt-get install -y python3.8
#RUN apt-get update
RUN apt-get install -y python3-pip 
#RUN apt-get update
RUN apt-get install -y iputils-ping

RUN echo 'alias python="/usr/bin/python3.8"' >> /root/.bashrc


RUN pip3 install psycopg2-binary

#we are going to make the dir DAP here then make that the workingDir. This need to occur now because not until after the DockerFile is build are the volumne connected
RUN mkdir /dap
RUN mkdir /dap/b_insert_wcs
RUN mkdir /dap/b_insert_wcs/src
WORKDIR /dap/b_insert_wcs/src 



COPY /src/start_up.py /dap/b_insert_wcs/src/start_up.py
COPY /src/keepRunning.py /dap/b_insert_wcs/src/keepRunning.py

#COPY pythonServer.py /pythonServer.py
#COPY bashFile.sh /bashFile.sh
#this is to test if permission will work
#COPY sqs_test.py /sqs_test.py 
#COPY config /config

#RUN chmod +x /bashFile.sh
RUN chmod +x /dap/b_insert_wcs/src/start_up.py
RUN chmod +x /dap/b_insert_wcs/src/keepRunning.py

#RUN ./baseFile.sh
#RUN ./dap/a_start_up/src/start_up.py

#RUN ["chmod", "+x", "/bashFile.sh"]
#ENTRYPOINT [ "/bashFile.sh"]
#ENTRYPOINT ["/dap/a_start_up/src/start_up.py"]
CMD ["python3.8", "/dap/b_insert_wcs/src/b_insert_wcs.py"]
#CMD ["python3.8", "/dap/b_insert_wcs/src/keepRunning.py"]

#RUN ["chmod", "+x", "/dap/a_start_up/src/start_up.py"] #change permission of file
#ENTRYPOINT ["python", "/dap/a_start_up/src/start_up.py"]
#ENTRYPOINT ["python3.8", "start_up.py"] #I assume if the workdir is already there



#CMD python --version


#CMD ["apache2ctl", "-D", "FOREGROUND"]

