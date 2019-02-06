import os
import logging

logFormatter = logging.Formatter("[RASA-LOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler("{0}/{1}.log".format('./', 'core'))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
os.system("gnome-terminal -e 'tail -f core.log'")
