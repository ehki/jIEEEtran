import os
import re
import sys
import unicodedata


CHK_KEY = r'\s*author|\s*journal|\s*title|\s*publisher'
CHK_JPC = r'CJK UNIFIED|HIRAGANA|KATAKANA'


def chk_jp_char(string):
    for ch in string:
        if re.search(CHK_JPC, unicodedata.name(ch, 'Undefined')):
            return True
    else:
        return False


def format_authors(t):
    if not re.match(r'\s*author', t):
        return t
    rp, lp = t.find('{'), t.rfind('}')
    if rp == -1 or lp == -1:
        raise ValueError('No bracket found in the text.')
    keysplit = ' and '
    preauth = t[: rp + 1]
    authors = t[rp + 1 : lp]
    aftauth = t[lp:]
    convert = [s.replace(' ', '~') for s in authors.split(keysplit)]
    authors = keysplit.join(convert)
    return preauth + authors + aftauth


def chk_last_comma(line):
    b = True if line[-1] == ',' else False
    return b


def format_jp_keys(line, skip=False):
    line = format_authors(line)
    if not skip:
        nspace = re.match(r'\s*', line).end()
        prefix = '\n' if chk_last_comma(line) else ',\n'
        indent = ' '*nspace
        jp_key = 'isjapanese = {true},'
        line += prefix + indent + jp_key
    return line


def format_entry(e, jpflag=False, ret=''):
    keyvals = []
    for line in e.split('\n'):
        if re.search(CHK_KEY, line) and chk_jp_char(line):
            ret = format_jp_keys(line, skip=jpflag)
            jpflag = True
        else:
            ret = line
        keyvals.append(ret)
    return '\n'.join(keyvals)


def convert_bib(fname_i, fname_o):
    # 1. read file
    with open(fname_i, 'r', encoding='utf-8') as fi:
        data = fi.read()
    # 2. split file
    sdata = data.split('@')
    # 3. format each entry
    entries = [ format_entry(entry) for entry in sdata ]
    # 4. save as new files
    output_bib = '@'.join(entries)
    with open(fname_o, 'w', encoding='utf-8') as fo:
        fo.write(output_bib)


if __name__ == '__main__':
    argv = sys.argv

    if len(sys.argv) == 1:
        print('Please parse .bib file name!')
        exit(-1)

    fname_i = argv[1]
    dirn, fn = os.path.split(fname_i)
    rt, ext = os.path.splitext(fn)
    fname_o = os.path.join(dirn, rt+'_withJP'+ext)
    convert_bib(fname_i, fname_o)