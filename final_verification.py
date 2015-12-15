import os
import hashlib
import re
import datetime
import logging

# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_test_1000'
# DESTINATION_DIR = '/gfs1/work/bebesook/beesbook_data_test_structured'
SOURCE_DIR = './dummyFiles/gfs1/work/bebesook/beesbook_data_2014'
DESTINATION_DIR = './structure'

EXT = '.tar'

def __get_cam(file_name):
    split = re.split('_|\.', file_name, 2)
    return split[1]

def __get_all_filenames(path):
    '''
    This method returns a stable sorted list, with all files in directory and
    subfolders.
    '''
    filenames_list = []
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(EXT):
                filenames_list = filenames_list + [filename]
    filenames_list.sort()
    return filenames_list



def __list_to_string(list):
    '''
    This method converts a list to string.
    '''
    string = ''.join(list)
    return string


def check_integrity(src, dst):
    '''
    This method checks if all files which exist in the 'src'-directory,
    also exists in 'dst'-directory.

    WARNING: the integrity of file content, has to be checked separately
    '''
    src_sum = hashlib.md5(__list_to_string(__get_all_filenames(
    src)).encode('utf-8')).hexdigest()
    dst_sum = hashlib.md5(__list_to_string(__get_all_filenames(
    dst)).encode('utf-8')).hexdigest()
    if src_sum == dst_sum:
        return True
    return False

def __absolute_file_paths(directory):
    """
    returns an iterable list of all files with absolute path in directory
    and  his subfolders
    :param directory:
    :return:
    """
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def file_count_size (path):
    """
    returns the number and the sum total of the .tar-files
    :param directory:
    :return:
    """
    count = 0
    size = 0
    for file_path in __absolute_file_paths(path):
        if file_path.endswith(EXT):
            count = count + 1
            size += os.path.getsize(file_path)

    return (count, size)


logger = logging.getLogger('myLog')
formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


startTime = datetime.datetime.now()

src_size = file_count_size(SOURCE_DIR)
dst_size = file_count_size(DESTINATION_DIR)
logger.info('dst: (#files, size)= ' + str(src_size))
logger.info('src: (#files, size)= ' +str(dst_size))
logger.info(file_count_size(SOURCE_DIR)==file_count_size(DESTINATION_DIR))
#
logger.info(check_integrity(SOURCE_DIR, DESTINATION_DIR))
endTime = datetime.datetime.now()
diffTime = endTime - startTime
logger.info(diffTime.total_seconds())