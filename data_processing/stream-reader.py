from __future__ import print_function
import ijson
import json
import sys

input_file = sys.argv[1]
split_stem = sys.argv[2]
split_index = 0

reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(10000)
f = open(input_file)
progs = ijson.items(f, 'programs.item')

def write_split(split_stem, split_index, split_progs):
    output_file = split_stem + '_' + str(split_index) + '.json'
#    split_index += 1
    print('starts writing {}'.format(output_file))
    with open(output_file, 'w') as f:
        json.dump({'programs': split_progs}, f, ensure_ascii=False, indent=2)
    print('finishes writing {}'.format(output_file))
    del split_progs

doc_count = 0
split_progs = []
for prog in progs:
    doc_count += 1
    if doc_count % 10000 == 0:
        print(doc_count)
    if doc_count % 1000000 == 0:
        write_split(split_stem, split_index, split_progs)
        split_progs = []
        split_index += 1
    if prog['javadoc'] != None and prog['javadoc'] != '':
        split_progs.append(prog)

write_split(split_stem, split_index, split_progs)
