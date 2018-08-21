import sys
import json
sys.setrecursionlimit(10000)

file_list = sys.argv[1]

with open(file_list) as f:
    files = f.readlines()

count_total = 0
for file in files:
    file = file[:-1]
    print('counting %s' % file)
    with open(file) as f:
        progs =json.load(f)['programs']
    count = len(progs)
    del progs
    print('%s has %i programs' % (file, count))
    count_total += count
    print('current total is %i' % count_total)

print('done')