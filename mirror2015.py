# Mirror images 2015 from /gfs1/work/bebesook/beesbook_data_2015 to /gfs2/work/bebesook/beesbook_data_2015
# One Directory per day
# Author: ferwar
# Python 3.4.3



import os
import re
import shelve
import shutil
import subprocess

TAR_LIST = list()

# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2015.status'

# SOURCE_DIR = '/home/b/beesbook'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2014'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2014.status'

SOURCE_DIR = '/media/mrpoin/myStorage/BA_SKRIPTE/dummyFiles/gfs1/work/bebesook_data_2014'
DEST_DIR = '/media/mrpoin/myStorage/BA_SKRIPTE/structure'
STATUSFILE = '/media/mrpoin/myStorage/BA_SKRIPTE/Mirror2015.status'
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

# enables Multi-threaded Copy and MD5 Checksums
# module load mutil

# Checks if there is a statusShelf		
try:
    statusShelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
except:
    pass
# If not then initializes one with progress = 0
if not ('progress' in statusShelf):
    putOnShelf('progress', 0)

TAR_LIST = [file for file in os.listdir(SOURCE_DIR) if filterFileName(file)]
TAR_LIST.sort()

# the process is executed for all of the tar files
while len(TAR_LIST) > getProgress():
    # gets next file name from the list
    nextFile = TAR_LIST[getProgress()]
    # generates the source path
    nextArchivePath = os.path.join(SOURCE_DIR, nextFile)
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
        os.mkdir(nextOutputPathDay)
        # Checks if the file exists to avoid overwriting
    if not os.path.exists(nextOutputPathCam):
        os.mkdir(nextOutputPathCam)
        # Checks if the file exists to avoid overwriting
    if not os.path.exists(existsPath):
        # shutil.copy(nextArchivePath, nextOutputPathCam)
        subprocess.call([COPY, nextArchivePath, nextOutputPathCam])
        print(nextArchivePath)
    incrementProgress()
