import json
import re
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    javadocs = f.readlines()
#     progs = json.load(f)['programs']

# out_progs = []
out_docs = []
count = 0
for javadoc in javadocs:
    count += 1
    if count % 1000 == 0:
        print(count)

    javadoc = javadoc[:-1]

    # removes <code>...</code> pairs and content in between
    code_patt = r'<code>.*?<\/code>'
    javadoc = re.sub(code_patt, '', javadoc)

    # gets the first sentence
    javadoc = javadoc.split('.')[0]

    # lowercases all
    javadoc = javadoc.lower()

    # removes all kinds of pairs of parentheses and their content
    paren_patt = r'\(.*?\)|\[.*?\]|\<.*?\>|\{.*?\}'
    javadoc = re.sub(paren_patt, '', javadoc)

    # replaces numbers with '#'
    num_patt = r'[-+]?[\d,]*\.?\d+([eE][-+]?\d+)?'
    javadoc = re.sub(num_patt, '', javadoc)

    # strips trailing zeros
    javadoc = javadoc.strip()

    # combine consecutive spaces
    javadoc = re.sub(' +', ' ', javadoc)

    # filters out those starting with NOTE, TODO or test
    if javadoc.startswith('NOTE') or javadoc.startswith('TODO') or javadoc.startswith('test'):
        continue

    # removes those with one word only (good for empty docs also)
    if ' ' not in javadoc:
        continue

    # filters out if containing non-ascii chracters
    non_ascii = False
    for c in javadoc:
        code = ord(c)
        if code > 126 or code < 32:
            non_ascii = True
            break
    if non_ascii:
        continue

    out_docs.append(javadoc)
    # prog['javadoc'] = javadoc
    # out_progs.append(prog)

with open(output_file, 'w') as f:
    f.write('\n'.join(out_docs))
    # json.dump({'programs': out_progs}, f, indent=2)