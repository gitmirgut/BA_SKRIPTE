import subprocess
MD5SUM = 'md5sum'
COPY = 'cp'
# declaring the options for md5 and cp
# MD5SUM_CMD = ['msum', '--buffer-size=128', '--direct-read', '--double-buffer', '--split-size=256', '--threads=128']
MD5SUM_OPT =['md5sum']
CP_OPT = ['cp']

def __getMD5sum(output):
    splitted = output.split(' ', 1)
    return splitted[0]

def verifiedCopy(src,dst):

    #  Concatenation of the md5-cmd with options and the dst-path
    cmd_md5sum_src = MD5SUM_OPT + [src]

    # calculates 128-bit MD5 hash of the src-file
    srcMD5sum = __getMD5sum(str(subprocess.check_output(cmd_md5sum_src, universal_newlines=True)))

    #  Concatenation of the cp-cmd, src-path, dst-path
    cmd_cp = CP_OPT + [src] + [dst]

    # copies file from src to dst
    subprocess.call(cmd_cp)

    #  Concatenation of the md5-cmd with options and the dst-path
    cmd_md5sum_dst = MD5SUM_OPT + [dst]

    # calculates 128-bit MD5 hash of the copied file
    dstMD5sum = __getMD5sum(str(subprocess.check_output(cmd_md5sum_dst, universal_newlines=True)))

    # checks if both hashes are equal, otherwise repeat the process
    if srcMD5sum != dstMD5sum:
        return False

    return True


print(verifiedCopy('falseChecksum.csv','test.csv'))