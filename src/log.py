
import logging
from datetime import datetime

try:
    logging.basicConfig( filename = '/container_a_log.log', level=logging.DEBUG)
except:
    logging.basicConfig( filename = '/Users/linder/container_a_log.log', level=logging.DEBUG)

def log(value):
    utcTime = datetime.utcnow()
    time = '%s-%s-%s %s:%s:%s'%( utcTime.strftime("%Y"), utcTime.strftime("%m"), utcTime.strftime("%d"), utcTime.strftime("%H"), utcTime.strftime("%M"), utcTime.strftime("%S"))
    logging.info("%s: %s"%(time, value))