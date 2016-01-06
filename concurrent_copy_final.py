import threading
import queue
import subprocess
import os
import datetime
import re
import shelve
import logging
import logging.handlers


# 1. Run HOME(beesbook) --> WORK2 (structured) 2014
# SOURCE_DIR = '/home/b/beesbook'
# DESTINATION_DIR = '/gfs1/work/bebesook/beesbook_data_2014'

# 2. Run WORK1 --> WORK2 (structured) 2015
# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2015'
# DESTINATION_DIR = '/gfs2/work/bebesook/beesbook_data_2015'

# 3. Run WORK1(structured) --> WORK2 (structured) 2014
# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_2014'
# DESTINATION_DIR = '/gfs2/work/bebesook/beesbook_data_2014'

# 4. Run WORK1(structured) --> WORK2 (structured) 2015
# SOURCE_DIR = '/gfs2/work/bebesook/beesbook_data_2015'
# DESTINATION_DIR = '/gfs1/work/bebesook/beesbook_data_2015'

# ----------------------------------------------------------------------------
# Test
# SOURCE_DIR = '/gfs1/work/bebesook/beesbook_data_test_1000'
# DESTINATION_DIR = '/gfs1/work/bebesook/beesbook_data_test_structured'

# SOURCE_DIR = './real'
# DESTINATION_DIR = './structure'
SOURCE_DIR = './dummyFiles/gfs1/work/bebesook/beesbook_data_2014'
DESTINATION_DIR = './test_dst'


STATUSFILE = 'Mirror_2014.status'
LOGFILEPATH = 'Mirror_2014.log'


def get_cam(file_name):
    split = re.split('_|\.', file_name, 2)
    return split[1]


class Copier(threading.Thread):
    '''
    class for creating worker-threads for copying the files
    '''
    # initialize lock for creation of new directory
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
            dst_file = os.path.join(dir, cur_file)

            # Path to source file
            src_file = os.path.join(SOURCE_DIR, cur_file)

            # Checks if the dir exists to avoid overwriting
            Copier.mkdir_lock.acquire()
            if not os.path.exists(dir):
                os.makedirs(dir)

            if os.path.exists(dst_file):
                logger.warning(dst_file + ' already exists and will be '
                                          'overwritten')
            Copier.mkdir_lock.release()

            cmd = ['cp'] + [src_file] + [dst_file]
            exit_status = subprocess.call(cmd)

            # checks if cmd was successful
            if exit_status == 0:
                self.finished_files.put(cur_file)

            self.pending_files.task_done()


class Memory(threading.Thread):
    '''
    class for creating a thread, which will save the progress of the overall
    copying
    '''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def add_completed_files(self, completed_file):
        status_shelf['finished_files'] += [completed_file]
        status_shelf['progress'] += 1
        status_shelf.sync()
        logger.debug('status: ' + str(status_shelf['progress']))

    def run(self):
        while True:
            cur_compl_file = self.queue.get()
            self.add_completed_files(cur_compl_file)
            self.queue.task_done()


# Initialize logger with two handlers, where each handler has a different
# level, so that the more important logs will be writen to file and the
# unimportant logs for debug will just will be shown on console output and
# can be disabled by
# logging.disable(logging.DEBUG)

logger = logging.getLogger('myLog')
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=LOGFILEPATH,
    when='midnight',
    backupCount=30)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

status_shelf = shelve.open(STATUSFILE, protocol=0, writeback=True)
logger.info('Status file has been opened')

if not ('finished_files' in status_shelf):
    status_shelf['finished_files'] = []
    status_shelf.sync()
    logger.info('START with a new copy process')
else:
    logger.info('Continue with the last copy process')

if not ('progress' in status_shelf):
    status_shelf['progress'] = 0
    status_shelf.sync()


finished_files_list = status_shelf['finished_files']

pending_files_queue = queue.Queue()
finished_files_queue = queue.Queue()

# spawn threads to copy files from pending_files_queue
for i in range(48):
    t = Copier(pending_files_queue, finished_files_queue)
    t.setDaemon(True)
    t.start()

# spawn thread to save the list of finished files
t = Memory(finished_files_queue)
t.setDaemon(True)
t.start()

# get all .tar-files for copy, which are not finished
tar_list = [file for file in os.listdir(SOURCE_DIR) if file.endswith(
    '.tar') and file not in finished_files_list]

logger.info(str(len(tar_list)) + ' files left for copy')
# add .tar-files to queue
for tar_file in tar_list:
    pending_files_queue.put(tar_file)
start_Time = datetime.datetime.now()

# just for testing and estimation of the average time
# for i in range(1000):
# pending_files_queue.put(tar_list[i])

pending_files_queue.join()
finished_files_queue.join()
end_time = datetime.datetime.now()
diff_time = end_time - start_Time
logger.debug('PROCESS FINISHED after ' + str(diff_time.total_seconds()) +
             ' Seconds')