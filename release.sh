latexmk \
    -e '$latex=q/uplatex %O -synctex=1 -interaction=nonstopmode -kanji=utf8 -file-line-error %S/' \
    -e '$bibtex=q/python mixej.py %B; upbibtex %O %B; python mixej.py %B/' \
    -e '$dvipdf=q/dvipdfmx -V 7 %O -o %D %S/' \
    -norc \
    -pdfdvi \
    howtouse.tex

latexmk \
    -e '$latex=q/uplatex %O -synctex=1 -interaction=nonstopmode -kanji=utf8 -file-line-error %S/' \
    -e '$bibtex=q/python mixej.py %B; upbibtex %O %B; python mixej.py %B/' \
    -e '$dvipdf=q/dvipdfmx -V 7 %O -o %D %S/' \
    -norc \
    -pdfdvi \
    ieejtran.tex

latexmk \
    -e '$latex=q/uplatex %O -synctex=1 -interaction=nonstopmode -kanji=utf8 -file-line-error %S/' \
    -e '$bibtex=q/python mixej.py %B; upbibtex %O %B; python mixej.py %B/' \
    -e '$dvipdf=q/dvipdfmx -V 7 %O -o %D %S/' \
    -norc \
    -pdfdvi \
    jieeetran.tex

latexmk \
    -e '$latex=q/latex %O -synctex=1 -interaction=nonstopmode -file-line-error %S/' \
    -e '$bibtex=q/bibtex %O %B/' \
    -e '$dvipdf=q/dvipdfmx -V 7 %O -o %D %S/' \
    -norc \
    -pdfdvi \
    ieejtran-en.tex

latexmk \
    -e '$latex=q/latex %O -synctex=1 -interaction=nonstopmode -file-line-error %S/' \
    -e '$bibtex=q/bibtex %O %B/' \
    -e '$dvipdf=q/dvipdfmx -V 7 %O -o %D %S/' \
    -norc \
    -pdfdvi \
    jieeetran-en.tex

rm *.aux *.bbl *.bib *.log *.out *.synctex.gz *.toc *.ejp *.blg *.dvi *.fdb_latexmk *.fls

cp ieejtran.tex ieejtran/
mv ieejtran.pdf ieejtran/
cp ieejtran-en.tex ieejtran/
mv ieejtran-en.pdf ieejtran/
cp mixej.py ieejtran/
cp IEEJtran.bst ieejtran/

cp jieeetran.tex jieeetran/
mv jieeetran.pdf jieeetran/
cp jieeetran-en.tex jieeetran/
mv jieeetran-en.pdf jieeetran/
cp mixej.py jieeetran/
cp jIEEEtran.bst jieeetran/

# git add ieejtran jieeetran .
# git commit -m "v0.17"
