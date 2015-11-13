import md5
import timeit

t1 = timeit.Timer("md5sum(\'falseChecksum.tar\')", "from md5 import md5sum")
t2 = timeit.Timer("md5py(\'falseChecksum.tar\')" ,"from md5 import md5py")
print(t1.timeit(100))
print(t2.timeit(100))