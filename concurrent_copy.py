import threading
import Queue
import subprocess
import os
import datetime
import re
import shelve

# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_test_1000'
# DESTINATION_DIR = '/gfs1/work/bebesook/beesbook_data_test_structured'
# SOURCE_DIR = './test_src'
# DESTINATION_DIR = './test_dst'
SOURCE_DIR = './real'
# SOURCE_DIR = './dummyFiles/gfs1/work/bebesook/beesbook_data_2014'
DESTINATION_DIR = './structure'
STATUSFILE = 'test.status'


def get_cam(file_name):
    split = re.split('_|\.', file_name, 2)
    return split[1]


class Copier(threading.Thread):

    mkdir_lock = threading.Lock()

    def __init__(self, pending_files, finished_files):
        threading.Thread.__init__(self)
        self.pending_files = pending_files
        self.finished_files = finished_files

    def run(self):
        while True:
            cur_file = self.pending_files.get()
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
            exit_status = subprocess.call(cmd)
            if exit_status == 0:
                print(cur_file + ' done')
                self.finished_files.put(cur_file)
            self.pending_files.task_done() # TODO was passiert wenn
            # exit_status==1 ist?


class Memory(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def add_completed_files(self, completed_file):
        status_shelf['finished_files'] += [completed_file]
        status_shelf.sync()

    def run(self):
        while True:
            cur_compl_file = self.queue.get()
            self.add_completed_files(cur_compl_file)
            self.queue.task_done()



status_shelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
if not ('finished_files' in status_shelf):
    status_shelf['finished_files']=[]
    status_shelf.sync()
    print('Statusfile initialisiert')

finished_files_list = status_shelf['finished_files']

pending_files_queue = Queue.Queue()
finished_files_queue = Queue.Queue()



start_Time = datetime.datetime.now()

# spawn threads to copy
for i in range(2):
    t = Copier(pending_files_queue, finished_files_queue)
    t.setDaemon(True)
    t.start()

# spawn thrad to save finished files
t = Memory(finished_files_queue)
t.setDaemon(True)
t.start()

print(finished_files_list)
# get all .tar-files for copy
tar_list = [file for file in os.listdir(SOURCE_DIR) if file.endswith(
        '.tar') and file not in finished_files_list]
print(tar_list)
# add .tar-files to queue
for tar_file in tar_list:
    pending_files_queue.put(tar_file)

# # for i in range(len(tar_list)):
# for i in range(1000):
#     copier.copy_queue.put(tar_list[i])

pending_files_queue.join()
finished_files_queue.join()
end_time = datetime.datetime.now()
diff_time = end_time - start_Time
print(diff_time.total_seconds())



