import sys
import platform
import json
import logging


SPLIT_KEY = '/ej/'
ITEM_SEP = '\\hspace{0mm}\\\\'

FILE_VERSION = '0.19'
FILE_DATE = '2023/01/26'
FILE_AUTHOR = 'Haruki Ejiri'
FILE_URL = 'https://github.com/ehki/jIEEEtran/'

logger = logging.getLogger(__name__)


def check_load_file(fn, asjson=False):
    """load file if exist else return -1.

    This code load text and json file if exist.
    If the file not exist, return -1

    Parameters
    ----------
    fn : str
        Path to the file to load
    asjson : bool
        whether the fn should be loaded using json or normal text file

    Returns
    -------
    int
        0 if success
    """

    logger.info('-- Checking file %s, ' % fn)
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            logger.info('exist, load.')
            if asjson:
                return json.load(f)
            else:
                return f.read()
    except FileNotFoundError:
        logger.info('not found.')
        return -1


def save_pairs(fn, pairs):
    """save pairs to the JSON format file with the extensions of ".ejp".

    This code save the pairs to the file in JSON format.

    Parameters
    ----------
    fn : str
        Path to the file to write pairs
    pairs : list of two strings
        for example: [["en1",  "jp1"], ["en2", "jp2"], ["en3", "jp3"]]

    Returns
    -------
    int
        0 if success
    """

    logger.info('-- Saving found pairs to %s, ' % fn)
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(pairs, f)
    logger.info('done.')
    return 0


def divide_aux(fn, pairs):
    """divide comined citation(s) and bibcite(s) in aux file.

    This code divide the combined key(s) in aux file.
    For example, the following citation(s) and bibcite(s) in aux file
    --
    \\citation{englishTest7/ej/japaneseTest7}

    \\bibcite{englishTest7/ej/japaneseTest7}{16}
    --
    will be converted to the following two divided citations and bibitems.
    --
    \\citation{englishTest7,japaneseTest7}

    \\bibcite{englishTest7,japaneseTest7}{16}
    --

    Parameters
    ----------
    fn : str
        Path to the aux file to proceess
    pairs : list of two strings
        for example: [["en1",  "jp1"], ["en2", "jp2"], ["en3", "jp3"]]

    Returns
    -------
    int
        -1 if the file to process not found, 0 if success
    """

    aux = check_load_file(fn)
    if aux == -1:  # file not found
        return -1  # failed
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        # for example, combi is "engkey/ej/jpkey", wehere SPLIT_KEY is "/ej/"
        logger.info('-- Dividing %s into %s and %s' % (combi, k1, k2))
        aux = aux.replace('%s' % combi,
                          '%s,%s' % (k1, k2))
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(aux)
    return 0


def divide_bbl(fn, pairs):
    """divide comined bibitem(s) in bbl file.

    This code divide the combined key(s) in bbl file.
    For example, the following combined bibitem(s) in bbl file
    --
    \\bibitem{englishTest5/ej/japaneseTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)\\hspace{0mm}\\\\
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --
    will be converted to the following two divided bibitems.
    --
    \\bibitem{englishTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)

    \\bibitem{japaneseTest5}
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --

    Parameters
    ----------
    fn : str
        Path to the bbl file to proceess
    pairs : list of two strings
        for example: [["en1",  "jp1"], ["en2", "jp2"], ["en3", "jp3"]]

    Returns
    -------
    int
        -1 if the file to process not found, 0 if success
    """

    bbl = check_load_file(fn)
    if bbl == -1:  # file not found
        return -1  # failed
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        # for example, combi is "engkey/ej/jpkey", wehere SPLIT_KEY is "/ej/"
        logger.info('-- Dividing %s into %s and %s' % (combi, k1, k2))
        bbl = bbl.replace(ITEM_SEP, '\n\n\\bibitem{%s}' % k2)
        bbl = bbl.replace('\\bibitem{%s}' % combi, '\\bibitem{%s}' % k1)
    logger.info('-- Saving divided bbl to %s, ' % fn)
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(bbl)
    logger.info('done.')
    return 0  # successfully finished


