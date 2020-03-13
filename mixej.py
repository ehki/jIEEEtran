import sys
import platform
import os
import json

SPLIT_KEY = '/je/'
ITEM_SEP = '(in Japanese)\\\\'

FILE_VERSION = '0.12'
FILE_DATE = '2020/03/14'
FILE_AUTHOR = 'Haruki Ejiri'
FILE_URL = 'https://github.com/YoshiRi/JPandENbst/'


def check_load_file(fn, asjson=False):
    sys.stdout.write('-- Checking file %s, ' % fn)
    try:
        with open(fn, 'r') as f:
            sys.stdout.write('exist, load.\n')
            if asjson:
                return json.load(f)
            else:
                return f.read()
    except FileNotFoundError:
        sys.stdout.write('not found.\n')
        return -1


def save_pairs(fn, pairs):
    sys.stdout.write('-- Saving found pairs to %s, ' % fn)
    with open(fn, 'w') as f:
        json.dump(pairs, f)
    sys.stdout.write('done.\n')


def divide_aux(fn, pairs):
    aux = check_load_file(fn)
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        sys.stdout.write('-- Dividing %s into %s and %s\n' % (combi, k1, k2))
        aux = aux.replace('\\citation{%s}' % combi,
                        '\\citation{%s}\n\\citation{%s}' % (k1, k2))
        aux = aux.replace('\\bibcite{%s}' % combi,
                        '\\bibcite{%s}{1}\n\\bibcite{%s}' % (k1, k2))
    with open(fn, 'w') as f:
        f.write(aux)


def divide_bbl(fn, pairs):
    bbl = check_load_file(fn)
    if bbl == -1: # file not found
        return -1
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        sys.stdout.write('-- Dividing %s into %s and %s\n' % (combi, k1, k2))
        bbl = bbl.replace(ITEM_SEP, '\n\n\\bibitem{%s}' % k2)
        bbl = bbl.replace('\\bibitem{%s}' % combi,
                          '\\bibitem{%s}' % k1)
    sys.stdout.write('-- Saving divided bbl to %s, ' % fn)
    with open(fn, 'w') as f:
        f.write(bbl)
    sys.stdout.write('done.\n')


def find_pairs(fn, aux):
    pairs = []
    sys.stdout.write('-- ')
    for line in aux.split('\n'):
        if SPLIT_KEY in line and '\\citation' in line:
            line = line.replace('\\citation{', '').replace('}', '')
            pairs.append(line.split(SPLIT_KEY))
            sys.stdout.write('.')
    if len(pairs) == 0:
        sys.stdout.write('No combined keys found.\n')
        ret = 0
    if len(pairs) > 0:
        sys.stdout.write(' %d combined keys found.\n' % len(pairs))
        ret =  pairs
        save_pairs(fn, pairs)
    return ret


def combine_aux(fn, pairs):
    aux = check_load_file(fn)
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        sys.stdout.write('-- Combining %s and %s to %s\n' % (k1, k2, combi))
        aux = aux.replace('\\citation{%s}\n\\citation{%s}' % (k1, k2),\
                          '\\citation{%s}' % combi)
        aux = aux.replace('\\bibcite{%s}{1}\n\\bibcite{%s}' % (k1, k2),\
                          '\\bibcite{%s}' % combi)
    sys.stdout.write('-- Saving combined aux to %s, ' % fn)
    with open(fn, 'w') as f:
        f.write(aux)
    sys.stdout.write('done.\n')


def combine_bbl(fn, pairs):
    bbl = check_load_file(fn)
    if bbl == -1:
        return -1
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        sys.stdout.write('-- Combining %s and %s to %s\n' % (k1, k2, combi))
        bbl = bbl.replace('\n\n\\bibitem{%s}' % k2, ITEM_SEP)
        bbl = bbl.replace('\\bibitem{%s}' % k1,
                          '\\bibitem{%s}' % combi)
    sys.stdout.write('-- Saving combined bbl to %s, ' % fn)
    with open(fn, 'w') as f:
        f.write(bbl)
    sys.stdout.write('done.\n')


def split_je_key(bn):
    sys.stdout.write('--\n')
    sys.stdout.write('-- Dividing combinecd keys.\n')  
    aux = check_load_file(bn + '.aux')
    if aux == -1: # aux file not found
        return -1 # abort
    sys.stdout.write('-- Search combined keys from %s.aux.\n' % bn)
    pairs = find_pairs(bn + '.jep', aux)
    if pairs == 0: # no combined keys
        return 0 # probably already divided
    divide_aux(bn + '.aux', pairs)
    divide_bbl(bn + '.bbl', pairs)
    return len(pairs)


def combine_je_key(bn):
    sys.stdout.write('--\n')
    sys.stdout.write('-- Combining divided keys.\n')  
    jepairs = check_load_file(bn + '.jep', asjson=True)
    if len(jepairs) == 0: # no combined keys
        return 0
    combine_aux(bn + '.aux', jepairs)
    combine_bbl(bn + '.bbl', jepairs)
    return len(jepairs)


if __name__ == '__main__':
    sys.stdout.write(
        'This is python version %s ' % platform.python_version())
    sys.stdout.write(
        'mixje.py version %s (%s) by %s.\n' % \
        (FILE_VERSION, FILE_DATE, FILE_AUTHOR))
    sys.stdout.write('See web site: %s\n' % FILE_URL)
    try:
        fname = sys.argv[1]
        sys.stdout.write('Target: %s\n' % fname)
    except IndexError:
        sys.stdout.write('Fatal error: You must assign target.')
        sys.exit(0)

    sk = split_je_key(fname) 
    if sk > 0: # combined keys existed
        sys.stdout.write('-- Fin, %d keys were divided.\n' % sk)
        sys.exit(0)
    elif sk < 0: # Abort
        sys.exit(0)

    ck = combine_je_key(fname)
    if ck != 0:
        # print('-- %d divided citation keys were successfully combined' % ck)
        sys.stdout.write('-- Fin, %d keys were combined.\n' % ck)
        sys.exit(0)
    with open(sys.argv[1]+ '.jep', 'w') as f:
        json.dump([], f)
    sys.stdout.write(
        '-- No cmobined nor divided citation key in the aux file')
    sys.exit(0)
