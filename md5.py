"""
computes the md5sum of file with md5sum or msum from the module mutil
"""
import subprocess
import hashlib


def __getMD5sum(output):
    splitted = output.split(' ', 1)
    return splitted[0]


def md5sum(filename):
    """
    calculates 128-bit MD5 hashes, with the default installed md5sum program of
    LINUX
    :return: md5 hash of the file
    """
    md5sum = str(subprocess.check_output(["md5sum", filename], universal_newlines=True))
    return __getMD5sum(md5sum)


def md5py(filename, blocksize=128):
    """
    calculates the MD5 hashes (default blocksize=128 bit) with a modified version of
    the md5()-function of the python module 'hashlib'
    :return: md5 hash of the file
    """
    m = hashlib.md5()
    with open(filename, "r") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()
    
