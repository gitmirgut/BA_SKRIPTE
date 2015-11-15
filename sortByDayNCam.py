""" sortByDayNCam.py copies YYYYMMDDhhmmss_C.tar-files from SOURCE_DIR to DEST_DIR/YYYYMMDD/camC/YYYYMMDDhhmmss_C.tar
     Python 3.4.3
"""



import datetime
import logging
import logging.handlers
import os
import re
import shelve
import subprocess
import csv




# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2015.status'

# SOURCE_DIR = '/home/b/beesbook'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2014'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2014.status'

# Just for testing
SOURCE_DIR = './dummyFiles/gfs1/work/bebesook_data_2014'
# SOURCE_DIR = './realData'
DEST_DIR = './structure'

if not os.path.exists(DEST_DIR):
    os.mkdir(DEST_DIR)


# STATUSFILE = os.getcwd() + '/Mirror2015.status'
STATUSFILE = 'Mirror2015.status'
LOGFILEPATH = 'Mirror2015.log'

EXT = 'tar'
PREFIXCAM = 'cam'
COPY = 'cp'
MD5SUM = 'md5sum'

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


logger = logging.getLogger('myLog')
formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# logFilePath = "my.log"
file_handler = logging.handlers.TimedRotatingFileHandler(filename = LOGFILEPATH, when ='midnight', backupCount = 30)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)





# Checks if there is a statusShelf
startTime = datetime.datetime.now()

try:
    statusShelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
    logger.info('Status file has been opened')
except:
    pass
# If not then initializes one with progress = 0
if not ('progress' in statusShelf):
    putOnShelf('progress', 0)
    logger.info('START with a new copy process')

if getProgress() > 0:
    logger.info('Continue with the last copy process')

TAR_LIST = [file for file in os.listdir(SOURCE_DIR) if filterFileName(file)]
numFiles = str(len(TAR_LIST))
logger.info(numFiles + 'files to copy')
TAR_LIST.sort()

# the process is executed for all of the tar files
while len(TAR_LIST) > getProgress():

    actFile = getProgress() + 1
    logger.debug('[' + str(actFile) + ' of ' + str(numFiles) + ']')

    # gets next file name from the list
    nextFile = TAR_LIST[getProgress()]

    # generates the source path
    nextArchivePath = os.path.join(SOURCE_DIR, nextFile)
    logger.debug(nextArchivePath)

    # generates the md5 checksum for the file
    md5sumOutput = str(subprocess.check_output([MD5SUM, nextArchivePath], universal_newlines=True))
    md5sumOrg = getMD5sum(md5sumOutput)
    logger.debug(md5sumOrg)

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
        logger.info('Folder %s was created', DAY_DIR)
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
        logger.debug(outputFile)

        # generate MD5sum of the copied file
        md5sumOutput = str(subprocess.check_output([MD5SUM, outputFile], universal_newlines=True))

        # Just for Testing
        if (getProgress() == 2) | (getProgress() == 5):
          md5sumOutput = "e62766ec7a443d346858b3faec2e5c4b"

        md5sumCp = getMD5sum(md5sumOutput)
        logger.debug(md5sumCp)
        if md5sumOrg == md5sumCp:
            logger.debug('md5sum OK')
        else:
            logger.warning('File Checksum of the following File was not correct:' + nextArchivePath)

            # Open csv for saving copied files with false checksums
            falseChecksumFile = open('falseChecksum.csv', 'a')
            falseChecksumWriter = csv.writer(falseChecksumFile)
            falseChecksumWriter.writerow([nextArchivePath])
            falseChecksumFile.close()

    incrementProgress()

# measure the time of the entire process
endTime = datetime.datetime.now()
diffTime = endTime - startTime

logger.info('Number of copied files %s', getProgress())
logger.info(str(getProgress()) + ' files have been copied')
logger.info('PROCESS FINISHED after %s Seconds', diffTime.total_seconds())


