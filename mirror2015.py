# Mirror images 2015 from /gfs1/work/bebesook/beesbook_data_2015 to /gfs2/work/bebesook/beesbook_data_2015
# One Directory per day
# Author: ferwar
# Python 3.4.3



import datetime
import logging
import logging.handlers
import os
import re
import shelve
import subprocess

TAR_LIST = list()

# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2015.status'

# SOURCE_DIR = '/home/b/beesbook'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2014'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2014.status'

SOURCE_DIR = '/media/mrpoin/myStorage/BA_SKRIPTE/dummyFiles/gfs1/work/bebesook_data_2014'
# SOURCE_DIR = '/media/mrpoin/myStorage/BA_SKRIPTE/realData'
DEST_DIR = '/media/mrpoin/myStorage/BA_SKRIPTE/structure'
STATUSFILE = '/media/mrpoin/myStorage/BA_SKRIPTE/Mirror2015.status'
LOGFILE = '/media/mrpoin/myStorage/BA_SKRIPTE/Mirror2015.log'
EXT = 'tar'
PREFIXCAM = 'cam'
COPY = 'cp'
MD5SUM = 'md5sum'

# For Testing of MD5sum
FILEFALSECHECKSUM = '/media/mrpoin/myStorage/BA_SKRIPTE/20140724191905_0.tar'


# change to the following line for multi- threaded replacements mcps and msum
# for single-threaded Linux utilities cp and md5dum
# COPY = 'mcp'
# MD5SUM = 'msum'


def filterFileName(file):
    splitted = file.split('.', 1)
    if splitted[1] == EXT:
        return True


def getCam(file):
    splitted = re.split('_|\.', file, 2)
    return splitted[1]


def getMD5sum(output):
    splitted = output.split(' ', 1)
    return splitted[0]


def putOnShelf(key, value):
    statusShelf[key] = value
    statusShelf.sync()


def deleteFromShelf(key):
    del (statusShelf[key])
    statusShelf.sync()


def getProgress():
    return statusShelf['progress']


def incrementProgress():
    statusShelf['progress'] += 1
    statusShelf.sync()


# Initializes logging
def initLogging():
    logHandler = logging.handlers.TimedRotatingFileHandler(filename=LOGFILE, when='midnight', backupCount=60)
    logHandler.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(levelname)s - %(message)s'))
    logHandler.setLevel(logging.DEBUG)
    logging.getLogger('').setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(logHandler)
    print('logging to:', LOGFILE)


# enables Multi-threaded Copy and MD5 Checksums
# module load mutil

initLogging()
# Checks if there is a statusShelf
startTime = datetime.datetime.now()

try:
    statusShelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
    logging.info('Status file has been opened')
except:
    pass
# If not then initializes one with progress = 0
if not ('progress' in statusShelf):
    putOnShelf('progress', 0)
    logging.info('START with a new copy process')

if getProgress() > 0:
    logging.info('Continue with the last copy process')

TAR_LIST = [file for file in os.listdir(SOURCE_DIR) if filterFileName(file)]
numFiles = str(len(TAR_LIST))
print(numFiles + 'files to copy')
TAR_LIST.sort()

# the process is executed for all of the tar files
while len(TAR_LIST) > getProgress():

    print('\n[' + str(getProgress()) + ' of ' + str(numFiles) + ']')

    # gets next file name from the list
    nextFile = TAR_LIST[getProgress()]

    # generates the source path
    nextArchivePath = os.path.join(SOURCE_DIR, nextFile)
    print(nextArchivePath)

    # generates the md5 checksum for the file
    md5sumOutput = str(subprocess.check_output([MD5SUM, nextArchivePath], universal_newlines=True))
    md5sumOrg = getMD5sum(md5sumOutput)
    print(md5sumOrg)

    # the first 8 characters correspond to YYYYMMDD
    DAY_DIR = nextFile[:8]

    # Path to day dir
    nextOutputPathDay = os.path.join(DEST_DIR, DAY_DIR)

    # parses the cam from the filename
    CAM_DIR = getCam(nextFile)

    # final Output path
    nextOutputPathCam = os.path.join(nextOutputPathDay, PREFIXCAM + CAM_DIR)

    # and path to validate if the file was previously copied
    existsPath = os.path.join(nextOutputPathCam, nextFile)
    if not os.path.exists(nextOutputPathDay):
        logging.info('Folder %s was created', DAY_DIR)
        os.mkdir(nextOutputPathDay)

    # Checks if the file exists to avoid overwriting
    if not os.path.exists(nextOutputPathCam):
        os.mkdir(nextOutputPathCam)

    # Checks if the file exists to avoid overwriting
    if not os.path.exists(existsPath):

        # shutil.copy(nextArchivePath, nextOutputPathCam)
        subprocess.call([COPY, nextArchivePath, nextOutputPathCam])

        # check output path
        outputFile = os.path.join(nextOutputPathCam, nextFile)
        print(outputFile)

        # generate MD5sum of the copied file
        # md5sumOutput = str(subprocess.check_output([MD5SUM, outputFile], universal_newlines=True))
        md5sumOutput = str(subprocess.check_output([MD5SUM, FILEFALSECHECKSUM], universal_newlines=True))
        md5sumCp = getMD5sum(md5sumOutput)
        print(md5sumCp)
        if md5sumOrg == md5sumCp:
            print('md5sum OK')
        else:
            logging.warning('File Checksum was not correct')

    incrementProgress()

# measure the time of the entire process
endTime = datetime.datetime.now()
diffTime = endTime - startTime

logging.info('Number of copied files %s', getProgress())
print(str(getProgress()) + ' files have been copied')
logging.info('PROCESS FINISHED after %s Seconds', diffTime.total_seconds())
