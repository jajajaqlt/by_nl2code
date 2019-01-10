import sys
import json

input_file = sys.argv[1]

with open(input_file) as f:
    progs = json.load(f)['programs']

method_constructor_count = 0
constructor_count = 0
method_count = 0

general_count = 0
for prog in progs:
    general_count += 1
    if general_count % 1000 == 0:
        print(general_count)
    method = prog['method']
    ats_len = method.count('@')
    if ats_len == 3:
        method_constructor_count += 1
    elif ats_len == 2:
        constructor_count += 1
    elif ats_len == 1:
        method_count += 1

print('both: %i, con: %i, meth: %i' % (method_constructor_count, constructor_count, method_count))