def find_pairs(fn, aux):
    """find english/japanese pair from string in aux.

    This code find and store english/japanese pair.
    Reading each line in aux strings, the engligh and japanese keys
    are extracted if SPLIT_KEY is in the line.
    If the combined english/japanese keys in the aux file,
    the pairs are stored to the external JSON file

    Parameters
    ----------
    fn : str
        Path to the aux file to proceess
    aux : strings in aux file
        loaded string

    Returns
    -------
    int
        0 if no combined keys found
        num-of-pairs if successfully processed
    """

    pairs = []
    logger.info('-- ')
    for line in aux.split('\n'):
        if SPLIT_KEY not in line or '\\citation' not in line:
            continue
        # the line contains \citation and /ej/
        for ln in line.replace('\\citation{', '').replace('}', '').split(','):
            # convert '\citation{hoge1/ej/hoge2}' to 'hoge1/ej/hoge2'
            if len(ln.split(SPLIT_KEY)) == 2:
                pairs.append(ln.split(SPLIT_KEY))
                # store as ['hoge1', 'hoge2'] pairs
                logger.info('%s' % str(ln.split(SPLIT_KEY)))
    if len(pairs) == 0:
        logger.info('No combined keys found.')
        ret = 0
    if len(pairs) > 0:
        logger.info(' %d combined keys found.' % len(pairs))
        ret = pairs
        save_pairs(fn, pairs)
    return ret


def combine_aux(fn, pairs):
    """combine divided citation(s) and bibcite(s) in aux file.

    This code combine the divided key(s) in aux file.
    For example, the following two divided citation(s) and bibcite(s)
    in aux file
    --
    \\citation{englishTest7,japaneseTest7}

    \\bibcite{englishTest7,japaneseTest7}{16}
    --
    will be converted to the following combined citations and bibitems.
    --
    \\citation{englishTest7/ej/japaneseTest7}

    \\bibcite{englishTest7/ej/japaneseTest7}{16}
    --

    Parameters
    ----------
    fn : str
        Path to the aux file to proceess
    pairs : list of two strings
        for example: [["en1",  "jp1"], ["en2", "jp2"], ["en3", "jp3"]]

    Returns
    -------
    int
        -1 if the file to process not found, 0 if success
    """

    aux = check_load_file(fn)
    if aux == -1:  # file not found
        return -1  # failed
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        # for example, combi is "engkey/ej/jpkey", wehere SPLIT_KEY is "/ej/"
        logger.info('-- Combining %s and %s to %s' % (k1, k2, combi))
        aux = aux.replace('%s,%s' % (k1, k2), '%s' % combi)
    logger.info('-- Saving combined aux to %s, ' % fn)
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(aux)
    logger.info('done.')


def combine_bbl(fn, pairs):
    """combine divided bibitem(s) in bbl file.

    This code divide the combined key(s) in bbl file.
    For example, the following two divided bibitem(s) in bbl file
    --
    \\bibitem{englishTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)

    \\bibitem{japaneseTest5}
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --
    will be converted to the following combined citations and bibitems.
    --
    \\bibitem{englishTest5/ej/japaneseTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)\\hspace{0mm}\\\\
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --

    Parameters
    ----------
    fn : str
        Path to the aux file to proceess
    pairs : list of two strings
        for example: [["en1",  "jp1"], ["en2", "jp2"], ["en3", "jp3"]]

    Returns
    -------
    int
        -1 if the file to process not found, 0 if success
    """

    bbl = check_load_file(fn)
    if bbl == -1:  # file not found
        return -1  # failed
    for k1, k2 in pairs:
        combi = SPLIT_KEY.join([k1, k2])
        # for example, combi is "engkey/ej/jpkey", wehere SPLIT_KEY is "/ej/"
        logger.info('-- Combining %s and %s to %s' % (k1, k2, combi))
        bbl = bbl.replace('\n\n\\bibitem{%s}' % k2, ITEM_SEP)
        bbl = bbl.replace('\\bibitem{%s}' % k1,
                          '\\bibitem{%s}' % combi)
    logger.info('-- Saving combined bbl to %s, ' % fn)
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(bbl)
    logger.info('done.')


