# 日英両対応bibtexスタイルファイル（電気学会/IEEE）
日本語と英語文献を同時に扱えるように調整を加えたbstファイルです。
IEEEtranとIEEJtranの2形式を扱うようにしています。

- IEEJtran.bst：電気学会の日英両対応フォーマット
- jIEEEtran.bst：通常のIEEEtranの日本語対応版
- jIEEEtranS.bst：著者のアルファベット順で並び替えたIEEEtranSの日本語対応版
- addjp.py：上記3つのbstファイルを正しく動作させる日本語フラグを追加するスクリプト

# 使い方

## 日本語フラグを含む bib ファイルの生成

```
python addjp.py FILENAME.bib
```
上記のコマンドで、`FILENAME`と同一のディレクトリに`jFILENAME.bib`というファイルが生成されます。ただし、`FILENAME`は使用するbibファイルの名前に置き換えてください。`addjp.py`では、各エントリの要素内に2バイト文字が混ざっている場合、そのエントリに`isjapanese = {true}` のフラグを追記します。ただし、2バイト文字の探索は`author`、`journal`、`title`、`publisher` の4つのタグに限定しています。

## Texファイル中での記述

`IEEJtran.bst`を例としますが、他のbstファイルも同様です。使用するbstファイルをPathの通った箇所かtexファイルと同じフォルダに入れて、以下のように文章内で記述します。

```tex
\bibliographystyle{IEEJtran}
\bibliography{jFILENAME.bib}
```
`addjp.py`で作成した`jFILENAME.bib`を使用することで、`isjapanese`のキーをbstファイルが読み取り、日本語と英語で異なる処理をしてくれます。サンプルのbibファイルや出力結果は`test`ディレクトリにあります。

# 参考文献
- [日本語と英語を混ぜられるようにbibtexスタイルファイルを改造しよう](https://qiita.com/HexagramNM/items/3ad757a9f5ee5d15e363#_reference-2be0cc9a71381591bb17)
- [IEEEtran.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtran.bst)
- [IEEEtranS.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtranS.bst)
- [ShiroTakeda/jecon-bst](https://github.com/ShiroTakeda/jecon-bst)