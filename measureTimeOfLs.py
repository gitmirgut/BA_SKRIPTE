import subprocess

# BLOCK_SIZE = 4
# block_size = "--block-size=" + str(BLOCK_SIZE)
# print(block_size)
# for BLOCK_SIZE in range(0, 1):
#      for FORMAT in ['--format=vertical',]:
#         print(str(subprocess.call(["ls","--block-size=" + str(2**BLOCK_SIZE),FORMAT], universal_newlines=False)))
#         print(2**BLOCK_SIZE)
#
# print(['test', 'test2'])

FORMAT = [  '',
            '--format=vertical',
            '--format=horizontal',
            '--format=verbose']
ALL = ['','-a']

BLOCKSIZE = ['']
for i in range(0,1):
    BLOCKSIZE = BLOCKSIZE + ['--block-size=' + str(2**i)]

test =[]
liste=['ls']

for f in FORMAT:
    format = liste
    if f != '':
        format = liste + [f]
    for b in BLOCKSIZE:
        blocksize = format
        if b != '':
            blocksize =format + [b]
        print(blocksize)
        test = test + [[blocksize]]
        print(str(subprocess.call(blocksize, universal_newlines=False)))

print('Laenge: ', len(test))