def divide_ej_key(bn):
    """divide combined english and japanese bibiteems in bbl and aux file.

    This code divide the combined key(s) in aux and bbl file.
    For example, the following combined bibitem(s) in bbl file
    --
    \\bibitem{englishTest5/ej/japaneseTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)\\hspace{0mm}\\\\
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --
    will be converted to the following two divided bibitems.
    --
    \\bibitem{englishTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)

    \\bibitem{japaneseTest5}
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --
    The following two combined citation(s) and bibcite(s) in aux file
    --
    \\citation{englishTest7/ej/japaneseTest7}

    \\bibcite{englishTest7/ej/japaneseTest7}{16}
    --
    will also be converted to the following combined citations and bibitems.
    --
    \\citation{englishTest7}
    \\citation{japaneseTest7}

    \\bibcite{englishTest7}{1}
    \\bibcite{japaneseTest7}{16}
    --
    The first process during LaTeX compile, there would no bbl file.
    If the bbl file not exist, the dividing process would be skipped.
    A list of english/japanese pairs will be extracted from aux file,
    and if will be saved in the JSON file with
    ".ejp" (english-japanese-pair) extension

    Parameters
    ----------
    bn : str
        Target file to process without extension.
        if your target tex file is '/DIRNAME/main.tex'
        the bn would be '/DIRNAME/main'

    Returns
    -------
    int
        -1 if the file to process not found
        0 if no combined keys found
        num-of-pairs if successfully processed
    """

    logger.info('--')
    logger.info('-- Dividing combinecd keys.')
    aux = check_load_file(bn + '.aux')
    if aux == -1:  # aux file not found
        return -1  # abort
    logger.info('-- Search combined keys from %s.aux.' % bn)
    pairs = find_pairs(bn + '.ejp', aux)
    if pairs == 0:  # no combined keys
        return 0  # probably already divided
    divide_aux(bn + '.aux', pairs)
    divide_bbl(bn + '.bbl', pairs)
    return len(pairs)


def combine_ej_key(bn):
    """combine english and japanese bibiteems in bbl and aux file.

    This code combine the divided key(s) in aux and bbl file.
    For example, the following divided bibitem(s) in bbl file
    --
    \\bibitem{englishTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)

    \\bibitem{japaneseTest5}
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --
    will be converted to the following two divided bibitems.
    --
    \\bibitem{englishTest5/ej/japaneseTest5}
    I.~Yamada, J.~Sato, S.~Tanaka, S.~Suzuki: ``Article title'', Japanese
    Transaction, Vol.10, No.5, pp.45--60 (2016-3)\\hspace{0mm}\\\\
    山田~一郎・佐藤~次郎・田中~三郎・鈴木~四郎：「文献タイトル」，
    日本語学会，Vol.10，No.5，pp.45--60（2016-3）
    --
    The following two divided citation(s) and bibcite(s) in aux file
    --
    \\citation{englishTest7}
    \\citation{japaneseTest7}

    \\bibcite{englishTest7}{1}
    \\bibcite{japaneseTest7}{16}
    --
    will also be converted to the following combined citations and bibitems.
    --
    \\citation{englishTest7/ej/japaneseTest7}

    \\bibcite{englishTest7/ej/japaneseTest7}{16}
    --

    Parameters
    ----------
    bn : str
        Target file to process without extension.
        if your target tex file is '/DIRNAME/main.tex'
        the bn would be '/DIRNAME/main'

    Returns
    -------
    int
        -1 if the file to process not found
        0 if no combined keys found
        num-of-pairs if successfully processed
    """

    logger.info('--')
    logger.info('-- Combining divided keys.')
    pairs = check_load_file(bn + '.ejp', asjson=True)
    if pairs == -1:  # file not found
        return -1
    if len(pairs) == 0:  # no combined keys
        return 0
    combine_aux(bn + '.aux', pairs)
    combine_bbl(bn + '.bbl', pairs)
    return len(pairs)


if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    logger.addHandler(sh)

    logger.info(
        'This is python version %s ' % platform.python_version())
    logger.info(
        'mixje.py version %s (%s) by %s.' %
        (FILE_VERSION, FILE_DATE, FILE_AUTHOR)
    )
    logger.info('See web site: %s' % FILE_URL)
    try:
        fname = sys.argv[1]
        logger.info('Target: %s' % fname)
    except IndexError:
        logger.info('Fatal error: You must assign target.')
        sys.exit(0)

    sk = divide_ej_key(fname)
    if sk > 0:  # combined keys existed
        logger.info('-- Fin, %d keys were divided.' % sk)
        sys.exit(0)
    elif sk < 0:  # Abort
        sys.exit(0)

    ck = combine_ej_key(fname)
    if ck != 0:
        # print('-- %d divided citation keys were successfully combined' % ck)
        logger.info('-- Fin, %d keys were combined.' % ck)
        sys.exit(0)
    with open(sys.argv[1] + '.ejp', 'w', encoding='utf-8') as f:
        json.dump([], f)
    logger.info(
        '-- No cmobined nor divided citation key in the aux file')
    sys.exit(0)
