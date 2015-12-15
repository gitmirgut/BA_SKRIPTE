import threading
import queue
import subprocess
import os
import datetime
import re

# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_test_1000'
# DESTINATION_DIR = '/gfs1/work/bebesook/beesbook_data_test_structured'
# SOURCE_DIR = './test_src'
# DESTINATION_DIR = './test_dst'
# SOURCE_DIR = './real'
SOURCE_DIR = './dummyFiles/gfs1/work/bebesook/beesbook_data_2014'
DESTINATION_DIR = './structure'
# STATUSFILE = 'test.status'


def get_cam(file_name):
    split = re.split('_|\.', file_name, 2)
    return split[1]


class Copier(threading.Thread):
    copy_queue = queue.Queue()
    mkdir_lock = threading.Lock()

    def run(self):
        while True:
            cur_file = Copier.copy_queue.get()
            if cur_file is None:
                break
            # the first 8 characters correspond to YYYYMMDD
            day = cur_file[:8]

            # parses the cam from the filename
            cam = get_cam(cur_file)

            # Path to day dir
            dir = os.path.join(DESTINATION_DIR, day,  'cam' + cam)
            
            # Path to destination file
            dst_file = os.path.join(dir,cur_file)

            # Path to source file
            src_file = os.path.join(SOURCE_DIR, cur_file)

            # Checks if the dir exists to avoid overwriting
            Copier.mkdir_lock.acquire()
            if not os.path.exists(dir):
                os.makedirs(dir)
            Copier.mkdir_lock.release()

            cmd = ['cp'] + [src_file] + [dst_file]
            subprocess.call(cmd)
            Copier.copy_queue.task_done()




start_Time = datetime.datetime.now()
copier_threads = [Copier() for i in range(48)]

# statusShelf = shelve.open(STATUSFILE, protocol=0, writeback=True)

for thread in copier_threads:
    thread.setDaemon(True)
    thread.start()

tar_list = [file for file in os.listdir(SOURCE_DIR) if file.endswith('.tar')]

for tar_file in tar_list:
    Copier.copy_queue.put(tar_file)

# # for i in range(len(tar_list)):
# for i in range(1000):
#     copier.copy_queue.put(tar_list[i])

Copier.copy_queue.join()
end_time = datetime.datetime.now()
diff_time = end_time - start_Time
print(diff_time.total_seconds())



