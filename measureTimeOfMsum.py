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
    buffer_size = msum_list
    buffer_size = msum_list + [b]

    for dr in direct_read_list:
        direct_read = buffer_size
        if dr != '':
            direct_read = buffer_size + [dr]

        for db in double_buffer_list:
            double_buffer = direct_read
            if db != '':
                double_buffer = direct_read + [db]

            for s in split_size_list:
                split_size = double_buffer
                split_size = double_buffer + [s]

                for t in threads_list:
                    threads = split_size
                    threads = split_size + [t]
                    print(threads)
                    all_combinations = all_combinations +[[threads]]

print(str(len(all_combinations)))