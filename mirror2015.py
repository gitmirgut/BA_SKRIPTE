# Mirror images 2015 from /gfs1/work/bebesook/beesbook_data_2015 to /gfs2/work/bebesook/beesbook_data_2015
# One Directory per day
# Author: ferwar
# Python 3.4.3



import os
import shutil
import shelve
import re
from bsddb3 import db

TAR_LIST = list()

# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
# DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2015.status'

SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
DEST_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2015.status'
EXT = 'tar'


def filterFileName(file):
    splitted = file.split('.', 1)
    if splitted[1] == EXT:
        return True


def getCam(file):
    splitted = re.splt('_|\.', 2)
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


# Checks if there is a statusShelf		
try:
    statusShelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
except:
    pass
# If not then initializes one with progress = 0
if not statusShelf.has_key('progress'):
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
    # Output path
    nextOutputPath = os.path.join(DEST_DIR, DAY_DIR)
    # and path to validate if the file was previously copied
    existsPath = os.path.join(nextOutputPath, nextFile)
    if not os.path.exists(nextOutputPath):
        os.mkdir(nextOutputPath)
        # Checks if the file exists to avoid overwriting
    if not os.path.exists(existsPath):
        shutil.copy(nextArchivePath, nextOutputPath)
        print(nextArchivePath)
    incrementProgress()
