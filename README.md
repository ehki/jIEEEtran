# 日英両対応bibtexスタイルファイル（電気学会/IEEE）
日本語と英語文献を同時に扱えるように調整を加えたbstファイルです。
IEEEtranとIEEJtranの2形式を扱うようにしています。

- IEEJtran.bst：電気学会の日英両対応フォーマット
- jIEEEtran.bst：通常のIEEEtranの日本語対応版
- mixej.py：同一文献で日本語と英語を併記するために、pbibtexコマンドの前後に挟むスクリプト

# 使い方

## 基本：引用スタイルの指定

`IEEJtran.bst`を例としますが、他のbstファイルも同様です。使用するbstファイルをPathの通った箇所かtexファイルと同じフォルダに入れて、以下のように文章内で記述します。

```tex
\bibliographystyle{IEEJtran}
\bibliography{FILENAME.bib}
```
コンパイル時に`.bib`ファイルを処理するコマンドには英語用の`bibtex`ではなく、日本語用の`pbibtex`を使用してください。`pbibtex`でのみ用意されている`is.kanji.str$`という関数を使用して日本語/英語の判断をしているため、英語用の`bibtex`ではどの`.bst`ファイルも正しく動きません。`is.kanji.str$`関数を使用した日本語の探索は、`author`、`journal`、`title`、`publisher` の4つのタグに限定しています。

## 応用：英語と日本語を併記

電気学会が求める英語と日本語の併記を実現するため、中間ファイルの`.aux`と`.bbl`をlatexの外部で`python+mixej.py`で改変します。`mixej.py`はメインtexファイルと同じフォルダに入れてください。英語文献と日本語文献のcitationkeyがそれぞれ`engkey`と`jpkey`であるとすれば、合わせて一つの文献として表示するには`engkey/ej/jpkey`という一つのcitationkeyとしてtexファイル中に記載します(`mixej.py`上部の設定で`/ej/`という特殊文字列は変更可能です)。bibファイル中には`engkey`と`jpkey`それぞれに相当するエントリが必要です。伝統的な通常のコンパイル過程である
```text
latex → bibtex → latex → latex → dvipdfmx
```
という手順を変更し、
```text
latex → python mixej.py → bibtex → python mixej.py → latex → latex → dvipdfmx
```
と、`mixej.py`を`bibtex`前後に1回ずつ実行します。一回目の`python mixej.py`で、`.aux`と`.bbl`中の`engkey/ej/jpkey`を`engkey`と`jpkey`の二つに分け、続く`bibtex`で`engkey`と`jpkey`をそれぞれbibtexにて整形させます。二回目の`python mixej.py`で、`.aux`と`.bbl`中の`engkey`と`jpkey`を再び`engkey/ej/jpkey`の一つのcitationkeyとして扱うように改変し、最後の二回の`latex`で一つのcitationkeyである`engkey/ej/jpkey`として扱います。

以上の操作により、`\cite{engkye, jpkey}`として引用すると`.bbl`中に
```latex
\bibitem{engkey}
I.~Yamada, J.~Sato: ``Article title3'', Japanese Transaction, Vol.6, No.10,
  p.156 (2020-10)

\bibitem{jpkey}
山田~一郎・佐藤~次郎：「文献タイトル3」，日本語学会，Vol.6，No.10，p.156（2020-10）
```
と二つの`\bibitem`として出力される英語と日本語の文献を、`(in Japanese)\\\n`を間に挟み`citationkey`を変更して
```latex
\bibitem{engkey/ej/jpkey}
I.~Yamada, J.~Sato: ``Article title3'', Japanese Transaction, Vol.6, No.10,
  p.156 (2020-10)(in Japanese)\\
山田~一郎・佐藤~次郎：「文献タイトル3」，日本語学会，Vol.6，No.10，p.156（2020-10）
```
と、一つの`\bibitem`と扱うことができます。

Latexmkを使用する場合には`bibtx/pbibtx`の実行の有無が自動で判別されますが、`$bibtex`部分のコマンドを書き換えればpythonコマンドを含めて必要な回数実行されます。例えばVScode+Latex Workshopのシンプルなコンパイル設定は次のように変更できます。お使いのコマンドに合わせて適宜変更してください。

```json
"latex-workshop.latex.tools": [
  {
  "command": "latexmk",
  "name": "latexmk python mixej.py",
  "args": [
    "-e", "$ENV{'PYCMD'}=''",
    "-e", "$latex='platex %O -synctex=1 -interaction=nonstopmode -kanji=utf8 -file-line-error %S'",
    "-e", "$bibtex='python mixej.py; pbibtex %O %B; python mixej.py'",
    "-e", "$dvipdf='dvipdfmx -V 7 %O -o %D %S'",
    "-norc", "-pdfdvi", "%DOC%"
    ],
  }
],
"latex-workshop.latex.recipes": [
  { "name": "latexmk, mixej.py", "tools": [ "latexmk python mixej.py" ] }
],
```
なお、`mixej.py`の置き場所がメインtexファイルと異なる場合には`mixej.py`のパスを変更してください。
`"name": "latexmk python mixej.py`や`"name ": "latexmk, mixej.py"`は単なる識別子ですので結果には影響しません。
この設定で、latexmkが`bibtex`での処理が必要だと判断した場合に、`python mixej.py %B`→`pbibtex %B`→`python mixej.py %B`と連続して処理を行ってくれます。

# 参考文献
- [日本語と英語を混ぜられるようにbibtexスタイルファイルを改造しよう](https://qiita.com/HexagramNM/items/3ad757a9f5ee5d15e363#_reference-2be0cc9a71381591bb17)
- [IEEEtran.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtran.bst)
- [How to Use the IEEEtran BIBTEX Style](http://ftp.jaist.ac.jp/pub/CTAN/macros/latex/contrib/IEEEtran/bibtex/IEEEtran_bst_HOWTO.pdf)
- [ShiroTakeda/jecon-bst](https://github.com/ShiroTakeda/jecon-bst)