import os, datetime, time

DEST_DIR = './dummyFiles'
# IMAGES 2014 PATH
IMG14HOME = DEST_DIR + "/home/b/beesbook/"
IMG14WORK1 = DEST_DIR + "/gfs1/work/bebesook/beesbook_data_2014/"

# IMAGES 2015 PATH
IMG15WORK1 = DEST_DIR + "/gfs1/work/bebesook/beesbook_data_2015/"

# IMAGES 2015 PAtH
IMG15WORK2 = DEST_DIR + "/gfs2/work/bebesook/beesbook_data_2015/"


def createFile(dirpath, seqNum):
    filepath = dirpath + incDatetime.strftime('%Y%m%d%H%M%S') + '_' + str(i) + \
               '.tar'
    newFile = open(filepath, 'w')
    newFile.write(filepath)
    newFile.close()


# IMAGES 2014
# /home/b/beesbook/
# /gfs1/work/bebesook_data_2014/
STARTDATETIME = datetime.datetime(2014, 7, 24, 23, 59, 30)
ENDDATETIME = datetime.datetime(2014, 7, 25, 0, 0, 30)
# ENDDATETIME = datetime.datetime(2014, 9, 25, 12, 0, 0)

incStep = datetime.timedelta(seconds=1)
incDatetime = STARTDATETIME

os.makedirs(os.path.dirname(IMG14HOME))
os.makedirs(os.path.dirname(IMG14WORK1))

for path in [IMG14HOME, IMG14WORK1]:
    while incDatetime <= ENDDATETIME:
        for i in range(4):
            createFile(path, i)
        incDatetime += incStep
    incDatetime = STARTDATETIME
print('IMAGES 2014 Done!')

# IMAGES 2015
# /gfs1/work/bebesook_data_2015/
STARTDATETIME = datetime.datetime(2015, 8, 18, 17, 30, 0)
ENDDATETIME = datetime.datetime(2015, 8, 18, 17, 31, 0)
# ENDDATETIME = datetime.datetime(2015, 10, 26, 11, 0, 0)

incDatetime = STARTDATETIME  # redundant

os.makedirs(os.path.dirname(IMG15WORK1))

while incDatetime <= ENDDATETIME:
    for i in range(4):
        createFile(IMG15WORK1,i)
    incDatetime += incStep
print('IMAGES 2015 pt.1 Done!')

# IMAGES 2015
# /gfs2/work/bebesook/beesbook_data_2015/
STARTDATETIME = datetime.datetime(2015, 8, 18, 0, 0, 0)
ENDDATETIME = datetime.datetime(2015, 9, 18, 17, 31, 0)
endDatetime = datetime.datetime(2015, 10, 26, 11, 0, 0)

incDayDatetime = STARTDATETIME
incDayStep = datetime.timedelta(days=1)
incHourStep = datetime.timedelta(hours=1)
while incDayDatetime <= ENDDATETIME:
    filepath = IMG15WORK2 + incDayDatetime.strftime('%Y%m%d') + '/'
    os.makedirs(os.path.dirname(filepath))
    nextDay = incDayDatetime + incDayStep
    while incDayDatetime < nextDay:
        for i in range(4):
            createFile(filepath,i)
        incDayDatetime += incHourStep
print('Fertig!')
incHourDatetime = STARTDATETIME
