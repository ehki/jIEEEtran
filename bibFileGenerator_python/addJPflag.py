import bibtexparser
import unicodedata
import sys


CHK_KEY = ("title", "publisher", "journal", "author")
COMMENT = """
-----
This file is converted by addJPflag.py
in order to add isjapanese flag."""


def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch, "Undefined")
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
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


def format_jp_authors(entry):
    try:
        atx = " and "
        aut = []
        for d in entry["author"].split(atx):
            ret = d.replace(" ", "~") if d[0] == "{" else d
            aut.append(ret)
        entry["author"] = atx.join(aut)
    except:
        pass


if __name__ == "__main__":
    argv = sys.argv

    if len(sys.argv) == 1:
        print("Please parse .bib file name!")
        exit(-1)

    fname = argv[1]
    with open(fname, "r") as f:
        bibdat = bibtexparser.loads(f.read())

    bibdat.comments[0] += str(COMMENT)

    for ent in bibdat.entries:
        format_jp_authors(ent)
        if is_japanese_entry(ent, CHK_KEY):
            ent["isjapanese"] = "true"

    fname_o = fname.replace(".bib", "_withJPflag.bib")
    writer = bibtexparser.bwriter.BibTexWriter()
    with open(fname_o, "w") as f:
        f.write(writer.write(bibdat))

