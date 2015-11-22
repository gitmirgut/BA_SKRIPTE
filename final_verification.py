import os
import hashlib

SOURCE_DIR = './dummyFiles/gfs1/work/bebesook_data_2014'
# SOURCE_DIR = './realData'
DESTINATION_DIR = './structure'

EXT = '.tar'

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


def list_to_string(list):
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
    src_sum = hashlib.md5(list_to_string(__get_all_filenames(
    src)).encode('utf-8')).hexdigest()
    dst_sum = hashlib.md5(list_to_string(__get_all_filenames(
    dst)).encode('utf-8')).hexdigest()
    if src_sum == dst_sum:
        return True
    return False

print(check_integrity(SOURCE_DIR, DESTINATION_DIR))
