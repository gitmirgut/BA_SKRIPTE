'''
computes the md5sum of file or makes a verified copy
'''

import subprocess
import os
import hashlib

MCP_OPTIONS = []
MSUM_OPTIONS = []


def __parse_MD5sum(output):
    splitted = output.split(' ', 1)
    return splitted[0]


def cp(src, dst):
    '''
    Copy (single) src to dst.
    Makes use of single-threaded Linux utilities cp.
    :param src: source file
    :param dst: destination file / directory
    '''
    cmd = ['cp'] + [src] + [dst]
    subprocess.call(cmd)


def md5sum(file):
    '''
    Returns MD5 (128-bit) checksum of file.
    Makes use of the single-threaded Linux utilities md5sum
    '''
    cmd = ['md5sum'] + [file]
    out = str(subprocess.check_output(cmd, universal_newlines=True))
    return __parse_MD5sum(out)

def md5py(filename, blocksize=128):
    """
    Returns MD5 (128-bit) checksum of file.
    Makes use of hashlib module

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


def mcp(src, dst):
    '''
    Copy (single) src to dst.
    Makes use of the multi-threaded replacement mcp of 'module mutil'.
    (on Cray the the module 'module load mutil' has to be loaded)
    '''
    cmd = ['mcp'] + MCP_OPTIONS + [src] + [dst]
    subprocess.call(cmd)


def mcp_with_sum(src, dst):
    '''
    Copy (single) src to dest.
    Makes use of the multi-threaded replacement mcp and incorporated checksum
    for speedup (see https://www.usenix.org/legacy/event/lisa10/tech
    /full_papers/Kolano.pdf)

    on Cray the the module 'module load mutil' has to be loaded

    :return: hash of file
    '''
    cmd = ['mcp'] + ['--print-hash'] + MCP_OPTIONS + [src] + [dst]
    out = str(subprocess.check_output(cmd, universal_newlines=True))
    return __parse_MD5sum(out)


def msum(file):
    '''
    Returns MD5 checksum of file.
    Makes use of the multi-threaded replacement msum of 'module mutil'.
    (On Cray the the module 'module load mutil' has to be loaded)

    :param file:
    :return:hash of file
    '''
    cmd = ['msum'] + MSUM_OPTIONS + [file]
    out = str(subprocess.check_output(cmd, universal_newlines=True))
    return __parse_MD5sum(out)


def single_threaded_copy_verify(src, dst):
    '''
    Copy (single) src to dst and verify file after copy with md5sum.
    Makes use of single-threaded Linux utilities cp and md5sum.

    :return: True, if hash of source file and destination file are equal;
    False otherwise
    '''
    cp(src, dst)
    if os.path.isfile(dst):
        if md5sum(src) == md5sum(dst):
            return True
    elif os.path.isdir(dst):
        dst_file = os.path.join(dst, os.path.basename(src))
        if md5sum(src) == md5sum(dst_file):
            return True
    return False


def multi_threaded_copy_verify(src, dst):
    '''
    Copy (single) src to dst and verify file after copy with msum.
    Makes use of the multi-threaded replacement mcp and msum of 'module mutil'.
    (On Cray the the module 'module load mutil' has to be loaded.)

    :return: True, if hash of source file and destination file are equal;
    False otherwise
    '''
    md5sum_src = mcp_with_sum(src, dst)
    if os.path.isfile(dst):
        if md5sum_src == msum(dst):
            return True
    elif os.path.isdir(dst):
        dst_file = os.path.join(dst, os.path.basename(src))
        if md5sum_src == msum(dst_file):
            return True
    return False
