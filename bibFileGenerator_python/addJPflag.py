import unicodedata
import sys

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch,'Undefined') 
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False


if __name__ == "__main__":
    argv = sys.argv

    if len(sys.argv)==1:
        print('Please parse .bib file name!')
        exit(-1)

    # 1. read file
    fname = argv[1]
    f = open(fname,encoding="utf-8")
    data = f.read()
    # 2. split file
    sdata = data.split('@')
    # 3. add string
    output = ''
    for strings in sdata:
        if is_japanese(strings):
            output = output +'@' + strings[:-3] + ',\n isjapanese = {true}\n}\n'
        else:
            output = output +'@'+ strings
    output_bib = output[1:]
    # 4. save as new files
    fname_o = fname.replace('.bib','_withJPflag.bib')
    with open(fname_o,'w',encoding='utf-8') as fo:
        fo.write(output_bib)

