# 日英両対応bibtexスタイルファイル（電気学会/IEEE）
日本語と英語文献を同時に扱えるように調整を加えたbstファイルです。
IEEEtranとIEEJtranの2形式を扱うようにしています。

- IEEJtran.bst：電気学会の日英両対応フォーマット
- jIEEEtran.bst：通常のIEEEtranの日本語対応版
- jIEEEtranS.bst：著者のアルファベット順で並び替えたIEEEtranSの日本語対応版

# 使い方


`IEEJtran.bst`を例としますが、他のbstファイルも同様です。使用するbstファイルをPathの通った箇所かtexファイルと同じフォルダに入れて、以下のように文章内で記述します。

```tex
\bibliographystyle{IEEJtran}
\bibliography{FILENAME.bib}
```
コンパイル時に`.bib`ファイルを処理するコマンドには英語用の`bibtex`ではなく、日本語用の`pbibtex`を使用してください。`pbibtex`でのみ用意されている`is.kanji.str$`という関数を使用して日本語/英語の判断をしているため、英語用の`bibtex`ではどの`.bst`ファイルも正しく動きません。`is.kanji.str$`関数を使用した日本語の探索は、`author`、`journal`、`title`、`publisher` の4つのタグに限定しています。サンプルのbibファイルや出力結果は`test`ディレクトリにあります。

# 参考文献
- [日本語と英語を混ぜられるようにbibtexスタイルファイルを改造しよう](https://qiita.com/HexagramNM/items/3ad757a9f5ee5d15e363#_reference-2be0cc9a71381591bb17)
- [IEEEtran.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtran.bst)
- [IEEEtranS.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtranS.bst)
- [ShiroTakeda/jecon-bst](https://github.com/ShiroTakeda/jecon-bst)