""" sortByDayNCam.py copies YYYYMMDDhhmmss_C.tar-files from SOURCE_DIR to
    DEST_DIR/YYYYMMDD/camC/YYYYMMDDhhmmss_C.tar
    Python 3.4.3
"""

import datetime
import logging
import logging.handlers
import os
import re
import shelve
import csv
import copy_verify


# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
# DESTINATION_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2015.status'

# SOURCE_DIR = '/home/b/beesbook'
# DESTINATION_DIR = '/gfs2/work/bebesook/beesbook_data_2014'
# STATUSFILE = '/home/b/bebesook/CrayPy2015/Mirror2014.status'

# Just for testing
SOURCE_DIR = './dummyFiles/gfs1/work/bebesook_data_2014'
# SOURCE_DIR = './realData'
DESTINATION_DIR = './structure'



STATUSFILE = 'Mirror2015.status'
LOGFILEPATH = 'Mirror2015.log'

EXT = '.tar'
PREFIX_CAM = 'cam'


def get_cam(file_name):
    split = re.split('_|\.', file_name, 2)
    return split[1]


def append_false_checksum(file_name):
    # Open csv for saving copied files with false checksums
    false_checksum_file = open('falseChecksum.csv', 'a')
    false_checksum_writer = csv.writer(false_checksum_file)
    false_checksum_writer.writerow([file_name])
    false_checksum_file.close()


def put_on_shelf(key, value):
    statusShelf[key] = value
    statusShelf.sync()


def get_progress():
    return statusShelf['progress']


def increment_progress():
    statusShelf['progress'] += 1
    statusShelf.sync()

# Initialize logger with two handlers, where each handler has a different
# level, so that the more important logs will be writen to file and the
# unimportant logs for debug will just will be shown on console output and
# can be disabled by
# logging.disable(logging.DEBUG)

logger = logging.getLogger('myLog')
formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=LOGFILEPATH,
    when='midnight',
    backupCount=30)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


################################################################################
# Start
################################################################################

startTime = datetime.datetime.now()

if not os.path.exists(DESTINATION_DIR):
    os.mkdir(DESTINATION_DIR)

# Checks if there is a statusShelf
statusShelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
logger.info('Status file has been opened')

# If not then initializes one with progress = 0
if not ('progress' in statusShelf):
    put_on_shelf('progress', 0)
    logger.info('START with a new copy process')

if get_progress() > 0:
    logger.info('Continue with the last copy process')

tar_list = [file for file in os.listdir(SOURCE_DIR) if file.endswith(EXT)]

num_files = len(tar_list)

left_files = num_files - int(get_progress())


logger.info(str(left_files) + ' files left for copy')
tar_list.sort()

# the process is executed for all of the tar files
while len(tar_list) > get_progress():

    # writes progress to logger
    act_file = get_progress() + 1
    logger.debug('[' + str(act_file) + ' of ' + str(num_files) + ']')

    # gets next file name from the list
    next_file = tar_list[get_progress()]

    # generates the source path to file
    src_file = os.path.join(SOURCE_DIR, next_file)
    logger.debug('src: ' + src_file)

    # the first 8 characters correspond to YYYYMMDD
    day = next_file[:8]

    # Path to day dir
    day_dir = os.path.join(DESTINATION_DIR, day)

    # parses the cam from the filename
    cam_dir = get_cam(next_file)

    # final Output path
    dst_dir = os.path.join(day_dir, PREFIX_CAM + cam_dir)

    # and path to validate if the file was previously copied
    dst_file = os.path.join(dst_dir, next_file)
    if not os.path.exists(day_dir):
        logger.info('Folder %s created', day)
        os.mkdir(day_dir)

    # Checks if the dir exists to avoid overwriting
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    # Checks if the file exists to avoid overwriting
    if not os.path.exists(dst_file):

        check_md5sum = copy_verify.single_threaded_copy_verify_py(src_file,
                                                               dst_file)

        # check output path
        logger.debug('dst: ' + dst_file + ' created')

        if check_md5sum:
            logger.debug('md5sum OK')
        else:
            logger.warning('hash of the following file is not correct:' +
                           src_file)

            # Open csv for saving copied files with false checksums
            append_false_checksum(src_file)

    else:
        logger.info(src_file + ' was not copied to  ' + dst_file + ' (file '
                                                                   'already '
                                                                   'exists)')
        if copy_verify.md5sum_py(src_file) == copy_verify.md5sum_py(dst_file):
            logger.info('md5sum of existing file OK')
        else:
            logger.warning('md5sum of existing file was not correct, copy of '
                           + src_file + ' was not successful')
            append_false_checksum(src_file)

    increment_progress()

# measure the time of the entire process
endTime = datetime.datetime.now()
diffTime = endTime - startTime

logger.info('Number of copied files %s', get_progress())
logger.info(str(get_progress()) + ' files have been copied')
logger.info('PROCESS FINISHED after %s Seconds', diffTime.total_seconds())
