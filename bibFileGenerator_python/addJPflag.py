import unicodedata
import sys
import re


CHK_KEY = r'\s*author|\s*journal|\s*title|\s*publisher'


def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch, 'Undefined')
        if 'CJK UNIFIED' in name or 'HIRAGANA' in name or 'KATAKANA' in name:
            return True
    return False

def is_japanese_excludefilepath(string):
    stringtoken = string.split(' ') # separate token with space 
    for chs in stringtoken:
        if '\\' in chs or ' / ' in chs:
            continue # exclude file path
        else:
            for ch in chs:
                name = unicodedata.name(ch,'Undefined') 
                if "CJK UNIFIED" in name \
                or "HIRAGANA" in name \
                or "KATAKANA" in name:
                    return True
    return False


def is_japanese_entry(entry, keys):
    for k in keys:
        try:
            if is_japanese(entry[k]):
                return True
        except:
            continue
    else:
        return False


def format_jp_authors(t):
    rp, lp = t.find('{'), t.rfind('}')
    if rp == -1 or lp == -1:
        raise ValueError('No bracket found in the text.')
    atx = ' and '
    ret = t[: rp + 1]
    ret += atx.join([s.replace(' ', '~') for s in t[rp + 1 : lp].split(atx)])
    ret += t[lp:]
    return ret


if __name__ == '__main__':
    argv = sys.argv

    if len(sys.argv) == 1:
        print('Please parse .bib file name!')
        exit(-1)

    # 1. read file
    fname = argv[1]
    f = open(fname, encoding='utf-8')
    data = f.read()
    # 2. split file
    sdata = data.split('@')
    # 3. add string
    output = ''
    for entry in sdata:
        jpflag = False
        output += '@'
        for line in entry.split('\n'):
            if re.search(CHK_KEY, line) and is_japanese(line):
                jpflag = True
                if re.match(r'\s*author', line):
                    line = format_jp_authors(line)
                line += '\nisjapanese = {true},'
            output += line + '\n'
    output_bib = output[1:]
    # 4. save as new files
    fname_o = fname.replace('.bib', '_withJP.bib')
    with open(fname_o, 'w', encoding='utf-8') as fo:
        fo.write(output_bib)

