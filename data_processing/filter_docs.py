import json
import re
import sys

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from re import finditer

wordnet_lemmatizer = WordNetLemmatizer()

def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

input_file = sys.argv[1]
output_file = sys.argv[2]

sys.setrecursionlimit(10000)

with open(input_file) as f:
    progs = json.load(f)['programs']

out_progs = []
count = 0
verb_count = 0
non_verb_count = 0
for prog in progs:
    count += 1
    if count % 1000 == 0:
        print(count)

    javadoc = prog['javadoc']

    if javadoc == None or javadoc == '':
        continue

    # removes <code>...</code> pairs and content in between
    code_patt = r'<code>.*?<\/code>'
    javadoc = re.sub(code_patt, '', javadoc)

    # gets the first sentence
    javadoc = javadoc.split('.')[0]

    # filters out those containing "TODO", "FIXME", "NOTE"
    if "TODO" in javadoc or "FIXME" in javadoc or "NOTE" in javadoc:
        continue

    # removes all kinds of pairs of parentheses and their content
    paren_patt = r'\(.*?\)|\[.*?\]|\<.*?\>|\{.*?\}'
    javadoc = re.sub(paren_patt, '', javadoc)

    # replaces numbers with '#'
    num_patt = r'[-+]?[\d,]*\.?\d+([eE][-+]?\d+)?'
    javadoc = re.sub(num_patt, ' # ', javadoc)

    # strips trailing zeros
    javadoc = javadoc.strip()

    # combine consecutive spaces
    javadoc = re.sub(' +', ' ', javadoc)

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

    # only keep those with first words as verbs
    first_word = javadoc.split(' ', 1)[0]
    synsets = wordnet.synsets(first_word, 'v')
    if len(synsets) > 0:
        verb_count += 1
    else:
        non_verb_count += 1
        continue

    # removes punctuation except '#'
    javadoc = re.sub(r'[^\w\s#]', ' ', javadoc)

    # split camel case (naive regex approach)
    camels = []
    for split in javadoc.split():
        camels.extend(camel_case_split(split))
    javadoc = ' '.join(camels)

    # lowercases all
    javadoc = javadoc.lower()

    # filters out those starting with test
    if javadoc.startswith('test'):
        continue

    # do lemmatization on javadoc tokens
    javadoc = ' '.join([wordnet_lemmatizer.lemmatize(word) for word in javadoc.split() if word != 'as'])

    prog['javadoc'] = javadoc
    out_progs.append(prog)

print('There are totally %i programs, among which %i are generally good. %i start with verbs and are reserved' % (len(
    progs), verb_count + non_verb_count, verb_count))

with open(output_file, 'w') as f:
    json.dump({'programs': out_progs}, f, indent=2)