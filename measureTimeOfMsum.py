# import md5
# import timeit
# import cProfile
#
# FILENAME = 'falseChecksum.tar'
# # FILENAME = './realData/20151024192956_2.tar'
#
# t1 = timeit.Timer('md5sum(\''+ FILENAME + '\')', "from md5 import md5sum")
# t2 = timeit.Timer('md5py(\''+ FILENAME + '\')' ,"from md5 import md5py")
# print(md5.md5sum(FILENAME))
# print(md5.md5sum(FILENAME))
# print('mdsum:', t1.timeit(1))
# print('md5py:', t2.timeit(1))
# # cProfile.run('md5.md5sum(\'falseChecksum.tar\')')
import csv
import timeit
import subprocess
# Open csv for saving copied files with false checksums

MD5SUM_OPT =['md5sum']

def get_MD5_sum(file):
    cmd_md5sum = MD5SUM_OPT + [file]
    output = str(subprocess.check_output(cmd_md5sum, universal_newlines=True))
    md5sum = output.split(' ', 1)
    return md5sum[0]


cases_file = open('cases.csv', 'w')
cases_writer = csv.writer(cases_file)


all_combinations =[]
msum_list = ['msum']

buffer_size_list = []
for i in range(0,8):
    buffer_size_list = buffer_size_list + ['--buffer-size=' + str(2**i)]

direct_read_list = ['', '--direct-read']
double_buffer_list = ['', '--double-buffer']

split_size_list = []
for i in range(0,9):
    split_size_list = split_size_list + ['--split-size=' + str(2**i)]

threads_list = []
for i in range(1,8):
    threads_list = threads_list + ['--threads=' + str(2**i)]

for b in buffer_size_list:
    cmd_buffer_size = msum_list
    cmd_buffer_size = msum_list + [b]
    csv_buffer_size = cmd_buffer_size

    for dr in direct_read_list:
        cmd_direct_read = cmd_buffer_size
        if dr != '':
            cmd_direct_read = cmd_buffer_size + [dr]
        csv_direct_read = csv_buffer_size + [dr]

        for db in double_buffer_list:
            cmd_double_buffer = cmd_direct_read
            if db != '':
                cmd_double_buffer = cmd_direct_read + [db]
            csv_double_buffer = csv_direct_read + [db]

            for s in split_size_list:
                cmd_split_size = cmd_double_buffer
                cmd_split_size = cmd_double_buffer + [s]
                csv_split_size = csv_double_buffer + [s]

                for t in threads_list:
                    cmd_threads = cmd_split_size
                    cmd_threads = cmd_split_size + [t]
                    csv_threads = csv_split_size + [t]
                    # t1 = timeit.Timer("get_MD5_sum(\'Mirror2015.log\')",
                    #                   setup="from __main__ import get_MD5_sum")
                    # time = t1.timeit(10)
                    # cases_writer.writerow(csv_threads+ [time])
                    all_combinations = all_combinations +[[cmd_threads]]

print(str(len(all_combinations)))
cases_file.close()