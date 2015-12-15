'''
computes the md5sum of file or makes a verified copy
'''

import subprocess
import os
import hashlib
import shutil
import timeit
import filecmp
MCP_OPTIONS = []
MSUM_OPTIONS = []


def __parse_MD5sum(output):
    split = output.split(' ', 1)
    return split[0]

################################################################################
# copy and hashsum based on Linux utilities
################################################################################

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

################################################################################
# copy and hashsum based on python modules
################################################################################


def cp_py(src, dst):
    '''
    Copy (single) src to dst.
    Makes use of shutil module (python).
    :param src: source file
    :param dst: destination file / directory
    '''
    shutil.copy(src, dst)


def md5sum_py(filename, blocksize=128):
    """
    Returns MD5 (128-bit) checksum of file.
    Makes use of hashlib module (python).

    :return: md5 hash of the file
    """
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def single_threaded_copy_verify_py_md5(src, dst):
    '''
    Copy (single) src to dst and verify file after copy with md5sum.
    Makes use of python modules hashlib and shutil.

    :return: True, if hash of source file and destination file are equal;
    False otherwise
    '''
    cp_py(src, dst)
    if os.path.isfile(dst):
        if md5sum_py(src) == md5sum_py(dst):
            return True
    elif os.path.isdir(dst):
        dst_file = os.path.join(dst, os.path.basename(src))
        if md5sum_py(src) == md5sum_py(dst_file):
            return True
    return False


def single_threaded_copy_verify_py_cmp(src, dst):
    '''
    Copy (single) src to dst and verify file after copy with filecmp.cmp.
    Makes use of python modules filecmp and shutil.

    :return: True, if files are equal;
    False otherwise
    '''
    cp_py(src, dst)
    if os.path.isfile(dst):
        return filecmp.cmp(src, dst, shallow=False)
    elif os.path.isdir(dst):
        dst_file = os.path.join(dst, os.path.basename(src))
        return filecmp.cmp(src, dst_file, shallow=False)
    return False

################################################################################
# copy and hashsum based on multi-threaded replacements of 'module mutil'
################################################################################

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

def file_cmp(src, dst):
    return filecmp.cmp(src, dst, shallow=False)

# t2 = timeit.Timer("cp_py(\'./realData/20151024192956_2.tar\',"
#                   "\'test.tar\')",
#                   "from __main__ import cp_py")
# time2 = t2.timeit(10)
# print('cp_py')
# print(time2)
#
# t2 = timeit.Timer("single_threaded_copy_verify_py_cmp(\'./realData/20151024192956_2.tar\',"
#                   "\'test.tar\')",
#                   "from __main__ import single_threaded_copy_verify_py_cmp")
# time2 = t2.timeit(10)
# print('cmp_py')
# print(time2)
# t2 = timeit.Timer("single_threaded_copy_verify_py(\'./realData/20151024192956_2.tar\',"
#                   "\'test.tar\')",
#                   "from __main__ import single_threaded_copy_verify_py")
# time2 = t2.timeit(10)
# print('md5_cp_py')
# print(time2)
# t2 = timeit.Timer("md5sum(\'./realData/20151024192956_2.tar\')",
#                   "from __main__ import md5sum")
# time2 = t2.timeit(10)
# print('md5sum')
# print(time2)
# t2 = timeit.Timer("file_cmp(\'./realData/20151024192956_2.tar\',"
#                   "\'test.tar\')",
#                   "from __main__ import file_cmp")
# time2 = t2.timeit(10)
# print('file_cmp')
# print(time2)
# t2 = timeit.Timer("md5sum_py(\'./realData/20151024192956_2.tar\')",
#                   "from __main__ import md5sum_py")
# time2 = t2.timeit(10)
# print('md5sum_py')
# print(time2)
#
#
